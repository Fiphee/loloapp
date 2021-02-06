from PIL import Image as pil_img
import ntpath
from os.path import join
from ..my_paths import TEST_FOLDER, TEST_IMAGES, TEST_THUMBS, TEMP
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation, AnimationTransition
from kivy.clock import Clock
from kivymd.uix.button import MDIconButton


class ShowImage(FloatLayout):
    def __init__(self, picture=None, indx=None, root=None, *args, **kwargs):
        super(ShowImage,self).__init__(*args, **kwargs)
        self.size = Window.size
        self.root = root
        self.avoid_collision = Button(disabled=True, background_color=(0,0,0,0))   # to disable clickable background widgets
        self.picture = picture
        self.indx = indx
        self.dark_level = .8
        with self.canvas.before:
            self.clr = Color(rgba=(0,0,0,0))
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def show(self):
        self._darken_background()
        self._make_layout()

    def dismiss(self):
        self._brighten_background()
        self.remove_widget(self.layout)   
        Clock.schedule_once(lambda x: self.parent.remove_widget(self),.15)

    def _darken_background(self):
        self.add_widget(self.avoid_collision)
        self.clr.a = 0
        anim = Animation(a=self.dark_level, duration=.15)
        anim.start(self.clr)

    def _brighten_background(self):
        self.remove_widget(self.avoid_collision)
        self.clr.a = self.dark_level
        anim = Animation(a=0, duration=.15)
        anim.start(self.clr)

    def _make_layout(self):
        self.layout = _DisplayImage(self.picture)
        self.add_widget(self.layout)
        self.root.currently_shown = self.indx


class _DisplayImage(BoxLayout):
    img = ObjectProperty()
    def __init__(self, picture, *args, **kwargs):
        super(_DisplayImage,self).__init__(*args, **kwargs)
        self.img.source = picture
        self.image_path = None

    def dismiss(self):
        self.parent.dismiss()

    def change(self, direction):
        if direction == 'left':
            if self.parent.root.currently_shown != 0:
                self.parent.root.currently_shown -= 1
                img = self.parent.root.pics[self.parent.root.currently_shown]
                if img != '':  # to deal with removed images during editing so they don't show up as grey boxes.
                    self.img.source = img
                else:
                    if self.parent.root.currently_shown != 0:
                        self.change('left')
                    else:
                        self.parent.root.currently_shown += 1
                    
        elif direction == 'right':
            if self.parent.root.currently_shown != len(self.parent.root.pics)-1:
                self.parent.root.currently_shown += 1
                img = self.parent.root.pics[self.parent.root.currently_shown]
                if img != '':       
                    self.img.source = img
                else:
                    if self.parent.root.currently_shown != 0:
                        self.change('right')
                    else:
                        self.parent.root.currently_shown -= 1


class ImageButton(Button):
    pic = StringProperty('')
    def __init__(self, indx=0, root=None, *args,**kwargs):
        super(ImageButton,self).__init__(*args,**kwargs)
        self.root = root
        self.indx = indx
        self.pic = ''
        self.img = ''
        self.viewing = False

    def on_press(self):
        if self.last_touch.button == 'left':
            img = ShowImage(self.img, self.indx, root=self.root)
            self.root.add_widget(img)
            img.show()
        elif self.last_touch.button == 'right':
            if not self.viewing:
                self.remove_img()

    def remove_img(self):
        self.parent.remove_widget(self)
        self.root.pics[self.indx] = ''

    def on_pic(self, *args):
        self.disabled = False

    def get_name(self, pth):
        head, tail = ntpath.split(pth)
        return tail or ntpath.basename(head)


class ImageBox(StackLayout):
    def __init__(self,*args,**kwargs):
        super(ImageBox,self).__init__(*args,**kwargs)
        self.slots = 0
    

class ImageHandler():
    def __init__(self, image_path):
        self.thumb = self._get_thumb(image_path)
        self.img_path = image_path
        self.name = ''

    def _crop_and_save_image(self, save=False):
        image = pil_img.open(self.img_path)
        if save:       
            self.name = self.get_filename(self.img_path)    
            new_path = join(TEST_IMAGES, self.name)
            image.save(new_path)
            self.image_path = new_path   
        self._make_thumbnail(self.img_path, save=save)
        image.close()

    def _make_thumbnail(self, img_path, save=False):
        with pil_img.open(img_path) as image:
            if image.size[0] != image.size[1]:
                points = self._get_crop_points(image.size)
            else:
                points = (0,0,image.width, image.height)
            thumb = image.crop(points)
            thumb = thumb.resize((140,140), pil_img.ANTIALIAS)
            if save:
                thumb.save(join(TEST_THUMBS, f'-thumb-{self.name}'))
            else:
                thumb.save(join(TEMP, f'-thumb-{self.name}.png'))
            thumb.close()

    def _get_thumb(self, img_path, indx=None):
        if indx == None:
            head, name = ntpath.split(img_path)
            if not name:
                name = ntpath.basename(head)
        else:
            name = str(indx) + '.png'
        thumbname = '-thumb-' + name
        return join(TEST_THUMBS, thumbname) if indx==None else join(TEMP, thumbname)

    def _get_crop_points(self, size):
        width, height = size[0], size[1]
        cropped = max(width,height) - min(width, height)
        cropped = cropped / 2
        if width > height:
            left = cropped
            top = 0
            right = cropped + height
            bottom = height
        else:
            left = 0
            top = 0 + cropped
            right = width
            bottom = height - cropped
        return (left, top, right, bottom)


    def get_filename(self, pth):
        head, tail = ntpath.split(pth)
        return tail or ntpath.basename(head)