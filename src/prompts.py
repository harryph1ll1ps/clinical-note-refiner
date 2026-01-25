from langchain_core.prompts import PromptTemplate


REFINE_NOTE_PROMPT = PromptTemplate.from_template("""
You are assisting a clinician by refining a draft clinical note.

You are given:
1. Relevant excerpts from the consult transcript (verbatim)
2. A draft clinical note written by the clinician

Your task is to improve the clinical note while following these rules strictly:

RULES:
- Do NOT introduce new clinical facts, diagnoses, symptoms, or management steps that are not explicitly supported by the transcript.
- If relevant clinical information is missing from the transcript, do NOT guess. Instead, list it under "missing_info".
- Preserve a professional clinical tone suitable for medical documentation.
- Every meaningful change or addition must be supported by the transcript.
- Output MUST be a single JSON object with the fields exactly as specified.
- Do NOT nest the output under "properties" or any other wrapper.
- Do NOT include schema definitions or explanations.

WHAT TO DO:
- Improve clarity, structure, and clinical precision.
- Make the assessment more explicit if supported by the transcript.
- Expand the plan only using information discussed in the consult.
- Remove vague or redundant phrasing.

OUTPUT FORMAT:
{format_instructions}

RELEVANT TRANSCRIPT EXCERPTS:
{relevant_transcript_excerpts}

DRAFT NOTE:
{draft_note}
""")