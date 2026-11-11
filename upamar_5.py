
from fastapi import FastAPI, UploadFile, File, HTTPException
import uvicorn
import os
from fastapi.responses import FileResponse


app = FastAPI(title="Upamar - 5")

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok = True)

@app.post("/upload/")
async def uploadedfile(upload_file : UploadFile = File(...)):
	filename = upload_file.filename
	data = await upload_file.read()

	file_location = os.path.join(UPLOAD_DIR, filename)

	with open(file_location, "wb") as f:
		f.write(data)

	return {"message" : "ok upload", "filename" : filename}

@app.post("/multiple_upload/")
async def uploadedmultiplefile(upload_files : list[UploadFile] = File(...)):
	saved_files_info = []

	for upload_file in upload_files:
		filename = upload_file.filename
		data = await upload_file.read()

		file_location = os.path.join(UPLOAD_DIR, filename)

		with open(file_location, "wb") as f:
			f.write(data)

		saved_files_info.append({"filename" : filename})

	return {"message" : "ok upload", "count" : len(saved_files_info)}

@app.get("/files/{filename}/")
async def get_file(filename : str):
	file_path = os.path.join(UPLOAD_DIR, filename)

	if not os.path.exists(file_path):
		raise HTTPException(status_code = 404, detail="File not found")

	return FileResponse(file_path)

if __name__ == "__main__":
    uvicorn.run("upamar_5:app", host="127.0.0.1", port=8000, reload=True)