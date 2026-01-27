from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import get_connection
from fastapi import Form
from fastapi.responses import RedirectResponse
from app.admin import router as admin_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(admin_router)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, location, price, image
        FROM properties
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    properties = []
    for row in rows:
        properties.append({
            "id": row[0],
            "title": row[1],
            "location": row[2],
            "price": row[3],
            "image": row[4]
        })

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "properties": properties}
    )

@app.get("/property/{property_id}", response_class=HTMLResponse)
def property_detail(request: Request, property_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, location, price, description, image
        FROM properties
        WHERE id = %s
    """, (property_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Property not found")

    property_data = {
        "id": row[0],
        "title": row[1],
        "location": row[2],
        "price": row[3],
        "description": row[4],
        "image": row[5]
    }

    return templates.TemplateResponse(
        "property.html",
        {"request": request, "property": property_data}
    )