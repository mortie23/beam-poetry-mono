#!/bin/bash
#
# Deploys workflows for DataFlow jobs based on custom built flex templates
# 
# Arguments:
#   env: a GCP project environment
#
# Usage
#    ./workflow-deploy.sh --env <dev/ppd/prd>
# Example
#   ./workflow-deploy.sh --env dev

source ../helpers/argon.sh
# Parse arguments
parse_args "$@"

# Ensure the argument existed when the script was called
if [[ -z ${env} ]]; then
    error_code=1
    echo "ERROR" "environment was not provided"
    exit ${error_code}
fi

# Configuration for environment
eval $(parse_config config.yaml $env)
# Set the active project foir environment
echo ${project_id}
gcloud config set project ${project_id}

# Create a temporary environment specific config file
config_env_file ${env}

# Deploy a workflow 
gcloud workflows deploy wkf-hellofruit \
    --source "workflows-hellofruit.yml" \
    --service-account "${service_account}@${project_id}.iam.gserviceaccount.com" \
    --location "${location}" \
    --call-log-level "log-all-calls" \
    --env-vars-file "config-${env}.yaml"

# Remove the tempory config file
rm config-${env}.yaml
