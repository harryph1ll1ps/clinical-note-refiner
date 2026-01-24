from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

MAX_CHUNKS = 4

def build_chunk_retriever(transcript_path: str):

    # create loader object and then load the transcript
    loader = TextLoader(transcript_path, encoding="utf-8")
    docs = loader.load()

    # chunk the transcript
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    # split into chunks of the form: Document(page_content="", metadata={})
    chunks = splitter.split_documents(docs)

    if not chunks:
        raise ValueError("Transcript produced no chunks. Check input file.")

    # extract the texts only
    texts: list[str] = [doc.page_content for doc in chunks]

    # embed text 
    embeddings = OpenAIEmbeddings().embed_documents(texts)

    # store embeddings in vector index structure for quick retrieval
    # note: FAISS is a local index compared to a hosted DB such as pinecone
    vectorstore = FAISS.from_embeddings(
        embeddings=embeddings,
        documents=chunks,
    )

    # return a retriever that gives the top-k relevant chunks, given some input text
    return vectorstore.as_retriever(
        search_kwargs={"k": MAX_CHUNKS}
    )
