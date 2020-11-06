from Bot import MONGO_CLIENT
from bson.objectid import ObjectId
from typing import Optional

collection = MONGO_CLIENT["Chizuru"]["Users"]
chats_collection = MONGO_CLIENT["Chizuru"]["Chats"]


def does_user_exist(user: int) -> bool:
    if collection.count_documents({"id": user}):
        return True
    return False


def add_user(data: dict) -> Optional[ObjectId]:
    return collection.insert_one(data)


def find_user(user: int) -> Optional[dict]:
    return collection.find_one({"id": user})


def user_count() -> int:
    return collection.count()


def does_chat_exist(chat: int) -> bool:
    if collection.count_documents({"id": chat}):
        return True
    return False


def add_chat(data: dict) -> Optional[ObjectId]:
    return collection.insert_one(data)


def find_chat(chat: int) -> Optional[dict]:
    return collection.find_one({"id": chat})


def chat_count() -> int:
    return collection.count()
