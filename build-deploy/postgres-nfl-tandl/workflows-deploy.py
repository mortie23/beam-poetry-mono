# Generate Workflows for Postgres tables
# Usage:
#   python3 workflows-deploy.py --env <dev/ppd/prd> --object_list_file objects.csv --run_flag

import os
import subprocess
import re
from dotenv import load_dotenv
import pandas as pd
import click
from rich.console import Console
from hydra import compose, initialize
from beammeup.kms import encode_dataflow_parameter

initialize(config_path="./")
cfg = compose(config_name="config")
console = Console()


def template_gloud_run_script(
    postgres_schema_name: str,
    table_name: str,
    encoded_connectionURL: str,
    encoded_username: str,
    encoded_password: str,
) -> str:
    """Generate a bash script to run a glcoud cli statement with encoded credentials

    Args:
        rdbms_database_name (str): The name of the source rdbms database
        table_name (str): The name of the table on both source and target
    """

    bigquery_dataset_name = "nfl"
    output_table = f"{cfg.project_id}:{bigquery_dataset_name}.{table_name}"

    # Job name must consist of only the characters [-a-z0-9] starting with a letter and ending with a letter or number
    pattern = r"[^a-zA-Z-]"
    job_name = f"{bigquery_dataset_name}-{table_name}"
    job_name = re.sub(pattern, "", job_name).lower()
    print(f"Template for job_name: {job_name}")

    with open("wkf-postgres-nfl-tandl-template.yaml", "r") as file:
        template = file.read()
    with open("header-text.txt", "r") as file:
        header_text = file.read()

    template = template.replace("<<username>>", encoded_username)
    template = template.replace("<<password>>", encoded_password)
    template = template.replace("<<connectionURL>>", encoded_connectionURL)
    template = template.replace("<<postgres_schema_name>>", postgres_schema_name)
    template = template.replace("<<bigquery_dataset_name>>", bigquery_dataset_name)
    template = template.replace("<<table_name>>", table_name)
    template = template.replace("<<output_table>>", output_table)
    template = template.replace("<<job_name>>", job_name)
    template = template.replace("<<header_text>>", header_text)

    # Replace any configuration variables
    for k, v in cfg.items():
        template = template.replace(f"<<{k}>>", v)

    # Write the file out again
    workflow_file = f"wkf-postgres-nfl-tandl-{postgres_schema_name}.{table_name}.yaml"
    with open(workflow_file, "w") as file:
        file.write(template)
    return workflow_file


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("--env", "-e", type=str, help="The environment dev/ppd/prd")
@click.option(
    "--object_list_file",
    "-o",
    type=str,
    default="objects-test.csv",
    help="File with list of objects",
    show_default=True,
)
@click.option(
    "--run_flag",
    "-r",
    is_flag=True,
    help="To also run after generate",
    default=False,
    show_default=True,
)
def all_objects(
    env: str,
    object_list_file: str,
    run_flag: bool = False,
) -> None:
    """Generate a run script for each Postgres table
    then execute each script if the run_flag is set to True

    Args:
        object_list_file (str): A file containing a list of Postgres tables
        run_flag (bool, optional): A flag to set if to run the templates after generating. Defaults to False
    """

    load_dotenv()

    username = os.getenv("username")
    password = os.getenv("password")
    connectionURL = os.getenv("connectionURL")

    # Replacing environment within configuration
    for k, v in cfg.items():
        cfg[k] = v.replace("<env>", env)

    with console.status("[bold green]Encrypting credentials...") as status:
        console.log("Username")
        encoded_username = encode_dataflow_parameter(
            project_id=cfg.project_id,
            location_id=cfg.location,
            key_ring_id=cfg.key_ring_id,
            key_id=cfg.key_id,
            parameter=username,
        )
        console.log("Password")
        encoded_password = encode_dataflow_parameter(
            project_id=cfg.project_id,
            location_id=cfg.location,
            key_ring_id=cfg.key_ring_id,
            key_id=cfg.key_id,
            parameter=password,
        )
        console.log("Connection URL")
        encoded_connectionURL = encode_dataflow_parameter(
            project_id=cfg.project_id,
            location_id=cfg.location,
            key_ring_id=cfg.key_ring_id,
            key_id=cfg.key_id,
            parameter=connectionURL,
        )
    object_list = pd.read_csv(object_list_file, keep_default_na=False)

    with console.status("[bold green]DataFlow jobs...") as status:
        for index, row in object_list.iterrows():
            postgres_schema_name = row["postgres_schema_name"]
            table_name = row["table_name"]

            console.print(f"Generating :memo: [bold cyan] {table_name} [/bold cyan]")
            workflow_file = template_gloud_run_script(
                postgres_schema_name=postgres_schema_name,
                table_name=table_name,
                encoded_connectionURL=encoded_connectionURL,
                encoded_username=encoded_username,
                encoded_password=encoded_password,
            )
            if run_flag:
                console.log(
                    f"Running :rocket: [bold magenta] {table_name} [/bold magenta]"
                )
                subprocess.run(
                    [
                        "bash",
                        "workflows-deploy.sh",
                        "--env",
                        f"{env}",
                        "--postgres_schema_name",
                        f"{postgres_schema_name}",
                        "--table_name",
                        f"{table_name}",
                    ]
                )


all_objects()
