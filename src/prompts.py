REFINE_NOTE_PROMPT = """
You are assisting a clinician by refining a draft clinical note.

You are given:
1. A consult transcript (verbatim conversation)
2. A draft clinical note written by the clinician

Your task is to improve the clinical note while following these rules strictly:

RULES:
- Do NOT introduce new clinical facts, diagnoses, symptoms, or management steps that are not explicitly supported by the transcript.
- If relevant clinical information is missing from the transcript, do NOT guess. Instead, list it under "missing_information".
- Preserve a professional clinical tone suitable for medical documentation.
- Every meaningful change or addition must be supported by the transcript.

WHAT TO DO:
- Improve clarity, structure, and clinical precision.
- Make the assessment more explicit if supported by the transcript.
- Expand the plan only using information discussed in the consult.
- Remove vague or redundant phrasing.

OUTPUT FORMAT:
You must return a structured response matching the provided schema:
- refined_note
- changes_made
- missing_information
- citations

TRANSCRIPT:
{transcript}

DRAFT NOTE:
{draft_note}
"""