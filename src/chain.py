from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda


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

    # build chain (like building a function, not calling it though)
    chain = (
        {
            "transcript": retriever, # takes the input and feeds it into the retriever
            "draft_note": RunnablePassthrough(), # takes the input and passes through unchanged
            "format_instructions": RunnableLambda(
                lambda _: parser.get_format_instructions() # gets the JSON schema instructions
            ),
        }
        | REFINE_NOTE_PROMPT # previous values are pasted into prompt
        | llm 
        | parser # llm output is parsed into pydantic object
    )

    return chain