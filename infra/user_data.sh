#!/bin/bash
# Log everything for troubleshooting
exec > /var/log/user-data.log 2>&1
set -euxo pipefail

yum update -y
yum install -y python3 python3-pip git

mkdir -p /opt/app && cd /opt/app
git clone https://github.com/Arvo-AI/hello_world.git /opt/app-src
cp -r /opt/app-src/app/* /opt/app/

pip3 install --upgrade pip setuptools wheel
if [ -f requirements.txt ]; then
  pip3 install -r requirements.txt || true
fi
pip3 install flask gunicorn

PUB_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 || echo "127.0.0.1")
grep -rl "localhost" /opt/app | xargs -r sed -i "s#http://localhost:5000#http://${PUB_IP}#g"

cat >/etc/systemd/system/app.service <<'UNIT'
[Unit]
Description=Autodeploy App
After=network.target

[Service]
WorkingDirectory=/opt/app
ExecStart=/usr/local/bin/gunicorn app:app -b 0.0.0.0:80 --workers 2 --timeout 60
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable --now app.service
