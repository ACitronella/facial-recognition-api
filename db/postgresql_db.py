import numpy as np
import numpy.typing as npt
import psycopg2
from .db import DB

class PostgresDB(DB):
    def __init__(self) -> None:
        super().__init__()

    def load_known_ids(self) -> tuple[list[str], list[npt.NDArray]]:
        ids = []
        vecs = []
        connection = cursor = None
        try:
            connection = psycopg2.connect(self.database_url)
            cursor = connection.cursor()

            # query
            cursor.execute('SELECT "studentId", "faceId" FROM attendance."StudentFace";')
            while (row:=cursor.fetchone()) != None:
                id, vec = row
                ids.append(id)
                vecs.append(np.asarray(vec))

        except (Exception, psycopg2.Error) as error:
            print("Error in load know faces", error)
        finally:
            # closing database connection.
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        assert len(ids) == len(vecs)
        return (ids, vecs)

    def register_one(self, id: str, vec: npt.NDArray) -> bool:
        success = True
        connection = cursor = None
        try:
            connection = psycopg2.connect(self.database_url)
            cursor = connection.cursor()
            
            cursor.execute('INSERT INTO attendance."StudentFace" ("studentId", "faceId") VALUES (%s, %s);', (id, list(vec)))
            connection.commit()
        except (Exception, psycopg2.Error) as error:
            print("Error in adding new faces in db", error)
            success = False
        finally:
            # closing database connection.
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return success

    def register_many(self, ids: list[str], vecs:list[npt.NDArray]) -> list[bool]:
        return [self.register_one(id, vec) for id, vec in zip(ids, vecs)] # i dont think that we should use this, implement it just in case

if __name__ == "__main__":
    print(PostgresDB().load_known_ids())