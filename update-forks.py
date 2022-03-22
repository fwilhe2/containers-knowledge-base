# Update forked repos in the fwilhe-containers org
# I fork those repos for two reasons:
#  1.: It allows me to control when they are synced with upstream (which might break things in the playbook)
#  2.: It allows me to change things for testing and experimentation purposes

from urllib.parse import urlparse
import subprocess

repos = []

with open('git-repos.txt') as git_urls:
    repos = [(urlparse(u).path[1:]) for u in git_urls]

[subprocess.run(['gh', 'repo', 'sync', r]) for r in repos]