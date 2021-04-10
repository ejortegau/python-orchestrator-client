#!/bin/bash

function err_die {
    echo $1 1>&2
    exit 1
}


test -z "$1" && err_die "Usage: $0 <path/to/your/gopath/src/github.com/github/orchestrator/go/http/api.go>"

test -f "$1" || err_die "$1 not found"

ENDPOINTS=$(grep 'this.registerAPIRequest(' "$1" | awk '{print $2}' | sed 's/[,"]//g')
echo "SUPPORTED_ENDPOINTS=\"\"\"$ENDPOINTS\"\"\""

