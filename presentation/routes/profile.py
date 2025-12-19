from fastapi import APIRouter, UploadFile, Depends, status, Request
from fastapi.responses import JSONResponse
from utils import get_settings, Settings
from business import DataController, resume_llm
import state


llm = resume_llm()
profile_router = APIRouter()

from fastapi import APIRouter, Form
from presentation.dto.profile import Profile


@profile_router.post("/profile")
async def create_or_update_profile(profile: Profile):
    return profile.model_dump()

# @profile_router.post("/profile")
# async def create_or_update_profile(
#     full_name: str = Form(...),
#     title: str = Form(...),
#     email: str = Form(...),
#     phone: str = Form(...),
#     location: str = Form(None),
#     linkedin_url: str = Form(None),
#     github_url: str = Form(None),
#     website: str = Form(None),
# ):
#     profile = Profile(
#         name=full_name,
#         title=title,
#         email=email,
#         phone=phone,
#         location=location,
#         linkedin=linkedin_url,
#         github=github_url,
#         website=website,
#     )
#     return profile.dict()




# @app.post("/profile")
# async def save_profile(profile: Profile):
#     return profile.get_json_profile()



