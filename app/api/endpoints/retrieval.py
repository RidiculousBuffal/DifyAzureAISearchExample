from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from typing import List, Optional
import dotenv
import os
dotenv.load_dotenv()
router = APIRouter()

# Define the request and response models
class RetrievalSetting(BaseModel):
    top_k: int
    score_threshold: float

class RetrievalRequest(BaseModel):
    knowledge_id: str
    query: str
    retrieval_setting: RetrievalSetting

class Metadata(BaseModel):
    path: str
    description: str

class Record(BaseModel):
    content: str
    score: float
    title: str
    metadata: Optional[Metadata]

class RetrievalResponse(BaseModel):
    records: List[Record]

# Azure Search configuration
SERVICE_ENDPOINT = os.getenv("SERVICE_ENDPOINT")
INDEX_NAME = os.getenv("INDEX_NAME")
KEY = os.getenv("KEY")
credential = AzureKeyCredential(KEY)
client = SearchClient(endpoint=SERVICE_ENDPOINT, index_name=INDEX_NAME, credential=credential)

@router.post("/retrieval", response_model=RetrievalResponse)
async def retrieval(request: RetrievalRequest):
    # Perform the search operation
    results = list(
        client.search(
            search_text=request.query,
            query_type="semantic",
            semantic_configuration_name="default",
            query_language="zh-cn",
            top=request.retrieval_setting.top_k
        )
    )

    # Prepare the response records
    records = []
    for result in results:
        if result['@search.reranker_score']/4.0 >= request.retrieval_setting.score_threshold:
            record = Record(
                content=result['content'],
                score=result['@search.reranker_score']/4.0,
                title=result['title'],
                metadata=Metadata(path=result['url'], description=result.get('description', ''))
            )
            records.append(record)

    return RetrievalResponse(records=records)
