
import sys
import os

# Permite importar o app da pasta principal
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from app import app


def test_home_status_code():
    """Verifica se a página inicial abre corretamente."""
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_home_content():
    """Verifica se os principais elementos estão presentes."""
    client = app.test_client()

    response = client.get("/")

    assert b"Viaje" in response.data
    assert b"Destinos em destaque" in response.data


def test_health_endpoint():
    """Verifica se a aplicação está saudável."""
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "ok"
    assert response.json["application"] == "Viaje+"


def test_destinations_rendered():
    """Verifica se os destinos demonstrativos aparecem."""
    client = app.test_client()

    response = client.get("/")

    assert b"Paris" in response.data
    assert b"Rio de Janeiro" in response.data
    assert b"Santorini" in response.data


def test_http_request_logging(caplog):
    """Verifica se as requisições HTTP são registradas corretamente."""
    import json
    import logging

    with caplog.at_level(logging.INFO, logger="viajeplus"):
        client = app.test_client()
        response = client.get("/health")

    assert response.status_code == 200

    request_logs = [
        record for record in caplog.records
        if record.name == "viajeplus"
        and record.getMessage() == "Requisição HTTP processada"
    ]

    assert len(request_logs) == 1

    log_data = json.loads(request_logs[0].getMessage()) \
        if False else request_logs[0].http_data

    assert log_data["event"] == "http_request"
    assert log_data["method"] == "GET"
    assert log_data["path"] == "/health"
    assert log_data["status"] == 200
    assert isinstance(log_data["duration_ms"], (int, float))
    assert log_data["duration_ms"] >= 0

