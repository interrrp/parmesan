from parmesan.encryption import FernetEncryptor
from parmesan.repository import EncryptedPasswordRepository, InMemoryPasswordRepository


def test_encryption() -> None:
    master_password = "master_password"  # noqa: S105
    secret_password = "secret_password"  # noqa: S105

    encryptor = FernetEncryptor()
    base_repository = InMemoryPasswordRepository()
    encrypted_repository = EncryptedPasswordRepository(base_repository, encryptor, master_password)

    encrypted_repository["secret_site"] = secret_password

    assert base_repository["secret_site"] != secret_password
    assert encrypted_repository["secret_site"] == secret_password
