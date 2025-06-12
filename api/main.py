from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.llm_dispatcher import router as llm_router

app = FastAPI(
    title="Multi-LLM API",
    description="API for dispatching requests to multiple LLM endpoints",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the LLM router
app.include_router(llm_router, prefix="/llm", tags=["LLM"])
