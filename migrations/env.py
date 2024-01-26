from logging.config import fileConfig

from sqlalchemy import engine_from_config, URL
from sqlalchemy import pool

from alembic import context

# from environs import Env
# env = Env()
# env.read_env('.prod.env') # path 정해서 phase 구분할 수 있다.

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# pw 등은 .env로 정의해두고 환경변수로 받아쓰는 게 낫다. 귀찮으므로 여기선 그냥 진행
url = URL.create(
    drivername="postgresql+psycopg2",
    username="testuser",
    password="testpassword",
    host="localhost",
    port=5432,
    database="testuser",
)

config.set_main_option(
    "sqlalchemy.url",
    url
)

# add your model's MetaData object here
# -> DB table 생성에 쓸 metadata 설정 가능. Base 모델 적용할 수 있다.
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

import lesson_2
target_metadata = lesson_2.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
