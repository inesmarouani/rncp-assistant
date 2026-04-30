def run_ingestion():
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_chroma import Chroma

    loader = TextLoader("data/rncp.md", encoding="utf-8")
    documents = loader.load()
    print(f"Pages chargées : {len(documents)}")

    # 2. Split
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
    )
    chunks = splitter.split_documents(documents)
    print(f"Chunks créés : {len(chunks)}")

    # 3. Embed + 4. Store
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )



    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="vectorstore"
    )
    print("Vectorstore créé et sauvegardé !")

    # Vérification qualité
    results = vectorstore.similarity_search(
        "déployer une application avec Docker",
        k=3
    )

    for i, doc in enumerate(results):
        print(f"\n--- Chunk {i+1} ---")
        print(doc.page_content[:300])