## Python Database Mastery: Dive into SQLAlchemy & Alembic

환경
- virtualenv + python 3.11
- Dependency는 requirements.txt 참고
- Postgresql은 docker-compose.yaml 참고

Dependency 간단한 설명
- psycopg2-binary: postgresql을 Python에서 쓰기 위한 것
- asyncpg: DB와의 async connection을 위해 필요함.

### alembic

install

```bash
pip install alembic
```

use
```bash
# python -m alembic init <dirName>
python -m alembic init migrations
```

위 방식은 sync. async 쓰려면 다른 방법 적용해야 함.
- 환경설정 파일은 alembic.ini 가 기본. but 보통은 ini 파일에 직접 넣기보다는 env.py 를 쓴다. 
  - 코드에 직접 DB 설정값을 넣을 필요가 없기 때문.
- 