"""Strict read-only integrity and Codex-first policy gate for the build package."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from model_policy_runtime import (
    CAPABILITY_ROLES,
    CONCRETE_PREFERRED_ENGINES,
    PolicyValidationError,
    validate_and_canonicalize_url,
    validate_candidate,
)


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8-sig"))


def _manifest_target(package: Path, manifest_path: str) -> Path:
    normalized = Path(manifest_path.replace("/", "\\"))
    if manifest_path.startswith("build-package/"):
        return package / Path(*normalized.parts[1:])
    return package.parents[1] / normalized


def _active_files(package: Path) -> set[str]:
    roots = [package / name for name in ("config", "schemas", "scripts", "templates", "tests", "fixtures")]
    files = {path for root in roots if root.exists() for path in root.rglob("*") if path.is_file() and "__pycache__" not in path.parts}
    files.update(path for path in package.iterdir() if path.is_file())
    return {"build-package/" + path.relative_to(package).as_posix() for path in files}


def _validate_effective_security(value: Any, path: tuple[str, ...] = ()) -> None:
    if isinstance(value, dict):
        for raw_key, child in value.items():
            key = str(raw_key)
            key_lower = key.lower()
            location = ".".join(path + (key,))
            if key.upper() == "ANTHROPIC_API_KEY" or (isinstance(child, str) and child.upper() == "ANTHROPIC_API_KEY"):
                raise PolicyValidationError(f"forbidden native credential reference: {location}")
            if key_lower in {"provider", "provider_id"} and str(child).strip().lower() == "anthropic":
                raise PolicyValidationError(f"forbidden native provider: {location}")
            if key == "preferred_engine" and str(child) in CONCRETE_PREFERRED_ENGINES:
                raise PolicyValidationError(f"concrete current preferred_engine: {location}")
            if key_lower in {"base_url", "default_base_url", "endpoint", "models_url"} and isinstance(child, str) and "://" in child:
                validate_and_canonicalize_url(child)
            _validate_effective_security(child, path + (key,))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _validate_effective_security(child, path + (str(index),))


def run_gate(package: Path, *, run_tests: bool = True) -> list[str]:
    errors: list[str] = []
    manifest_path = package / "MANIFEST.yaml"
    ledger_path = package / "PRODUCTION_IDENTITY_LEDGER.yaml"
    try:
        manifest = _load_yaml(manifest_path)
    except Exception as exc:
        return [f"MANIFEST parse failed: {exc}"]
    entries = manifest.get("files", []) if isinstance(manifest, dict) else []
    summary = manifest.get("build_package_files", {}) if isinstance(manifest, dict) else {}
    actual_required = sum(bool(entry.get("required")) for entry in entries if isinstance(entry, dict))
    actual_optional = sum(not bool(entry.get("required")) for entry in entries if isinstance(entry, dict))
    actual_breakdown = {
        "design_docs": sum(
            isinstance(entry, dict)
            and isinstance(entry.get("path"), str)
            and not entry["path"].startswith("build-package/")
            and not entry["path"].startswith("构建指导书中 ")
            for entry in entries
        ),
        "design_embedded": sum(
            isinstance(entry, dict) and str(entry.get("path", "")).startswith("构建指导书中 ") for entry in entries
        ),
    }
    for category in ("schemas", "config", "fixtures", "scripts", "tests", "templates"):
        actual_breakdown[category] = sum(
            isinstance(entry, dict) and str(entry.get("path", "")).startswith(f"build-package/{category}/")
            for entry in entries
        )
    actual_breakdown["build_meta"] = sum(
        isinstance(entry, dict)
        and str(entry.get("path", "")).startswith("build-package/")
        and str(entry.get("path", "")).count("/") == 1
        for entry in entries
    )
    for key, actual in (("total", len(entries)), ("required", actual_required), ("optional", actual_optional)):
        if summary.get(key) != actual:
            errors.append(f"MANIFEST summary mismatch: {key}={summary.get(key)!r}, actual={actual}")
    declared_breakdown = summary.get("breakdown", {}) if isinstance(summary, dict) else {}
    for key, actual in actual_breakdown.items():
        if declared_breakdown.get(key) != actual:
            errors.append(f"MANIFEST breakdown mismatch: {key}={declared_breakdown.get(key)!r}, actual={actual}")
    public_summary = manifest.get("summary", {}) if isinstance(manifest, dict) else {}
    public_expected = {
        "total_files": len(entries),
        "required": actual_required,
        "optional": actual_optional,
        "design_docs": actual_breakdown["design_docs"],
        "design_embedded_refs": actual_breakdown["design_embedded"],
        "build_package_files": sum(
            isinstance(entry, dict)
            and str(entry.get("path", "")).startswith("build-package/")
            for entry in entries
        ),
        "physical_files": len(entries) - actual_breakdown["design_embedded"],
    }
    for key, actual in public_expected.items():
        if public_summary.get(key) != actual:
            errors.append(
                f"MANIFEST public summary mismatch: {key}={public_summary.get(key)!r}, actual={actual}"
            )
    registered: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            errors.append("MANIFEST contains an invalid file entry")
            continue
        registered.add(entry["path"])
        target = _manifest_target(package, entry["path"])
        if entry.get("required") and not target.is_file():
            errors.append(f"required file missing: {entry['path']}")

    unregistered = sorted(_active_files(package) - registered)
    if unregistered:
        errors.extend(f"unregistered active file: {path}" for path in unregistered)

    yaml_files = sorted(
        list((package / "config").glob("*.yaml"))
        + list((package / "templates").glob("*.yaml"))
        + [manifest_path, ledger_path]
    )
    documents: dict[Path, Any] = {}
    for path in yaml_files:
        try:
            documents[path] = _load_yaml(path)
        except Exception as exc:
            errors.append(f"YAML parse failed: {path.relative_to(package)}: {exc}")
    json_files = sorted(list((package / "schemas").glob("*.json")) + list((package / "templates").glob("*.json")))
    json_documents: dict[Path, Any] = {}
    for path in json_files:
        try:
            json_documents[path] = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception as exc:
            errors.append(f"JSON parse failed: {path.relative_to(package)}: {exc}")

    if errors:
        return errors

    try:
        for path, schema in json_documents.items():
            if path.parent.name == "schemas":
                Draft202012Validator.check_schema(schema)
        tool_schema = json_documents[package / "schemas" / "tool_card.schema.json"]
        agent_schema = json_documents[package / "schemas" / "agent_card.schema.json"]
        model_policy_schema = json_documents[package / "schemas" / "model_policy.schema.json"]
        production_identity_schema = json_documents[
            package / "schemas" / "production_identity_ledger.schema.json"
        ]
        tools = documents[package / "config" / "tools.yaml"]["tools"]
        agents = documents[package / "config" / "agents.yaml"]["agents"]
        for tool in tools:
            Draft202012Validator(tool_schema).validate(tool)
        for agent in agents:
            Draft202012Validator(agent_schema).validate(agent)
        Draft202012Validator(model_policy_schema).validate(documents[package / "config" / "model_capabilities.yaml"])
        Draft202012Validator(production_identity_schema).validate(documents[ledger_path])
        validate_candidate(documents[package / "config" / "model_capabilities.yaml"])
    except Exception as exc:
        errors.append(f"schema validation failed: {exc}")
        return errors

    tool_ids = {tool["id"] for tool in tools}
    provider_ids = set(documents[package / "config" / "model_capabilities.yaml"]["providers"])
    production_identity = documents[ledger_path]
    effective_receipts = production_identity["receipts"]["effective"]
    superseded_receipts = production_identity["receipts"]["superseded"]
    effective_receipt_ids = {receipt["id"] for receipt in effective_receipts}
    superseded_receipt_ids = {receipt["id"] for receipt in superseded_receipts}
    if len(effective_receipt_ids) != len(effective_receipts):
        errors.append("duplicate effective production receipt id")
    if len(superseded_receipt_ids) != len(superseded_receipts):
        errors.append("duplicate superseded production receipt id")
    overlap_receipt_ids = effective_receipt_ids & superseded_receipt_ids
    if overlap_receipt_ids:
        errors.append(f"effective/superseded production receipt overlap: {sorted(overlap_receipt_ids)}")
    source_receipt_id = production_identity["source_identity"]["receipt_id"]
    runtime_receipt_id = production_identity["production_runtime"]["receipt_id"]
    if source_receipt_id == runtime_receipt_id:
        errors.append("source and runtime production identities must use distinct receipts")
    for component, receipt_id in (
        ("source_identity", source_receipt_id),
        ("production_runtime", runtime_receipt_id),
    ):
        if receipt_id not in effective_receipt_ids:
            errors.append(f"production identity references non-effective receipt: {component} -> {receipt_id}")
    effective_authorities = {receipt["id"]: receipt["authority"] for receipt in effective_receipts}
    for receipt_id, expected_authority in (
        (source_receipt_id, "obsidian_claudian_bundle_identity"),
        (runtime_receipt_id, "omega_runtime_production"),
    ):
        actual_authority = effective_authorities.get(receipt_id)
        if actual_authority is not None and actual_authority != expected_authority:
            errors.append(
                "production receipt authority mismatch: "
                f"{receipt_id}={actual_authority}, expected={expected_authority}"
            )
    for receipt in superseded_receipts:
        if receipt["superseded_by"] not in effective_receipt_ids:
            errors.append(
                "superseded production receipt points to non-effective replacement: "
                f"{receipt['id']} -> {receipt['superseded_by']}"
            )
    valid_route_refs = tool_ids | set(CAPABILITY_ROLES)
    model_policy = documents[package / "config" / "model_capabilities.yaml"]
    provider_or_tool_ids = provider_ids | tool_ids
    for role_id, role in model_policy["capability_roles"].items():
        for reference in role.get("provider_chain", []):
            if reference not in provider_or_tool_ids:
                errors.append(f"unknown model capability provider/tool: {role_id} -> {reference}")
    migration = model_policy.get("migration", {})
    for alias, target in migration.get("provider_aliases", {}).items():
        if target not in provider_ids:
            errors.append(f"unknown provider alias target: {alias} -> {target}")
    for alias, target in migration.get("tool_aliases", {}).items():
        if target not in tool_ids:
            errors.append(f"unknown tool alias target: {alias} -> {target}")
    for tool in tools:
        for fallback in tool.get("fallbacks", []):
            if fallback not in tool_ids and fallback not in CAPABILITY_ROLES:
                errors.append(f"unknown tool fallback: {tool['id']} -> {fallback}")
    for agent in agents:
        overlap = set(agent.get("allowed_tools", [])) & set(agent.get("forbidden_tools", []))
        if overlap:
            errors.append(f"agent allowed/forbidden overlap: {agent['id']}: {sorted(overlap)}")
        for tool_id in agent.get("allowed_tools", []):
            if tool_id not in tool_ids:
                errors.append(f"unknown agent tool: {agent['id']} -> {tool_id}")
        for provider_id in agent.get("preferred_engines", []):
            if provider_id not in provider_ids:
                errors.append(f"unknown preferred provider class: {agent['id']} -> {provider_id}")
    for route in documents[package / "config" / "routing_table.yaml"]["routes"]:
        for stage in route["stages"]:
            for key in ("primary_tool", "fallback_tool"):
                reference = stage.get(key)
                if reference is not None and reference not in valid_route_refs:
                    errors.append(f"unknown route reference: {route['task_type']}.{stage['stage']}.{key}={reference}")
    engine_resolution = documents[package / "config" / "engine_resolution.yaml"]
    engine_provider_aliases = engine_resolution.get("provider_aliases", {})
    engine_tool_aliases = engine_resolution.get("tool_aliases", {})
    for alias, target in engine_provider_aliases.items():
        if target not in provider_ids:
            errors.append(f"unknown engine provider alias target: {alias} -> {target}")
    for alias, target in engine_tool_aliases.items():
        if target not in tool_ids:
            errors.append(f"unknown engine tool alias target: {alias} -> {target}")
    if engine_provider_aliases != migration.get("provider_aliases", {}):
        errors.append("engine/model provider alias maps differ from source of truth")
    if engine_tool_aliases != migration.get("tool_aliases", {}):
        errors.append("engine/model tool alias maps differ from source of truth")
    for strategy_id, strategy in engine_resolution.get("routing_strategies", {}).items():
        for reference in strategy.get("preference", []):
            if reference not in provider_or_tool_ids:
                errors.append(f"unknown engine strategy provider/tool: {strategy_id} -> {reference}")
    agent_ids = {agent["id"] for agent in agents}
    role_mapping = documents[package / "config" / "agent_role_mapping.yaml"]
    for mapping in role_mapping.get("mappings", []):
        for reference in mapping.get("runtime_agents", []):
            if reference not in agent_ids:
                errors.append(f"unknown agent role mapping target: {mapping.get('concept_agent')} -> {reference}")
    mapped_summary_ids = {item.get("id") for item in role_mapping.get("runtime_agents_summary", []) if isinstance(item, dict)}
    if mapped_summary_ids != agent_ids:
        errors.append(
            "runtime agent summary mismatch: "
            f"missing={sorted(agent_ids - mapped_summary_ids)}, unknown={sorted(mapped_summary_ids - agent_ids)}"
        )

    try:
        for name in ("tools.yaml", "agents.yaml", "routing_table.yaml", "active_engines.yaml"):
            source = documents.get(package / "config" / name) or documents.get(package / "templates" / name)
            if source is not None:
                _validate_effective_security(source, (name,))
    except PolicyValidationError as exc:
        errors.append(str(exc))

    if run_tests and not errors:
        test_env = dict(os.environ)
        test_env["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(package / "tests"), "-p", "test_*.py", "-v"],
            cwd=package,
            text=True,
            capture_output=True,
            check=False,
            env=test_env,
        )
        if completed.returncode != 0:
            errors.append("adversarial tests failed:\n" + completed.stdout + completed.stderr)
        powershells = []
        for shell_name in ("pwsh", "powershell"):
            resolved_shell = shutil.which(shell_name)
            if resolved_shell and resolved_shell.lower() not in {item.lower() for item in powershells}:
                powershells.append(resolved_shell)
        if not powershells:
            errors.append("PowerShell unavailable; endpoint policy test cannot run fail-closed")
        for powershell in powershells:
            shell_args = [powershell, "-NoProfile"]
            if Path(powershell).stem.lower() == "powershell":
                shell_args.extend(["-ExecutionPolicy", "Bypass"])
            shell_args.extend(["-File", str(package / "tests" / "test_endpoint_policy.ps1")])
            endpoint_test = subprocess.run(
                shell_args,
                cwd=package,
                text=True,
                capture_output=True,
                check=False,
                env=test_env,
            )
            if endpoint_test.returncode != 0 or "ENDPOINT_POLICY_TEST_PASS" not in endpoint_test.stdout:
                errors.append(
                    f"PowerShell endpoint adversarial test failed ({powershell}):\n"
                    + endpoint_test.stdout
                    + endpoint_test.stderr
                )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--skip-tests", action="store_true")
    args = parser.parse_args(argv)
    errors = run_gate(args.package.resolve(), run_tests=not args.skip_tests)
    if errors:
        for error in errors:
            print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    print("PACKAGE_GATE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
