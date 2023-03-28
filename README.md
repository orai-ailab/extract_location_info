# README
This is an API using FastAPI framework that helps finding roads nearby a given location (latitude, longitude). The API uses the Overpass API to retrieve data of OpenStreetMaps in a specific geographic area and then extracts the relevant data from that to finally return a sorted list of all the roads that are available within the given distance limit with their complete details.

## API endpoints:

### Health Check
- Endpoint: ```/```
- Description: Returns a message if the API is up and running.

### Findway
- Endpoint: ```/findway```
- Method: ```GET```
- Description: Returns a sorted list of all the roads within a given distance limit with their complete details such as name, length, min distance and the tags associated with that way.

#### Query Parameters
- ```lat``` (required): latitude of the location (float).
- ```lon``` (required): longitude of the location (float).

#### Response
- Status Code:
  - ```200``` : If the request was successful.
- Response Body: A list of dictionaries containing the following keys:
  - ```name``` : Name of the road (string).
  - ```length_way``` : The length of the road in meters (integer).
  - ```distance``` : The minimum distance from the given location to that road in meters (integer).
  - ```detail```: A dictionary containing the other details of the road (dict).


## How to run the API
1. Clone the repository by running ```git clone https://github.com/orai-ailab/extract_location_info.git```.
2. Install the dependencies using ```pip install -r requirements.txt```.
3. Run the API using ```uvicorn main:app --reload```.
4. The API should be up and running on ```http://127.0.0.1:8000/```.