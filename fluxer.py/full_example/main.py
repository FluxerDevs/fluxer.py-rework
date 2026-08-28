import os
import sys
from pathlib import Path

EXAMPLE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = EXAMPLE_ROOT.parent
WORKSPACE_ROOT = PROJECT_ROOT.parent


def ensure_repo_venv() -> None:
    if os.getenv("FLUXER_FULL_EXAMPLE_NO_VENV"):
        return
    if os.name == "nt":
        venv_python = WORKSPACE_ROOT / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = WORKSPACE_ROOT / ".venv" / "bin" / "python"
    if not venv_python.exists():
        return
    current = Path(sys.executable).resolve()
    target = venv_python.resolve()
    if str(current).lower() == str(target).lower():
        return
    os.execv(str(target), [str(target), *sys.argv])


ensure_repo_venv()

for path in (PROJECT_ROOT, EXAMPLE_ROOT):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)


def load_local_env() -> None:
    env_path = EXAMPLE_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_dev_token() -> str:
    load_local_env()
    token = os.getenv("DEV_TOKEN", "").strip()
    if not token:
        raise RuntimeError("DEV_TOKEN is not set in full_example/.env")
    return token

from bot import FullFeatureBot

load_local_env()
bot = FullFeatureBot(command_prefix=os.getenv("PREFIX", "!"))

if __name__ == "__main__":
    bot.run(load_dev_token())

