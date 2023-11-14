from fastapi import HTTPException
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from ...utils.databases import SQLDB
from ..models import users_table
from fastapi.templating import Jinja2Templates
from ..services.DatabaseManager import DatabaseManager
from sqlalchemy import and_
from fastapi import Body
import aiohttp

router = APIRouter()
templates = Jinja2Templates("templates")
db_manager = DatabaseManager(
    "postgres", "postgres", "db", "5432", "fast_api_db", [users_table])


@router.post("/api/add_user")
def add_user(name: str = Body(...), email: str = Body(...), db: SQLDB = Depends(db_manager.get_db)):
    try:
        response = None
        db_manager.validate_User(name, email)
        user = users_table(name=name, email=email)
        user_id = db.add_data(user)
        response = {'user_id': user_id}
    except ValueError as e:
        response = str(e)
    return response


@router.get("/api/get_user/{user_id}")
def get_user(user_id: str, db: SQLDB = Depends(db_manager.get_db)):
    try:
        response = db.get_user(users_table, user_id)
    except ValueError as e:
        response = str(e)
    return response


@router.post("/api/find_user")
def find_user(name: str = Body(...), email: str = Body(...), db: SQLDB = Depends(db_manager.get_db)):
    try:
        response = db.get_users_by_name_and_email(users_table, name, email)
    except ValueError as e:
        response = str(e)
    return response


@router.post("/api/update_user/{user_id}")
async def update_user(user_id: str, name: str = Body(...), email: str = Body(...), db: SQLDB = Depends(db_manager.get_db)):
    try:
        db_manager.validate_User(name, email)
        db.update_record(users_table, user_id, new_values={
                         "name": name, "email": email})
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://localhost:5000/api/get_user/{user_id}",
                timeout=10
            ) as resp:
                user = await resp.json()
        return user
    except ValueError as e:
        return templates.TemplateResponse("update_user.html", {"user_id": user_id, "error": str(e)})


@router.delete("/api/delete_user/{user_id}")
def update_user(user_id: int, db: SQLDB = Depends(db_manager.get_db)):
    try:
        user = db.get_user(users_table, user_id)
        db.delete_record(users_table, user_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/all_users")
async def all_users(db: SQLDB = Depends(db_manager.get_db)):
    try:
        users = db.get_all_users(users_table)
        return users
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
