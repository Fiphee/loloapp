from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty

class Manager(ScreenManager):
    scr_one = ObjectProperty()
    diary = ObjectProperty()
    create_entry = ObjectProperty()
    milestones = ObjectProperty()
    popup = False
    add_path = False
        
    def autofocus(self, txt):
        txt.focus = True


    