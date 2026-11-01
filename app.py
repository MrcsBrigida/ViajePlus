
from flask import Flask, render_template
import logging
import json
from datetime import datetime

app = Flask(__name__)

# Configuração inicial de logs
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "message": record.getMessage()
        }
        return json.dumps(log_data, ensure_ascii=False)


logger = logging.getLogger("viajeplus")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)


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
