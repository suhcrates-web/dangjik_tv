from database import db, cursor

cursor.execute(
    """
    drop table if exists dangbun_stuffs.naver;
    """
)

cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS dangbun_stuffs.naver(
        num int not null auto_increment,
        ind varchar(30),
        time0 timestamp,
        title blob,
        press varchar(30),
        url varchar(200),
        naver_cp boolean,
        good boolean,
        primary key(num, ind)
        );
        """
    )