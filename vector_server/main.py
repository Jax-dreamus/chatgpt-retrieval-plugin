# This is a version of the main.py file found in ../../../server/main.py without authentication.
# Copy and paste this into the main file at ../../../server/main.py if you choose to use no authentication for your retrieval plugin.
import json
from datetime import datetime
from glob import glob
from typing import Optional
import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, Body, UploadFile
from fastapi.staticfiles import StaticFiles
from loguru import logger
from starlette.responses import RedirectResponse

from models.api import (
    DeleteRequest,
    DeleteResponse,
    QueryRequest,
    QueryResponse,
    UpsertRequest,
    UpsertResponse, UpsertBulkResponse,
)
from datastore.factory import get_datastore
from services.vector_search.file import get_document_from_file

from models.models import DocumentMetadata, Source, Document

app = FastAPI()
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")

# Create a sub-application, in order to access just the query endpoints in the OpenAPI schema, found at http://0.0.0.0:8000/sub/openapi.json when the app is running locally
sub_app = FastAPI(
    title="Retrieval Plugin API",
    description="A retrieval API for querying and filtering documents based on natural language queries and metadata",
    version="1.0.0",
    servers=[{"url": "https://0.0.0.0:8001"}],
)
app.mount("/sub", sub_app)


@app.get("/")
async def docs_redirect():
    return RedirectResponse(url='/docs')


@app.post(
    "/upsert-file",
    response_model=UpsertResponse,
)
async def upsert_file(
        file: UploadFile = File(...),
        metadata: Optional[str] = Form(None),
):
    try:
        metadata_obj = (
            DocumentMetadata.parse_raw(metadata)
            if metadata
            else DocumentMetadata(source=Source.file)
        )
    except:
        metadata_obj = DocumentMetadata(source=Source.file)

    document = await get_document_from_file(file, metadata_obj)

    try:
        ids = await datastore.upsert([document])
        return UpsertResponse(ids=ids)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"str({e})")


@app.post(
    "/upsert-local-files",
    response_model=UpsertBulkResponse,
)
async def upsert_local_files():
    succeed_ids = []
    failed_ids = []
    for filename in glob("upsert_docs/*.json"):
        with open(filename, encoding='utf-8') as f:
            data = json.load(f)

        # TODO: metadata 및 id 정교화 필요
        document = Document(
            id=str(datetime.strptime(
                data['metadata']['post-date'],
                '%Y년 %m월 %d일').date()
                   ),
            text=data['text'],
            metadata=DocumentMetadata(source=Source.file)
        )
        try:
            ids = await datastore.upsert([document])
            succeed_ids.extend(ids)
        except Exception as e:
            logger.error(e)
            failed_ids.append(document.id)

    return UpsertBulkResponse(succeed_ids=succeed_ids,
                              failed_ids=failed_ids)


@app.post(
    "/upsert",
    response_model=UpsertResponse,
)
async def upsert(
        request: UpsertRequest = Body(...),
):
    try:
        ids = await datastore.upsert(request.documents)
        return UpsertResponse(ids=ids)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@app.post(
    "/query",
    response_model=QueryResponse,
)
async def query_main(
        request: QueryRequest = Body(...),
):
    try:
        results = await datastore.query(
            request.queries,
        )
        return QueryResponse(results=results)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@sub_app.post(
    "/query",
    response_model=QueryResponse,
    description="Accepts search query objects with query and optional filter. Break down complex questions into sub-questions. Refine results by criteria, e.g. time / source, don't do this often. Split queries if ResponseTooLargeError occurs.",
)
async def query(
        request: QueryRequest = Body(...),
):
    try:
        results = await datastore.query(
            request.queries,
        )
        return QueryResponse(results=results)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@app.delete(
    "/delete",
    response_model=DeleteResponse,
)
async def delete(
        request: DeleteRequest = Body(...),
):
    if not (request.ids or request.filter or request.delete_all):
        raise HTTPException(
            status_code=400,
            detail="One of ids, filter, or delete_all is required",
        )
    try:
        success = await datastore.delete(
            ids=request.ids,
            filter=request.filter,
            delete_all=request.delete_all,
        )
        return DeleteResponse(success=success)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@app.on_event("startup")
async def startup():
    global datastore
    datastore = await get_datastore()


def start():
    uvicorn.run("vector_server.main:app", host="0.0.0.0", port=8001, reload=True)
