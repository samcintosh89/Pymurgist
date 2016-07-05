import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.listview import ListItemButton
from kivy.factory import Factory 

class AddLocationForm(BoxLayout):
	search_input = ObjectProperty()
	current_weather = ObjectProperty()

	def search_location(self):
		search_template = "http://api.openweathermap.org/data/2.5/find?q={}&type=like&APPID=" + "57845a83cd7d330cdb88edd2b31ee018"
		search_url = search_template.format(self.search_input.text)
		request = UrlRequest(search_url, self.found_location)

	def found_location(self, request, data):
		data = json.loads(data.decode()) if not isinstance(data, dict) else data
		cities = [(d['name'], d['sys']['country']) for d in data['list']]
		self.search_results.item_strings = cities
		del self.search_results.adapter.data[:]
		self.search_results.adapter.data.extend(cities)
		self.search_results._trigger_reset_populate()

	def show_current_weather(self, location=None):
		self.clear_widgets()

		if location is None and self.current_weather is None:
			location = ("New York", "US")
		if location is not None:
			self.current_weather = Factory.CurrentWeather()
			self.current_weather.location = location
		self.add_widget(self.current_weather)

	def args_converter(self, index, data_item):
		city, country = data_item
		return {'location': (city, country)}

class LocationButton(ListItemButton):
	location = ListProperty()

class WeatherRoot(BoxLayout):
	def show_current_weather(self, location):
		self.clear_widgets()
		current_weather = Factory.CurrentWeather()
		current_weather.location = location
		self.add_widget(current_weather)

	def show_add_location_form(self):
		self.clear_widgets()
		self.add_widget(AddLocationForm())

class WeatherApp(App):
	pass

if __name__ == '__main__':
	WeatherApp().run()