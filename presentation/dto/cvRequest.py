from pydantic import BaseModel

class CVRequest(BaseModel):
    parsed_cv: dict
    job_description: str
    notes: str
    company_info: str