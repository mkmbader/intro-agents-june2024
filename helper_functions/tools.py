from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import StructuredTool
from langchain_community.utilities import WikipediaAPIWrapper
import requests
from helper_functions.keys import WEATHER_KEY, OPENAI_KEY

WIKI_API_WRAPPER = WikipediaAPIWrapper(top_k_results=1)

##### Wikipedia tool #####
def wikipedia_caller(query:str) ->str:
    """This function queries wikipedia through a search query."""
    return WIKI_API_WRAPPER.run(query)

# Input parameter definition
class QueryInput(BaseModel):
    query: str = Field(description="Input search query")

# the tool description
description: str = (
        "A wrapper around Wikipedia. "
        "Useful for when you need to answer general questions about "
        "people, places, companies, facts, historical events, or other subjects. "
        "Input should be a search query."
    )

# fuse the function, input parameters and description into a tool. 
my_own_wiki_tool = StructuredTool.from_function(
    func=wikipedia_caller,
    name="wikipedia",
    description=description,
    args_schema=QueryInput,
    return_direct=False,
)


##### Weather tool #####
def extract_city_weather(city:str)->str:
    api_key = 'ZHK4HRAZ3MTNV5FDNQKFYUGL7'

    # Build the API URL
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={api_key}&unitGroup=metric"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        current_temp = data['days'][0]['temp']
        output = f"Current temperature in {city}: {current_temp}°C"
    else:
        output = f"Error: {response.status_code}"

    return output

# Input parameter definition
class WeatherInput(BaseModel):
    city: str = Field(description="City name")


# the tool description
description: str = (
        "Allows to extract the current temperature in a specific city"
    )

# fuse the function, input parameters and description into a tool. 
weather_tool = StructuredTool.from_function(
    func=extract_city_weather,
    name="weather",
    description=description,
    args_schema=WeatherInput,
    return_direct=False,
)
