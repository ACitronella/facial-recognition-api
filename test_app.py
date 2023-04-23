import matplotlib.pyplot as plt
from people import PeopleCollection
from pathlib import Path
from util import image_reader, locate_faces_in_image

dataset_path = Path("datasets/bidenDataset") 

print("read image")
known_image = image_reader(dataset_path / "biden.webp")


print("creating collection of every people we want to compare")
people = PeopleCollection()

# load a group image
group_image = image_reader(dataset_path / "biden group 2.jpg")
face_locations = locate_faces_in_image(group_image)
print("all face locations in the image, bounding box [(y0, x0, y1, x1), ...]", face_locations) 

img_h, img_w, img_c = group_image.shape
num_faces = len(face_locations)
fig = plt.figure()
for idx, (y0, x0, y1, x1) in enumerate(face_locations, start=1):
    x_min, x_max = (x0, x1) if x0 < x1 else (x1, x0)
    y_min, y_max = (y0, y1) if y0 < y1 else (y1, y0)
    y_min, y_max, x_min, x_max = max(y_min-100, 0), min(y_max+100, img_h), max(x_min-100, 0), min(x_max+100, img_w)
    aface = group_image[y_min:y_max, x_min:x_max].copy()
    ax = fig.add_subplot(1, num_faces, idx)
    ax.axis("off")
    ax.imshow(aface)
    ids = people.compare_face_with_registered_faces(aface)
    title = "unknown"
    if ids:
        title = ids[0]
    ax.set_title(title)
plt.show()
