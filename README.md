# FastAPI Navigation

This project provides an API for navigation services using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python. The API supports the following functionalities:

- Find ways around a specific location with a certain radius.
- Find public facilities around a specific location with a certain radius.
- Find the three closest paths to a specific location, and return information on their details and walking distance.

## Features

- Utilizes the Google Maps API to retrieve walking distance between two locations.
- Uses the powerful and fast Overpass API to fetch data about ways and nodes in OpenStreetMap.
- Built with FastAPI, a modern, fast (high-performance) web framework for building APIs with Python.

## Installation

To run the API locally, follow these steps:

1. Clone this repository.

2. Install the required packages by running the following command in your terminal:

```bash
$ pip install -r requirements.txt
```
3. Create a `.env` file in the root directory and add your Google Maps API key:

```bash
API_KEY_GOOGLE="your-api-key-here"
```

4. Run the API using the following command:

```bash
$ uvicorn main:app --reload
```

5. The API should now be running at http://127.0.0.1:8000/.

## API Endpoints

### Find Ways

To find all the ways around a specific location with a certain radius, make a GET request to the following endpoint:

```http
GET /findway?lat={lat}&lon={lon}&distance={distance}
```

Query Parameters:

- `lat` (float): The latitude of the location to search around.
- `lon` (float): The longitude of the location to search around.
- `distance` (int): The maximum radius (in meters) to search around the specified location.

Example:

```http
GET /findway?lat=20.990063&lon=105.813204&distance=1000
```

Response:

The API returns a JSON object containing information about the ways returned, including their names, length, distance to the specified location, and any available tags:

```json
[
  {
    "name": "Trích Sài Street",
    "length_way": 294,
    "distance": 134,
    "detail": {}
  },
  {
    "name": "Lạc Long Quân - Nguyễn Đức Cảnh",
    "length_way": 349,
    "distance": 194,
    "detail": {
      "maxspeed": "60",
      "name:vi": "Lạc Long Quân - Nguyễn Đức Cảnh",
      "ref": "TL 42",
      "source:maxspeed": "VI:urban",
      "surface": "asphalt",
      "type": "multipolygon",
      "width": "10.2"
    }
  }
]
```

### Find Public Facilities

To find all the public facilities around a specific location with a certain radius, make a GET request to the following endpoint:

```http
GET /findpublicfacilities?lat={lat}&lon={lon}&distance={distance}
```

Query Parameters:

- `lat` (float): The latitude of the location to search around.
- `lon` (float): The longitude of the location to search around.
- `distance` (int): The maximum radius (in meters) to search around the specified location.

Example:

```http
GET /findpublicfacilities?lat=20.990063&lon=105.813204&distance=1000
```

Response:

The API returns a JSON object containing information about the public facilities returned:

```json
[
  {
    "type": "node",
    "id": 1209375073,
    "lat": 20.9898892,
    "lon": 105.8137527,
    "tags": {
      "amenity": "restaurant",
      "cuisine": "regional",
      "name": "Phở Khô Thượng ĐỈnh"
    }
  },
  {
    "type": "node",
    "id": 586564290,
    "lat": 20.9934299,
    "lon": 105.807684,
    "tags": {
      "amenity": "cafe",
      "name": "Gấu Coffee",
      "operator": "Gau Coffee",
      "outdoor_seating": "yes",
      "wifi": "free"
    }
  }
]
 ```

### Find Three Closest Paths

To find the three closest paths around a specific location, and their walking distance from the initial location, make a GET request to the following endpoint:

```http
GET /findwayv2?lat={lat}&lon={lon}
```

Query Parameters:

- `lat` (float): The latitude of the location to search around.
- `lon` (float): The longitude of the location to search around.

Example:

```http
GET /findwayv2?lat=20.990063&lon=105.813204
```

Response:

The API returns a JSON object containing information about the three closest paths, including their names, length, walking distance to the initial location, and any available tags:

```json
[
  {
    "name": "Trích Sài Street",
    "length_way": 294,
    "distance": 134,
    "detail": {}
  },
  {
    "name": "Lạc Long Quân - Nguyễn Đức Cảnh",
    "length_way": 349,
    "distance": 194,
    "detail": {
      "maxspeed": "60",
      "name:vi": "Lạc Long Quân - Nguyễn Đức Cảnh",
      "ref": "TL 42",
      "source:maxspeed": "VI:urban",
      "surface": "asphalt",
      "type": "multipolygon",
      "width": "10.2"
    },
    "distance_walking": 1163
  },
  {
    "name": "Phố Vọng - Đường Dậu",
    "length_way": 505,
    "distance": 230,
    "detail": {},
    "distance_walking": 1383
  }
]
```
