from database import db, cursor

cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS dangbun_stuffs.brods(
        brod varchar(10) PRIMARY KEY,
        date0 timestamp,
        content blob
        );
        """
    )