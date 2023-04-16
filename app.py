from fastapi import FastAPI, File, UploadFile
from io import BytesIO
from PIL import Image
import numpy as np
from people import PeopleCollection
from util import locate_faces_in_image
from typing import Union
# from torchvision.transforms import functional as F
# import model as M
people = PeopleCollection(ids=[], imgs=[])
app = FastAPI()

@app.post("/face_registeration")
async def face_registeration(id:str, file: UploadFile = File(...)):
    contents = await file.read() # <-- Important!
    img = Image.open(BytesIO(contents))
    img = np.array(img)
    img_h, img_w, _ = img.shape
    try:
        face_locations = locate_faces_in_image(img)
        y0, x0, y1, x1 = face_locations[0]
        x_min, x_max = (x0, x1) if x0 < x1 else (x1, x0)
        y_min, y_max = (y0, y1) if y0 < y1 else (y1, y0)
        y_min, y_max, x_min, x_max = max(y_min-100, 0), min(y_max+100, img_h), max(x_min-100, 0), min(x_max+100, img_w)
        people.add_new_faces([id], [img[y_min:y_max, x_min:x_max]])
    except AssertionError:
        return "face registeration failed, maybe try put a image with only a face"
    return "Success, '%s' was registered. a face was located around (%d, %d), (%d, %d)" % (id, x_min, y_min, x_max, y_max)

@app.post("/face_recognition")
async def face_recognition(file: UploadFile = File(...)) -> Union[list, str]:
    contents = await file.read() # <-- Important!
    img = Image.open(BytesIO(contents))
    img = np.array(img)
    img_h, img_w, _ = img.shape
    face_locations = locate_faces_in_image(img)
    face_location_with_names = []
    try:
        for y0, x0, y1, x1 in face_locations:
            x_min, x_max = (x0, x1) if x0 < x1 else (x1, x0)
            y_min, y_max = (y0, y1) if y0 < y1 else (y1, y0)
            y_min, y_max, x_min, x_max = max(y_min-100, 0), min(y_max+100, img_h), max(x_min-100, 0), min(x_max+100, img_w)
            predicted_ids = people.compare_face_with_registered_faces(img[y_min:y_max, x_min:x_max])
            face_location_with_names.append({"loc": ((x_min, y_min), (x_max, y_max)), 
                                             "id": predicted_ids[0] if predicted_ids else "unknown"})
    except AssertionError as e:
        print(e)
        return "face reconition failed " + str(e) 
    return face_location_with_names
@app.get("/")
def hello_world():
    return "hello world"
