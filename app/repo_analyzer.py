# --- DEBUG: show which analyzer file is actually imported ---
print("DEBUG repo_analyzer loaded from:", __file__)

from pathlib import Path
import re

def detect_type(repo_dir: Path):
    """Detect app type from requirements and key files."""
    # look for requirements both at repo root and app/
    reqs = ""
    for candidate in ["requirements.txt", "app/requirements.txt"]:
        f = repo_dir / candidate
        if f.exists():
            try:
                reqs += f.read_text(encoding="utf-8", errors="ignore").lower()
            except Exception:
                pass

    # quick scan of app.py variants
    app_py = ""
    for candidate in ["app.py", "app/app.py"]:
        f = repo_dir / candidate
        if f.exists():
            try:
                app_py += f.read_text(encoding="utf-8", errors="ignore").lower()
            except Exception:
                pass

    # Python frameworks
    if "django" in reqs:
        return "django"
    if ("flask" in reqs) or ("from flask import" in app_py) or ("flask(" in app_py):
        return "flask"
    if "fastapi" in reqs:
        return "fastapi"
    if reqs:
        return "python"

    # Node / Docker
    if (repo_dir / "package.json").exists():
        return "node"
    if (repo_dir / "Dockerfile").exists():
        return "dockerized"

    return "static_or_unknown"

def detect_port(repo_dir: Path):
    text = ""
    for p in repo_dir.rglob("*.*"):
        if p.suffix in {".py", ".js", ".ts", ".env", ".html"} and p.stat().st_size < 200_000:
            try:
                text += p.read_text(errors="ignore") + "\n"
            except Exception:
                pass

    m = re.search(r"port\s*=\s*(\d{2,5})", text, flags=re.IGNORECASE)
    if m:
        return int(m.group(1))

    m = re.search(r"PORT\s*[:=]\s*(\d{2,5})", text)
    if m:
        return int(m.group(1))

    for candidate in (5000, 8000, 8080, 3000):
        if str(candidate) in text:
            return candidate
    return 5000

def analyze(repo_dir: Path):
    app_type = detect_type(repo_dir)
    port = detect_port(repo_dir)
    has_dockerfile = (repo_dir / "Dockerfile").exists()
    has_lambda_handler = (repo_dir / "lambda_handler.py").exists() or (repo_dir / "handler.py").exists()
    env = []
    if (repo_dir / ".env.example").exists():
        try:
            env = [
                l.strip()
                for l in (repo_dir / ".env.example").read_text().splitlines()
                if l.strip() and "=" in l
            ]
        except Exception:
            pass
    return {
        "app_type": app_type,
        "port": port,
        "has_dockerfile": has_dockerfile,
        "has_lambda_handler": has_lambda_handler,
        "env": env,
    }
