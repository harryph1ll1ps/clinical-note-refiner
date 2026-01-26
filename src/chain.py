from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.documents import Document


from prompts import REFINE_NOTE_PROMPT, CODE_RETRIEVAL_PROMPT
from schemas import RefinedNote, CodeSuggestions


def format_docs(docs: list[Document]):
    """Format retrieved transcript documents into a prompt-ready string."""
    return "\n\n".join(doc.page_content for doc in docs)


def build_refinement_chain(retriever):
    """Chain that refines a clinical note based off a transcript. """
    llm = ChatOllama(
        model="llama3.2:3b",
        temperature=0.2,
    )


    # create parser to ensure LLM output matches schema
    parser = PydanticOutputParser(
        pydantic_object=RefinedNote
    )

    # build chain (like building a function)
    chain = (

        # takes an input, and produces a dictionary with 3 keys by running the input through 3 different runnables
        # transcript_value => retriever.invoke(input=draft_note_text)
        # draft_note => passes the input through unchanged
        # format_instructions => ignores the input and gets the JSON schema instructions
        {
            "relevant_transcript_excerpts": retriever | RunnableLambda(format_docs), 
            "draft_note": RunnablePassthrough(), 
            "format_instructions": RunnableLambda(
                lambda _: parser.get_format_instructions() 
            ),
        }
        | REFINE_NOTE_PROMPT # dictionary values are pasted into prompt
        | llm 
        | parser # llm output is parsed into pydantic object
    )

    return chain


def build_code_retrieval_chain(retriever):
    llm = ChatOllama(
        model="llama3.2:3b",
        temperature=0.2,
    )


    # create parser to ensure LLM output matches schema
    parser = PydanticOutputParser(
        pydantic_object=CodeSuggestions
    )

    chain = (
        {
            "clinical_note": RunnablePassthrough(),
            "relevant_codes": retriever | RunnableLambda(format_docs),
            "format_instructions": RunnableLambda(
                lambda _: parser.get_format_instructions() 
            ),
        }
        | CODE_RETRIEVAL_PROMPT
        | llm
        | parser
    )

    return chain