import ssl

import pytest

from app.database import config


@pytest.mark.parametrize(
    "url, local",
    [
        ("sqlite://", True),
        ("mysql+pymysql://root@localhost/db", True),
        ("mysql+pymysql://root@127.0.0.1/db", True),
        ("mysql+pymysql://user@gateway.example.test:4000/db", False),
    ],
)
def test_remote_database_does_not_enable_automatic_schema_creation(url, local):
    assert config.is_local_database(url) is local


def test_ca_path_enforces_certificate_and_hostname_verification(tmp_path, monkeypatch):
    certificate = tmp_path / "certs" / "root.pem"
    certificate.parent.mkdir()
    certificate.write_text("certificado de teste", encoding="utf-8")
    captured = {}
    monkeypatch.setattr(config, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(
        config.ssl, "create_default_context", lambda **kwargs: captured.update(validation=kwargs)
    )

    def capture_engine(url, **kwargs):
        captured.update(url=url, options=kwargs)
        return captured

    monkeypatch.setattr(config, "create_engine", capture_engine)
    config.database_engine(
        "mysql+pymysql://user@remote.test/db?ssl_verify_cert=false&ssl_verify_identity=false",
        "certs/root.pem",
    )
    options = captured["options"]
    assert options["connect_args"]["ssl_ca"] == str(certificate)
    assert options["connect_args"]["ssl_verify_cert"] is True
    assert options["connect_args"]["ssl_verify_identity"] is True
    assert captured["validation"] == {"cafile": str(certificate)}
    assert not captured["url"].query
    assert options["pool_pre_ping"] is True


def test_missing_or_invalid_certificate_is_not_silently_ignored(tmp_path):
    with pytest.raises(FileNotFoundError):
        config.database_engine("mysql+pymysql://user@remote.test/db", str(tmp_path / "missing.pem"))
    invalid = tmp_path / "invalid.pem"
    invalid.write_text("isto não é um certificado", encoding="utf-8")
    with pytest.raises(ssl.SSLError):
        config.database_engine("mysql+pymysql://user@remote.test/db", str(invalid))


def test_sqlite_does_not_receive_mysql_tls_options():
    engine = config.database_engine("sqlite://", "not-needed.pem")
    try:
        with engine.connect() as connection:
            assert connection.exec_driver_sql("SELECT 1").scalar() == 1
    finally:
        engine.dispose()


def test_query_tls_booleans_are_normalized(monkeypatch):
    captured = {}
    monkeypatch.setattr(config, "create_engine", lambda url, **kwargs: captured.update(kwargs))
    config.database_engine(
        "mysql+pymysql://user@remote.test/db?ssl_verify_cert=true&ssl_verify_identity=true"
    )
    assert captured["connect_args"]["ssl_verify_cert"] is True
    assert captured["connect_args"]["ssl_verify_identity"] is True
    with pytest.raises(ValueError):
        config.database_engine("mysql+pymysql://user@remote.test/db?ssl_verify_cert=invalid")
