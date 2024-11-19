import os
import pyodbc
from models import db, Pet

def import_access_data():
    access_file = 'E-Pets_Erika Sanders.accdb'
    if not os.path.exists(access_file):
        print(f"Access file {access_file} not found.")
        return

    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=' + access_file + ';'
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Pets")
        rows = cursor.fetchall()

        for row in rows:
            pet = Pet(
                name=row.Name,
                species=row.Species,
                breed=row.Breed,
                age=row.Age,
                gender=row.Gender,
                color=row.Color
            )
            db.session.add(pet)

        db.session.commit()
        print("Data imported successfully")

    except pyodbc.Error as e:
        print(f"Error importing data: {str(e)}")

    finally:
        if 'conn' in locals():
            conn.close()
