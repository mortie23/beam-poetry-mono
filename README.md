# Beam

Using Apache Beam on DataFlow with poetry and internal helper library functions.

## Reason

There was the need to:

- Write many Apache Beam pipelines and deploy them as custom Flex templates
- Reuse the many Flex templates (as well as the pre built ones from Google) and deploy many Workflows
- Run many DataFlow jobs

This made it necessary to write a few custom helper functions for things like reading secrets and using the Key Management Service (KMS).
So I needed a useful directory structure and method such that the custom helper functions can be tested and reused not only in local scripts but also deploying them to the Docker containers.

Following this repository should help give you an idea of how I have done this can be done.

## Requirements

- Cloud hosted Postgres instance for testing (mine was installed on a f1-micro GCE VM for this basic test) 
- Chromebook for development
  - All Python packages are managed using Poetry. 
    > This easily let's us have an internal development package and import it across other Python scripts. 
- Setup of other GCP services like DataFlow, Workflows, BigQuery

## Repository structure

```
📁 build-deploy/
│   ├── 📁 helpers/
│   │       📄 argon.sh
│   ├── 📁 <data-movement-01>/
📁 ddl/
│   ├── 📁 bigquery/
│   │       📄 <table_name>.sql
│   ├── 📁 <source-system>/
📁 eda/
│   ├── 📁 <exploratory-data-analysis-01>/
│   │       📄 <script>.py
📁 lib/
│   ├── 📁 beammeup/
│   │       ├── 📁 beammeup/
│   │       │       📄 __init__.py
│   │       │       📄 module.py
│   │       ├── 📁 tests/
│   │       │       📄 test_module.py
📁 pipelines/
│   ├── 📁 <data-movement-01>/
📄 requirements.txt
```

## Beam Me Up

Beam Me Up was the name given to the helper function Python package. 

## Custom Flex Template (Beam with Docker)

A few things to note for this specific example are the way we can simply import from Beam Me Up.

```py
import beammeup.fruit as fr
setup_file_path = Path(__file__).parent / "setup.py"
```

This is through 

### The use of `setup.py` 

```py
import setuptools

setuptools.setup(
    name="beammeup",
    version="0.0.1",
    install_requires=[],
    packages=setuptools.find_packages(),
)
```

### The PipelineOptions with `setup_file` set correctly

```py
options = PipelineOptions(
    beam_args,
    save_main_session=True,
    setup_file=str(setup_file_path),
)
```

### A temporary copy in the build step

```sh
# Copy the lib for shared modules
#? NOTE: Docker cannot copy from parent paths
cp -au "../../lib/beammeup/beammeup/" "../../pipelines/demo-docker/"
```

## Argon

Argon was created as a shared shell script library of helper functions for argument parsing and configuration management.