import base64
from beammeup.kms import (
    encrypt_symmetric,
    decrypt_symmetric,
    encode_dataflow_parameter,
)

"""
Usage: 
    # Run all unit tests
    pytest
    # Run a single unit test
    pytest ./tests/test_fruit.py::test_get_fruit
"""


def test_encrypt_symmetric():
    """Test that a string can be encrypted with a KMS key"""
    encrypted = encrypt_symmetric(
        project_id="prj-xyz-dev-fruit",
        location_id="australia-southeast1",
        key_ring_id="keyring-fruit",
        key_id="key-fruit",
        plaintext="someTestText",
    )
    assert type(base64.b64encode(encrypted.ciphertext)) == bytes


# %%
def test_decrypt_symmetric():
    """Test that a encrypted string can be decrypted with a KMS key"""
    project_id = "prj-xyz-dev-fruit"
    location_id = "australia-southeast1"
    key_ring_id = "keyring-fruit"
    key_id = "key-fruit"
    encrypted = encrypt_symmetric(
        project_id=project_id,
        location_id=location_id,
        key_ring_id=key_ring_id,
        key_id=key_id,
        plaintext="someTestText",
    )
    decrypted = decrypt_symmetric(
        project_id=project_id,
        location_id=location_id,
        key_ring_id=key_ring_id,
        key_id=key_id,
        ciphertext=encrypted.ciphertext,
    )

    assert decrypted.plaintext == b"someTestText"


def test_encode_dataflow_parameter():
    project_id = "prj-xyz-dev-fruit"
    location_id = "australia-southeast1"
    key_ring_id = "keyring-fruit"
    key_id = "key-fruit"
    encoded_parameter = encode_dataflow_parameter(
        project_id=project_id,
        location_id=location_id,
        key_ring_id=key_ring_id,
        key_id=key_id,
        parameter="somethingWeNeedEncodedForDataFlow",
    )
    assert type(encoded_parameter) == str
