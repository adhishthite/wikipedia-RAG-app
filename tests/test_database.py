import os
from unittest.mock import patch

import pytest
from pymongo.errors import PyMongoError, BulkWriteError


from app.database import MongoDB


@pytest.fixture(scope="class")
def mongo_client(request):
    test_mongo_url = os.environ.get("MONGO_URL")
    mongo_instance = MongoDB(mongo_url=test_mongo_url, database_name="test_db")
    if hasattr(request, "cls"):
        request.cls.mongo = mongo_instance
    yield mongo_instance
    mongo_instance.drop_db('test_db')  # Cleanup: Drop the test database after tests
    mongo_instance.close()


@pytest.mark.usefixtures("mongo_client")
class TestMongoDB:
    mongo: MongoDB

    def test_insert_one(self):
        test_data = {"name": "John Doe"}
        inserted_id = self.mongo.insert_one(test_data)
        assert inserted_id is not None
        found = self.mongo.find_one({"_id": inserted_id})
        assert found["name"] == "John Doe"

    def test_find(self):
        test_data = {"name": "Find Test"}
        self.mongo.insert_one(test_data)
        results = self.mongo.find({"name": "Find Test"})
        assert len(results) > 0
        assert results[0]["name"] == "Find Test"

    def test_update_one(self):
        test_data = {"name": "Update Test"}
        inserted_id = self.mongo.insert_one(test_data)
        self.mongo.update_one({"_id": inserted_id}, {"$set": {"name": "Updated Name"}})
        updated = self.mongo.find_one({"_id": inserted_id})
        assert updated["name"] == "Updated Name"

    def test_delete_one(self):
        test_data = {"name": "Delete Test"}
        inserted_id = self.mongo.insert_one(test_data)
        self.mongo.delete_one({"_id": inserted_id})
        result = self.mongo.find_one({"_id": inserted_id})
        assert result is None

    def test_insert_many(self):
        data_list = [{"name": "Test1"}, {"name": "Test2"}]
        result = self.mongo.insert_many(data_list)
        assert len(result) == 2
        # Verify that the documents are inserted
        assert self.mongo.find({"name": {"$in": ["Test1", "Test2"]}})

    def test_update_many(self):
        # Setup: Insert multiple documents to update
        self.mongo.insert_many([{"category": "update_many_test"}, {"category": "update_many_test"}])
        update_result = self.mongo.update_many({"category": "update_many_test"}, {"$set": {"updated": True}})
        assert update_result > 0
        # Verify that the documents are updated
        updated_docs = self.mongo.find({"category": "update_many_test", "updated": True})
        assert len(updated_docs) > 1

    def test_delete_many(self):
        # Setup: Insert multiple documents to delete
        self.mongo.insert_many([{"category": "delete_many_test"}, {"category": "delete_many_test"}])
        delete_result = self.mongo.delete_many({"category": "delete_many_test"})
        assert delete_result > 0
        # Verify that the documents are deleted
        deleted_docs = self.mongo.find({"category": "delete_many_test"})
        assert len(deleted_docs) == 0

    def test_exception_handling_insert_one(self):
        with patch('pymongo.collection.Collection.insert_one', side_effect=PyMongoError):
            result = self.mongo.insert_one({"name": "Exception Test"})
            assert result is None, "Expected insert_one to handle PyMongoError by returning None"

    def test_exception_handling_insert_many(self):
        with patch('pymongo.collection.Collection.insert_many', side_effect=BulkWriteError({})):
            result = self.mongo.insert_many([{"name": "Exception Test 1"}, {"name": "Exception Test 2"}])
            assert result is None, "Expected insert_many to handle BulkWriteError by returning None"

    def test_exception_handling_find(self):
        with patch('pymongo.collection.Collection.find', side_effect=PyMongoError):
            result = self.mongo.find({"name": "Exception Test"})
            assert result is None, "Expected find to handle PyMongoError by returning None"

    def test_exception_handling_find_one(self):
        with patch('pymongo.collection.Collection.find_one', side_effect=PyMongoError):
            result = self.mongo.find_one({"name": "Exception Test"})
            assert result is None, "Expected find_one to handle PyMongoError by returning None"

    def test_exception_handling_update_one(self):
        with patch('pymongo.collection.Collection.update_one', side_effect=PyMongoError):
            result = self.mongo.update_one({"name": "Original Name"}, {"$set": {"name": "Updated Name"}})
            assert result is None, "Expected update_one to handle PyMongoError by returning None"

    def test_exception_handling_update_many(self):
        with patch('pymongo.collection.Collection.update_many', side_effect=PyMongoError):
            result = self.mongo.update_many({"name": "Original Name"}, {"$set": {"name": "Updated Name"}})
            assert result is None, "Expected update_many to handle PyMongoError by returning None"

    def test_exception_handling_delete_one(self):
        with patch('pymongo.collection.Collection.delete_one', side_effect=PyMongoError):
            result = self.mongo.delete_one({"name": "Delete Test"})
            assert result is None, "Expected delete_one to handle PyMongoError by returning None"

    def test_exception_handling_delete_many(self):
        with patch('pymongo.collection.Collection.delete_many', side_effect=PyMongoError):
            result = self.mongo.delete_many({"name": "Delete Test"})
            assert result is None, "Expected delete_many to handle PyMongoError by returning None"
