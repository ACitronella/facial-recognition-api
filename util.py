import numpy as np
import numpy.typing as npt
from pathlib import Path
from PIL import Image
from typing import Union
import face_recognition

def image_reader(img_path: Union[str, Path]) -> npt.NDArray:
    return np.array(Image.open(img_path))

def locate_faces_in_image(img: np.ndarray) -> list[tuple[int, int, int, int]]:
    return face_recognition.face_locations(img)

def preprocessing_image_pil(img: Image.Image) -> Image.Image: # resize to 500, 500/width * height to speed up the later processes
    scale_ratio = 500/img.width
    img = img.resize((500, int(scale_ratio * img.height)), Image.Resampling.LANCZOS)
    return img