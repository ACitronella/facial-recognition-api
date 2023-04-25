from fastapi import FastAPI, File, UploadFile, Form
from io import BytesIO
from PIL import Image
import numpy as np
from people import PeopleCollection
from util import locate_faces_in_image
from typing import Union, Optional
from db import db

if db:
    ids, features = db.load_known_ids()
    people = PeopleCollection.from_existing_vecs(ids, features)
else:
    people = PeopleCollection()
print("existing ids: ", people.ids)
app = FastAPI()

@app.post("/face_registration")
async def face_registration(id:str = Form(...), file: UploadFile = File(...)) -> dict[str, Union[bool, Optional[str], tuple[tuple[int, int], tuple[int, int]]]]:
    contents = await file.read()
    img = Image.open(BytesIO(contents)).convert("RGB")
    # img = preprocessing_image_pil(img)
    img = np.array(img)
    img_h, img_w, _ = img.shape
    face_locations = locate_faces_in_image(img)
    if len(face_locations) == 0:
        return {"success": False, "id": None, "loc": None, "message": "face not found in the image"} 
    y0, x0, y1, x1 = face_locations[0]
    x_min, x_max = (x0, x1) if x0 < x1 else (x1, x0)
    y_min, y_max = (y0, y1) if y0 < y1 else (y1, y0)
    y_min, y_max, x_min, x_max = max(y_min-100, 0), min(y_max+100, img_h), max(x_min-100, 0), min(x_max+100, img_w)
    try:
        people.add_new_faces([id], [img[y_min:y_max, x_min:x_max]]) # assertion Error
    except AssertionError as e:
        return {"success": False, "id": None, "loc": None, "message": str(e)} 
    return {"success": True, "id": id, "loc": ((x_min, y_min), (x_max, y_max))} 

@app.post("/face_recognition")
async def face_recognition(file: UploadFile = File(...)) -> dict[str, Union[bool, str, list[dict[str, Union[str, tuple[tuple[int, int], tuple[int, int]]]]]]]:
    contents = await file.read() # <-- Important!
    img = Image.open(BytesIO(contents)).convert("RGB")
    # img = preprocessing_image_pil(img)
    img = np.array(img)
    img_h, img_w, _ = img.shape
    face_locations = locate_faces_in_image(img)
    face_location_with_names = []
    try:
        for y0, x0, y1, x1 in face_locations:
            x_min, x_max = (x0, x1) if x0 < x1 else (x1, x0)
            y_min, y_max = (y0, y1) if y0 < y1 else (y1, y0)
            y_min, y_max, x_min, x_max = max(y_min-100, 0), min(y_max+100, img_h), max(x_min-100, 0), min(x_max+100, img_w)
            predicted_id = people.compare_face_with_registered_faces(img[y_min:y_max, x_min:x_max])
            face_location_with_names.append({"loc": ((x_min, y_min), (x_max, y_max)), 
                                             "id": predicted_id if predicted_id else "unknown"})
    except AssertionError as e:
        return {"success": False, "found_faces": [], "message": "face reconition failed " + str(e)} 
    return {"success": True, "found_faces": face_location_with_names, "message": "hopefully face was found here if it exists"}

@app.get("/")
def hello_world():
    return "hello world"
