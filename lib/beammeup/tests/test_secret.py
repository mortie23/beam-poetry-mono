from beammeup.secret import access_secret_version

"""
Usage: 
    # Run all unit tests
    pytest
    # Run a single unit test
    pytest ./tests/test_secret.py::test_access_secret_version
"""


def test_access_secret_version():
    """Test that a secret can be accessed
    Note:
        need a unit test secret and version
    """
    project_id = "prj-xyz-dev-fruit"
    secret_id = "scr-unit-test"
    secret_value = access_secret_version(
        project_id=project_id,
        secret_id=secret_id,
    )
    assert type(secret_value) == str
    assert secret_value == "unit-test-secret"
