from fastapi import FastAPI
from app.api.endpoints.retrieval import router as retrieval_router

app = FastAPI()

# Include the retrieval router
app.include_router(retrieval_router)
