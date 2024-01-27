#!/bin/bash
#
# Deploys workflows for DataFlow jobs based on custom built flex templates
# 
# Arguments:
#   env: a GCP project environment
#
# Usage
#    ./workflows-deploy.sh --env <dev/ppd/prd> --postgres_schema_name <postgres_schema_name> --table_name <table_name>
# Example
#   ./workflows-deploy.sh --env dev --postgres_schema_name <schema_name> --table_name <table_name>

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

# Workflow name must consist of only the characters [-a-z0-9] starting with a letter and ending with a letter or number
workflow_name=$(echo "${postgres_schema_name}-${table_name}" | tr -dc 'a-zA-Z-_' | tr '[:upper:]' '[:lower:]')
echo ${workflow_name}

# Create a temporary environment specific config file
config_env_file ${env}

# Deploy a workflow 
gcloud workflows deploy wkf-postgres-nfl-tandl-${workflow_name} \
    --source "wkf-postgres-nfl-tandl-${postgres_schema_name}.${table_name}.yaml" \
    --service-account "${service_account}@${project_id}.iam.gserviceaccount.com" \
    --location "${location}" \
    --call-log-level "log-all-calls" \
    --env-vars-file "config-${env}.yaml"

# Remove the tempory config file
rm config-${env}.yaml
