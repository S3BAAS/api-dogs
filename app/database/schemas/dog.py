def dog_schema(dog) -> dict:
    return {
        "id": str(dog["_id"]),
        "name": dog["name"],
        "picture": dog["picture"],
        "create_date": dog["create_date"],
        "is_adopted": dog["is_adopted"]
    }


def dog_list(dogs) -> list:
    return [dog_schema(dog) for dog in dogs]
