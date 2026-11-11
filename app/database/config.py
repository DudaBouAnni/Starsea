"""Configuração de conexão local ou remota, com validação TLS quando houver certificado."""

import ssl
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOCAL_HOSTS = {None, "localhost", "127.0.0.1", "::1"}


def is_local_database(database_url: str) -> bool:
    url = make_url(database_url)
    return url.get_backend_name() == "sqlite" or url.host in LOCAL_HOSTS


def database_engine(database_url: str, ca_path: str | None = None):
    url = make_url(database_url)
    connect_args = {}
    if url.drivername == "mysql+pymysql":
        connect_args.update(connect_timeout=10, read_timeout=20, write_timeout=20)
        for name in ("ssl_verify_cert", "ssl_verify_identity"):
            if name in url.query:
                value = str(url.query[name]).lower()
                if value not in {"true", "false", "1", "0"}:
                    raise ValueError(f"Valor inválido para {name} na configuração do banco.")
                connect_args[name] = value in {"true", "1"}
        url = url.difference_update_query(("ssl_verify_cert", "ssl_verify_identity"))
        if ca_path:
            certificate = Path(ca_path).expanduser()
            if not certificate.is_absolute():
                certificate = PROJECT_ROOT / certificate
            if not certificate.is_file():
                raise FileNotFoundError("O certificado definido em CA_PATH não foi encontrado.")
            # Valida o formato do certificado antes de tentar a conexão.
            ssl.create_default_context(cafile=str(certificate))
            connect_args.update(
                ssl_ca=str(certificate), ssl_verify_cert=True, ssl_verify_identity=True
            )
    return create_engine(url, connect_args=connect_args, pool_pre_ping=True)
