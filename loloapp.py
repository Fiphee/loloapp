from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics','width',1200)
Config.set('graphics','height',700)
Config.set('graphics', 'resizable', False)
from app_utilities.data_handle import app_storage, verify
app_storage.create()
verify.check_dates()
verify.check_milestones()
verify.check_habits()
verify.handle_old_data()

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, StringProperty
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from app_utilities.imagetools.image_handler import ImageHandler, ImageButton, _DisplayImage
from app_utilities.my_paths import DAILY, OBJECTIVES, MILESTONES, HABITS, PROFILE, ARCHIVE, DIARY, ENTRIES_FOLDER, TEST_FOLDER, TEST_IMAGES, TEST_THUMBS, TEMP
from app_utilities.dates import DATE_TODAY, YESTERDAY, DAY_NAME, PREVIOUS_MONTH
from app_utilities.custom_buttons import FolderButton, TagButton, PriorityButton, HabitdayButton, MyIconButton, ObjSwitch, ImageButton, ArchivedMilestoneButton, MilestonesButton, MileDrop, ObjectiveButton, DropdownClick, DisplayHabit
from app_utilities.fileselect import FolderSelect, FileSelector, FileLoader, SelectorBox, SelectorImage, TagsList
from app_utilities.screens import ScreenOne, Milestones, CreateEntry, SideNav
 

class Manager(ScreenManager):
    scr_one = ObjectProperty()
    diary = ObjectProperty()
    create_entry = ObjectProperty()
    milestones = ObjectProperty()
    popup = False
    add_path = False
    def __init__(self, *args, **kwargs):
        super(Manager,self).__init__(*args, **kwargs)
        self.scr_one.MANAGER = self
        self.diary.MANAGER = self
        self.create_entry.MANAGER = self
        self.milestones.MANAGER = self

    def autofocus(self, txt):
        txt.focus = True


class MyApp(MDApp):
    profile_pic = StringProperty(PROFILE['init']['profile_pic'])
    username = StringProperty(PROFILE['init']['username'])
    paper_color = ListProperty([0.945, 0.882, 0.752, 1])

    def build(self):
        self.m = Manager(transition=FadeTransition(clearcolor=(1,1,1,1)))
        Window.bind(on_dropfile=self._on_file_drop)
        global MANAGER
        MANAGER = self.m
        self.m.create_entry.MANAGER = MANAGER
        return self.m

    def _on_file_drop(self, window, file_path):
        if self.m.current == 'create_entry':
            if '.' in file_path[-8:].decode('utf-8'):
                if not self.m.add_path and file_path[-4:].decode('utf-8').lower() in ['.jpg','.png']:
                    loaded = file_path.decode('utf-8')
                    handle = ImageHandler(loaded)
                    handle._crop_and_save_image(save=True)
                    self.m.create_entry.add_new_slot(handle.img_path, handle.thumb)
                    return
            else:
                if self.m.add_path:
                    self.m.create_entry._add_folder(file_path.decode('utf-8'))
                    PROFILE['init']['image_folders'].append(file_path.decode('utf-8'))
                    PROFILE['init'] = PROFILE['init']
        else:                   
            pic = file_path.decode('utf-8')
            pic = pic.lower()
            if pic.endswith('.jpg') or pic.endswith('.png') or pic.endswith('.jpeg'):
                self.profile_pic = pic
                PROFILE['init']['profile_pic'] = pic
                PROFILE['init'] = PROFILE['init']
            return

    def change_name(self):        
        content = BoxLayout(orientation='vertical')
        btn_box = BoxLayout()
        cancel_btn = Button(text='Cancel', on_press=lambda x: self.cancel())
        save_btn = Button(text='Save', on_press=lambda x: self.save())
        self.change_to = TextInput()
        btn_box.add_widget(save_btn)
        btn_box.add_widget(cancel_btn)
        content.add_widget(self.change_to)
        content.add_widget(btn_box)
        self.change = MDDialog(title=f'Change your profile name',type='custom',content_cls=content, auto_dismiss=False)
        self.change.open()
        Clock.schedule_once(lambda x: self.m.autofocus(self.change_to), .2)

    def cancel(self):
        self.change.dismiss()

    def save(self):
        self.username = self.change_to.text
        PROFILE['init']['username'] = self.username
        PROFILE['init'] = PROFILE['init']  
        self.cancel()      


if __name__ =='__main__':
    MyApp().run()
