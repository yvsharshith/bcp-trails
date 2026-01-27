from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import get_connection
from fastapi import Form
from fastapi.responses import RedirectResponse
from fastapi import UploadFile, File
import shutil
import os
import uuid

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# get admin page
@router.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    return templates.TemplateResponse(
        "admin.html",
        {"request": request}
    )


# add details functionality
@router.post("/admin/add", response_class=HTMLResponse)
def add_property(
    title: str = Form(...),
    location: str = Form(...),
    price: str = Form(...),
    description: str = Form(None),
    image: UploadFile = File(...)
):
    upload_dir = "static/uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_ext = image.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = f"{upload_dir}/{filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO properties (title, location, price, description, image)
        VALUES (%s, %s, %s, %s, %s)
    """, (title, location, price, description, file_path))

    conn.commit()
    cur.close()
    conn.close()

    return RedirectResponse(url="/admin", status_code=303)


# delete property functionality
@router.post("/admin/delete", response_class=HTMLResponse)
def delete_property(property_id: int = Form(...)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM properties WHERE id = %s", (property_id,))
    conn.commit()

    cur.close()
    conn.close()

    return RedirectResponse(url="/admin", status_code=303)


# lead-form submission function
@router.post("/leads/submit", response_class=HTMLResponse)
def submit_lead(
    name: str = Form(...),
    mobile: str = Form(...),
    location: str = Form(...),
    interest_type: str = Form(...)
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO leads (name, mobile, location, interest_type)
        VALUES (%s, %s, %s, %s)
    """, (name, mobile, location, interest_type))

    conn.commit()
    cur.close()
    conn.close()

    return RedirectResponse(url="/", status_code=303)


# get lead-form responses
@router.get("/admin/leads", response_class=HTMLResponse)
def view_leads(request: Request):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, mobile, location, interest_type, created_at
        FROM leads
        ORDER BY created_at DESC
    """)

    leads = cur.fetchall()

    cur.close()
    conn.close()

    return templates.TemplateResponse(
        "admin_leads.html",
        {
            "request": request,
            "leads": leads
        }
    )
