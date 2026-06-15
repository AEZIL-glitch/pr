#!/usr/bin/env python3
"""Push workflow files to GitHub using Git Tree API"""
import json, base64, subprocess, os, sys

GH = r"C:\Program Files\GitHub CLI\gh.exe"
REPO = "AEZIL-glitch/pr"
BASE_SHA = "a45948e6a3c7624ab98959b9735a77b22f3bed9a"

def gh_api(method, endpoint, data=None, verbose=False):
    cmd = [GH, "api", endpoint, "--method", method, "--input", "-"]
    env = os.environ.copy()
    payload = json.dumps(data).encode() if data else None
    proc = subprocess.run(cmd, input=payload, capture_output=True, timeout=30, env=env)
    stdout = proc.stdout.decode()
    stderr = proc.stderr.decode()
    if proc.returncode != 0:
        print(f"ERROR ({endpoint}): exit={proc.returncode}", file=sys.stderr)
        print(f"  stdout: {stdout[:300]}", file=sys.stderr)
        print(f"  stderr: {stderr[:300]}", file=sys.stderr)
        return None
    if verbose:
        print(f"OK ({endpoint[:60]}): {stdout[:200]}")
    return json.loads(stdout)

# 1. Get the current tree sha from the commit
commit = gh_api("GET", f"repos/{REPO}/git/commits/{BASE_SHA}", verbose=True)
if not commit:
    print("Failed to get commit")
    sys.exit(1)

tree_sha = commit["tree"]["sha"]
print(f"Base tree SHA: {tree_sha}")

# 2. Get the current tree
tree_result = gh_api("GET", f"repos/{REPO}/git/trees/{tree_sha}?recursive=1", verbose=True)
if not tree_result:
    print("Failed to get tree")
    sys.exit(1)

print(f"Current tree has {len(tree_result['tree'])} items")
for item in tree_result["tree"]:
    print(f"  {item['mode']} {item['type']} {item['sha'][:12]} {item['path']}")

# 3. Keep existing items (remove test.txt and .gitkeep)
tree_items = []
for item in tree_result["tree"]:
    if item["path"] in ("test.txt", ".github/.gitkeep"):
        continue
    tree_items.append({
        "path": item["path"],
        "mode": item["mode"],
        "type": item["type"],
        "sha": item["sha"]
    })

# 4. Create blobs for workflow files
workdir = r"C:\Users\27554\pr"
for path in [".github/workflows/pr-review.yml", ".github/workflows/daily-briefing.yml"]:
    with open(os.path.join(workdir, path), "rb") as f:
        content = f.read()
    result = gh_api("POST", f"repos/{REPO}/git/blobs", {
        "content": base64.b64encode(content).decode(),
        "encoding": "base64"
    })
    if not result:
        print(f"Failed to create blob for {path}")
        sys.exit(1)
    tree_items.append({
        "path": path,
        "mode": "100644",
        "type": "blob",
        "sha": result["sha"]
    })
    print(f"Blob {path}: {result['sha']}")

print(f"Tree will have {len(tree_items)} items")

# 5. Create new tree
payload = {
    "base_tree": tree_sha,
    "tree": tree_items
}
print(f"Creating tree with base={tree_sha}...")
result = gh_api("POST", f"repos/{REPO}/git/trees", payload, verbose=True)
if not result:
    print("Failed to create tree")
    sys.exit(1)
new_tree_sha = result["sha"]
print(f"Tree created: {new_tree_sha}")

# 6. Create commit
result = gh_api("POST", f"repos/{REPO}/git/commits", {
    "message": "Add CI workflows (PR review + daily briefing)",
    "tree": new_tree_sha,
    "parents": [BASE_SHA]
})
if not result:
    print("Failed to create commit")
    sys.exit(1)
commit_sha = result["sha"]
print(f"Commit: {commit_sha}")

# 7. Update ref
result = gh_api("PATCH", f"repos/{REPO}/git/refs/heads/main", {
    "sha": commit_sha,
    "force": True
})
if result:
    print("Success! Workflows pushed to GitHub.")
    print(f"https://github.com/{REPO}/actions")
