# CRUD_Python_Module.py

from typing import Any, Dict, List, Optional
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import urllib.parse


class AnimalShelter:
    """CRUD operations for the AAC 'animals' collection in MongoDB."""

    def __init__(
        self,
        user: str,
        password: str,
        host: str = "localhost",
        port: int = 27017,
        db: str = "aac",
        col: str = "animals",
    ):
        # URL-encode in case the password has special chars
        user_enc = urllib.parse.quote_plus(user)
        pass_enc = urllib.parse.quote_plus(password)

        uri = (
            f"mongodb://{user_enc}:{pass_enc}@{host}:{port}"
            f"/?authSource=admin&serverSelectionTimeoutMS=5000"
        )
        self.client = MongoClient(uri)
        self.database = self.client[db]
        self.collection = self.database[col]

    # CREATE
    def create(self, data: Dict[str, Any]) -> bool:
        """
        Insert a document. Return True if successful else False.
        """
        try:
            if not isinstance(data, dict) or not data:
                return False
            result = self.collection.insert_one(data)
            return bool(result.acknowledged)
        except PyMongoError as e:
            print(f"[CREATE ERROR] {e}")
            return False

    # READ
    def read(self, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Find documents matching query. Return list of docs.
        """
        try:
            cursor = self.collection.find(query or {})
            return list(cursor)
        except PyMongoError as e:
            print(f"[READ ERROR] {e}")
            return []

    # UPDATE
    def update(
        self,
        query: Dict[str, Any],
        new_values: Dict[str, Any],
        many: bool = False,
    ) -> int:
        """
        Update one or many documents using a MongoDB update document
        . Return the number of modified docs.
        """
        try:
            if many:
                result = self.collection.update_many(query, new_values)
            else:
                result = self.collection.update_one(query, new_values)
            return int(result.modified_count)
        except PyMongoError as e:
            print(f"[UPDATE ERROR] {e}")
            return 0

    # DELETE
    def delete(self, query: Dict[str, Any], many: bool = False) -> int:
        """
        Delete one or many documents matching query.
        Return the number of deleted docs.
        """
        try:
            if many:
                result = self.collection.delete_many(query)
            else:
                result = self.collection.delete_one(query)
            return int(result.deleted_count)
        except PyMongoError as e:
            print(f"[DELETE ERROR] {e}")
            return 0