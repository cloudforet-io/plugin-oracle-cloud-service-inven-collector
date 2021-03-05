from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType, BooleanType


class Tags(Model):
    key = StringType()
    value = StringType()


class Database(Model):
    id = StringType()
    name = StringType()
    tags = ListType(ModelType(Tags), default=[])

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://cloud.oracle.com/db/adb/{self.id}?region={self.region}",
        }