# import fastapi
from fastapi import FastAPI, Form, File, UploadFile
app = FastAPI()

# Create a route
@app.get("/")
def index():
    return {"data": {"api": "textomatic api", "version": "0.1", "author": "Sufiya ansari"}}

# Create a route that excepts files from form
@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

# Create a route that excepts files from form
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

# create a api route that summarizes the text str 
@app.get("textomatic/api/v1/summarize")
def summarize_text(text: str = Form(...)):
    return {"data": text}

# create an api route that summarizes the file after getting text from the file
@app.post("/textomatic/api/v1/summarize")
async def summarize_text(file: UploadFile = File(...)):
    return {"filename": file.filename}
     
