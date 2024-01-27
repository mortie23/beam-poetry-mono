"""Basic read from postgres using a local runner

Setup:
    Install dependencies with poetry
        poetry lock && poetry install --no-root

Usage:
    python3 jdbc.py

Returns:
    Printing to std out
    BeamSchema_6b9e7646_0916_437b_9421_24e0e4f5f964(game_type_id=1, game_type='REG', created_date=Timestamp(1539587059), create_user='mortimer')
    BeamSchema_6b9e7646_0916_437b_9421_24e0e4f5f964(game_type_id=2, game_type='PST', created_date=Timestamp(1539587059), create_user='mortimer')
"""

import apache_beam as beam
from apache_beam.io.jdbc import ReadFromJdbc
from beammeup.secret import access_secret_version
from apache_beam.typehints.schemas import MillisInstant
from apache_beam.typehints.schemas import LogicalType

LogicalType.register_logical_type(MillisInstant)

# If environment has this and want to test a local runner need to unset
# unset GOOGLE_APPLICATION_CREDENTIALS
secret_project_id = "prj-xyz-dev-fruit"

# %%
with beam.Pipeline() as p:
    postgres_username = access_secret_version(
        project_id=secret_project_id,
        secret_id="scr-xyz-fruit-postgres-username",
    )
    postgres_password = access_secret_version(
        project_id=secret_project_id,
        secret_id="scr-xyz-fruit-postgres-password",
    )
    postgres_hostname = access_secret_version(
        project_id=secret_project_id,
        secret_id="scr-xyz-fruit-postgres-hostname",
    )

    result = (
        p
        | "Read from jdbc"
        >> ReadFromJdbc(
            table_name="mortimer_nfl.game_type",
            driver_class_name="org.postgresql.Driver",
            jdbc_url=f"jdbc:postgresql://{postgres_hostname}:5432/mortimer_dev",
            username=postgres_username,
            password=postgres_password,
        )
        | "Print the results" >> beam.Map(print)
    )
