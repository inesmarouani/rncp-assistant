import gradio as gr
from retriever import chain

def analyser_projet(description):
    result = chain.invoke(description)
    return result

interface = gr.Interface(
    fn=analyser_projet,
    inputs=gr.Textbox(
        placeholder="Décris ton projet ici...",
        label="Description de ton projet",
        lines=5
    ),
    outputs=gr.Textbox(label="Analyse des compétences RNCP"),
    title="🎓 Assistant RNCP Dev IA — Simplon",
    description="Décris ton projet et découvre quelles compétences RNCP il couvre !"
)

interface.launch()