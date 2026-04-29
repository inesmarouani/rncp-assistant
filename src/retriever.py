from langchain_huggingface import HuggingFaceEmbeddings, ChatHuggingFace, HuggingFaceEndpoint
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from dotenv import load_dotenv

import os

load_dotenv()

# 1. Embeddings HuggingFace (gratuit, local)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 2. Charger le vectorstore
vectorstore = Chroma(
    persist_directory="vectorstore",
    embedding_function=embeddings
)

# 3. Retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# 4. LLM via HuggingFace Inference API

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1,
)
#llm = HuggingFaceEndpoint(
 #   repo_id="HuggingFaceH4/zephyr-7b-beta",  
  #  huggingfacehub_api_token=os.getenv("HF_TOKEN"),
   # temperature=0.1,
    #task="conversational",
#)
#chat_model = ChatHuggingFace(llm=llm)


# 5. Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """Tu es un assistant pédagogique Simplon spécialisé dans le référentiel RNCP Développeur IA.
Utilise UNIQUEMENT les extraits ci-dessous pour répondre.
Si l'information n'est pas dans les extraits, dis-le explicitement.
Ne invente JAMAIS de compétences absentes des extraits.

Extraits du référentiel RNCP :
{context}

Réponds en 3 parties :
1. ✅ Compétences couvertes (cite le numéro exact ex: C13, C9...)
2. ❌ Compétences non couvertes
3. 💡 Recommandations concrètes"""),
    ("human", "{question}"),
])

# 6. Chaîne RAG
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