from app import db
from zimmerman.models.user import User
from zimmerman.models.content import Post
from zimmerman.models.schemas import PostSchema

from tests.utils.base import BaseTestCase


class TestPostModel(BaseTestCase):
    def test_schema(self):
        content = "Hemlo World"

        p = Post(content=content)
        p_dump = PostSchema().dump(p)

        self.assertEquals(p_dump["content"], content)
