
from pathlib import Path
import re

def detect_type(repo_dir: Path):
    if (repo_dir / "package.json").exists():
        return "node"
    if (repo_dir / "manage.py").exists() or (repo_dir / "requirements.txt").exists() or (repo_dir / "app.py").exists():
        reqs = ""
        if (repo_dir / "requirements.txt").exists():
            try: reqs = (repo_dir / "requirements.txt").read_text().lower()
            except: pass
        if "django" in reqs: return "django"
        if "flask" in reqs: return "flask"
        if "fastapi" in reqs: return "fastapi"
        return "python"
    if (repo_dir / "Dockerfile").exists():
        return "dockerized"
    return "static_or_unknown"

def detect_port(repo_dir: Path):
    text = ""
    for p in repo_dir.rglob("*.*"):
        if p.suffix in {".py", ".js", ".ts", ".env", ".html"} and p.stat().st_size < 200_000:
            try: text += p.read_text(errors="ignore") + "\n"
            except: pass
    m = re.search(r'PORT\s*[:=]\s*(\d{2,5})', text)
    if m: return int(m.group(1))
    for candidate in (5000, 8000, 8080, 3000):
        if str(candidate) in text: return candidate
    return 5000

def analyze(repo_dir: Path):
    app_type = detect_type(repo_dir)
    port = detect_port(repo_dir)
    has_dockerfile = (repo_dir/"Dockerfile").exists()
    has_lambda_handler = (repo_dir/"lambda_handler.py").exists() or (repo_dir/"handler.py").exists()
    env = []
    if (repo_dir/".env.example").exists():
        try:
            env = [l.strip() for l in (repo_dir/".env.example").read_text().splitlines() if l.strip() and "=" in l]
        except: pass
    return {
        "app_type": app_type,
        "port": port,
        "has_dockerfile": has_dockerfile,
        "has_lambda_handler": has_lambda_handler,
        "env": env
    }
