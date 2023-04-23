import face_recognition
import numpy as np
import numpy.typing as npt
from db import db
from typing import Optional

class PeopleCollection:
    def __init__(self):
        self.ids = []
        self.features = []
        self.thres = 0.6 # from dlib docs

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, idx:int):
        return self.ids[idx], self.features[idx]

    def compare_face_with_registered_faces(self, unknown_image:np.ndarray) -> Optional[str]:
        """return names of found registered face"""
        unknown_encoding = PeopleCollection.extract_face_encoding_for_registeration(unknown_image)
        face_distances = face_recognition.face_distance(self.features, unknown_encoding) # as distance -> 0, the faces are more similar

        id_list = []
        for face_idx in np.argsort(face_distances):
            if face_distances[face_idx] > self.thres: break
            id_list.append(self.ids[face_idx])
        predicted_id = id_list[0] if id_list else None
        return predicted_id


    def add_new_faces(self, ids: list[str], imgs: list[npt.NDArray]):
        assert len(ids) == len(imgs)
        for id, img in zip(ids, imgs):
            try:
                vec = PeopleCollection.extract_face_encoding_for_registeration(img) # may raise assert
                if db:
                    insert_sucess = db.register_one(id, vec)
                    assert insert_sucess
                self.ids.append(id)
                self.features.append(vec)
                
            except AssertionError: # if add failed, skip it
                print('face not found in register or add into db failed')

    def add_existing_faces(self, ids: list[str], vecs: list[npt.NDArray]):
        assert len(ids) == len(vecs)
        self.ids.extend(ids)
        self.features.extend(vecs)
        
    @staticmethod
    def extract_face_encoding_for_registeration(img: npt.NDArray) -> npt.NDArray:
        encodings = face_recognition.face_encodings(img.copy())
        assert len(encodings) == 1
        return encodings[0]

    @staticmethod
    def from_existing_vecs(ids: list[str], vecs: list[npt.NDArray]) -> 'PeopleCollection':
        assert len(ids) == len(vecs)
        pc = PeopleCollection()
        pc.add_existing_faces(ids, vecs)
        return pc
        
