# Facial recognition API

## Run

### Install Dependencies

Requires python 3.9 or above.

```bash
pip install -r requirements.txt
pip install python-dotenv # for test_app.py, not required
```

`face-recognition` also require CMake to install.

```bash
winget install cmake
brew install cmake
```

more detail for windows in [face-recognition's github issue](https://github.com/ageitgey/face_recognition/issues/175#issue-257710508).

### Run server

```bash
uvicorn app:app --host 0.0.0.0 --reload
```

### Run test

For sanity check. Load biden dataset from [this](https://drive.google.com/drive/folders/1BtC5S1ZBDgm2QXzBwBpsV7b6vNsKV3wC?usp=share_link).

```bash
python test_app.py
```

## Routes

### GET /

response with "hello world"

### POST /face_registration

requires
- id: string
- image: file(image)

response prototype
```json
{
    "success": boolean,
    "id": string or null,
    "message": string
}

```

### POST /face_recognition

requires
- image: file(image)

response prototype
```json
{
    "success": boolean,
    "found_faces": [ // might be empty list or has more than 1 elem
        {
            "loc": ((x_min, y_min), (x_max, y_max)), // face location in the image as int
            "id": string
        },
        ...
    ],
    "message": string
}
```