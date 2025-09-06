
def choose_platform(analysis, nl_prompt: str):
    p = nl_prompt.lower()
    if analysis.get("has_dockerfile"):
        return "ecs"
    if ("serverless" in p or "lambda" in p) and analysis.get("has_lambda_handler"):
        return "lambda"
    return "ec2"

def build_plan(analysis, nl_prompt, extra: dict | None = None):
    platform = choose_platform(analysis, nl_prompt)
    port = analysis.get("port", 5000)
    start_cmd = {
        "django": f"gunicorn app.wsgi:application --bind 0.0.0.0:{port}",
        "flask":  f"gunicorn app:app -b 0.0.0.0:{port}",
        "fastapi":f"uvicorn app:app --host 0.0.0.0 --port {port}",
        "node":   f"node server.js"
    }.get(analysis.get("app_type"), f"python app.py --port {port}")
    plan = {
        "platform": platform,
        "port": port,
        "env": analysis.get("env", []),
        "start_cmd": start_cmd,
        "health_path": "/"
    }
    if extra: plan.update(extra)
    return plan
