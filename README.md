---
title: RNCP Assistant Dev IA
emoji: 🎓
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# 🎓 Assistant RNCP Dev IA — Simplon

## Description
Cet outil permet de vérifier si un projet étudiant couvre bien les compétences 
du référentiel RNCP du titre Développeur en Intelligence Artificielle.
Il analyse une description de projet en langage naturel et identifie les 
compétences couvertes et manquantes, avec justification.

## Architecture RAG
📄 PDF RNCP → ✂️ Split (chunks 800 car.) → 🔢 Embed (nomic-embed-text) → 🗄️ Chroma
↓
👤 Question → 🔍 Similarité (top 4 chunks) → 🤖 llama3.2 → 💬 Réponse

## Technologies
- **LangChain** — pipeline RAG
- **Ollama** — LLM local (llama3.2 + nomic-embed-text)
- **ChromaDB** — base vectorielle locale
- **Gradio** — interface utilisateur web
- **Docker** — conteneurisation

## Installation et lancement

### Prérequis
- Docker installé
- Ollama installé avec les modèles suivants :
```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### Lancement
```bash
# 1. Cloner le repo
git clone https://github.com/TON_USERNAME/rncp-assistant.git
cd rncp-assistant

# 2. Build Docker
docker build -t rncp-assistant .

# 3. Lancer
docker run -p 7860:7860 \
  --add-host=host.docker.internal:host-gateway \
  -v "${PWD}/vectorstore:/app/vectorstore" \
  rncp-assistant

# 4. Ouvrir dans le navigateur
http://localhost:7860
```

## Exemples de questions testées
1. *"Mon projet déploie une API FastAPI avec Docker et un pipeline GitHub Actions. Quelles compétences RNCP couvre-t-il ?"*
2. *"La compétence C13 est-elle validée si j'ai seulement un Dockerfile sans CI/CD ?"*

## Auteur
Ines Marouani
=======
---
title: Rncp Assistant
emoji: 👁
colorFrom: red
colorTo: purple
sdk: docker
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
>>>>>>> 09d27b428e6c33bf8b5a6e938cc6c4dca054c120
