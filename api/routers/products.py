"""Employes router."""
from utils.connect_mysql import ConfigureDBConnection
from utils.logger import log
from typing import Dict
import mysql.connector

import utils.logger as logger
import os
from dotenv import load_dotenv

from fastapi import APIRouter


load_dotenv("api/.env")

host=os.environ.get("HOST")
port=os.environ.get("PORT")
username=os.environ.get("USERNAME")
password=os.environ.get("PASSWORD")
database=os.environ.get("DATABASE")

db = ConfigureDBConnection(
                host=host,
                port=port,
                username=username,
                password=password,
                database=database
)




s_query = "SELECT * FROM products"

log.info("Loading data from products table.")
results = db.query(s_query)



router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

@router.get("/data", tags=["all_data"])
async def get_data() -> Dict:
    return results
