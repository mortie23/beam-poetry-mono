#!/bin/bash
#
# Runs a custom flex template for a the hellofruit Beam pipeline
# Usage
#    ./dataflow-run.sh --env dev

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

run_timestamp=$(date '+%Y%m%d%H%M%S')

gcloud dataflow flex-template run hellofruit-${run_timestamp} \
    --template-file-gcs-location gs://${storage_bucket}/dataflow/flex-template/hellofruit.json \
    --region ${location} \
    --parameters output_table="fruit.hellofruit" \
    --parameters staging_location=gs://${storage_bucket}/dataflow/staging \
    --parameters temp_location=gs://${storage_bucket}/dataflow/temp \
    --parameters service_account_email=${service_account}@${project_id}.iam.gserviceaccount.com \
