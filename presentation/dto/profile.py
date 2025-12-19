from pydantic import BaseModel
from typing import Optional

class Profile(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    title: Optional[str] = None
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None

    def get_json_profile(self):
        return self.model_dump()
