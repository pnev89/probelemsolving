"""Recommender api module."""
from fastapi import FastAPI

from utils.logger import log
from .routers import employes
from .routers import products

app = FastAPI()

log.info("Starting API")
app.include_router(employes.router)
app.include_router(products.router)


