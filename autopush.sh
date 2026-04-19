#!/bin/bash
# Autopush script: adds all changes, commits with timestamp, pushes to origin main

set -e

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

git add .

git commit -m "chore: auto-commit at ${TIMESTAMP}"

git push origin main

echo "Pushed at ${TIMESTAMP}"
