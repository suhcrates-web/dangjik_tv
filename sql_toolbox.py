from database import db, cursor


def time_checker(what0):

    cursor.execute(
        f"""
        select date0 from dangbun_stuffs.brods where brod="{what0}"
        """
    )
    time0 = cursor.fetchall()[0][0]
    return time0