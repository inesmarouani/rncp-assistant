

import os
import sys
sys.path.append(os.path.dirname(__file__))

# Générer le vectorstore si absent
if not os.path.exists("vectorstore"):
    print("Vectorstore absent — lancement de l'ingestion...")
    from ingest import run_ingestion
    run_ingestion()

import gradio as gr
from retriever import chain, retriever

def analyser_projet(description, history):
    docs = retriever.invoke(description)
    sources = "\n\n".join([
        f"📄 Source {i+1} :\n{doc.page_content[:300]}..."
        for i, doc in enumerate(docs)
    ])
    
    result = chain.invoke(description)
    reponse = f"{result}\n\n---\n### 📚 Sources utilisées\n{sources}"
    
    # ✅ Nouveau format Gradio 6.0
    history.append({"role": "user", "content": description})
    history.append({"role": "assistant", "content": reponse})
    
    return history, ""

with gr.Blocks(
    title="Assistant RNCP Dev IA"
) as interface:
    
    gr.Markdown("""
    # 🎓 Assistant RNCP Dev IA — Simplon
    > Analyse la couverture de ton projet par rapport au référentiel RNCP Développeur IA
    """)
    
    chatbot = gr.Chatbot(
        label="Conversation",
        height=500
    )
    
    with gr.Row():
        input_box = gr.Textbox(
            placeholder="Décris ton projet ici... ex: Mon projet déploie une API FastAPI avec Docker",
            label="Description du projet",
            lines=3,
            scale=4
        )
        submit_btn = gr.Button("🔍 Analyser", variant="primary", scale=1)
    
    gr.Examples(
        examples=[
            "Mon projet déploie une API FastAPI avec Docker et un pipeline GitHub Actions. Quelles compétences RNCP couvre-t-il ?",
            "La compétence C13 est-elle validée si j'ai seulement un Dockerfile sans CI/CD ?",
            "Quelles compétences me manquent pour valider le bloc MLOps ?"
        ],
        inputs=input_box
    )
    
    history_state = gr.State([])
    
    submit_btn.click(
        fn=analyser_projet,
        inputs=[input_box, history_state],
        outputs=[chatbot, input_box]
    )
    
    input_box.submit(
        fn=analyser_projet,
        inputs=[input_box, history_state],
        outputs=[chatbot, input_box]
    )

interface.launch(
    server_name="0.0.0.0",
    server_port=7860,
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="green",
    )
)