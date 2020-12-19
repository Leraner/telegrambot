from aiogram import types, Bot
from gino import Gino
from sqlalchemy import (
    Column, Integer, BigInteger, String, Sequence, TIMESTAMP, Boolean, JSON
)
from sqlalchemy import sql
from gino.schema import GinoSchemaVisitor

from .config import db_user, db_pass, host
import datetime

db = Gino()


# TODO: вынести модели в models.py
class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, unique=True)
    user_id = Column(BigInteger)
    full_name = Column(String(100))
    username = Column(String(100))
    query: sql.Select


class Order(db.Model):
    """Order model"""
    __tablename__ = 'orders'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, unique=True)
    full_user_name = Column(String(100))
    buyer_id = Column(BigInteger)
    shoes_count = Column(Integer)
    created_date = Column(TIMESTAMP)
    address = Column(String(100))
    # TODO: добавить номер телефона, статус покупки (оплачена или нет)
    query: sql.Select


class DBCommands:
    async def get_user(self, user_id) -> User:
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    async def add_new_user(self):
        user = types.User.get_current()
        old_user = await self.get_user(user.id)
        if old_user:
            return old_user
        new_user = User()
        new_user.user_id = user.id
        new_user.username = user.username
        new_user.full_name = user.full_name

        await new_user.create()
        return new_user

    async def add_new_order(self, count, address) -> Order:
        user = types.User.get_current()

        new_order = Order()
        new_order.full_user_name = user.full_name
        new_order.buyer_id = user.id
        new_order.shoes_count = count
        new_order.address = address
        new_order.created_date = datetime.datetime.strptime(
            datetime.datetime.now().strftime("%Y/%m/%d %H:%M"),
            "%Y/%m/%d %H:%M")
        await new_order.create()
        return new_order

    async def show_orders(self):
        orders = await Order.query.gino.all()
        return orders


async def create_db():
    await db.set_bind(f'postgresql://{db_user}:{db_pass}@{host}/gino')
    db.gino: GinoSchemaVisitor
    await db.gino.drop_all()
    await db.gino.create_all()
