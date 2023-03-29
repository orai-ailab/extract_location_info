# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
import math

def extract_way(test_data_way, location, data_node):
      tags = test_data_way['tags']
      nodes = test_data_way['nodes']
      name = test_data_way['tags']['name']
      lat_lon = []
      for node in nodes:
            frame = [x for x in data_node if x['id'] == node]
            lat_lon.append([frame[0]['lat'], frame[0]['lon']])
      sum = 0
      for i in range(len(lat_lon)-1):
            sum += distance(lat_lon[i][0], lat_lon[i][1], lat_lon[i+1][0], lat_lon[i+1][1])
      min = distance(location[0], location[1], lat_lon[0][0], lat_lon[0][1])
      for i in range(len(lat_lon)):
            if min > distance(location[0], location[1], lat_lon[i][0], lat_lon[i][1]):
                  min = distance(location[0], location[1], lat_lon[i][0], lat_lon[i][1])
      return [name, int(sum), int(min),tags]

def distance(lat1, lon1, lat2, lon2):
            R = 6371
            dLat = (lat2-lat1) * math.pi / 180
            dLon = (lon2-lon1) * math.pi / 180
            lat1 = lat1 * math.pi / 180
            lat2 = lat2 * math.pi / 180
            a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            d = R * c
            return d*1000


app = FastAPI()

# health check
@app.get("//")
async def root():
      return {"message": "By AILab - Oraichain Labs"}
# tìm đường xung quanh 1 địa điểm lat,long
@app.get("//findway")
async def findway(lat: float, lon: float):
      location = [lat,lon]
      overpass_url = "http://overpass-api.de/api/interpreter"
      overpass_query = """
      [out:json];
      way(around:500, """+str(lat)+","+str(lon)+""")["highway"];
      (._;>;);
      out;
      """
      response = requests.get(overpass_url,
                              params={'data': overpass_query})
      data = response.json()

      data_way = []
      for way in data["elements"]:
            if way["type"] == "way":
                  data_way.append(way)
      data_node = []
      for node in data["elements"]:
            if node["type"] == "node":
                  data_node.append(node)
      list_result = []
      for way in data_way:
            try:
                  list_result.append(extract_way(way, location, data_node))
            except:
                  pass
      list_result.sort(key=lambda x: x[2])
      json_result = []
      for i in list_result:

            # remove frame 'name' in i[3]
            i[3].pop('name')
            
            frame = ({'name' : i[0], 'length_way' : i[1], 'distance' : i[2], 'detail' : i[3]})
            json_result.append(frame)
      return json_result
      