
# Imagem base do Python
FROM python:3.12-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copiar dependências
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar os arquivos do projeto
COPY . .

# Porta utilizada pela aplicação
EXPOSE 5000

# Executar Flask com Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]