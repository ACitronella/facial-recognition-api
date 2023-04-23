import face_recognition
import numpy as np
import numpy.typing as npt
class PeopleCollection:
    def __init__(self):
        self.ids = []
        self.features = []
        self.thres = 0.6 # from dlib docs

    def __len__(self):
        return len(self.ids)

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
        pc = PeopleCollection()
        pc.add_existing_faces(ids, vecs)
        return pc
        
