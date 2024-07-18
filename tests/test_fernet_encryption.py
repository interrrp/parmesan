from parmesan.encryption import FernetEncryptor


def test_fernet_encryption_decryption() -> None:
    encryptor = FernetEncryptor()

    encrypted = encryptor.encrypt("secret", "master")
    decrypted = encryptor.decrypt(encrypted, "master")

    assert decrypted == "secret"
