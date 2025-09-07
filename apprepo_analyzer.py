from pathlib import Path

def analyze(repo_dir: Path):
    reqs = ""
    try:
        reqs = (repo_dir / "requirements.txt").read_text().lower()
    except Exception:
        pass

    # Debug print
    print("DEBUG requirements.txt content:", reqs)

    if "flask" in reqs:
        return {
            "app_type": "flask",
            "port": 5000,
            "has_dockerfile": False,
            "has_lambda_handler": False,
            "env": []
        }

    return {
        "app_type": "static_or_unknown",
        "port": 5000,
        "has_dockerfile": False,
        "has_lambda_handler": False,
        "env": []
    }
