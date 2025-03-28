from fastapi import FastAPI
import uvicorn
# from endpoints.gem_endpoints import gem_router  # Import gem-related endpoints
# from endpoints.user_endpoints import user_router  # Import user-related endpoints
# from models.gem_models import *  # Import gem models (if needed for additional processing)

app = FastAPI()

# # Include the gem and user routers to add their endpoints to the app
# app.include_router(gem_router)
# app.include_router(user_router)

# Optionally, you can create database tables at startup by uncommenting the following:
# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
    # create_db_and_tables()  # Uncomment this if you want to create tables on startup  