from pydantic import BaseModel
from typing import List, Optional

from models.models import Document, Query, QueryResult, DocumentMetadataFilter


class UpsertRequest(BaseModel):
    documents: List[Document]


class UpsertResponse(BaseModel):
    ids: List[str]


class UpsertBulkResponse(BaseModel):
    succeed_ids: List[str]
    failed_ids: List[str]


class QueryRequest(BaseModel):
    queries: List[Query]


class QueryResponse(BaseModel):
    results: List[QueryResult]


class DeleteRequest(BaseModel):
    ids: Optional[List[str]] = None
    filter: Optional[DocumentMetadataFilter] = None
    delete_all: Optional[bool] = False


class DeleteResponse(BaseModel):
    success: bool
