
from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from .repo_analyzer import analyze
from .planner import build_plan
from .tfgen.render import render_ec2, render_ecs, render_lambda
from .deploy.provisioner import terraform_apply
import uuid, shutil

app = FastAPI(title="Autodeployment Chat System")

class DeployRequest(BaseModel):
    prompt: str
    repo_url: str
    branch: str | None = "main"
    region: str | None = "ca-central-1"

@app.post("/plan")
def plan(req: DeployRequest):
    workdir = Path(".autodeploy") / str(uuid.uuid4())
    workdir.mkdir(parents=True, exist_ok=True)
    repo_dir = workdir / "repo"
    from git import Repo
    Repo.clone_from(req.repo_url, repo_dir, branch=req.branch, depth=1)
    analysis = analyze(repo_dir)
    plan = build_plan(analysis, req.prompt)
    shutil.rmtree(workdir, ignore_errors=True)
    return {"analysis": analysis, "plan": plan}

@app.post("/deploy")
def deploy(req: DeployRequest):
    workdir = Path(".autodeploy") / str(uuid.uuid4())
    repo_dir = workdir / "repo"
    tf_dir   = workdir / "tf"
    from git import Repo
    Repo.clone_from(req.repo_url, repo_dir, branch=req.branch, depth=1)
    analysis = analyze(repo_dir)
    plan = build_plan(analysis, req.prompt)

    if plan['platform'] == 'ecs':
        render_ecs(tf_dir, repo_dir, plan, region=req.region)
    elif plan['platform'] == 'lambda':
        render_lambda(tf_dir, repo_dir, plan, region=req.region)
    else:
        render_ec2(tf_dir, repo_dir, plan, region=req.region)

    outputs = terraform_apply(tf_dir)
    return {"plan": plan, "outputs": outputs, "workdir": str(workdir)}
