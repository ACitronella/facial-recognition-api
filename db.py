import numpy as np
import numpy.typing as npt
import psycopg2
import re

from setting import DATABASE_URL

p = re.compile("postgresql://(.*):(.*)@(.*):(.*)/.*").match(DATABASE_URL)

pg_connection_dict = {
    'user': p[1],
    'password': p[2],
    'host': p[3],
    'port': p[4],
}


def load_known_ids() -> tuple[list[str], list[npt.NDArray]]:
    connection = cursor = None
    ids = []
    vecs = []
    try:
        pg_connection_dict["dbname"] = "StudentFace"
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()

        # query
        cursor.execute('SELECT "studentId", "faceId" FROM attendance."StudentFace";')
        while (row:=cursor.fetchone()) != None:
            id, vec = row
            print(id, vec, type(vec))
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
    assert ids == vecs
    return (ids, vecs)

if __name__ == "__main__":
    print(load_known_ids())