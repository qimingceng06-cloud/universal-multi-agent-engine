import json
import sys
from pathlib import Path

from universal_multi_agent_sim.engine import main, run_from_config


def test_minimal_simulation_writes_expected_outputs(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    source_config = repo_root / "configs" / "minimal.yaml"
    config_text = source_config.read_text(encoding="utf-8").replace("outputs/run_local", str(tmp_path / "run_local"))
    config_path = tmp_path / "minimal.yaml"
    config_path.write_text(config_text, encoding="utf-8")

    summary = run_from_config(str(config_path))

    assert summary["scenario_name"] == "minimal-local-run"
    summary_path = tmp_path / "run_local" / "summary.json"
    events_path = tmp_path / "run_local" / "events.jsonl"
    metrics_path = tmp_path / "run_local" / "metrics.json"
    assert summary_path.exists()
    assert events_path.exists()
    assert metrics_path.exists()
    stored = json.loads(summary_path.read_text(encoding="utf-8"))
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    assert stored["event_count"] == 16
    assert stored["history_points"] == 16
    assert sum(stored["layer_usage"].values()) == 16
    assert len(metrics) == 16
    assert "world_temperature" in metrics[-1]
    assert "system_stability" in metrics[-1]
    assert len(events_path.read_text(encoding="utf-8").strip().splitlines()) == 16


def test_showcase_v2_writes_expected_outputs(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    source_config = repo_root / "configs" / "showcase_v2.yaml"
    config_text = source_config.read_text(encoding="utf-8").replace("outputs/run_showcase_v2", str(tmp_path / "run_showcase_v2"))
    config_path = tmp_path / "showcase_v2.yaml"
    config_path.write_text(config_text, encoding="utf-8")

    summary = run_from_config(str(config_path))

    assert summary["scenario_name"] == "v0.2-showcase-supply-demand-policy"
    summary_path = tmp_path / "run_showcase_v2" / "summary.json"
    events_path = tmp_path / "run_showcase_v2" / "events.jsonl"
    metrics_path = tmp_path / "run_showcase_v2" / "metrics.json"
    assert summary_path.exists()
    assert events_path.exists()
    assert metrics_path.exists()

    stored = json.loads(summary_path.read_text(encoding="utf-8"))
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))

    assert stored["history_points"] > 0
    assert sum(stored["layer_usage"].values()) == stored["event_count"]
    assert len(metrics) == stored["history_points"]

    last_metrics = metrics[-1]
    assert "world_temperature" in last_metrics
    assert "system_stability" in last_metrics
    assert "volatility_index" in last_metrics
    assert "confidence_index" in last_metrics
    assert "liquidity_index" in last_metrics
    assert "stress_index" in last_metrics

    assert len(events_path.read_text(encoding="utf-8").strip().splitlines()) == stored["event_count"]


def test_cli_main_pretty_outputs_json_and_writes_artifacts(tmp_path, monkeypatch, capsys):
    repo_root = Path(__file__).resolve().parents[1]
    source_config = repo_root / "configs" / "minimal.yaml"
    config_text = source_config.read_text(encoding="utf-8").replace("outputs/run_local", str(tmp_path / "run_local"))
    config_path = tmp_path / "minimal.yaml"
    config_path.write_text(config_text, encoding="utf-8")

    monkeypatch.setattr(sys, "argv", ["universal-multi-agent-sim", str(config_path), "--pretty"])

    main()

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert payload["scenario_name"] == "minimal-local-run"
    assert payload["output_dir"] == str(tmp_path / "run_local")
    assert (tmp_path / "run_local" / "summary.json").exists()
    assert (tmp_path / "run_local" / "events.jsonl").exists()
    assert (tmp_path / "run_local" / "metrics.json").exists()
