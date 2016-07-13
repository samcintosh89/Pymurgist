from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.uix.listview import ListItemButton

class AddMaltForm(BoxLayout):
	def args_converter():
		pass

class LocationButton(ListItemButton):
	location = ListProperty()

class MashApp(App):
	pass

if __name__ == '__main__':
	MashApp().run()