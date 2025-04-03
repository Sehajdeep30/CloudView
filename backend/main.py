from fastapi import FastAPI
import uvicorn
# from endpoints.gem_endpoints import gem_router  # Import gem-related endpoints
from endpoints.user_endpoints import user_router  # Import user-related endpoints
# from models.gem_models import *  # Import gem models (if needed for additional processing)

app = FastAPI()

# # Include the gem and user routers to add their endpoints to the app
# app.include_router(gem_router)
app.include_router(user_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)