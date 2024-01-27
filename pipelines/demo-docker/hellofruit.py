"""Testing a basic write to BigQuery
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import beammeup.fruit as fr

setup_file_path = Path(__file__).parent / "setup.py"


def run(
    output_table: str,
    beam_args: list[str] = None,
) -> None:
    """Build and run the pipeline."""
    options = PipelineOptions(
        beam_args,
        save_main_session=True,
        setup_file=str(setup_file_path),
    )

    with beam.Pipeline(options=options) as pipeline:
        pCollection = pipeline | "Create fruit data" >> beam.Create(
            [
                {"name": fr.get_fruit(), "test_number": 1},
            ]
        )
        # Output the results into BigQuery table.
        _ = pCollection | "Write to Big Query" >> beam.io.WriteToBigQuery(output_table)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_table",
        help="Output BigQuery table for results specified as: "
        "PROJECT:DATASET.TABLE or DATASET.TABLE.",
    )
    args, beam_args = parser.parse_known_args()

    run(
        output_table=args.output_table,
        beam_args=beam_args,
    )
