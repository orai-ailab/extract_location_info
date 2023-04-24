# FastAPI
from fastapi import FastAPI,Form
import requests
import math
import threading




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

def direction_google_map(lat,lon,destination,google_api_key):
      origin = f"{lat},{lon}" # Vị trí xuất phát
      mode = "walking" # Chế độ đi bộ
      

      url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination['name']}&mode={mode}&key={google_api_key}"
      response = requests.get(url)

      data = response.json()
      distance = data['routes'][0]['legs'][0]['distance']['value']
      distance_m = distance
      destination.update({'distance_walking' : distance_m})
      return destination


app = FastAPI()

# health check
@app.get("//")
async def root():
      return {"message": "By AILab - Oraichain Labs"}
# tìm đường xung quanh 1 địa điểm lat,long
@app.get("//findway")
async def findway(lat: float, lon: float, distance: int):
      location = [lat,lon]
      overpass_url = "http://overpass-api.de/api/interpreter"
      overpass_query = f"""
      [out:json];
      way(around:{distance}, """+str(lat)+","+str(lon)+""")["highway"];
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
      

@app.get("//findpublicfacilities")
async def findpublicfacilities(lat: float, lon: float, distance: int):
      def school(lat,lon,distance):
            overpass_url = "http://overpass-api.de/api/interpreter"
            overpass_query = f"""
            [out:json];
            (
            node["amenity"="school"](around:{distance},{lat},{lon});
            way["amenity"="school"](around:{distance},{lat},{lon});
            rel["amenity"="school"](around:{distance},{lat},{lon});
            node["amenity"="kindergarten"](around:{distance},{lat},{lon});
            way["amenity"="kindergarten"](around:{distance},{lat},{lon});
            rel["amenity"="kindergarten"](around:{distance},{lat},{lon});
            node["amenity"="university"](around:{distance},{lat},{lon});
            way["amenity"="university"](around:{distance},{lat},{lon});
            rel["amenity"="university"](around:{distance},{lat},{lon});
            );
            out center;
            """
            response = requests.get(overpass_url, 
                                    params={'data': overpass_query})
            data = response.json()
            data_json = []
            for name in data['elements']:
                  try:
                        data_json.append({'name' : name['tags']['name'],'distance' : distance(lat,lon,name['lat'],name['lon'])})
                  except:
                        try:
                              data_json.append({'name' : name['tags']['name'],'distance' : distance(lat,lon,name['center']['lat'],name['center']['lon'])})
                        except:
                              pass
            return data_json
      def bus_station(lat,lon,distance):
            overpass_url = "http://overpass-api.de/api/interpreter"
            overpass_query = f"""
            [out:json];
            (
            node["highway"="bus_stop"](around:{distance},{lat},{lon});
            );
            out center;
            """
            response = requests.get(overpass_url, 
                                    params={'data': overpass_query})
            data = response.json()
            data_json = []
            for name in data['elements']:
                  try:
                        data_json.append({'name' : name['tags']['name'],'distance' : distance(lat,lon,name['lat'],name['lon'])})
                  except:
                        pass
            return data_json
      def market(lat,lon,distance):
            overpass_url = "http://overpass-api.de/api/interpreter"
            overpass_query = f"""
            [out:json];
            (
            node["amenity"="marketplace"](around:{distance},{lat},{lon});
            way["amenity"="marketplace"](around:{distance},{lat},{lon});
            rel["amenity"="marketplace"](around:{distance},{lat},{lon});
            );
            out center;
            """
            response = requests.get(overpass_url, 
                                    params={'data': overpass_query})
            data = response.json()
            data_json = []
            for name in data['elements']:
                  try:
                        data_json.append({'name' : name['tags']['name'],'distance' : distance(lat,lon,name['lat'],name['lon'])})
                  except:
                        try:
                              data_json.append({'name' : name['tags']['name'],'distance' : distance(lat,lon,name['center']['lat'],name['center']['lon'])})
                        except:
                              pass
            return data
      def super_market(lat,lon,distance):
            overpass_url = "http://overpass-api.de/api/interpreter"
            overpass_query = f"""
            [out:json];
            (
            node["shop"="supermarket"](around:{distance},{lat},{lon});
            way["shop"="supermarket"](around:{distance},{lat},{lon});
            rel["shop"="supermarket"](around:{distance},{lat},{lon});
            );
            out center;
            """
            response = requests.get(overpass_url,
                                    params={'data': overpass_query})
            data = response.json()
            data_json = []
            for name in data['elements']:
                  try:
                        data_json.append({'name' : name['tags']['name'],'distance' : distance(lat,lon,name['lat'],name['lon'])})
                  except:
                        try:
                              data_json.append({'name' : name['tags']['name'],'distance' : distance(lat,lon,name['center']['lat'],name['center']['lon'])})
                        except:
                              pass
            return data_json
      def lake(lat,lon,distance):
            overpass_url = "http://overpass-api.de/api/interpreter"
            overpass_query = f"""
            [out:json];
            (
            node["natural"="water"](around:{distance},{lat},{lon});
            way["natural"="water"](around:{distance},{lat},{lon});
            rel["natural"="water"](around:{distance},{lat},{lon});
            );
            out center;
            """
            response = requests.get(overpass_url,
                                    params={'data': overpass_query})
            data = response.json()
            data_json = []
            for name in data['elements']:
                  try:
                        data_json.append({'name' : name['tags']['name'],'distance' : distance(lat,lon,name['lat'],name['lon'])})
                  except:
                        try:
                              data_json.append({'name' : name['tags']['name'],'distance' : distance(lat,lon,name['center']['lat'],name['center']['lon'])})
                        except:
                              pass
            return data_json
      
      def park(lat,lon,distance):
            overpass_url = "http://overpass-api.de/api/interpreter"
            overpass_query = f"""
            [out:json];
            (
            node["leisure"="park"](around:{distance},{lat},{lon});
            way["leisure"="park"](around:{distance},{lat},{lon});
            rel["leisure"="park"](around:{distance},{lat},{lon});
            );
            out center;
            """
            response = requests.get(overpass_url,
                                    params={'data': overpass_query})
            data = response.json()
            data_json = []
            for name in data['elements']:
                  try:
                        data_json.append({'name' : name['tags']['name'],'distance' : distance(lat,lon,name['lat'],name['lon'])})
                  except:
                        try:
                              data_json.append({'name' : name['tags']['name'],'distance' : distance(lat,lon,name['center']['lat'],name['center']['lon'])})
                        except:
                              pass
            return data_json
      def police(lat,lon,distance):
            overpass_url = "http://overpass-api.de/api/interpreter"
            overpass_query = f"""
            [out:json];
            (
            node["amenity"="police"](around:{distance},{lat},{lon});
            way["amenity"="police"](around:{distance},{lat},{lon});
            rel["amenity"="police"](around:{distance},{lat},{lon});
            );
            out center;
            """
            response = requests.get(overpass_url, 
                                    params={'data': overpass_query})
            data = response.json()
            data_json = []
            for name in data['elements']:
                  try:
                        data_json.append({'name' : name['tags']['name'],'distance' : distance(lat,lon,name['lat'],name['lon'])})
                  except:
                        try:
                              data_json.append({'name' : name['tags']['name'],'distance' : distance(lat,lon,name['center']['lat'],name['center']['lon'])})
                        except:
                              pass
            return data_json
      return police(lat,lon,distance)




@app.post("//findwayv2")
async def findwayv2(lat: float = Form(), lon: float = Form() ,google_api_key: str = Form()):
      # tìm 3 con gần nhất đường xung quanh 1 địa điểm lat,long và khoảng cách đến con đường đó
      location = [lat,lon]
      overpass_url = "http://overpass-api.de/api/interpreter"
      overpass_query = f"""
      [out:json];
      way(around:1000, """+str(lat)+","+str(lon)+""")["highway"];
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
      data = json_result[0:4]
      # create 3 thread to find direction
      threads = [] 
      for i in data:
            t = threading.Thread(target=direction_google_map, args=(lat,lon,i,google_api_key))
            threads.append(t)
            t.start()
      # wait for all threads to finish print result of thread
      for t in threads:
            t.join()
      return data


      
