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
📄 Markdown RNCP → ✂️ Split (chunks 800 car.) → 🔢 Embed (all-MiniLM-L6-v2) → 🗄️ Chroma
↓
👤 Question → 🔍 Similarité (top 4 chunks) → 🤖 Groq (llama-3.1-8b) → 💬 Réponse

## Technologies
- **LangChain** — pipeline RAG
- **HuggingFace** — embeddings (all-MiniLM-L6-v2)
- **ChromaDB** — base vectorielle locale
- **Groq** — LLM (llama-3.1-8b-instant), API gratuite
- **Gradio** — interface utilisateur web avec historique
- **Docker** — conteneurisation

## Installation et lancement

### Prérequis
- Docker installé
- Une clé API Groq gratuite sur [console.groq.com](https://console.groq.com)

### Variables d'environnement
Copie `.env.example` en `.env` et remplis ta clé :
```bash
cp .env.example .env
# Puis édite .env et ajoute ta clé GROQ_API_KEY
```

### Lancement
```bash
# 1. Cloner le repo
git clone https://github.com/inesmarouani/rncp-assistant.git
cd rncp-assistant

# 2. Build Docker
docker build -t rncp-assistant .

# 3. Lancer
docker run -p 7860:7860 \
  -e GROQ_API_KEY=ta_clé_groq \
  -v "${PWD}/vectorstore:/app/vectorstore" \
  rncp-assistant

# 4. Ouvrir dans le navigateur
http://localhost:7860
```

## Déploiement
L'application est déployée publiquement sur HuggingFace Spaces :
👉 [huggingface.co/spaces/inesmarouani/rncp-assistant](https://huggingface.co/spaces/inesmarouani/rncp-assistant)

## Exemples de questions testées
1. *"Mon projet déploie une API FastAPI avec Docker et un pipeline GitHub Actions. Quelles compétences RNCP couvre-t-il ?"*
2. *"La compétence C13 est-elle validée si j'ai seulement un Dockerfile sans CI/CD ?"*
3. *"Quelles compétences me manquent pour valider le bloc MLOps ?"*

## Auteur
Ines Marouani 