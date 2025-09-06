
import subprocess, json
from pathlib import Path

def run(cmd, cwd=None):
    p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out = []
    for line in p.stdout:
        print(line, end="")
        out.append(line)
    code = p.wait()
    if code != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return "".join(out)

def terraform_apply(tf_dir: Path):
    run(["terraform", "init"], cwd=tf_dir)
    run(["terraform", "apply", "-auto-approve"], cwd=tf_dir)
    out = run(["terraform", "output", "-json"], cwd=tf_dir)
    try: return json.loads(out)
    except: return {"raw_output": out}
