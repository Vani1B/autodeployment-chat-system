
# Autodeployment Chat System (EC2 + ECS + Lambda)

A backend + CLI that takes a natural language prompt and a repository link/zip, analyzes the app,
selects a deployment target (EC2/ECS/Lambda), renders Terraform, provisions AWS, and deploys with minimal intervention.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Plan (no infra created)
python -m cli --plan --prompt "Deploy this Flask app on AWS" --repo https://github.com/Arvo-AI/hello_world

# Deploy (auto-select)
python -m cli --deploy --prompt "Deploy this Flask app on AWS" --repo https://github.com/Arvo-AI/hello_world
```
**Defaults:** EC2 if no Dockerfile and no serverless hint. ECS if Dockerfile. Lambda if prompt requests serverless **and** a `lambda_handler.py` is present.

## Prereqs
- AWS creds & Terraform installed locally; default VPC present.
- Docker installed (only needed for ECS builds).
- Python 3.10+

## Structure
```
app/
  main.py                # FastAPI API
  repo_analyzer.py
  planner.py
  tfgen/
    render.py
    templates/
      ec2/...
      ecs/...
      lambda/...
  deploy/provisioner.py
cli/__main__.py
scripts/build_push_ecr.sh
requirements.txt
.gitignore
LICENSE
```
