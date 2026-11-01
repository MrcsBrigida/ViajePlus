
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
