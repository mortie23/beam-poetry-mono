#!/bin/bash
#
# Creates a flex template for a the hellofruit test Beam pipeline
# Usage
#    ./dataflow-build.sh --env dev

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
# Set the active project for environment
echo ${project_id}
gcloud config set project ${project_id}

# Copy the lib for shared modules
#? NOTE: Docker cannot copy from parent paths
cp -au "../../lib/beammeup/beammeup/" "../../pipelines/demo-docker/"

# Build a Docker image
docker build -t ${artifact_registry}/${project_id}/${artifact_repo_docker}/dataflow/hellofruit:0.1 ../../pipelines/demo-docker/
# Authenticate with the registry
gcloud auth configure-docker ${artifact_registry}
# Push to registry
docker push ${artifact_registry}/${project_id}/${artifact_repo_docker}/dataflow/hellofruit:0.1

# Create Flex Template from already build and pushed container image
gcloud dataflow flex-template build gs://${storage_bucket}/dataflow/flex-template/hellofruit.json \
    --image "${artifact_registry}/${project_id}/${artifact_repo_docker}/dataflow/hellofruit:0.1" \
    --sdk-language "PYTHON" \
    --metadata-file "metadata.json" \
    --staging-location "gs://${storage_bucket}/dataflow/staging" \
    --temp-location "gs://${storage_bucket}/dataflow/temp"

# Clean up temp lib for beammeup used to build container
rm -rf ../../pipelines/demo-docker/beammeup
