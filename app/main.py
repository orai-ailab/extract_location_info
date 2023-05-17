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
            sum += calculator_distance(lat_lon[i][0], lat_lon[i][1], lat_lon[i+1][0], lat_lon[i+1][1])
      min = calculator_distance(location[0], location[1], lat_lon[0][0], lat_lon[0][1])
      for i in range(len(lat_lon)):
            if min > calculator_distance(location[0], location[1], lat_lon[i][0], lat_lon[i][1]):
                  min = calculator_distance(location[0], location[1], lat_lon[i][0], lat_lon[i][1])
      return [name, int(sum), int(min),tags]

def calculator_distance(lat1, lon1, lat2, lon2):
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

def fillter_json(data,lat,lon):
      json_result = []
      for i in data:
      
            # kiểm tra trong json có key 'amenity' hay không
            if 'amenity' in i['tags']:
                  
                  try:
                        if i['tags']['amenity'] == 'school' or i['tags']['amenity'] == 'kindergarten' or i['tags']['amenity'] == 'university':
                              try:
                                    json_result.append({'name' : i['tags']['name'], 'distance' : calculator_distance(lat,lon,i['lat'],i['lon']),'type':'school','lat':i['lat'],'lon':i['lon']})
                              except:
                                    json_result.append({'name' : i['tags']['name'], 'distance' : calculator_distance(lat,lon,i['center']['lat'],i['center']['lon']),'type':'school','lat':i['center']['lat'],'lon':i['center']['lon']})
                  except:
                        # no detail
                        pass
                        
                  try:
                        if i['tags']['amenity'] == 'marketplace':
                              try:
                                    json_result.append({'name' : i['tags']['name'], 'distance' : calculator_distance(lat,lon,i['lat'],i['lon']), 'type':'market','lat':i['lat'],'lon':i['lon']})
                              except:
                                    json_result.append({'name' : i['tags']['name'], 'distance' : calculator_distance(lat,lon,i['center']['lat'],i['center']['lon']), 'type':'market','lat':i['center']['lat'],'lon':i['center']['lon']})
                  except:
                        # no detail
                        pass

                  try:
                        if i['tags']['amenity'] == 'police':
                              try:
                                    json_result.append({'name' : i['tags']['name'], 'distance' : calculator_distance(lat,lon,i['lat'],i['lon']), 'type':'police','lat':i['lat'],'lon':i['lon']})
                              except:
                                    json_result.append({'name' : i['tags']['name'], 'distance' : calculator_distance(lat,lon,i['center']['lat'],i['center']['lon']), 'type':'police','lat':i['center']['lat'],'lon':i['center']['lon']})
                  except:
                        # no detail
                        pass
            if 'shop' in i['tags']:
                  try:
                        if i['tags']['shop'] == 'supermarket':
                              try:
                                    json_result.append({'name' : i['tags']['name'], 'distance' : calculator_distance(lat,lon,i['lat'],i['lon']), 'type':'superMarket','lat':i['lat'],'lon':i['lon']})
                              except:
                                    json_result.append({'name' : i['tags']['name'], 'distance' : calculator_distance(lat,lon,i['center']['lat'],i['center']['lon']), 'type':'superMarket','lat':i['center']['lat'],'lon':i['center']['lon']})
                  except:
                        # no detail
                        pass
            if 'highway' in i['tags']:
                  try:
                        if i['tags']['highway'] == 'bus_stop':
                              try:
                                    json_result.append({'name' : i['tags']['name'], 'distance' : calculator_distance(lat,lon,i['lat'],i['lon']), 'type':'busStop','lat':i['lat'],'lon':i['lon']})
                              except:
                                    json_result.append({'name' : i['tags']['name'], 'distance' : calculator_distance(lat,lon,i['center']['lat'],i['center']['lon']), 'type':'busStop','lat':i['center']['lat'],'lon':i['center']['lon']})
                  except:
                        # no detail
                        pass
            if 'natural' in i['tags']:
                  try:
                        if i['tags']['natural'] == 'water':
                              try:
                                    json_result.append({'name' : i['tags']['name'], 'distance' : calculator_distance(lat,lon,i['lat'],i['lon']), 'type':'lake','lat':i['lat'],'lon':i['lon']})
                              except:
                                    json_result.append({'name' : i['tags']['name'], 'distance' : calculator_distance(lat,lon,i['center']['lat'],i['center']['lon']), 'type':'lake','lat':i['center']['lat'],'lon':i['center']['lon']})
                  except:
                        # no detail
                        pass
            if 'leisure' in i['tags']:
                  try:
                        if i['tags']['leisure'] == 'park':
                              try:
                                    json_result.append({'name' : i['tags']['name'], 'distance' : calculator_distance(lat,lon,i['lat'],i['lon']), 'type':'park','lat':i['lat'],'lon':i['lon']})
                              except:
                                    json_result.append({'name' : i['tags']['name'], 'distance' : calculator_distance(lat,lon,i['center']['lat'],i['center']['lon']), 'type':'park','lat':i['center']['lat'],'lon':i['center']['lon']})
                  except:
                        # no detail
                        pass
      return json_result
def get_value(data, attr):
      try:
            return data[attr]
      except:
            return None

def fillter_json_v2(data,lat,lon):
      json_result = []
      for i in data:
            try:
                  name = i['tags']['operator']
            except KeyError:
                  try:
                        name = i['tags']['name']
                  except KeyError:
                        try:
                              name = i['tags']['brand']
                        except KeyError:
                              try:
                                    name = i['tags']['name:en']
                              except KeyError:
                                    name = i['tags']['amenity'].upper()

            try:
                  lat_ = i['lat']
                  lon_ = i['lon']
            except KeyError:
                  lat_ = i['center']['lat']
                  lon_ = i['center']['lon']
            
            json_result.append({'name': name, 'distance': calculator_distance(lat, lon, lat_, lon_),'lat': lat_, 'lon':lon_, 'type': i['tags']['amenity']})
      
      return json_result






app = FastAPI()

# health check
@app.get("//")
async def root():
      return {"message": "By AILab - Oraichain Labs"}
# tìm đường xung quanh 1 địa điểm lat,long
@app.get("//findway")
async def findway(lat: float, lon: float, distance: int):
      location = [lat,lon]
      overpass_url = "http://65.109.112.52/api/interpreter"
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
      
      overpass_url = "http://65.109.112.52/api/interpreter"
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
      node["highway"="bus_stop"](around:{distance},{lat},{lon});
      node["amenity"="marketplace"](around:{distance},{lat},{lon});
      way["amenity"="marketplace"](around:{distance},{lat},{lon});
      rel["amenity"="marketplace"](around:{distance},{lat},{lon});
      node["shop"="supermarket"](around:{distance},{lat},{lon});
      way["shop"="supermarket"](around:{distance},{lat},{lon});
      rel["shop"="supermarket"](around:{distance},{lat},{lon});
      node["natural"="water"](around:{distance},{lat},{lon});
      way["natural"="water"](around:{distance},{lat},{lon});
      rel["natural"="water"](around:{distance},{lat},{lon});
      node["leisure"="park"](around:{distance},{lat},{lon});
      way["leisure"="park"](around:{distance},{lat},{lon});
      rel["leisure"="park"](around:{distance},{lat},{lon});
      node["amenity"="police"](around:{distance},{lat},{lon});
      way["amenity"="police"](around:{distance},{lat},{lon});
      rel["amenity"="police"](around:{distance},{lat},{lon});
      );
      out center;
      """
      response = requests.get(overpass_url, 
                              params={'data': overpass_query})
      data = response.json()
      return fillter_json(data['elements'],lat,lon)
      
# Endpoint của Long :v
@app.get("//findpublicfacilitiesv2")
async def findpublicfacilities(lat: float, lon: float, distance: int):
      
      overpass_url = "http://65.109.112.52/api/interpreter"
      keys = ["university", "fuel", "cafe", "parking", "parking_entrance", "fast_food", "marketplace", "restaurant",
                         "hospital", "school", "kindergarten", "townhall", " community_centre", "police", "place_of_worship", "bank", "atm"] 
      overpass_query = f"""
      [out:json];
      (
      """
      for key in keys:
            overpass_query += f"""
            node["amenity"="{key}"](around:{distance},{lat},{lon});
            way["amenity"="{key}"](around:{distance},{lat},{lon});
            rel["amenity"="{key}"](around:{distance},{lat},{lon});
            """
      overpass_query += f"""
      );
      out center;
      """
      response = requests.get(overpass_url,
                              params={'data': overpass_query})
      data = response.json()
      return fillter_json_v2(data['elements'],lat,lon)


      



@app.post("//findwayv2")
async def findwayv2(lat: float = Form(), lon: float = Form() ,google_api_key: str = Form()):
      # tìm 3 con gần nhất đường xung quanh 1 địa điểm lat,long và khoảng cách đến con đường đó
      location = [lat,lon]
      overpass_url = "http://65.109.112.52/api/interpreter"
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


@app.post("//get_detail_way")
async def get_detail_way(lat: float = Form(), lon: float = Form() ,distance: int = Form()):
      location = [lat,lon]
      overpass_url = "http://65.109.112.52/api/interpreter"
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