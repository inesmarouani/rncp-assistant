# 1. Image de base
FROM python:3.11-slim

# 2. Installer uv
RUN pip install uv

# 3. Répertoire de travail
WORKDIR /app

# 4. Copier les fichiers de dépendances
COPY pyproject.toml .
COPY uv.lock .

# 5. Installer les dépendances
RUN uv sync --frozen --python /usr/local/bin/python3

# 6. Copier le reste du code
COPY . .

# Générer le vectorstore pendant le build
RUN uv run --python /usr/local/bin/python3 src/ingest.py

# 7. Exposer le port Gradio
EXPOSE 7860

# 8. Lancer l'application
CMD ["uv", "run", "--python", "/usr/local/bin/python3", "src/app.py"]
