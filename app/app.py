from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware
from app.config.settings import api_settings
import uvicorn
from fastapi.responses import JSONResponse


app = FastAPI(
    title=api_settings.TITLE,
    openapi_url=f'{api_settings.PREFIX}/openapi.json',
    docs_url=f'{api_settings.PREFIX}/docs',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# set prefix  all routes
app.router.prefix = api_settings.PREFIX


@app.get("/")
def root():
    return {"message": f"Welcome to {api_settings.TITLE}"}


def run():
    uvicorn.run(app,
                host=api_settings.HOST,
                port=api_settings.PORT,
                )
