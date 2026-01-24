from pydantic import BaseModel, Field
from typing import List

class RefinedNote(BaseModel):
    refined_note: str = Field(
        description="The improved clinical note, based strictly on the consult transcript"
    )

    changes_made: List[str] = Field(
        description="List describing what was changed or added"
    )

    missing_info: List[str] = Field(
        description="Clinically relevant info that was missing"
    )

    citations: List[str] = Field(
        description="Short quotes or phrases from the transcript that support the changes"
    )

