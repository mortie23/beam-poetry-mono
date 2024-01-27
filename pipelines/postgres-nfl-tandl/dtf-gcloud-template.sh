# <<header_text>>

gcloud dataflow flex-template run dtf-postgres-nfl-tandl-<<job_name>> \
    --template-file-gcs-location gs://dataflow-templates-australia-southeast1/latest/flex/PostgreSQL_to_BigQuery \
    --region <<location>> \
    --temp-location gs://<<storage_bucket>>/dataflow/temp/ \
    --parameters connectionURL="<<connectionURL>>" \
    --parameters username="<<username>>" \
    --parameters password="<<password>>" \
    --parameters KMSEncryptionKey=projects/<<project_id>>/locations/<<location>>/keyRings/keyring-fruit/cryptoKeys/key-fruit \
    --parameters query="select * from <<postgres_schema_name>>.<<table_name>>" \
    --parameters isTruncate=true \
    --parameters fetchSize=50000 \
    --parameters outputTable="<<project_id>>:<<bigquery_dataset_name>>.<<table_name>>" \
    --parameters bigQueryLoadingTemporaryDirectory=gs://<<storage_bucket>>/dataflow/temp/ \
    --parameters stagingLocation=gs://<<storage_bucket>>/dataflow/staging/ \
    --parameters saveHeapDumpsToGcsPath=gs://<<storage_bucket>>/dataflow/logs/ \
    --parameters zone=<<zone>> \
    --parameters serviceAccount=<<service_account>>@<<project_id>>.iam.gserviceaccount.com