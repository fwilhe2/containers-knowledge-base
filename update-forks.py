# Update forked repos in the fwilhe-containers org
# I fork those repos for two reasons:
#  1.: It allows me to control when they are synced with upstream (which might break things in the playbook)
#  2.: It allows me to change things for testing and experimentation purposes

from urllib.parse import urlparse
import subprocess

repos = []

# Only GitHub repos can be synced with `gh`. passt is not on GitHub, so it is
# cloned straight from upstream and simply skipped here.
with open('git-repos.txt') as git_urls:
    urls = [urlparse(u.strip()) for u in git_urls if u.strip()]
    repos = [u.path[1:] for u in urls if u.netloc == 'github.com']

[subprocess.run(['gh', 'repo', 'sync', r]) for r in repos]