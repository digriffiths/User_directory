from fastapi import HTTPException
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from ..models import users_table
from fastapi.templating import Jinja2Templates
from ..services.DatabaseManager import DatabaseManager
import aiohttp
import requests

router = APIRouter()
templates = Jinja2Templates("templates")
db_manager = DatabaseManager(
    "postgres", "postgres", "db", "5432", "fast_api_db", [users_table])


@router.get("/")
def read_form(request: Request):
    return templates.TemplateResponse("add_user.html", {"request": request})


@router.post("/add_user")
async def add_user(request: Request, name: str = Form(...), email: str = Form(...)):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:5000/api/add_user",
                json={"name": name,
                      "email": email},
                timeout=10
            ) as resp:
                data = await resp.json()
                # assuming the response data contains 'user_id'
                user_id = data.get('user_id')
                response = RedirectResponse(
                    url=f"/get_user/{user_id}", status_code=303)
    except requests.exceptions.RequestException as e:
        response = templates.TemplateResponse(
            "add_user.html", {"request": request, "error": str(e)})

    return response


@router.get("/get_user/{user_id}")
async def get_users(request: Request):
    try:
        user_id = request.path_params['user_id']
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://localhost:5000/api/get_user/{user_id}",
                timeout=10
            ) as resp:
                user = await resp.json()
                return templates.TemplateResponse("get_user.html", {"request": request, "users": [user]})
    except requests.exceptions.RequestException as e:
        response = templates.TemplateResponse(
            "add_user.html", {"request": request, "error": str(e)})

    return response


@router.get("/find_user")
def find_user(request: Request):
    return templates.TemplateResponse("find_user.html", {"request": request})


@router.post("/find_user")
async def find_user(request: Request, name: str = Form(None), email: str = Form(None)):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:5000/api/find_user",
                json={"name": name,
                      "email": email},
                timeout=10
            ) as resp:
                users = await resp.json()
                return templates.TemplateResponse("get_user.html", {"request": request, "users": users})
    except requests.exceptions.RequestException as e:
        response = templates.TemplateResponse(
            "find_user.html", {"request": request, "error": str(e)})
    return response


@router.get("/update_user/{user_id}")
def update_user(user_id: str, request: Request):
    try:
        return templates.TemplateResponse("update_user.html", {"request": request, "user_id": user_id})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/update_user/{user_id}")
async def update_user(request: Request, user_id: str, name: str = Form(...), email: str = Form(...)):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"http://localhost:5000/api/update_user/{user_id}",
                json={"name": name,
                      "email": email},
                timeout=10
            ) as resp:
                updated_user = await resp.json()
        return templates.TemplateResponse("get_user.html", {"request": request, "users": [updated_user]})
    except ValueError as e:
        return templates.TemplateResponse("update_user.html", {"request": request, "user_id": user_id, "error": str(e)})


@router.get("/delete_user/{user_id}")
async def delete_user(user_id: str, request: Request):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"http://localhost:5000/api/delete_user/{user_id}",
                timeout=10
            ) as resp:
                deleted_user = await resp.json()
        return templates.TemplateResponse("deleted_user.html", {"request": request, "users": [deleted_user]})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all_users")
async def all_users(request: Request):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "http://localhost:5000/api/all_users",
                timeout=10
            ) as resp:
                users = await resp.json()
        return templates.TemplateResponse("get_user.html", {"request": request, "users": users})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
