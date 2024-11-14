from motor.motor_asyncio import AsyncIOMotorClient
from core.config import config

class Database:
    client: AsyncIOMotorClient = None

    @classmethod
    def connect(cls):
        cls.client = AsyncIOMotorClient(config.MONGO_URI)
        return cls.client

    @classmethod
    def get_database(cls):
        return cls.client.get_database(config.MONGO_DATABASE)
    
    @classmethod
    def get_collection(cls, collection_name: str):
        """Retrieve the users collection within the database."""
        if cls.client is None:
            cls.connect()
        db = cls.get_database()
        return db[collection_name]

    @classmethod
    async def setup_indexes(cls):
        db = cls.get_database()
        # strategies index for user collection
        users_collection = db["users"]
        await users_collection.create_index("email", unique=True)
        await users_collection.create_index([("name", 1)])
        # add more indexes here

    @classmethod
    async def close(cls):
        cls.client.close()
