#!/bin/bash
#
# Creates a flex template for a the hellofruit test Beam pipeline
# Usage
#    ./helper-test.sh --env dev

source argon.sh
# Parse arguments
parse_args "$@"

# Ensure the argument existed when the script was called
if [[ -z ${env} ]]; then
    error_code=1
    echo "ERROR" "environment was not provided"
    exit ${error_code}
fi

# Configuration for environment
eval $(parse_config config-test.yaml $env)
echo ${env_resolve}

config_env_file ${env}
