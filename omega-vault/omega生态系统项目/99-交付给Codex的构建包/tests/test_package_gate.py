from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
import copy
from pathlib import Path
from unittest import mock

import yaml

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "scripts"))

import package_gate  # noqa: E402


class PackageGateTests(unittest.TestCase):
    def test_current_package_passes_without_recursive_test_run(self) -> None:
        self.assertEqual(package_gate.run_gate(PACKAGE, run_tests=False), [])

    def test_missing_required_file_and_unregistered_active_file_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            clone = Path(directory) / "package"
            shutil.copytree(PACKAGE, clone, ignore=shutil.ignore_patterns("__pycache__"))
            (clone / "config" / "model_capabilities.yaml").unlink()
            (clone / "config" / "rogue-active.yaml").write_text("provider: anthropic\n", encoding="utf-8")
            errors = package_gate.run_gate(clone, run_tests=False)
            joined = "\n".join(errors)
            self.assertIn("required file missing: build-package/config/model_capabilities.yaml", joined)
            self.assertIn("unregistered active file: build-package/config/rogue-active.yaml", joined)

    def test_stale_public_manifest_summary_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            clone = Path(directory) / "package"
            shutil.copytree(PACKAGE, clone, ignore=shutil.ignore_patterns("__pycache__"))
            manifest_path = clone / "MANIFEST.yaml"
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            manifest["summary"]["total_files"] -= 1
            manifest_path.write_text(
                yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False),
                encoding="utf-8",
            )
            errors = package_gate.run_gate(clone, run_tests=False)
            self.assertIn(
                "MANIFEST public summary mismatch: total_files=84, actual=85",
                errors,
            )

    def test_production_identity_schema_rejects_non_codex_primary(self) -> None:
        original_load = package_gate._load_yaml

        def non_codex_primary(path: Path):
            value = original_load(path)
            if path.name == "PRODUCTION_IDENTITY_LEDGER.yaml":
                value = copy.deepcopy(value)
                value["policy"]["primary_provider"] = "anthropic"
            return value

        with mock.patch.object(package_gate, "_load_yaml", side_effect=non_codex_primary):
            errors = package_gate.run_gate(PACKAGE, run_tests=False)
        self.assertTrue(any("schema validation failed" in error for error in errors), errors)

    def test_production_identity_reference_must_resolve_to_effective_receipt(self) -> None:
        original_load = package_gate._load_yaml

        def missing_effective_receipt(path: Path):
            value = original_load(path)
            if path.name == "PRODUCTION_IDENTITY_LEDGER.yaml":
                value = copy.deepcopy(value)
                value["production_runtime"]["receipt_id"] = "unknown-runtime-receipt"
            return value

        with mock.patch.object(package_gate, "_load_yaml", side_effect=missing_effective_receipt):
            errors = package_gate.run_gate(PACKAGE, run_tests=False)
        self.assertIn(
            "production identity references non-effective receipt: production_runtime -> unknown-runtime-receipt",
            errors,
        )

    def test_superseded_receipt_must_point_to_effective_replacement(self) -> None:
        original_load = package_gate._load_yaml

        def missing_replacement(path: Path):
            value = original_load(path)
            if path.name == "PRODUCTION_IDENTITY_LEDGER.yaml":
                value = copy.deepcopy(value)
                value["receipts"]["superseded"][0]["superseded_by"] = "unknown-replacement"
            return value

        with mock.patch.object(package_gate, "_load_yaml", side_effect=missing_replacement):
            errors = package_gate.run_gate(PACKAGE, run_tests=False)
        self.assertIn(
            "superseded production receipt points to non-effective replacement: "
            "omega-r142-production-codex-e2e -> unknown-replacement",
            errors,
        )

    def test_engine_alias_namespace_confusion_fails(self) -> None:
        original_load = package_gate._load_yaml

        def confused(path: Path):
            value = original_load(path)
            if path.name == "engine_resolution.yaml":
                value = copy.deepcopy(value)
                value["provider_aliases"]["claude_api"] = "codex_cli"
            return value

        with mock.patch.object(package_gate, "_load_yaml", side_effect=confused):
            errors = package_gate.run_gate(PACKAGE, run_tests=False)
        self.assertTrue(
            any("unknown engine provider alias target" in error for error in errors),
            errors,
        )
        self.assertIn("engine/model provider alias maps differ from source of truth", errors)

    def test_engine_alias_drift_from_source_of_truth_fails(self) -> None:
        original_load = package_gate._load_yaml

        def drifted(path: Path):
            value = original_load(path)
            if path.name == "engine_resolution.yaml":
                value = copy.deepcopy(value)
                value["provider_aliases"]["gpt3_api"] = "openai_api"
            return value

        with mock.patch.object(package_gate, "_load_yaml", side_effect=drifted):
            errors = package_gate.run_gate(PACKAGE, run_tests=False)
        self.assertIn("engine/model provider alias maps differ from source of truth", errors)


if __name__ == "__main__":
    unittest.main()
