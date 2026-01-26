from pydantic import BaseModel
from typing import List

class RefinedNote(BaseModel):
    refined_note: str
    changes_made: List[str] 
    missing_info: List[str]
    citations: List[str]

class SuggestedCode(BaseModel):
    code: str
    description: str
    rationale: str


class CodeSuggestions(BaseModel):
    suggested_codes: List[SuggestedCode]


