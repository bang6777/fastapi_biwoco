# app/users/adapter/repository.py

from typing import Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from app.users.domain.entity.user import User  # Your User Pydantic model

from core.db.database import Database

class UserRepository:
    def __init__(self):
        self.user_collection = Database.get_collection("users")

    async def find_by_id(self, user_id: str) -> Optional[User]:
        """Fetch a user by their ID."""
        if not ObjectId.is_valid(user_id):
            return None
        user_data = await self.user_collection.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return {
                "email": user_data.get("email"),
                "_id": str(user_data.get("_id")),
                "is_active": user_data.get("is_active"),
                "is_admin": user_data.get("is_admin"),
            }
        return None

    async def find_by_email(self, email: str) -> Optional[User]:
        """Fetch a user by their email."""
        user_data = await self.user_collection.find_one({"email": email})
        if user_data:
            return {
                "email": user_data.get("email"),
                "_id": str(user_data.get("_id")),
                "is_active": user_data.get("is_active"),
                "is_admin": user_data.get("is_admin"),
                "password": user_data.get("password"),
            }
        return None

    async def create_user(self, user_data: dict) -> User:
        """Insert a new user document into the collection."""
        result = await self.user_collection.insert_one(user_data)
        new_user = await self.find_by_id(str(result.inserted_id))
        return new_user

    async def update_user(self, user_id: str, update_data: dict) -> Optional[User]:
        """Update a user document."""
        if not ObjectId.is_valid(user_id):
            return None
        await self.user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        updated_user = await self.find_by_id(user_id)
        return updated_user

    async def delete_user(self, user_id: str) -> bool:
        """Delete a user document."""
        if not ObjectId.is_valid(user_id):
            return False
        result = await self.user_collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count == 1