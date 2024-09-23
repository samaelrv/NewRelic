import newrelic.agent
import os
from fastapi import FastAPI
import logging
import json
import random

# Initialize New Relic Agent
newrelic.agent.initialize('newrelic.ini')

# List of 10 random restaurant names
restaurant_names = [
    "Tasty Bites",
    "Sizzling Grill",
    "Cafe Savory",
    "Munchies Palace",
    "Spice Junction",
    "Golden Spoon",
    "Flavor Haven",
    "Bistro Bliss",
    "Gourmet Delight",
    "Street Eats"
]

# Function to return a random restaurant name
def get_random_restaurant():
    return random.choice(restaurant_names)

# Create an instance of the FastAPI app
app = FastAPI()
logging.basicConfig(filename='log.txt', level=logging.INFO)

# Define a route for the GET request
@app.get("/")
async def get_hello_world():
    random_number = random.randint(1, 10)
    random_restaurant = get_random_restaurant()
    json_data = {
        "Restaurant_Name": random_restaurant,
        "OrderValue": 100,
        "CardNumber": "525211144" + str(random_number),
        "CardType": "visa"
    }
    logging.info(json.dumps(json_data, indent=2))
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    logging.shutdown()
