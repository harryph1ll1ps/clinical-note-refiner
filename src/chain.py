from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import PydanticOutputParser

from prompts import REFINE_NOTE_PROMPT
from schemas import RefinedNote


def build_refinement_chain(retriever):
    """
    Chain that refines a clinical note based off a transcript.
    """

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
    )


    # create parser to ensure LLM output matches schema
    parser = PydanticOutputParser(
        pydantic_object=RefinedNote
    )

    # build chain 
    chain = (
        {
            "transcript": retriever,
            "draft_note": RunnablePassthrough(),
        }
        | REFINE_NOTE_PROMPT
        | llm
        | parser
    )

    return chain