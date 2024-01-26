from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

from sqlalchemy import BIGINT, VARCHAR, TIMESTAMP, ForeignKey, func, INTEGER, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, declared_attr


class Base(DeclarativeBase):
    pass


# Mixin: 여러 테이블에 공통으로 들어갈 columns를 정의하기 위한 용도로 쓴다
# created_at, updated_at 같은 거
class TimestampMixin:
    # default values. server_default에 Object or function를 파라미터로 넣어줘야 한다. 여기서는 sqlalchemy에서 제공하는 functions 중 now()를 사용함.
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())


class TableNameMixin:
    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower() + "s"


# for repeating columns
int_pk = Annotated[int, mapped_column(INTEGER, primary_key=True)]
# for foreign key
# ForeignKey 항목에 string 대신 User.telegram_id 넣는 식의 문법도 동작은 하는데,
# self-reference 예시라 여기서는 쓰지 않았다. string 넣을 거면 __tablename__ 정의한 것과 같아야 함.
# not nullable 설정하려면 Optional 타입을 정의부에 추가해도 된다.
user_fk = Annotated[int, mapped_column(BIGINT, ForeignKey("users.telegram_id", ondelete="SET NULL"))]
str_255 = Annotated[str, mapped_column(VARCHAR(255))]


class User(Base, TimestampMixin, TableNameMixin):
    # sqlalchemy 2.0 버전부터는 mapped_column()을 사용하는 것을 권장.
    # mapped_columns 함수의 파라미터로 sql 타입과 동일한 모듈 사용 (BIGINT, VARCHAR...)
    # -> Mapped[type] 만 써도 되긴 하는데, 디테일한 설정하려면 mapped_columns 메소드를 써야 함.
    telegram_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    full_name: Mapped[str_255]
    # null constraint: nullable=True
    username: Mapped[Optional[str_255]]
    language_code: Mapped[str_255]

    referrer_id: Mapped[Optional[user_fk]]

    # id로 reference만 넣는 대신, object 간 relation을 직접 정의할 수도 있다
    # referrer: relationship("User")


### many to many relationship
"""
CREATE TABLE products
(
    product_id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEST,
    created_at TIMESTAMP default NOW()
);
"""


class Product(Base, TimestampMixin, TableNameMixin):
    product_id: Mapped[int_pk]
    title: Mapped[str_255]
    description: Mapped[Optional[str_255]]


"""
CREATE TABLE orders
(
    order_id INTEGER PRIMARY KEY,
    user_id BIGINT NOT NULL,
    created_at TIMESTAMP default NOW(),
    FOREIGN KEY (user_id)
        REFERENCES users (telegram_id)
        ON DELETE CASCADE 
        # user 삭제 시 order도 삭제
);
"""


class Order(Base, TimestampMixin, TableNameMixin):
    order_id: Mapped[int_pk]
    user_id: Mapped[user_fk]


"""
CREATE TABLE order_products 
(
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (order_id)
        REFERENCES orders (order_id)
        on delete CASCADE
    FOREIGN KEY (product_id)
        References products (product_id)
        on delete CASCADE
);
"""


class OrderProduct(Base, TableNameMixin):
    order_id: Mapped[int] = mapped_column(
        INTEGER, ForeignKey("orders.order_id", ondelete="CASCADE"), primary_key=True
    )
    product_id: Mapped[int_pk] = mapped_column(
        INTEGER, ForeignKey("products.product_id", ondelete="RESTRICT"), primary_key=True
    )
    quantity: Mapped[int]

    # access the related product more easily.
    order = relationship("Order", back_populates="order_products")
    product = relationship("Product", back_populates="order_products")
