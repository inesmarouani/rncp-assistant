from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# 1. Charger le vectorstore
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url=OLLAMA_HOST
)

vectorstore = Chroma(
    persist_directory="vectorstore",
    embedding_function=embeddings
)

# 2. Créer le retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# 3. Définir le LLM
llm = OllamaLLM(
    model="llama3.2",
    base_url=OLLAMA_HOST
)

# 4. Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """Tu es un assistant pédagogique Simplon spécialisé dans le référentiel RNCP Développeur IA.

Utilise UNIQUEMENT les extraits ci-dessous pour répondre.
Si l'information n'est pas dans les extraits, dis-le explicitement.
N'invente JAMAIS de compétences absentes des extraits.

Extraits du référentiel RNCP :
{context}

Réponds en 3 parties :
1. ✅ Compétences couvertes (cite le numéro exact ex: C13, C9...)
2. ❌ Compétences non couvertes
3. 💡 Recommandations concrètes"""),
    ("human", "{question}"),
])

# 5. Chaîne RAG
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

## 6. Test
#question = "Mon projet déploie une API FastAPI avec Docker et un pipeline GitHub Actions. Quelles compétences RNCP couvre-t-il ?"
#result = chain.invoke(question)
#print(result)