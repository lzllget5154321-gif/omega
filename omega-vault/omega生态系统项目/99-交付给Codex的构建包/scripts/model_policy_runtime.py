"""Executable Codex-first model policy validation, discovery and migration.

This module never logs credential values. It is deliberately standard-library-only
except for PyYAML, which is already required by Omega's YAML configuration layer.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable, Mapping

import yaml

FORBIDDEN_ENV_KEYS = frozenset({"ANTHROPIC_API_KEY"})
FORBIDDEN_PROVIDER_IDS = frozenset({"anthropic"})
FORBIDDEN_HOST_SUFFIXES = ("anthropic.com",)
CONCRETE_PREFERRED_ENGINES = frozenset(
    {
        "claude_api",
        "gpt4_api",
        "deepseek_api",
        "qwen_api",
        "zhipu_api",
        "moonshot_api",
        "siliconflow_api",
    }
)
CAPABILITY_ROLES = frozenset(
    {
        "engineering_primary",
        "quality_reasoning",
        "academic_writing",
        "economical_general",
        "realtime_search",
    }
)
_UNICODE_DOTS = str.maketrans({"\u3002": ".", "\uff0e": ".", "\uff61": "."})


class PolicyValidationError(ValueError):
    """Raised when a provider, endpoint or candidate policy fails closed."""


Probe = Callable[[str, Mapping[str, Any]], bool | Mapping[str, Any]]


def _decode_percent(value: str) -> str:
    """Decode nested percent escapes with a strict finite bound."""

    current = value
    for _ in range(6):
        decoded = urllib.parse.unquote(current, errors="strict")
        if decoded == current:
            return decoded
        current = decoded
    raise PolicyValidationError("excessive nested percent encoding")


def canonicalize_host(host: str) -> str:
    """Return an IDNA/lowercase host with Unicode/encoded dots normalized."""

    normalized = _decode_percent(host).translate(_UNICODE_DOTS).rstrip(".").lower()
    if not normalized or any(ch in normalized for ch in "/\\@:#"):
        raise PolicyValidationError("invalid endpoint host")
    try:
        return normalized.encode("idna").decode("ascii")
    except UnicodeError as exc:
        raise PolicyValidationError("invalid IDNA endpoint host") from exc


def is_forbidden_host(host: str) -> bool:
    """Return True for Anthropic native hosts and all their subdomains."""

    canonical = canonicalize_host(host)
    return any(canonical == suffix or canonical.endswith(f".{suffix}") for suffix in FORBIDDEN_HOST_SUFFIXES)


def validate_and_canonicalize_url(url: str) -> str:
    """Validate a request/redirect URL and return its canonical representation."""

    decoded = _decode_percent(url.strip()).translate(_UNICODE_DOTS)
    try:
        parsed = urllib.parse.urlsplit(decoded)
        port = parsed.port
    except ValueError as exc:
        raise PolicyValidationError("invalid endpoint URL or port") from exc
    scheme = parsed.scheme.lower()
    if scheme not in {"http", "https"}:
        raise PolicyValidationError("endpoint scheme must be http or https")
    if parsed.username is not None or parsed.password is not None:
        raise PolicyValidationError("endpoint userinfo is forbidden")
    if not parsed.hostname:
        raise PolicyValidationError("endpoint host is required")
    host = canonicalize_host(parsed.hostname)
    if is_forbidden_host(host):
        raise PolicyValidationError("native Anthropic endpoints are forbidden")
    if ":" in host and not host.startswith("["):
        host_display = f"[{host}]"
    else:
        host_display = host
    default_port = (scheme == "https" and port == 443) or (scheme == "http" and port == 80)
    netloc = host_display if port is None or default_port else f"{host_display}:{port}"
    path = parsed.path or "/"
    return urllib.parse.urlunsplit((scheme, netloc, path, parsed.query, ""))


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


def fetch_json_with_validated_redirects(
    url: str,
    *,
    headers: Mapping[str, str] | None = None,
    timeout_seconds: float = 2.0,
    max_redirects: int = 4,
) -> Any:
    """Fetch JSON while validating every request and redirect target fail-closed."""

    opener = urllib.request.build_opener(_NoRedirect())
    current = validate_and_canonicalize_url(url)
    for _ in range(max_redirects + 1):
        current = validate_and_canonicalize_url(current)
        request = urllib.request.Request(current, headers=dict(headers or {}))
        try:
            with opener.open(request, timeout=timeout_seconds) as response:
                final_url = validate_and_canonicalize_url(response.geturl())
                if final_url != validate_and_canonicalize_url(current):
                    raise PolicyValidationError("unvalidated implicit redirect")
                payload = response.read(4 * 1024 * 1024 + 1)
                if len(payload) > 4 * 1024 * 1024:
                    raise PolicyValidationError("model discovery response too large")
                return json.loads(payload.decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code not in {301, 302, 303, 307, 308}:
                raise
            location = exc.headers.get("Location")
            exc.close()
            if not location:
                raise PolicyValidationError("redirect without Location") from exc
            current = validate_and_canonicalize_url(urllib.parse.urljoin(current, location))
    raise PolicyValidationError("too many redirects")


def _walk_security(value: Any, path: tuple[str, ...] = (), *, allow_legacy_preferred: bool = False) -> None:
    if isinstance(value, dict):
        for raw_key, child in value.items():
            key = str(raw_key)
            upper_key = key.upper()
            if upper_key in FORBIDDEN_ENV_KEYS:
                raise PolicyValidationError(f"forbidden credential key at {'.'.join(path + (key,))}")
            if key.lower() in {"provider", "provider_id"} and str(child).strip().lower() in FORBIDDEN_PROVIDER_IDS:
                raise PolicyValidationError(f"forbidden provider at {'.'.join(path + (key,))}")
            if not allow_legacy_preferred and key == "preferred_engine" and str(child) in CONCRETE_PREFERRED_ENGINES:
                raise PolicyValidationError(f"concrete preferred_engine at {'.'.join(path + (key,))}")
            if isinstance(child, str) and child.upper() in FORBIDDEN_ENV_KEYS:
                raise PolicyValidationError(f"forbidden credential reference at {'.'.join(path + (key,))}")
            if isinstance(child, str) and any(token in key.lower() for token in ("url", "endpoint")) and "://" in child:
                validate_and_canonicalize_url(child)
            child_allow_legacy = allow_legacy_preferred or (not path and key == "_migration")
            _walk_security(child, path + (key,), allow_legacy_preferred=child_allow_legacy)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_security(child, path + (str(index),), allow_legacy_preferred=allow_legacy_preferred)


def validate_candidate(candidate: Mapping[str, Any]) -> None:
    """Validate a current or migrated registry without discarding unknown fields."""

    if not isinstance(candidate, Mapping):
        raise PolicyValidationError("candidate must be a mapping")
    _walk_security(candidate)
    current = candidate.get("current", candidate)
    agents = current.get("agents", []) if isinstance(current, Mapping) else []
    if agents:
        if not isinstance(agents, list):
            raise PolicyValidationError("current agents must be a list")
        for agent in agents:
            if not isinstance(agent, Mapping) or agent.get("capability_role") not in CAPABILITY_ROLES:
                raise PolicyValidationError("every current agent requires a stable capability_role")


def validate_legacy_candidate(candidate: Mapping[str, Any]) -> None:
    """Validate compatibility input while allowing old engine IDs only inside the preserved envelope."""

    if not isinstance(candidate, Mapping):
        raise PolicyValidationError("legacy candidate must be a mapping")
    _walk_security(candidate, allow_legacy_preferred=True)


def resolve_engine(
    policy: Mapping[str, Any],
    capability_role: str,
    probe: Probe,
    *,
    allow_local_disaster_recovery: bool = False,
) -> dict[str, Any]:
    """Resolve a stable capability role without pinning or deleting unknown IDs.

    ``probe`` is the integration boundary. It receives a provider/candidate ID and
    its current settings and returns either a boolean or a mapping containing
    ``healthy`` and optional ``models``. Probe failures are treated as unhealthy;
    the ordered chain continues without mutating ``policy``.
    """

    validate_candidate(policy)
    roles = policy.get("capability_roles")
    providers = policy.get("providers")
    if not isinstance(roles, Mapping) or capability_role not in roles:
        raise PolicyValidationError(f"unknown capability role: {capability_role}")
    if not isinstance(providers, Mapping):
        raise PolicyValidationError("provider registry is missing")
    role = roles[capability_role]
    chain = role.get("provider_chain", []) if isinstance(role, Mapping) else []
    if not isinstance(chain, list):
        raise PolicyValidationError("provider chain must be a list")

    for provider_id in chain:
        provider_id = str(provider_id)
        provider_settings = providers.get(provider_id, {})
        if not isinstance(provider_settings, Mapping):
            raise PolicyValidationError(f"provider settings must be a mapping: {provider_id}")
        if provider_id == "local_disaster_recovery" and not allow_local_disaster_recovery:
            continue
        candidates = provider_settings.get("candidates")
        candidate_ids = [str(value) for value in candidates] if isinstance(candidates, list) and candidates else [provider_id]
        for candidate_id in candidate_ids:
            candidate_settings = providers.get(candidate_id, provider_settings if candidate_id == provider_id else {})
            if not isinstance(candidate_settings, Mapping):
                candidate_settings = {}
            try:
                result = probe(candidate_id, copy.deepcopy(dict(candidate_settings)))
            except Exception:
                continue
            details = {"healthy": result} if isinstance(result, bool) else dict(result) if isinstance(result, Mapping) else {}
            if not details.get("healthy", False):
                continue
            models = details.get("models", [])
            if models is None:
                models = []
            if not isinstance(models, list):
                raise PolicyValidationError(f"probe models must be a list: {candidate_id}")
            configured_model = candidate_settings.get("model")
            model_id = configured_model if configured_model in models else (models[0] if models else configured_model)
            return {
                "capability_role": capability_role,
                "provider_id": provider_id,
                "candidate_id": candidate_id,
                "model_id": model_id,
                "discovered_models": copy.deepcopy(models),
            }
    raise PolicyValidationError(f"no healthy engine for capability role: {capability_role}")


def migrate_legacy(source: Mapping[str, Any]) -> dict[str, Any]:
    """Create a v3 lossless envelope; restore_legacy returns byte-meaning-equivalent data."""

    validate_legacy_candidate(source)
    legacy = copy.deepcopy(dict(source))
    result: dict[str, Any] = {
        "schema_version": "3.0",
        "current": {
            "policy_source": "model_capabilities.yaml",
            "providers": [],
            "agents": [],
            "unknown_entries": [],
        },
        "_migration": {
            "format": "lossless-envelope-v1",
            "legacy_input": legacy,
            "route_history": copy.deepcopy(legacy.get("route_history", [])),
            "unknown_preservation": "exact-structural-copy",
        },
    }
    validate_candidate(result)
    return result


def restore_legacy(migrated: Mapping[str, Any]) -> dict[str, Any]:
    """Restore the exact legacy structure stored in a lossless migration envelope."""

    migration = migrated.get("_migration")
    if not isinstance(migration, Mapping) or migration.get("format") != "lossless-envelope-v1":
        raise PolicyValidationError("not a lossless migration envelope")
    legacy = migration.get("legacy_input")
    if not isinstance(legacy, Mapping):
        raise PolicyValidationError("lossless legacy input missing")
    return copy.deepcopy(dict(legacy))


def _serialized(
    candidate: Mapping[str, Any],
    *,
    validator: Callable[[Mapping[str, Any]], None] = validate_candidate,
) -> bytes:
    validator(candidate)
    payload = yaml.safe_dump(dict(candidate), allow_unicode=True, sort_keys=False).encode("utf-8")
    loaded = yaml.safe_load(payload.decode("utf-8"))
    validator(loaded)
    return payload


def atomic_replace_yaml(
    target: Path,
    candidate: Mapping[str, Any],
    *,
    replace: Callable[[str | bytes | os.PathLike[str] | os.PathLike[bytes], str | bytes | os.PathLike[str] | os.PathLike[bytes]], None] = os.replace,
    validator: Callable[[Mapping[str, Any]], None] = validate_candidate,
) -> Path | None:
    """Validate, fsync and atomically replace target; retain target.previous."""

    payload = _serialized(candidate, validator=validator)  # Validation failure occurs before any filesystem write.
    target = target.resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    previous = target.with_name(f"{target.name}.previous")
    temp_path: Path | None = None
    backup_temp: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix=f".{target.name}.", suffix=".tmp", delete=False) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
            temp_path = Path(handle.name)
        if target.exists():
            with tempfile.NamedTemporaryFile(dir=target.parent, prefix=f".{target.name}.previous.", suffix=".tmp", delete=False) as handle:
                backup_temp = Path(handle.name)
            shutil.copyfile(target, backup_temp)
            with backup_temp.open("r+b") as handle:
                handle.flush()
                os.fsync(handle.fileno())
            replace(backup_temp, previous)
            backup_temp = None
        replace(temp_path, target)
        temp_path = None
        return previous if previous.exists() else None
    finally:
        for leftover in (temp_path, backup_temp):
            if leftover is not None:
                leftover.unlink(missing_ok=True)


def rollback_yaml(target: Path) -> None:
    """Atomically restore target.previous after validating it."""

    target = target.resolve()
    previous = target.with_name(f"{target.name}.previous")
    if not previous.exists():
        raise PolicyValidationError("rollback file is missing")
    candidate = yaml.safe_load(previous.read_text(encoding="utf-8"))
    try:
        payload = _serialized(candidate)
    except PolicyValidationError:
        # A migration may have replaced a legacy active file. Rollback must be
        # lossless while still enforcing the legacy security boundary.
        payload = _serialized(candidate, validator=validate_legacy_candidate)
    with tempfile.NamedTemporaryFile(dir=target.parent, prefix=f".{target.name}.rollback.", suffix=".tmp", delete=False) as handle:
        temp = Path(handle.name)
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        os.replace(temp, target)
    finally:
        temp.unlink(missing_ok=True)


def _load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise PolicyValidationError("YAML root must be a mapping")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("path", type=Path)
    migrate_parser = sub.add_parser("migrate")
    migrate_parser.add_argument("source", type=Path)
    migrate_parser.add_argument("target", type=Path)
    restore_parser = sub.add_parser("restore")
    restore_parser.add_argument("source", type=Path)
    restore_parser.add_argument("target", type=Path)
    rollback_parser = sub.add_parser("rollback")
    rollback_parser.add_argument("target", type=Path)
    resolve_parser = sub.add_parser("resolve")
    resolve_parser.add_argument("policy", type=Path)
    resolve_parser.add_argument("capability_role")
    resolve_parser.add_argument("health", type=Path, help="YAML mapping of candidate ID to healthy/models")
    resolve_parser.add_argument("--allow-local-disaster-recovery", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "validate":
        validate_candidate(_load_yaml(args.path))
    elif args.command == "migrate":
        atomic_replace_yaml(args.target, migrate_legacy(_load_yaml(args.source)))
    elif args.command == "restore":
        atomic_replace_yaml(
            args.target,
            restore_legacy(_load_yaml(args.source)),
            validator=validate_legacy_candidate,
        )
    elif args.command == "resolve":
        health = _load_yaml(args.health)

        def health_probe(candidate_id: str, _: Mapping[str, Any]) -> bool | Mapping[str, Any]:
            return health.get(candidate_id, False)

        resolved = resolve_engine(
            _load_yaml(args.policy),
            args.capability_role,
            health_probe,
            allow_local_disaster_recovery=args.allow_local_disaster_recovery,
        )
        print(yaml.safe_dump(resolved, allow_unicode=True, sort_keys=False).rstrip())
    else:
        rollback_yaml(args.target)
    print("MODEL_POLICY_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
