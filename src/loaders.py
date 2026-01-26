from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

TOP_K_CHUNKS = 4

def build_chunk_retriever(path: str):

    # create loader object and then load the transcript
    loader = TextLoader(path, encoding="utf-8")
    docs = loader.load()

    # chunk the document
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    # split into chunks of the form: Document(page_content="", metadata={})
    chunks = splitter.split_documents(docs)

    if not chunks:
        raise ValueError("Transcript produced no chunks. Check input file.")


    # initialise embedding object
    embedding_model = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    # 1) extracts page content from each chunk
    # 2) embeds each chunk of content
    # 3) stores each embedding in a vector index structure for efficient retrieval
    # note: FAISS is a local index compared to a hosted DB such as pinecone
    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model,
    )


    # return a retriever that gives the top-k relevant chunks, given some input text
    return vectorstore.as_retriever(
        search_kwargs={"k": TOP_K_CHUNKS}
    )
