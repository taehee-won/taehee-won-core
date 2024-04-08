from typing import Any, Final, List, Optional, Dict
from pymongo import MongoClient, ASCENDING, DESCENDING

from ..library.macro import KWARGS


_SYSTEM_DATABASES: Final[List[str]] = ["admin", "config", "local"]


class MongoDB:
    class SortOrder:
        ASCENDING = ASCENDING
        DESCENDING = DESCENDING

    def __init__(self):
        self._client = MongoClient(serverSelectionTimeoutMS=500, connectTimeoutMS=500)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close()

    def __del__(self):
        self._close()

    def _close(self):
        if self._client:
            self._client.close()

    def get_databases(self) -> List[str]:
        return [
            d for d in self._client.list_database_names() if d not in _SYSTEM_DATABASES
        ]

    def get_collections(self, database: str) -> List[str]:
        return [c for c in self._client[database].list_collection_names()]

    def drop_database(self, database: str) -> bool:
        if database in self.get_databases():
            self._client.drop_database(database)
            return True

        else:
            return False

    def drop_collection(self, database: str, collection: str) -> bool:
        if collection in self.get_collections(database):
            self._client[database].drop_collection(collection)
            return True

        else:
            return False

    def get_indexes(self, database: str, collection: str) -> List[str]:
        return [
            field
            for index in self._client[database][collection].list_indexes()
            if not index["name"].startswith("_")
            for field in index["key"].keys()
        ]

    def set_index(
        self,
        database: str,
        collection: str,
        key: str,
        sort: int = SortOrder.ASCENDING,
    ) -> None:
        self._client[database][collection].create_index([(key, sort)], unique=True)

    def drop_index(self, database: str, collection: str, key: str) -> bool:
        for index in self._client[database][collection].list_indexes():
            if key in index["key"]:
                self._client[database][collection].drop_index(index["name"])
                return True

        return False

    def insert(
        self,
        database: str,
        collection: str,
        data: List[Dict[str, Any]],
    ) -> bool:
        if not data:
            return False

        r = self._client[database][collection].insert_many(data)
        return len(r.inserted_ids) == len(data)

    def select(
        self,
        database: str,
        collection: str,
        key: Optional[str] = None,
        value: Optional[Any] = None,
        start: Optional[Any] = None,
        end: Optional[Any] = None,
        count: Optional[int] = None,
    ) -> List:
        cursor = self._client[database][collection].find(
            projection={"_id": False},
            filter=(
                None
                if key is None
                else (
                    {key: value}
                    if value is not None
                    else {key: KWARGS(**{"$gte": start, "$lte": end})}
                )
            ),
        )

        if count is not None:
            cursor = cursor.limit(count)

        if indexes := [
            (field, direction)
            for index in self._client[database][collection].list_indexes()
            if not index["name"].startswith("_")
            for field, direction in index["key"].items()
        ]:
            cursor = cursor.sort(indexes)

        return list(cursor)

    def update(
        self,
        database: str,
        collection: str,
        key: str,
        value: Any,
        element: Dict,
    ) -> bool:
        r = self._client[database][collection].update_one(
            {key: value},
            {"$set": element},
        )
        return r.modified_count > 0
