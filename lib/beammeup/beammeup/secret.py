from google.cloud import secretmanager


def access_secret_version(
    project_id: str,
    secret_id: str,
    version_id: str = "latest",
) -> str:
    """Get a secret and return as string

    Args:
        project_id (str): GCP Project ID
        secret_id (str): The name of the secret
        version_id (int, optional): version of secret. Defaults to "latest".

    Returns:
        str: The secret value as a string
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
