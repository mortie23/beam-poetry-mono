# Data movement from rdbms to BigQuery

## Setup

Ensure you have installed the requirements in the parent `beam` directory first.
Also you much have run:

```
gcloud auth login
gcloud auth application-default login
```

### Environment variables

Create a `.env` file in this directory with the contents for RDBMS

```ini
username=<username>
password=<password>
connectionURL=jdbc:rdbms://<rdbms-host>
```

## Using Google pre built flex template

This is the chosen method for truncate and load.
A `gcloud` cli statement is generated for each rdbms object (table or view) using the Python script `dataflow-generate-run.py`.
It can be run in a Python interactive session stepping through the cells. This only needs to be run once.

Once you have generated all the scripts for each rdbms object, you can run each from the command line to start a DataFlow Job.

```sh
# Example running the CodeDetail table
./dataflow-run-gcloud.<table-name>.sh
```

Example output:

```yml
job:
  createTime: '2024-01-21T23:51:51.635792Z'
  currentStateTime: '1970-01-01T00:00:00Z'
  id: 2024-01-21_15_51_51-1602857575721442141
  location: australia-southeast1
  name: dtf-postgres-nfl-tandl
  projectId: prj-xyz-dev-fruit
  startTime: '2024-01-21T23:51:51.635792Z'
```
