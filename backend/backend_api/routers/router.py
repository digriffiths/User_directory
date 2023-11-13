from fastapi import HTTPException
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from ...utils.databases import SQLDB
from ..models import users_table
from fastapi.templating import Jinja2Templates
from ..services.DatabaseManager import DatabaseManager
from sqlalchemy import and_

router = APIRouter()
templates = Jinja2Templates("templates")
db_manager = DatabaseManager(
    "postgres", "postgres", "db", "5432", "fast_api_db", [users_table])


@router.get("/")
def read_form(request: Request):
    return templates.TemplateResponse("add_user.html", {"request": request})


@router.post("/add_user")
def add_user(request: Request, name: str = Form(...), email: str = Form(...), db: SQLDB = Depends(db_manager.get_db)):
    try:
        response = None
        db_manager.validate_User(name, email)
        user = users_table(name=name, email=email)
        user_id = db.add_data(user)
        response = RedirectResponse(
            url=f"/get_user/{user_id}", status_code=303)
    except ValueError as e:
        response = templates.TemplateResponse(
            "add_user.html", {"request": request, "error": str(e)})
    return response


@router.get("/get_user/{user_id}")
def get_users(request: Request, db: SQLDB = Depends(db_manager.get_db)):
    try:
        user_id = request.path_params['user_id']
        user = db.get_user(users_table, user_id)
        return templates.TemplateResponse("get_user.html", {"request": request, "users": [user]})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/find_user")
def find_user(request: Request):
    return templates.TemplateResponse("find_user.html", {"request": request})


@router.post("/find_user")
def find_user(request: Request, name: str = Form(None), email: str = Form(None), db: SQLDB = Depends(db_manager.get_db)):
    try:
        users = db.get_users_by_name_and_email(users_table, name, email)
        return templates.TemplateResponse("get_user.html", {"request": request, "users": users})
    except ValueError as e:
        response = templates.TemplateResponse(
            "find_user.html", {"request": request, "error": str(e)})
    return response


@router.get("/update_user/{user_id}")
def update_user(request: Request):
    try:
        user_id = request.path_params['user_id']
        return templates.TemplateResponse("update_user.html", {"request": request, "user_id": user_id})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/update_user/{user_id}")
def update_user(request: Request, name: str = Form(...), email: str = Form(...), db: SQLDB = Depends(db_manager.get_db)):
    try:
        db_manager.validate_User(name, email)
        user_id = request.path_params['user_id']
        db.update_record(users_table, user_id, new_values={
                         "name": name, "email": email})
        return RedirectResponse(
            url=f"/user_updated/{user_id}", status_code=303)
    except ValueError as e:
        user_id = request.path_params['user_id']
        return templates.TemplateResponse("update_user.html", {"request": request, "user_id": user_id, "error": str(e)})


@router.get("/user_updated/{user_id}")
def user_updated(request: Request, db: SQLDB = Depends(db_manager.get_db)):
    try:
        user_id = request.path_params['user_id']
        user = db.get_user(users_table, user_id)
        return templates.TemplateResponse("get_user.html", {"request": request, "users": [user]})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/delete_user/{user_id}")
def update_user(request: Request, db: SQLDB = Depends(db_manager.get_db)):
    try:
        user_id = request.path_params['user_id']
        user = db.get_user(users_table, user_id)
        db.delete_record(users_table, user_id)
        return templates.TemplateResponse("deleted_user.html", {"request": request, "users": [user]})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all_users")
def all_users(request: Request, db: SQLDB = Depends(db_manager.get_db)):
    try:
        users = db.get_all_users(users_table)
        return templates.TemplateResponse("get_user.html", {"request": request, "users": users})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
