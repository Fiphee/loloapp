from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from .imagetools.image_handler import ShowImage, ImageHandler
from .my_paths import PROFILE, TEMP
from kivy.graphics import Color, Rectangle
import os
from os.path import isdir, join



class FolderSelect(BoxLayout):
    listed_folders = ObjectProperty()

    def __init__(self, *args, root=None, **kwargs):
        super(FolderSelect,self).__init__(*args, **kwargs)
        self.root = root

    def _load_folders(self):
        from .custom_buttons import FolderButton
        for x in PROFILE['init']['image_folders']:
            self.listed_folders.add_widget(FolderButton(x))

    def close(self):
        self.root.my_pop.dismiss()
        self.root.parent.add_path = False


class SelectorBox(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(SelectorBox,self).__init__(*args, **kwargs)


class FileLoader(BoxLayout):
    loaded_images = ObjectProperty()
    load_btn = ObjectProperty()
    show_selected = ObjectProperty()

    def __init__(self, root, *args, **kwargs):
        super(FileLoader,self).__init__(*args, **kwargs)
        self.files = []
        self.currently_loaded = 0
        self.indx = 0
        self.root = root
        self.selections = {}

    def _load_files(self):
        for directory in PROFILE['init']['image_folders']: ## replace with saved directories from PROFILE 
            for image in os.listdir(directory):
                if image[-4:].lower() in ['.jpg','.png']:
                    self.files.append(join(directory, image))
        self.files = sorted(self.files, key=os.path.getctime, reverse=True)
        self.select_file(self.files[0])
        self._load_more()

    def _load_more(self):
        more = self.currently_loaded + 20
        if self.currently_loaded + 20 > len(self.files):
            more = len(self.files)
            self.load_btn.disabled = True
        self.loaded_images.rows += 4 
        for img in self.files[self.currently_loaded:more]:
            self._show_file(img, self.indx)
            self.indx += 1
        self.currently_loaded += more

    def _show_file(self, filepath, indx):
        box = SelectorBox()
        image = SelectorImage(root=self)
        image.img = filepath
        image.thumb = self._get_thumb_path(filepath, indx)
        image.on_press= lambda filepath=filepath: self.clickd(filepath, image)
        box.add_widget(image)
        self.loaded_images.add_widget(box)

    def select_file(self, filepath):
        self.show_selected.source = filepath

    def clickd(self, filepath, image):         
        self.select_file(filepath)
        if image.transp == 0:
            image.transp = .4
            self.selections[filepath] = 1
        else:
            image.transp = 0
            self.selections[filepath] = 0

    def add_image(self):
        for image in self.selections:
            if self.selections[image] == 1:
                img = ImageHandler(image)
                img._crop_and_save_image(save=True)
                self.root.add_new_slot(img.img_path, img.thumb)

        self.parent.dismiss()

    def _get_thumb_path(self, filepath, indx):
        thumb = ImageHandler(filepath)
        thumb.name = indx
        thumb._crop_and_save_image()
        thumb = thumb._get_thumb(None, indx=indx)
        self.thumb = thumb
        return thumb


class FileSelector(ShowImage):
    def __init__(self, *args, **kwargs):
        super(FileSelector,self).__init__(*args, **kwargs)
        self.avoid_collision = Button(disabled=True, background_color=(0,0,0,0))   # to disable clickable background widgets
        self.root = self.parent

        with self.canvas.before:
            self.clr = Color(rgba=(0,0,0,0))
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def _make_layout(self):
        self.layout = FileLoader(self.root)
        self.layout._load_files()
        self.add_widget(self.layout)

    def dismiss(self):
        super().dismiss()
        self._clear_temp()

    def _clear_temp(self):
        import shutil
        shutil.rmtree(TEMP)
        os.mkdir(TEMP)
class SelectorImage(Button):
    img = StringProperty()
    thumb = StringProperty()
    transp = NumericProperty(0)
    def __init__(self, root=None, *args, **kwargs):
        self.root = root
        super(SelectorImage,self).__init__(*args, **kwargs)


    def _make_layout(self):
        self.layout = FileLoader(self.root)
        self.layout._load_files()
        self.add_widget(self.layout)

    def dismiss(self):
        super().dismiss()
        self._clear_temp()

    def _clear_temp(self):
        import shutil
        shutil.rmtree(TEMP)
        os.mkdir(TEMP)


class TagsList(StackLayout):
    clr = ListProperty([.5,.5,.5,1])
    def __init__(self, root, pos=[0,0],*args, **kwargs):
        super(TagsList,self).__init__(*args, **kwargs)
        from .custom_buttons import TagButton
        self.pos = pos
        self.root = root
        for tag in ['Lifestyle', 'Health', 'Family',  'Friends', 'Love', 'Work', 'Recipes']:
            btn = TagButton(root)
            btn.btn.text = tag
            if tag in self.root.tag_list:
                btn.chk.active = True
            self.add_widget(btn)

        close = Button(text='Close', size_hint=(None,None), height=35, width=self.width)
        close.on_press = lambda: self.close()
        self.add_widget(close)

    def close(self):
        self.parent.remove_widget(self)


