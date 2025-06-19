from fastapi import FastAPI, Query
from pydantic import BaseModel
import random
import requests
from bs4 import BeautifulSoup

app = FastAPI()

def get_form_fields(form_url):
    res = requests.get(form_url)
    soup = BeautifulSoup(res.text, "html.parser")
    inputs = soup.find_all("input", {"name": lambda x: x and x.startswith("entry.")})
    return [inp['name'] for inp in inputs]

def submit_form(form_url, field_names):
    form_data = {}
    for name in field_names:
        form_data[name] = random.choice(["Test", "Example", "Demo", "Value"])
    
    form_url = form_url.replace("viewform", "formResponse")
    response = requests.post(form_url, data=form_data)
    return response.status_code

@app.get("/fill-form")
def fill_form(link: str = Query(...), count: int = Query(1)):
    try:
        field_names = get_form_fields(link)
        statuses = []
        for _ in range(count):
            status = submit_form(link, field_names)
            statuses.append(status)
        return {"status": "done", "results": statuses}
    except Exception as e:
        return {"error": str(e)}
