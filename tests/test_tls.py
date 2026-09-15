from datetime import datetime, timedelta, timezone
import ssl
from types import SimpleNamespace
from unittest.mock import Mock

import aiohttp
import certifi
import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

from decimal_web3_sdk import DecimalClient, NetworkConfig
from decimal_web3_sdk._tls import create_client_ssl_context
from decimal_web3_sdk.rpc import RpcPool
from decimal_web3_sdk.ws import DecimalWsClient


@pytest.fixture(autouse=True)
def isolated_ca_environment(monkeypatch):
    for name in (
        "SSL_CERT_FILE", "SSL_CERT_DIR", "DECIMAL_TLS_CA_FILE",
        "DECIMAL_TESTNET_TLS_CA_FILE", "DECIMAL_DEVNET_TLS_CA_FILE",
    ):
        monkeypatch.delenv(name, raising=False)


def test_default_context_uses_certifi_not_system_store(monkeypatch):
    original = ssl.create_default_context
    factory = Mock(wraps=original)
    monkeypatch.setattr(ssl, "create_default_context", factory)
    context = create_client_ssl_context()
    factory.assert_called_once_with(cafile=certifi.where(), capath=None)
    assert context.verify_mode == ssl.CERT_REQUIRED
    assert context.check_hostname is True


@pytest.mark.parametrize("value", [False, True, "", " ", 1])
def test_invalid_ca_configuration_cannot_disable_tls(value):
    with pytest.raises(ValueError, match="CA PEM bundle"):
        NetworkConfig(tls_ca_file=value)
    with pytest.raises(ValueError, match="CA PEM bundle"):
        RpcPool(["https://rpc.example.invalid"], ca_file=value)
    with pytest.raises(ValueError, match="CA PEM bundle"):
        create_client_ssl_context(value)


def test_missing_and_invalid_ca_fail_closed(tmp_path, monkeypatch):
    missing = str(tmp_path / "missing.pem")
    with pytest.raises(FileNotFoundError):
        create_client_ssl_context(missing)
    monkeypatch.setenv("SSL_CERT_FILE", missing)
    with pytest.raises(FileNotFoundError):
        create_client_ssl_context()
    monkeypatch.delenv("SSL_CERT_FILE")
    monkeypatch.setenv("SSL_CERT_DIR", str(tmp_path / "missing-dir"))
    with pytest.raises(FileNotFoundError):
        create_client_ssl_context()
    invalid = tmp_path / "invalid.pem"
    invalid.write_text("not a certificate", encoding="ascii")
    with pytest.raises(ssl.SSLError):
        create_client_ssl_context(str(invalid))


def test_network_presets_and_custom_ca(monkeypatch):
    monkeypatch.setenv("DECIMAL_TLS_CA_FILE", "shared.pem")
    for preset in (NetworkConfig.mainnet, NetworkConfig.testnet, NetworkConfig.devnet):
        assert preset().tls_ca_file == "shared.pem"
    monkeypatch.setenv("DECIMAL_TESTNET_TLS_CA_FILE", "testnet.pem")
    monkeypatch.setenv("DECIMAL_DEVNET_TLS_CA_FILE", "devnet.pem")
    assert NetworkConfig.testnet().tls_ca_file == "testnet.pem"
    assert NetworkConfig.devnet().tls_ca_file == "devnet.pem"
    assert NetworkConfig.custom(tls_ca_file="custom.pem").tls_ca_file == "custom.pem"
    assert NetworkConfig.custom().tls_ca_file is None


def test_rpc_keeps_requests_defaults_or_explicit_bundle(monkeypatch):
    provider = Mock()
    web3_factory = Mock(HTTPProvider=provider)
    monkeypatch.setattr("decimal_web3_sdk.rpc.Web3", web3_factory)
    pool = RpcPool(["https://rpc.example.invalid"])
    pool._create_web3(pool.current_url)
    provider.assert_called_with(pool.current_url, request_kwargs={"timeout": 10})
    client = DecimalClient(NetworkConfig.custom(
        web3_urls=["https://rpc.example.invalid"], tls_ca_file="custom.pem",
    ))
    client.rpc._create_web3(client.rpc.current_url)
    provider.assert_called_with(pool.current_url, request_kwargs={"timeout": 10, "verify": "custom.pem"})


async def test_owned_rest_and_ws_sessions_use_verified_context(monkeypatch):
    context = create_client_ssl_context()
    config = NetworkConfig.custom(web3_urls=["https://rpc.example.invalid"], tls_ca_file="custom.pem")
    factory = Mock(return_value=context)
    monkeypatch.setattr("decimal_web3_sdk.client.create_client_ssl_context", factory)
    monkeypatch.setattr("decimal_web3_sdk.ws.create_client_ssl_context", factory)
    connector_factory = Mock(wraps=aiohttp.TCPConnector)
    monkeypatch.setattr(aiohttp, "TCPConnector", connector_factory)
    client = DecimalClient(config)
    try:
        session = await client._get_session()
        assert await client._get_session() is session
        ws_session = await client.ws._get_session()
        assert await client.ws._get_session() is ws_session
        assert connector_factory.call_count == 2
        for call in connector_factory.call_args_list:
            assert call.kwargs["ssl"] is context
        assert factory.call_count == 2
        factory.assert_called_with("custom.pem")
    finally:
        await client.close()
    assert session.closed and ws_session.closed


async def test_external_ws_session_is_preserved(monkeypatch):
    factory = Mock(side_effect=AssertionError("must preserve external session"))
    monkeypatch.setattr("decimal_web3_sdk.ws.create_client_ssl_context", factory)
    async with aiohttp.ClientSession() as external:
        ws = DecimalWsClient(SimpleNamespace(), session=external)
        assert await ws._get_session() is external
        await ws.close()
        assert not external.closed
    factory.assert_not_called()


@pytest.fixture
def certificates(tmp_path):
    now = datetime.now(timezone.utc)
    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "SDK ephemeral test CA")])
    ca = (
        x509.CertificateBuilder().subject_name(name).issuer_name(name)
        .public_key(key.public_key()).serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(days=2)).not_valid_after(now + timedelta(days=2))
        .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
        .add_extension(x509.KeyUsage(True, False, False, False, False, True, True, False, False), critical=True)
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False)
        .sign(key, hashes.SHA256())
    )
    ca_path = tmp_path / "ca.pem"
    ca_path.write_bytes(ca.public_bytes(serialization.Encoding.PEM))
    servers = {}
    for label, expiry in (("valid", now + timedelta(days=1)), ("expired", now - timedelta(days=1))):
        leaf_key = ec.generate_private_key(ec.SECP256R1())
        leaf = (
            x509.CertificateBuilder()
            .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")]))
            .issuer_name(name).public_key(leaf_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now - timedelta(days=2)).not_valid_after(expiry)
            .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
            .add_extension(x509.SubjectAlternativeName([x509.DNSName("localhost")]), critical=False)
            .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
            .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(key.public_key()), critical=False)
            .sign(key, hashes.SHA256())
        )
        leaf_path = tmp_path / f"{label}.pem"
        key_path = tmp_path / f"{label}-key.pem"
        leaf_path.write_bytes(leaf.public_bytes(serialization.Encoding.PEM))
        key_path.write_bytes(leaf_key.private_bytes(
            serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption(),
        ))
        server = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        server.load_cert_chain(leaf_path, key_path)
        servers[label] = server
    return str(ca_path), servers


def handshake(client_context, server_context, hostname="localhost"):
    # Real OpenSSL handshakes in memory: no external endpoint or stored test key.
    client_in, client_out, server_in, server_out = [ssl.MemoryBIO() for _ in range(4)]
    client = client_context.wrap_bio(client_in, client_out, server_hostname=hostname)
    server = server_context.wrap_bio(server_in, server_out, server_side=True)
    for _ in range(20):
        complete = 0
        for peer in (client, server):
            try:
                peer.do_handshake()
                complete += 1
            except ssl.SSLWantReadError:
                pass
        if complete == 2:
            return
        if client_out.pending:
            server_in.write(client_out.read())
        if server_out.pending:
            client_in.write(server_out.read())
    pytest.fail("TLS handshake did not finish")


def test_explicit_private_ca_replaces_defaults_and_verifies(certificates, monkeypatch):
    ca_file, servers = certificates
    monkeypatch.setenv("SSL_CERT_FILE", "nonexistent-ignored.pem")
    context = create_client_ssl_context(ca_file)
    assert context.verify_mode == ssl.CERT_REQUIRED and context.check_hostname
    assert len(context.get_ca_certs()) == 1
    handshake(context, servers["valid"])


def test_ssl_cert_file_is_honored(certificates, monkeypatch):
    ca_file, servers = certificates
    monkeypatch.setenv("SSL_CERT_FILE", ca_file)
    context = create_client_ssl_context()
    assert len(context.get_ca_certs()) == 1
    handshake(context, servers["valid"])


def test_ssl_cert_dir_does_not_add_public_or_system_cas(tmp_path, monkeypatch):
    monkeypatch.setenv("SSL_CERT_DIR", str(tmp_path))
    context = create_client_ssl_context()
    assert context.get_ca_certs() == []
    assert context.verify_mode == ssl.CERT_REQUIRED and context.check_hostname


@pytest.mark.parametrize("reason", ["untrusted", "expired", "wrong-host"])
def test_bad_server_certificates_are_rejected(certificates, reason):
    ca_file, servers = certificates
    context = create_client_ssl_context(None if reason == "untrusted" else ca_file)
    with pytest.raises(ssl.SSLCertVerificationError) as error:
        handshake(context, servers["expired" if reason == "expired" else "valid"],
                  "other.example.invalid" if reason == "wrong-host" else "localhost")
    if reason == "expired":
        assert error.value.verify_code == 10
    elif reason == "wrong-host":
        assert error.value.verify_code == 62
