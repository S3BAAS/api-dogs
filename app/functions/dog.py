from app.database.client import client
from app.database.models.dog import Dog
from app.database.schemas.dog import dog_schema
import requests


# --- DOG FUNCTIONS ---
def search_dog(name: str) -> Dog | None:
    try:
        dog = client.dogs.find_one({
            "name": name
        })
        return Dog(**dog_schema(dog))
    except:
        return None


url = "https://dog.ceo/api/breeds/image/random"


def get_dog_image() -> str | None:
    response = requests.get(url)

    if response.status_code == 200:
        return str(response.json().get("message"))
    else:
        return None