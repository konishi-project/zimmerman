# Import schemas
from api.main.model.schemas import PostSchema

# Define deserializers
posts_schema = PostSchema(many=True)


def load_info_many(posts):
    info = posts_schema.dump(posts)
    return info


def uniq(a_list):
    encountered = set()
    result = []
    for elem in a_list:
        if elem not in encountered:
            result.append(elem)
        encountered.add(elem)

    return result
