📖 Project Overview

This project demonstrates a fully automated pipeline that takes a natural language prompt and a GitHub repository and transforms it into a running web application on AWS.
Using Python, Terraform, and AWS EC2, the system analyzes the app, provisions cloud resources, configures dependencies, and serves the application with zero manual intervention.

For this submission, the EC2 path was implemented successfully: the Flask demo app from Arvo-AI/hello_world
 is provisioned, started via gunicorn, and accessible directly over HTTP.

🔄 High-Level Architecture
```
   ┌─────────────────────┐
   │   User Prompt/CLI   │
   │ "Deploy this app…"  │
   └─────────┬───────────┘
             │
             ▼
   ┌─────────────────────┐
   │   Repo Analyzer     │
   │  (detect Flask app) │
   └─────────┬───────────┘
             │
             ▼
   ┌─────────────────────┐
   │ Terraform Generator │
   │  (main.tf, vars,    │
   │   outputs, user_data│
   └─────────┬───────────┘
             │
             ▼
   ┌─────────────────────┐
   │    Terraform Apply  │
   │  (provisions EC2,   │
   │   SG, networking)   │
   └─────────┬───────────┘
             │
             ▼
   ┌─────────────────────┐
   │   EC2 Instance      │
   │  - Flask + Gunicorn │
   │  - Port 80 exposed  │
   └─────────┬───────────┘
             │
             ▼
   ┌─────────────────────┐
   │   Web Browser       │
   │  http://<public_ip> │
   │  ✅ Hello, World!   │
   └─────────────────────┘
```

🌐 Workflow (EC2 Path)

User provides input

python -m cli --deploy \
  --prompt "Deploy this Flask app on AWS" \
  --repo https://github.com/Arvo-AI/hello_world


Analyzer detects app type

Framework: Flask
Default port: 5000
Entrypoint: app:app
Terraform is generated
Security Group → allows HTTP (80)
EC2 Instance → Amazon Linux 2 (t3.micro)
User Data script → installs Python, dependencies, gunicorn, systemd service
iptables redirects port 80 → 5000
Infrastructure is provisioned
Terraform apply runs inside .autodeploy/<id>/tf/

Outputs:

public_ip = "x.x.x.x"
url       = "http://x.x.x.x"


App boots on EC2

Systemd starts gunicorn at boot
Application served on port 80

Validation

Open browser: http://<public_ip>/

✅ App displays “Simple Deploy App – Hello, World!”

▶️ Quick Start
Prerequisites

AWS CLI configured (aws configure)

Terraform installed

Python 3.10+

Run
git clone <your-repo>
cd autodeployment-chat-system

# Setup Python venv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Deploy
python -m cli --deploy \
  --prompt "Deploy this Flask app on AWS" \
  --repo https://github.com/Arvo-AI/hello_world


Terraform will output:

public_ip = "3.96.xxx.xxx"
url       = "http://3.96.xxx.xxx"


Open the URL in your browser 🎉

🛠️ Components

Analyzer (repo_analyzer.py) → detects framework, port, entrypoint
Terraform templates (infra/ or .autodeploy/.../tf/)
main.tf
variables.tf
outputs.tf
terraform.tfvars
User Data script → installs dependencies, configures gunicorn, starts app

🧹 Destroy
cd .autodeploy/<last-run>/tf
terraform destroy -auto-approve

✅ Demo Status

 Natural language → plan
 Terraform → EC2 provisioned
 Flask app bootstrapped & live on HTTP (80)

🔥 Future Enhancements

ECS Fargate for containerized repos
Lambda + API Gateway path for handler-based repos
HTTPS via ALB + ACM cert
CI/CD integration with GitHub Actions
Multi-environment support (dev/stage/prod)