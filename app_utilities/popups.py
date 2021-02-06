from kivymd.uix.snackbar import Snackbar
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from .my_paths import DIARY
from kivy.uix.stacklayout import StackLayout
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
from datetime import datetime, date
from kivymd.uix.picker import MDDatePicker
from kivy.clock import Clock
from kivy.properties import StringProperty
from .imagetools.image_handler import ShowImage, ImageButton
from kivymd.uix.button import MDIconButton
from .dates import DATE_TODAY, DAY_NAME
from .my_paths import DAILY, OBJECTIVES, HABITS, MILESTONES
from kivy.uix.label import Label
from .create import MARKUP_SIZE
from .screens import CreateEntry



class Mypop(Snackbar):
    def __init__(self, *args, root=None, btn_text=None, **kwargs):
        super(Mypop,self).__init__(*args,**kwargs)
        self.root = root
        self.btn_text = btn_text
        self.btn = Button(size_hint=(.35,1),background_normal='', background_color=root.highlight, text=self.btn_text, color=(.3,.3,.3,1), on_press=lambda x: self.root.popup())
        self.ids.box.add_widget(Image(source="", allow_stretch=False, keep_ratio=True, size_hint=(None,None), size=(40,40)))
        self.ids.box.add_widget(self.btn)
        self.ids.box.children[-1], self.ids.box.children[-2] = self.ids.box.children[-2], self.ids.box.children[-1] 



class CreateObjective(BoxLayout):
    def __init__(self,root=None, name='', edit=False, priority=1, date_picked=str(DATE_TODAY), habit=False, days={}, *args,**kwargs):
        super(CreateObjective,self).__init__(*args,**kwargs)
        self.habit = habit
        self.stored_name = name
        self.name = name.replace('_', ' ')
        self.edit = edit
        self.popu = None
        self.root = root
        self.dialog = self
        self.date_picked = date_picked
        self.priority = priority
        self.days = days
        self.priority_select_height = 405.5
        self.priority_select = {1:(572,self.priority_select_height),2:(629, self.priority_select_height),3:(685, self.priority_select_height),4:(742, self.priority_select_height)}
        box = StackLayout(orientation='tb-lr',spacing=10)
        btns = BoxLayout(size_hint_y=None, height=50)
        cancel_btn = Button(text='Cancel',on_press=lambda x: self.cancel(),size_hint_y=1)
        save_btn = Button(text='Save', on_press=lambda x: self.save(),size_hint_y=1)
        btns.add_widget(cancel_btn)
        btns.add_widget(save_btn)

        priority_box = BoxLayout(size_hint_y=None, height=50, spacing=31.5)
        priority_label = MDLabel(text='Select Color:', size_hint=(None,None), height=25, width=200)
        from .custom_buttons import PriorityButton, HabitdayButton, ObjSwitch
        p1 = PriorityButton(btn_color=root.my_pink)
        p2 = PriorityButton(btn_color=root.my_orange)
        p3 = PriorityButton(btn_color=root.my_blue)
        p4 = PriorityButton(btn_color=root.my_green)

        with self.canvas.before:
            Color(rgba=(.3,.3,.3,1))
            self.selection = Rectangle(pos=self.priority_select[priority], size=(31,31))

        p4.on_press= lambda: self.selected_priority(4)
        p3.on_press= lambda: self.selected_priority(3)
        p2.on_press= lambda: self.selected_priority(2)
        p1.on_press= lambda: self.selected_priority(1)

        priority_box.add_widget(priority_label)
        priority_box.add_widget(p1)
        priority_box.add_widget(p2)
        priority_box.add_widget(p3)
        priority_box.add_widget(p4)
        
        if self.date_picked == None:
            date_btn = 'Select date'
        else:
            date_btn = f"{datetime.strptime(self.date_picked, '%Y-%m-%d').strftime('%A')} - {self.date_picked} selected"
        self.select_date_btn = Button(text=date_btn, on_press=lambda x: self.date_pick(),size_hint_y=None, height=50)


        habit_box = BoxLayout(size_hint_y=None, height=50)
        check_habit_label = MDLabel(text='Make this a habit', size_hint_y=None, height=50)

        
        habit_days_box = BoxLayout(size_hint_y=None, height=70, spacing=20,padding=[0,30])
        habit_days_label = MDLabel(text='Habit Schedule: ', size_hint=(None,None), height=35, width=120)
        habit_days_label.color =[.965,.965,.965,1]
        self.d1 = HabitdayButton(btn_text='M', day='Monday', indx='1', dialog=self.dialog)
        self.d2 = HabitdayButton(btn_text='T', day='Tuesday', indx='2', dialog=self.dialog)
        self.d3 = HabitdayButton(btn_text='W', day='Wednesday', indx='3', dialog=self.dialog)
        self.d4 = HabitdayButton(btn_text='T', day='Thursday', indx='4', dialog=self.dialog)
        self.d5 = HabitdayButton(btn_text='F', day='Friday', indx='5', dialog=self.dialog)
        self.d6 = HabitdayButton(btn_text='S', day='Saturday', indx='6', dialog=self.dialog)
        self.d7 = HabitdayButton(btn_text='S', day='Sunday', indx='7', dialog=self.dialog)

        self.habit_check = ObjSwitch([self.d1,self.d2,self.d3,self.d4,self.d5,self.d6,self.d7], habit_days_label)
        if self.habit == True:
            self.habit_check.active = True

        self.info_label = MDLabel(text='', size_hint_y=None, height=70, theme_text_color='Custom', text_color=(1,0,0,1))

        habit_box.add_widget(check_habit_label)
        habit_box.add_widget(self.habit_check)

        initial_days = {}
        for k in self.days:
            initial_days[k] = self.days[k]

        if edit:
            self.btn_days = [self.d1,self.d2,self.d3,self.d4,self.d5,self.d6,self.d7]
            for x in self.btn_days:
                x.disabled = False
                for i in initial_days:
                    if x.day == self.days[i]:
                        self.selected_habit_day(x)

        habit_days_box.add_widget(habit_days_label)
        habit_days_box.add_widget(self.d1)
        habit_days_box.add_widget(self.d2)
        habit_days_box.add_widget(self.d3)
        habit_days_box.add_widget(self.d4)
        habit_days_box.add_widget(self.d5)
        habit_days_box.add_widget(self.d6)
        habit_days_box.add_widget(self.d7)

        self.obj_name = TextInput(text=self.name, multiline=False, size_hint_y=None, height=40)
        box.add_widget(self.obj_name)
        box.add_widget(self.select_date_btn)
        box.add_widget(priority_box)

        box.add_widget(habit_box)
        box.add_widget(habit_days_box)
        box.add_widget(self.info_label)
        box.add_widget(btns)

        self.add_widget(box)

        self.size_hint_y = None
        self.height=500



    def selected_priority(self, n):
        self.priority = n
        if n == 1:
            self.selection.pos = (572,self.priority_select_height)
        elif n == 2:
            self.selection.pos = (629, self.priority_select_height)
        elif n == 3:
            self.selection.pos = (685, self.priority_select_height)
        elif n == 4:
            self.selection.pos = (742, self.priority_select_height)

    def selected_habit_day(self, btn):
        if btn.background_color == [0.7, 0.7, 0.7, 1]:
            color = self.root.highlight
            self.days[btn.indx] = btn.day
        else:
            self.days.pop(btn.indx)
            color = [0.7, 0.7, 0.7, 1]
        btn.background_color = color

    def date_pick(self):
        if self.date_picked == None:
            today = str(date.today()).split('-')
        else:
            today = str(self.date_picked).split('-')
        date_dialog = MDDatePicker(year=int(today[0]),month=int(today[1]),day=int(today[2]),callback=self.get_date)
        date_dialog.open()
    
    def save(self):
        try:
            self.clear_info.cancel()
        except:
            pass

        self.clear_info = Clock.schedule_once(lambda x: self.clear_label(self.info_label), 2)
        if self.obj_name.text == '':
            if self.habit_check.active == False:
                self.info_label.text = 'You must name the objective'
            else:
                self.info_label.text = 'You must name the habit'
        elif self.select_date_btn.text == 'Select date':
            self.info_label.text = 'You must select a date for the objective'
        else:
            if self.habit_check.active == True and len(self.days) == 0:
                self.info_label.text = "You must select repeating days for the habit"
            else:
                obj_name = f'{self.date_picked}-{self.obj_name.text.replace(" ", "_")}'
                try:
                    obj = DAILY[self.date_picked]['objectives']
                    completed = DAILY[self.date_picked]['completed']
                    if obj_name not in obj:
                        if self.edit:
                            if f'{self.date_picked}-{self.stored_name}' in obj:
                                obj.remove(f'{self.date_picked}-{self.stored_name}')
                            obj.append(obj_name)
                        else:
                            if self.habit_check.active == False:
                                obj.append(obj_name)
                            else:
                                for x in self.days:
                                    if self.days[x] == f'{DAY_NAME}':
                                        obj.append(obj_name)

                    DAILY.put(self.date_picked, objectives=obj, completed=completed)
                except:
                    DAILY.put(self.date_picked, objectives=[obj_name], completed=0)
                self.popu.dismiss()
                try:
                    status = OBJECTIVES[f'{DATE_TODAY}-{self.stored_name}']['status']
                except:
                    status = 'uncompleted'
                if self.habit_check.active == True:
                    habit = True
                    if self.edit == True:
                        streak = HABITS[self.stored_name]['streak']
                        progress = MILESTONES[self.stored_name]['progress']
                        reward = MILESTONES[self.stored_name]['reward']
                        started = MILESTONES[self.stored_name]['started_date']
                        t = ''
                        tt = MILESTONES[self.stored_name]['text']
                        for L in tt:
                            if t.endswith('\nReward:'):
                                break
                            t += L
                        mtext = t.replace(f'{self.name}', f'{self.obj_name.text}') + reward

                        if self.obj_name.text != self.name:
                            HABITS.delete(self.stored_name)
                            OBJECTIVES.delete(f'{self.date_picked}-{self.stored_name}')
                            OBJECTIVES.put(obj_name, status=status, priority=self.priority)
                            MILESTONES.delete(self.stored_name)
                    else:
                        progress = (0,60)
                        reward = ""
                        started = f'{DATE_TODAY}'
                        mtext = f"[size={MARKUP_SIZE}]Acquire habit: {self.obj_name.text} - %p%[/size]\nReward: %r%"
                        streak = 0

                    HABITS.put(self.obj_name.text.replace(' ', '_'), repeats=self.days, streak=streak, started=self.date_picked, priority=self.priority, skippable=0)
                    # text = f"[size={MARKUP_SIZE}]Acquire habit: {self.obj_name.text} - %p%[/size]\nReward: %r%"
                    MILESTONES.put(self.obj_name.text.replace(' ', '_'), progress=progress, reward=reward, started_date=started, completed_date=None, text=f'{mtext}', category='habit')
                    for x in self.days:
                        if self.days[x] == DATE_TODAY.strftime('%A'):
                            OBJECTIVES.put(obj_name, status=status, priority=self.priority, habit=habit)
                            break
                else:
                    habit = False
                    OBJECTIVES.put(obj_name, status=status, priority=self.priority, habit=habit)
                
                if str(self.date_picked) == str(DATE_TODAY):
                    self.root.load_objectives()
                self.root.load_habits()



    def clear_label(self, lbl):
        lbl.text = ''

    def cancel(self):
        self.popu.dismiss()

    def _set_pop(self,arg):
        self.popu = arg

    def get_date(self, date):
        self.date_picked = str(date)
        self.select_date_btn.text = f"{date.strftime('%A')} - {date} selected"
        return date


class EntryDisplayed(BoxLayout):
    content = ObjectProperty()
    img_box = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(EntryDisplayed ,self).__init__(*args, **kwargs)
        self.next_gallery_slot = 0
        self.currently_shown = None
        self.pics = {}


class ViewEntry(ShowImage):
    def __init__(self, root, manager, *args, **kwargs):
        super(ViewEntry ,self).__init__(*args, **kwargs)
        self.root = root
        self.entry = None
        self.dark_level = .9
        self.next_gallery_slot = 0
        self.currently_shown = None
        self.pics = {}
        self.root.now_on_screen = self.entry
        self.MANAGER = manager

    def add_new_slot(self, source, thumb):
        if self.next_gallery_slot != self.img_box.slots:
            img = self.img_box.children[self.get_indx(self.next_gallery_slot)]
            img.pic = thumb
            img.img = source  
        else:
            img = ImageButton(indx=self.img_box.slots, root=self)
            img.pic = thumb
            img.img = source
            img.viewing = True
            self.img_box.add_widget(img)
            self.img_box.slots += 1
        self.pics[self.next_gallery_slot] = source
        self.next_gallery_slot += 1

    def get_indx(self, n):
        return (self.img_box.slots - n) -1          # true parent/child index

    def _make_layout(self):
        infos = self._get_entry_infos(str(self.entry))
        self.layout = EntryDisplayed()
        self.layout.content.text = infos['content']
        self.img_box = self.layout.img_box
        self.add_widget(self.layout)
        self.load_images(infos)

        # Close btn
        self.close_btn = MDIconButton(icon='close', user_font_size='48sp', pos=(Window.width-100, Window.height-90), theme_text_color='Custom', text_color=(1,1,1,1))
        self.close_btn.on_press = lambda: self.dismiss()
        self.parent.now_on_screen = None
        self.add_widget(self.close_btn)

        # Title
        self.title = Label(text=f"{infos['title']}", text_size=self.size, font_size=40, pos=(125, Window.height - 75))
        self.add_widget(self.title)

        # Edit btn
        self.edit_btn = MDIconButton(icon='file-document-edit', user_font_size='48sp', pos=(25, Window.height-90), theme_text_color='Custom', text_color=(1,1,1,1))
        self.edit_btn.on_press = lambda: self.edit_entry()
        self.add_widget(self.edit_btn)
    
    def _update_infos(self):
        self.next_gallery_slot = 0
        infos = self._get_entry_infos(str(self.entry))
        self.title.text = infos['title']
        self.remove_widget(self.layout)
        self.layout = EntryDisplayed()
        self.layout.content.text = infos['content']
        self.img_box = self.layout.img_box
        self.add_widget(self.layout)
        self.load_images(infos)

    def edit_entry(self):
        self.edit_page = CreateEntry()
        self.edit_page.edit = True
        self.edit_page.entry = self.entry
        self.edit_page.name='edit_page'
        self.edit_page.MANAGER = self.MANAGER
        # self.manager = MANAGER
        self.MANAGER.add_widget(self.edit_page)
        self.MANAGER.current = 'edit_page'
        self.root.now_on_screen = str(self.entry)

    def load_images(self, infos):
        pics = infos['pics']
        thumbs = infos['thumbnails']
        for img in range(0, len(pics)):
            self.add_new_slot(pics[img], thumbs[img])

    def _get_entry_infos(self, entry):
        infos = {}
        infos['title'] = DIARY[entry]['title'][:-4]
        infos['date_created'] = DIARY[entry]['date_created']
        infos['thumbnails'] = DIARY[entry]['thumbnails']
        infos['pics'] = DIARY[entry]['pics']
        tags = []
        for tag in ["lifestyle", "health", "family", "friends", "love", "work", "recipes"]:
            if DIARY[entry][tag] == 1:
                tags.append(tag)
        infos['tags'] = tags
        text = ''
        with open(DIARY[entry]['content']) as txt:
            for character in txt:
                text += character
        infos['content'] = text
        return infos



