
#!/usr/bin/env bash
set -euo pipefail
while [[ "$#" -gt 0 ]]; do case $1 in
  --repo) REPO_URL="$2"; shift;;
  --branch) BRANCH="$2"; shift;;
  --region) REGION="$2"; shift;;
  --name) NAME="$2"; shift;;
  *) echo "Unknown param: $1"; exit 1;;
esac; shift; done
: "${REPO_URL:?--repo required}"
REGION="${REGION:-ca-central-1}"
NAME="${NAME:-autodeploy-repo}"
TMP=$(mktemp -d)
git clone "${REPO_URL}" "$TMP/repo" ${BRANCH:+--branch "$BRANCH"} --depth 1
cd "$TMP/repo"
aws ecr describe-repositories --repository-names "$NAME" --region "$REGION" >/dev/null 2>&1 ||   aws ecr create-repository --repository-name "$NAME" --region "$REGION" >/dev/null
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"
IMAGE_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$NAME:latest"
docker build -t "$IMAGE_URI" .
docker push "$IMAGE_URI"
echo "$IMAGE_URI"
