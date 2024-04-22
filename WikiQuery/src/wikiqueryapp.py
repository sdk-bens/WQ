from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.myrouter import router

app = FastAPI(
    title="WikiQuery",
    description="""Documentation for all APIs for WikiQuery Project, 
    Seddik Benaissa, 
    Northeastern University Boston, 
    Spring 2024""",
    version="1.0.0",
)

# CORS middleware to allow all origins in development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
