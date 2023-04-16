import numpy as np
from pathlib import Path
from PIL import Image
from typing import Union
import face_recognition

def image_reader(img_path: Union[str, Path]) -> np.ndarray:
    return np.array(Image.open(img_path))

def locate_faces_in_image(img: np.ndarray) -> list[tuple[int, int, int, int]]:
    return face_recognition.face_locations(img)
    