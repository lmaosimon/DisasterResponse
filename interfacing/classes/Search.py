import csv
import os
import math
from geopy.geocoders import Nominatim

city_coords = [(29.9511, -90.0715), (34.0522, -118.2437), (40.7128, -74.0060), (35.4676, -97.5164)]
city_coord_map = {(29.9511, -90.0715): "southeast", (34.0522, -118.2437): "southwest",
                  (40.7128, -74.0060): "northeast", (35.4676, -97.5164): "midwest"}


def locate(coords, data):
	if coords in data.keys():
		return data[coords]


def distance(v1, v2):
	x1 = v1[0]
	x2 = v2[0]
	y1 = v1[1]
	y2 = v2[1]
	return math.hypot(x2 - x1, y2 - y1)


def nearest_region(coords):
	nearest = min(city_coords, key=lambda x: distance(x, coords))
	return city_coord_map[nearest]


class Search:
	def __init__(self):
		self.geolocater = Nominatim(user_agent='Disaster Response Sim')
		self.cities = {}
		self.gps = {}
		self.coords = []
		self.regions = {}
		if not self._init_data():
			print('Init failed')

	def search(self, location):
		data = location.split(',')
		near_region = ""
		info = {}
		try:
			city = data[0].title().rstrip(' ')
			state = data[1].upper().replace(' ', '')
			if (city, state) in self.cities.keys():
				info = self.cities[(city, state)]
				lat = info['latitude']
				long = info['longitude']
				near_region = nearest_region((lat, long))
			else:
				raise IndexError

		except IndexError:
			location = self.geolocater.geocode(location)
			if location:
				loc = (location.latitude, location.longitude)
				near_region = nearest_region(loc)
				nearest = min(self.coords, key=lambda x: distance(x, loc))
				key = self.gps[nearest]
				city = key['name']
				state = key['state']
				info = self.cities[(city, state)]
			else:
				return -1
		return (near_region, info)

	def _init_data(self):
		cur_path = os.path.dirname(__file__)
		base = os.path.basename(cur_path)
		while base != 'DisasterResponse':
			cur_path = os.path.dirname(cur_path)
			base = os.path.basename(cur_path)
		new_path = os.path.join(cur_path, 'resources/uscities.csv')
		with open(new_path, newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			next(reader)
			for row in reader:
				name = row[0]
				state = row[2]
				population = row[10]
				population_dens = row[11]
				latitude = float(row[8])
				longitude = float(row[9])

				self.cities[(name, state)] = {'population': population, 'population_dens': population_dens,
				                              'latitude': latitude, 'longitude': longitude}
				self.gps[(latitude, longitude)] = {'name': name, 'state': state}
				self.coords.append((latitude, longitude))

		self.coords.sort(key=lambda tup: tup[0])
		if self.coords and self.gps and self.cities:
			return 1
		else:
			return -1


def main():
	finder = Search()
	if not finder:
		return -1
	inp = ''
	while inp != 'quit':
		results = finder.search(inp)
		if not results:
			print('City not found.')
		else:
			print(results)
		inp = input('>>')


if __name__ == '__main__':
	main()
