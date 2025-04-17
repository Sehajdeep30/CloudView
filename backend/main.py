from fastapi import FastAPI
import uvicorn
from endpoints.user_endpoints import user_router  # Import user-related endpoints
from endpoints.aws_cred_endpoints import aws_router #Import aws-manager endpoints
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


origins = [
    "http://localhost:5173",  # Vite default dev server port
    "http://127.0.0.1:5173",  # In case it's accessed via IP
    "http://localhost:3000",  # Just in case you're using CRA
    "http://localhost",       # Generic fallback
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for public APIs (not recommended with credentials)
    allow_credentials=True,  # Important for cookies (e.g. HttpOnly refresh tokens)
    allow_methods=["*"],     # You can narrow this down to ["GET", "POST"] etc.
    allow_headers=["*"],     # You can also specify custom headers here if needed
)


app.include_router(user_router)
app.include_router(aws_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)