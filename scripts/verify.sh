#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PARENT=${DIR}/..
cd "$PARENT"

mypy ./pyorchestratorclient
black -l 80 --check ./pyorchestratorclient
pylint ./pyorchestratorclient

cd "$DIR"

