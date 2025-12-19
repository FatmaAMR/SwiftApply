from fastapi import FastAPI
import presentation


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(presentation.base_router)
app.include_router(presentation.data_router)
app.include_router(presentation.resume_router)
app.include_router(presentation.helper_router)
app.include_router(presentation.profile_router)

