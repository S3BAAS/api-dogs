from fastapi import APIRouter, HTTPException, status

from typing import List
from bson import ObjectId
from datetime import datetime

from app.database.models.dog import Dog
from app.database.schemas.dog import dog_schema, dog_list
from app.database.client import client
from app.functions.dog import search_dog, get_dog_image


# --- ROUTER ---
router = APIRouter(
    prefix="/api/dogs",
    responses={404: {"description": "Not found"}},
    tags=["dogs"]
)


# --- ENDPOINTS GET DOGS ---
@router.get("/", response_model=List[Dog])
async def get_dogs():

    if client.dogs.count_documents({}) == 0:
        raise HTTPException(status_code=404, detail="No dogs found")

    return dog_list(client.dogs.find())


@router.get("/is_adopted", response_model=List[Dog])
async def get_dogs_is_adopted():
    """
    Get all dogs that are adopted.

    :return: The dogs.
    """

    dogs = client.dogs.find({"is_adopted": True})

    if client.dogs.count_documents({}) == 0:
        raise HTTPException(status_code=404, detail="No dogs found")

    if not dogs:
        raise HTTPException(status_code=404, detail="No dogs adopted found")

    return dog_list(dogs)


@router.get("/{name}", response_model=Dog)
async def get_dog_by_name(name: str) -> Dog:
    """
    Get a dog by name.

    :param name: The name of the dog.
    :return: The dog.
    """

    dog = search_dog(name)

    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    else:
        return dog


# --- ENDPOINTS POST DOGS ---
@router.post("/{dog_name}", response_model=Dog)
async def post_dog(dog: Dog, dog_name: str) -> Dog:
    """
    Create a new dog.

    :param dog: The dog.
    :param dog_name: The name of the dog.
    :return: The dog.
    """

    search = search_dog(dog_name)
    if search:
        raise HTTPException(
            status_code=409, detail=f"Dog with name {dog_name} already exists")

    dog_dict = dict(dog)
    del dog_dict["id"]
    del dog_dict["picture"]
    del dog_dict["create_date"]

    result = client.dogs.insert_one(dog_dict)
    image_dog = get_dog_image()
    date_time = str(datetime.now())

    client.dogs.update_one(
        {"_id": result.inserted_id},
        {"$set": {
            "picture": image_dog,
            "create_date": date_time
        }}
    )

    new_dog = dog_schema(client.dogs.find_one({"_id": result.inserted_id}))

    return Dog(**new_dog)


# --- ENDPOINTS PUT DOGS ---
@router.put("/{dog_name}", response_model=Dog)
async def put_dog(dog: Dog, dog_name: str) -> Dog:
    """
    Update the information of a dog.

    :param dog: The dog.
    :param dog_name: The name of the dog.
    :return: The dog.
    """

    search = search_dog(dog_name)
    if not search:
        raise HTTPException(status_code=404, detail="Dog not found")

    image_dog = get_dog_image()

    client.dogs.update_one(
        {"_id": ObjectId(search.id)},
        {"$set": {
            "picture": image_dog,
            "name": dog.name,
            "is_adopted": dog.is_adopted
        }}
    )

    update_dog = dog_schema(client.dogs.find_one({"_id": ObjectId(search.id)}))

    return Dog(**update_dog)


# --- ENDPOINTS DELETE DOGS ---
@router.delete("/{dog_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dog(dog_name: str) -> None:
    """
    Delete a dog.

    :param dog_name: The name of the dog.
    :return: None.
    """

    search = search_dog(dog_name)

    if not search:
        raise HTTPException(status_code=404, detail="Dog not found")

    client.dogs.delete_one({"_id": ObjectId(search.id)})

    return None
