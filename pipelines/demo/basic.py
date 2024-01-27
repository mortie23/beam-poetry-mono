"""Basic run of Beam pipeline with no connections

Setup:
    Install dependencies with poetry
        poetry lock && poetry install --no-root

Usage:
    python3 basic.py
    or
    using Run Cell for interactive

Returns:
    Printing to std out
    {'name': 'Currant'}
    {'name': 'Blueberry'}
    {'name': 'Tangerine'}
    {'name': 'Fig'}
    {'name': 'Gooseberry'}
"""

# %%
import apache_beam as beam
import beammeup.fruit as fr

# %%
with beam.Pipeline() as p:
    random_fruits = (
        p
        | "Random fruits"
        >> beam.Create(
            [
                {"name": fr.get_fruit()},
                {"name": fr.get_fruit()},
                {"name": fr.get_fruit()},
                {"name": fr.get_fruit()},
                {"name": fr.get_fruit()},
            ]
        )
        | beam.Map(print)
    )

# %%
