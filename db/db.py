import numpy.typing as npt
from setting import DATABASE_URL

# base class with embedded db url
class DB:
    def __init__(self) -> None:
        self.database_url = DATABASE_URL
    def load_known_ids(self) -> tuple[list[str], list[npt.NDArray]]:
        raise NotImplementedError() 
    def register_one(self, ids: str, vecs: npt.NDArray) -> bool:
        raise NotImplementedError() 
    def register_many(self, ids: list[str], vecs: list[npt.NDArray]) -> bool:
        raise NotImplementedError() 
