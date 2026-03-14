from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from universal_multi_agent_sim.engine import run_from_config


if __name__ == "__main__":
    config_path = ROOT / "configs" / "minimal.yaml"
    summary = run_from_config(str(config_path))
    print(summary)
