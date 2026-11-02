
from flask import Flask, render_template, request, g
import logging
import json
import time
from datetime import datetime, timezone

app = Flask(__name__)

# Configuração de logs estruturados em JSON
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage()
        }

        # Campos adicionais das requisições HTTP
        if hasattr(record, "http_data"):
            log_data.update(record.http_data)

        return json.dumps(log_data, ensure_ascii=False)


logger = logging.getLogger("viajeplus")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)

logger.propagate = False


# Captura o início de cada requisição
@app.before_request
def start_request_timer():
    g.start_time = time.perf_counter()


# Registra os dados ao finalizar cada requisição
@app.after_request
def log_http_request(response):
    duration_ms = round(
        (time.perf_counter() - g.start_time) * 1000, 2
    )

    logger.info(
        "Requisição HTTP processada",
        extra={
            "http_data": {
                "event_type": "http_request",
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "duration_ms": duration_ms
            }
        }
    )

    return response


# Dados demonstrativos dos destinos
destinos = [
    {
        "nome": "Paris",
        "pais": "França",
        "categoria": "Internacional",
        "descricao": "Descubra a cidade da luz, da arte e da arquitetura.",
        "imagem": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34"
    },
    {
        "nome": "Rio de Janeiro",
        "pais": "Brasil",
        "categoria": "Nacional",
        "descricao": "Praias icônicas, paisagens naturais e cultura vibrante.",
        "imagem": "https://images.unsplash.com/photo-1483729558449-99ef09a8c325"
    },
    {
        "nome": "Santorini",
        "pais": "Grécia",
        "categoria": "Internacional",
        "descricao": "Casas brancas, mar azul e pores do sol inesquecíveis.",
        "imagem": "https://images.unsplash.com/photo-1533105079780-92b9be482077"
    }
]


@app.route("/")
def home():
    logger.info("Página inicial acessada")
    return render_template("index.html", destinos=destinos)


@app.route("/health")
def health():
    return {"status": "ok", "application": "Viaje+"}


if __name__ == "__main__":
    logger.info("Iniciando aplicação Viaje+")
    app.run(host="0.0.0.0", port=5000, debug=True)
