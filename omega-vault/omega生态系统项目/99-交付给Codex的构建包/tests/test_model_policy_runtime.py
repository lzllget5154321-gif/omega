from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

import yaml
from jsonschema import Draft202012Validator, ValidationError

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "scripts"))

import model_policy_runtime as runtime  # noqa: E402


class _Response:
    def __init__(self, url: str, body: bytes = b'{"data": []}') -> None:
        self._url = url
        self._body = body

    def __enter__(self) -> "_Response":
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def geturl(self) -> str:
        return self._url

    def read(self, _: int) -> bytes:
        return self._body


class ModelPolicyRuntimeTests(unittest.TestCase):
    def test_native_anthropic_url_variants_are_rejected(self) -> None:
        variants = [
            "https://api.anthropic.com",
            "https://api.anthropic.com.:443/v1/models",
            "https://API.ANTHROPIC.COM:8443/v1/models",
            "https://api\u3002anthropic\uff0ecom/v1/models",
            "https://api%2eanthropic%2ecom/v1/models",
            "https://api%252eanthropic.com/v1/models",
            "https://api.anthropic.com%2e/v1/models",
            "https://x.api.anthropic.com/v1/models",
        ]
        for value in variants:
            with self.subTest(value=value), self.assertRaises(runtime.PolicyValidationError):
                runtime.validate_and_canonicalize_url(value)

    def test_safe_endpoint_is_canonicalized(self) -> None:
        self.assertEqual(
            runtime.validate_and_canonicalize_url("HTTPS://OPENROUTER.AI.:443/api/v1/models#fragment"),
            "https://openrouter.ai/api/v1/models",
        )

    def test_redirect_target_is_validated_before_second_request(self) -> None:
        class RedirectingOpener:
            calls = 0

            def open(self, request: object, timeout: float) -> object:
                self.calls += 1
                headers = {"Location": "https://api%2eanthropic%2ecom/v1/models"}
                raise urllib.error.HTTPError(str(getattr(request, "full_url")), 302, "redirect", headers, None)

        opener = RedirectingOpener()
        with mock.patch.object(runtime.urllib.request, "build_opener", return_value=opener):
            with self.assertRaises(runtime.PolicyValidationError):
                runtime.fetch_json_with_validated_redirects("https://openrouter.ai/api/v1/models")
        self.assertEqual(opener.calls, 1)

    def test_final_response_url_is_revalidated(self) -> None:
        class FinalUrlOpener:
            def open(self, request: object, timeout: float) -> _Response:
                return _Response("https://api.anthropic.com/v1/models")

        with mock.patch.object(runtime.urllib.request, "build_opener", return_value=FinalUrlOpener()):
            with self.assertRaises(runtime.PolicyValidationError):
                runtime.fetch_json_with_validated_redirects("https://openrouter.ai/api/v1/models")

    def test_security_tree_rejects_native_credentials_provider_url_and_concrete_preference(self) -> None:
        negatives = [
            {"env_var": "ANTHROPIC_API_KEY"},
            {"ANTHROPIC_API_KEY": ""},
            {"provider": "anthropic"},
            {"base_url": "https://api%2eanthropic.com"},
            {"preferred_engine": "deepseek_api"},
        ]
        for candidate in negatives:
            with self.subTest(candidate=candidate), self.assertRaises(runtime.PolicyValidationError):
                runtime.validate_candidate(candidate)

    def test_current_agent_requires_capability_role(self) -> None:
        with self.assertRaises(runtime.PolicyValidationError):
            runtime.validate_candidate({"current": {"agents": [{"id": "writer"}]}})

    def test_resolver_uses_ordered_fallback_and_preserves_unknown_discovered_model(self) -> None:
        policy = yaml.safe_load((PACKAGE / "config" / "model_capabilities.yaml").read_text(encoding="utf-8"))
        calls = []

        def probe(candidate_id: str, settings: object) -> object:
            calls.append(candidate_id)
            if candidate_id == "codex_session":
                raise TimeoutError("candidate probe failed")
            if candidate_id == "openai_api":
                return {"healthy": True, "models": ["future-model-id-unchanged"]}
            return False

        before = copy.deepcopy(policy)
        resolved = runtime.resolve_engine(policy, "engineering_primary", probe)
        self.assertEqual(calls, ["codex_session", "openai_api"])
        self.assertEqual(resolved["candidate_id"], "openai_api")
        self.assertEqual(resolved["model_id"], "future-model-id-unchanged")
        self.assertEqual(policy, before)

    def test_resolver_skips_local_disaster_recovery_until_explicit(self) -> None:
        policy = {
            "capability_roles": {"engineering_primary": {"provider_chain": ["local_disaster_recovery"]}},
            "providers": {"local_disaster_recovery": {"candidates": ["unknown_local_runtime"]}},
        }
        with self.assertRaises(runtime.PolicyValidationError):
            runtime.resolve_engine(policy, "engineering_primary", lambda *_: {"healthy": True, "models": ["local-unknown"]})
        resolved = runtime.resolve_engine(
            policy,
            "engineering_primary",
            lambda *_: {"healthy": True, "models": ["local-unknown"]},
            allow_local_disaster_recovery=True,
        )
        self.assertEqual(resolved["candidate_id"], "unknown_local_runtime")

    def test_current_and_legacy_agent_schemas_separate_compatibility_input(self) -> None:
        current_schema = json.loads((PACKAGE / "schemas" / "agent_card.schema.json").read_text(encoding="utf-8"))
        legacy_schema = json.loads((PACKAGE / "schemas" / "legacy_agent_card.schema.json").read_text(encoding="utf-8"))
        legacy = {"id": "writer", "preferred_engine": "deepseek_api", "future_unknown": {"keep": True}}
        Draft202012Validator(legacy_schema).validate(legacy)
        with self.assertRaises(ValidationError):
            Draft202012Validator(current_schema).validate(legacy)
        current = {
            "id": "writer",
            "role": "writer",
            "allowed_tools": [],
            "capability_role": "engineering_primary",
        }
        for legacy_field in ("model", "provider", "preferred_model", "preferred_provider"):
            with self.subTest(legacy_field=legacy_field), self.assertRaises(ValidationError):
                Draft202012Validator(current_schema).validate(
                    {**current, legacy_field: "fixed-version-or-provider"}
                )
        Draft202012Validator(current_schema).validate(
            {**current, "future_non_model_setting": {"preserve": True}}
        )

    def test_model_policy_schema_rejects_native_provider_and_credential(self) -> None:
        schema = json.loads((PACKAGE / "schemas" / "model_policy.schema.json").read_text(encoding="utf-8"))
        base = yaml.safe_load((PACKAGE / "config" / "model_capabilities.yaml").read_text(encoding="utf-8"))
        negatives = []
        provider = copy.deepcopy(base)
        provider["providers"]["anthropic"] = {"transport": "claude_messages"}
        negatives.append(provider)
        credential = copy.deepcopy(base)
        credential["providers"]["openai_api"]["api_key_env_var"] = "ANTHROPIC_API_KEY"
        negatives.append(credential)
        endpoint = copy.deepcopy(base)
        endpoint["providers"]["openai_api"]["default_base_url"] = "https://api.anthropic.com"
        negatives.append(endpoint)
        for candidate in negatives:
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(candidate)

    def test_unknown_nested_fields_models_and_route_history_round_trip_losslessly(self) -> None:
        legacy = {
            "schema_version": "2.8",
            "provider_id": "future_provider_x",
            "model_id": "future-model-2039",
            "preferred_engine": "deepseek_api",
            "nested": {"unknown": [{"alpha": 1, "beta": [True, None, "原样"]}]},
            "route_history": [{"from": "old", "to": "future", "metadata": {"unknown": 9}}],
        }
        migrated = runtime.migrate_legacy(legacy)
        restored = runtime.restore_legacy(migrated)
        self.assertEqual(restored, legacy)
        self.assertEqual(migrated["_migration"]["route_history"], legacy["route_history"])
        self.assertIsNot(migrated["_migration"]["legacy_input"], legacy)
        with self.assertRaises(runtime.PolicyValidationError):
            runtime.validate_candidate({"current": {"preferred_engine": legacy["preferred_engine"]}})

    def test_restore_cli_path_accepts_valid_legacy_and_preserves_unknowns(self) -> None:
        legacy = {
            "id": "writer",
            "preferred_engine": "deepseek_api",
            "model": "future-model-2039",
            "future_unknown": {"keep": [1, True, None]},
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "migrated.yaml"
            target = root / "restored.yaml"
            source.write_text(
                yaml.safe_dump(runtime.migrate_legacy(legacy), allow_unicode=True, sort_keys=False),
                encoding="utf-8",
            )
            self.assertEqual(runtime.main(["restore", str(source), str(target)]), 0)
            self.assertEqual(yaml.safe_load(target.read_text(encoding="utf-8")), legacy)

    def test_rollback_restores_secure_legacy_previous_file(self) -> None:
        legacy = {"id": "writer", "preferred_engine": "deepseek_api", "future": "preserved"}
        current = {"current": {"capability_role": "engineering_primary"}}
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "active.yaml"
            target.write_text(yaml.safe_dump(legacy, sort_keys=False), encoding="utf-8")
            runtime.atomic_replace_yaml(target, current)
            runtime.rollback_yaml(target)
            self.assertEqual(yaml.safe_load(target.read_text(encoding="utf-8")), legacy)

    def test_validation_failure_writes_nothing_and_does_not_replace_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "active.yaml"
            original = b"sentinel: original\n"
            target.write_bytes(original)
            before = sorted(path.name for path in Path(directory).iterdir())
            with self.assertRaises(runtime.PolicyValidationError):
                runtime.atomic_replace_yaml(target, {"provider": "anthropic"})
            self.assertEqual(target.read_bytes(), original)
            self.assertEqual(sorted(path.name for path in Path(directory).iterdir()), before)

    def test_atomic_replace_retains_previous_and_rollback_restores_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "active.yaml"
            original = {"schema_version": "3.0", "unknown": {"keep": True}}
            target.write_text(yaml.safe_dump(original), encoding="utf-8")
            candidate = {"schema_version": "3.0", "current": {"agents": []}, "future": [1, 2, 3]}
            previous = runtime.atomic_replace_yaml(target, candidate)
            self.assertIsNotNone(previous)
            self.assertEqual(yaml.safe_load(target.read_text(encoding="utf-8")), candidate)
            self.assertEqual(yaml.safe_load(previous.read_text(encoding="utf-8")), original)
            runtime.rollback_yaml(target)
            self.assertEqual(yaml.safe_load(target.read_text(encoding="utf-8")), original)

    def test_replace_failure_leaves_original_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "active.yaml"
            original = {"schema_version": "3.0", "value": "original"}
            target.write_text(yaml.safe_dump(original), encoding="utf-8")
            calls = 0

            def fail_on_target(source: object, destination: object) -> None:
                nonlocal calls
                calls += 1
                if Path(destination) == target:
                    raise OSError("simulated replace failure")
                runtime.os.replace(source, destination)

            with self.assertRaises(OSError):
                runtime.atomic_replace_yaml(target, {"schema_version": "3.0", "value": "candidate"}, replace=fail_on_target)
            self.assertEqual(yaml.safe_load(target.read_text(encoding="utf-8")), original)
            self.assertEqual(calls, 2)


if __name__ == "__main__":
    unittest.main()
