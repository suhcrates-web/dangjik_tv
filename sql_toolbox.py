from database import db, cursor
import mysql.connector

def time_checker(what0):
    config = {
        'user': 'root',
        'password': 'Seoseoseo7!',
        'host': 'localhost',
        # 'database':'shit',
        'port': '3306'
    }

    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    cursor.execute(
        f"""
        select date0 from dangbun_stuffs.brods where brod="{what0}"
        """
    )
    time0 = cursor.fetchall()[0][0]
    return time0