
import argparse, uuid
from pathlib import Path
from app.repo_analyzer import analyze
from app.planner import build_plan
from app.tfgen.render import render_ec2, render_ecs, render_lambda
from app.deploy.provisioner import terraform_apply

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--branch", default="main")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--deploy", action="store_true")
    ap.add_argument("--region", default="ca-central-1")
    args = ap.parse_args()

    workdir = Path(".autodeploy") / str(uuid.uuid4())
    repo_dir = workdir / "repo"
    tf_dir   = workdir / "tf"
    workdir.mkdir(parents=True, exist_ok=True)

    from git import Repo
    Repo.clone_from(args.repo, repo_dir, branch=args.branch, depth=1)

    analysis = analyze(repo_dir)
    plan = build_plan(analysis, args.prompt)
    print("ANALYSIS:", analysis)
    print("PLAN:", plan)

    if args.plan and not args.deploy:
        print("Plan only. Exiting.")
        return

    renderer = {"ec2": render_ec2, "ecs": render_ecs, "lambda": render_lambda}[plan["platform"]]
    renderer(tf_dir, repo_dir, plan, region=args.region)
    outputs = terraform_apply(tf_dir)
    print("OUTPUTS:", outputs)

if __name__ == "__main__":
    main()
