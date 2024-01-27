FROM gcr.io/dataflow-templates-base/python39-template-launcher-base

# env var in order to use custom lib, for more info, see:
# https://cloud.google.com/dataflow/docs/guides/templates/configuring-flex-templates#set_required_dockerfile_environment_variables
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="/template/hellofruit.py"
ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="/template/requirements.txt"

RUN mkdir -p /template/beammeup

COPY hellofruit.py /template
COPY setup.py /template
COPY requirements.txt /template
COPY beammeup /template/beammeup/

RUN apt-get update \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r $FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE \
    # Download the requirements to speed up launching the Dataflow job.
    && pip download --no-cache-dir --dest /tmp/dataflow-requirements-cache -r $FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE

# Since we already downloaded all the dependencies, there's no need to rebuild everything.
ENV PIP_NO_DEPS=True

ENTRYPOINT ["/opt/google/dataflow/python_template_launcher"]