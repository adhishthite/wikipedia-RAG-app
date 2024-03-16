import os
from typing import Optional


import pymongo
from pymongo.errors import BulkWriteError, ConnectionFailure, PyMongoError
from bson import ObjectId


class MongoDB:
    """
    A MongoDB class for managing connections and operations with a MongoDB database.

    Attributes:
        __client (MongoClient): A client connection to the MongoDB server.
        __db (Database): The MongoDB database instance.
        collection (Collection): The MongoDB collection instance.
    """
    def __init__(self, mongo_url: str, database_name: str = "admin", collection_name: str = "admin"):
        """
        Initializes the MongoDB connection using the provided MongoDB URL, database name, and collection name.
        If the mongo_url is not provided, it attempts to retrieve it from the environment variable "MONGO_URL".

        Args:
            mongo_url (str): The MongoDB connection URL.
            database_name (str, optional): The name of the database. Defaults to "admin".
            collection_name (str, optional): The name of the collection. Defaults to "admin".

        Raises:
            Exception: If the connection to MongoDB fails.
        """
        if not mongo_url:
            mongo_url = os.environ.get("MONGO_URL")

        try:
            self.__client = pymongo.MongoClient(
                host=mongo_url,
                serverSelectionTimeoutMS=5000,
                appname=os.getenv("SERVICE_NAME", "flask-app-template"),
                connect=True
            )

            self.__db = self.__client[database_name]
            self.collection = self.__db[collection_name]
        except ConnectionFailure as exc:
            raise Exception(f"Connection to MongoDB failed: {exc}")

    def ping(self) -> dict:
        """
        Pings the MongoDB server

        Returns:
            dict: A dictionary containing the server status.
        """
        return self.__client.admin.command("ping")

    def set_collection(self, collection_name: str) -> None:
        """
        Sets the collection to the specified collection name within the current database.

        Args:
            collection_name (str): The name of the collection to switch to.
        """
        self.collection = self.__db[collection_name]

    def insert_one(self, data) -> Optional[ObjectId]:
        """
        Inserts a single document into the collection.

        Args:
            data (dict): The document to insert.

        Returns:
            ObjectId or None: The ObjectId of the inserted document, or None if insertion fails.
        """
        try:
            result = self.collection.insert_one(data)
            return result.inserted_id
        except PyMongoError as exc:
            print(f"Insert failed: {exc}")
            return None

    def insert_many(self, data_list) -> Optional[list[ObjectId]]:
        """
        Inserts multiple documents into the collection.

        Args:
            data_list (list): A list of documents to insert.

        Returns:
            list or None: A list of ObjectIds of the inserted documents, or None if insertion fails.
        """
        try:
            result = self.collection.insert_many(data_list)
            return result.inserted_ids
        except BulkWriteError as exc:
            print(f"Bulk insert failed: {exc}")
            return None

    def find(self, query) -> Optional[list[dict]]:
        """
        Finds documents in the collection matching the query.

        Args:
            query (dict): The query criteria to apply.

        Returns:
            list or None: A list of matching documents, or None if the query fails.
        """
        try:
            return list(self.collection.find(query))
        except PyMongoError as exc:
            print(f"Query failed: {exc}")
            return None

    def find_one(self, query) -> Optional[dict]:
        """
       Finds a single document in the collection matching the query.

       Args:
           query (dict): The query criteria to apply.

       Returns:
           dict or None: The first document matching the query, or None if the query fails.
       """
        try:
            return self.collection.find_one(query)
        except PyMongoError as exc:
            print(f"Query failed: {exc}")
            return None

    def update_one(self, query, update) -> Optional[int]:
        """
       Updates a single document in the collection matching the query.

       Args:
           query (dict): The query criteria for the document to update.
           update (dict): The update operations to apply.

       Returns:
           int or None: The count of documents modified, or None if the update fails.
       """
        try:
            result = self.collection.update_one(query, update)
            return result.modified_count
        except pymongo.errors.PyMongoError as exc:
            print(f"Update failed: {exc}")
            return None

    def update_many(self, query, update) -> Optional[int]:
        """
        Updates multiple documents in the collection matching the query.

        Args:
            query (dict): The query criteria for the documents to update.
            update (dict): The update operations to apply.

        Returns:
            int or None: The count of documents modified, or None if the update fails.
        """
        try:
            result = self.collection.update_many(query, update)
            return result.modified_count
        except pymongo.errors.PyMongoError as exc:
            print(f"Update failed: {exc}")
            return None

    def delete_one(self, query) -> Optional[int]:
        """
        Deletes a single document from the collection matching the query.

        Args:
            query (dict): The query criteria for the document to delete.

        Returns:
            int or None: The count of documents deleted, or None if the delete operation fails.
        """
        try:
            result = self.collection.delete_one(query)
            return result.deleted_count
        except pymongo.errors.PyMongoError as exc:
            print(f"Delete failed: {exc}")
            return None

    def delete_many(self, query) -> Optional[int]:
        """
        Deletes multiple documents from the collection matching the query.

        Args:
            query (dict): The query criteria for the documents to delete.

        Returns:
            int or None: The count of documents deleted, or None if the delete operation fails.
        """
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except pymongo.errors.PyMongoError as exc:
            print(f"Delete failed: {exc}")
            return None

    def close(self) -> None:
        """
        Closes the MongoDB client connection.
        """
        self.__client.close()

    def drop_db(self, db_name) -> None:
        """
        Drops the specified database from the MongoDB server.

        Args:
            db_name (str): The name of the database to drop.
        """
        self.__client.drop_database(db_name)
