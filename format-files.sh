#!/bin/bash
set -o nounset
set -o errexit
set -o xtrace

npx prettier --write README.md
npx prettier --write "./**/*.yml"
