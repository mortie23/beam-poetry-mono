# Deploy all workflows

Setup Python environment

```sh
poetry lock && poetry install --no-root
```

Run

```sh
python3 workflows-deploy.py --env <dev/ppd/prd> --object_list_file objects.csv --run_flag
```

