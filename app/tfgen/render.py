
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def render_ec2(out_dir: Path, repo_dir: Path, plan: dict, region: str = "ca-central-1"):
    out_dir.mkdir(parents=True, exist_ok=True)
    tpl_root = Path(__file__).parent / "templates" / "ec2"
    env = Environment(loader=FileSystemLoader(str(tpl_root)))
    for name in ["main.tf.j2", "variables.tf.j2", "outputs.tf.j2", "user_data.sh.j2"]:
        tpl = env.get_template(name)
        rendered = tpl.render(start_cmd=plan["start_cmd"], region=region)
        (out_dir / name.replace(".j2","")).write_text(rendered, encoding="utf-8")

def render_ecs(out_dir: Path, repo_dir: Path, plan: dict, region: str = "ca-central-1"):
    out_dir.mkdir(parents=True, exist_ok=True)
    tpl_root = Path(__file__).parent / "templates" / "ecs"
    env = Environment(loader=FileSystemLoader(str(tpl_root)))
    for name in ["main.tf.j2", "variables.tf.j2", "outputs.tf.j2"]:
        tpl = env.get_template(name)
        rendered = tpl.render(region=region, service_name="autodeploy-svc", container_port=plan["port"])
        (out_dir / name.replace(".j2","")).write_text(rendered, encoding="utf-8")

def render_lambda(out_dir: Path, repo_dir: Path, plan: dict, region: str = "ca-central-1"):
    out_dir.mkdir(parents=True, exist_ok=True)
    tpl_root = Path(__file__).parent / "templates" / "lambda"
    env = Environment(loader=FileSystemLoader(str(tpl_root)))
    for name in ["main.tf.j2", "variables.tf.j2", "outputs.tf.j2"]:
        tpl = env.get_template(name)
        rendered = tpl.render(region=region, handler="handler.lambda_handler")
        (out_dir / name.replace(".j2","")).write_text(rendered, encoding="utf-8")
