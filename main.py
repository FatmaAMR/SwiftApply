from fastapi import FastAPI
import presentation


app = FastAPI()
app.include_router(presentation.base_router)
app.include_router(presentation.data_router)
app.include_router(presentation.resume_router)
app. include_router(presentation.helper_router)

