from sqlalchemy import create_engine, URL, text
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker

from lesson_2 import Base

# DB와 연결하기 위한 connection engine 생성
# connection string form: driver+postgrsql://user:password@host:port/dbname
url = URL.create(
    drivername="postgresql+psycopg2",
    username="testuser",
    password="testpassword",
    host="localhost",
    port=5432,
    database="testuser",
)

# powering connection. 실제 connection을 만들어주는 건 아니다.
engine = create_engine(
    url, # for connection
    echo=True, # for logging. what happens during our query.
    # future=True : 2.0 버전부터는 default on 이라는 듯
)

# session pool로 application과 DB 간 connection 관리.
# 정확히는, 이 함수도 pool 자체를 만드는 게 아니라 factory를 생성하는 것.
## sessions are designed to serve as a primary point of interaction btwn your app and DB.
## -> 각 session은 본인의 session 내에서 발생하는 managing the state / transaction of object를 관리한다.
## -> 일반적으로 connection pool은 engine에서 관리하고, session은 connection 정보를 connection pool에서 가져온다.
## create engine 한다고 connection pool이 바로 만들어지는 건 아님. lazy allocated as a needed basis.

# connection pool은 limit과 overhead가 있다.
## limit: 얼마까지는 connection pool에서 상시 관리. typical pool size
## overhead: 필요 시 추가로 더 만들 수 있는 connection 개수. 이 connection은 연결이 끝나면 destroy. overhead of connection.
session_pool = sessionmaker(engine)

# session 가져오는 방법은 크게 두 가지.
# 1. 직접 session 할당받아서 호출하고, commit하고, 반납한다
# session = session_pool()
# session.execute()
# session.commit()
# session.close()

# 2. with open 메소드. close는 자동으로 해준다. 앞에 async 붙이면 async로도 동작함.
# with session_pool() as session:
#     # ORM 없이 sql문을 직접 입력하는 방식
#     session.execute(text("""
#         CREATE TABLE users
# (
#     telegram_id   BIGINT PRIMARY KEY,
#     full_name     VARCHAR(255) NOT NULL,
#     username      VARCHAR(255),
#     language_code VARCHAR(255) NOT NULL,
#     created_at    TIMESTAMP DEFAULT NOW(),
#     referrer_id   BIGINT,
#     FOREIGN KEY (referrer_id)
#         REFERENCES users (telegram_id)
#         ON DELETE SET NULL
# );
#     """))
#     session.commit()
#     insert_query = text("""
#     INSERT INTO users (telegram_id, full_name, username, language_code, referrer_id)
#     VALUES (1, 'John Doe', 'johndoe', 'en', NULL),
#               (2, 'Jane Doe', 'janedoe', 'en', 1);
#     """)
#     session.execute(insert_query)
#     session.commit()
#     select_query = text("""
#         SELECT * FROM users;
#     """)
#     result = session.execute(select_query)
#     print(result.all()) # <sqlalchemy.engine.cursor.CursorResult Object>
#     for row in result:
#         print(row) # (1, 'John Doe', 'johndoe', 'en', NULL) ...
#         print(row.telegram_id) # 1
#
#     rows = result.all() # python list로 변환


# async_sessionmaker() -> aync session을 만들 때 사용하는 함수.

# lesson2에서 만든 object -> DB로 생성
# Base 클래스를 상속한 모든 object를 DB table로 매핑한다. DB에 이미 있으면 modify하지 않음.
# 올바른 방법은 아니다. track changes하기엔 적합하지 않음.
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

