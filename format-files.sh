#!/bin/bash
set -o nounset
set -o errexit
set -o xtrace

# *.yaml as well as *.yml: playbook.yaml and container-lab.yaml were never
# covered by the old glob, so they went unformatted.
npx prettier --write README.md CLAUDE.md "./**/*.yml" "./**/*.yaml"
