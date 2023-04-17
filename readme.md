# Facial recognition API

## Run

### Install Dependencies

Requires python 3.9 or above.

```bash
pip install numpy face-recognition fastapi "uvicorn[standard]" chardet requests python-multipart matplotlib
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

### POST /face_registeration

requires
- id: string
- image: file(image)

response with success or failed

### POST /face_recognition

requires
- image: file(image)

response with list of location and id ("unknown" for unknown)