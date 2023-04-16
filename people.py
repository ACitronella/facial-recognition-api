import face_recognition
import numpy as np
class PeopleCollection:
    def __init__(self, ids: list[str], imgs: list[np.ndarray]):
        assert len(ids) == len(imgs)
        self.ids = ids
        self.features = [PeopleCollection.extract_face_encoding_for_registeration(img) for img in imgs]
        self.n = len(ids)
        self.thres = 0.6 # from dlib docs
    def __len__(self):
        return self.n
    def __getitem__(self, idx:int):
        return self.ids[idx], self.features[idx]
    def compare_face_with_registered_faces(self, unknown_image:np.ndarray) -> list[str]:
        """return names of found registered face"""
        unknown_encoding = PeopleCollection.extract_face_encoding_for_registeration(unknown_image)
        face_distances = face_recognition.face_distance(self.features, unknown_encoding) # as distance -> 0, the faces are more similar
        
        id_list = []
        for face_id in np.argsort(face_distances):
            if face_distances[face_id] > self.thres:
                break
            id_list.append(self.ids[face_id])
        return id_list
    def add_new_faces(self, names: list[str], imgs: list[np.ndarray]):
        assert len(names) == len(imgs)
        self.ids.extend(names)
        try:
            self.features.extend([PeopleCollection.extract_face_encoding_for_registeration(img) for img in imgs])
        except AssertionError: # if add failed, make name same length as feature to cutout unregisterable one
            self.ids = self.ids[:len(self.features)]
    @staticmethod
    def extract_face_encoding_for_registeration(img: np.ndarray) -> np.ndarray:
        encodings = face_recognition.face_encodings(img.copy())
        assert len(encodings) == 1
        return encodings[0]
