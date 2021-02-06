from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from .my_paths import PROFILE, MILESTONES
from kivy.uix.button import Button
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.button import MDIconButton
from kivymd.uix.snackbar import Snackbar
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from .my_paths import ARCHIVE
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.clock import Clock
import ntpath
from kivymd.uix.dialog import MDDialog
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from .my_paths import DAILY, OBJECTIVES, HABITS, MILESTONES, PROFILE, ARCHIVE, DIARY, ENTRIES_FOLDER
from .dates import DATE_TODAY
from .popups import Mypop, ViewEntry, CreateObjective, EntryDisplayed
from .imagetools.image_handler import ShowImage
from os.path import join
import shutil

MARKUP_SIZE = 25


class DisplayHabit(BoxLayout):
    def __init__(self, root=None, hab_text=None, argus=[], indx=None, streak=None, *args,**kwargs):
        super(DisplayHabit, self).__init__(*args,**kwargs)
        self.padding = [0,10,0,0]
        self.func = None
        self.argus = argus
        self.indx = indx
        self.root = root
        self.hab_btn = Button(text=hab_text,size_hint=(.8,None), height=50, background_normal='', background_color=[.5,.5,.5,1])
        self.hab_streak = Button(text=streak, size_hint=(.2,None), height=50)
        self.hab_btn.on_press = lambda: self.pressd(self.hab_btn)
        self.add_widget(self.hab_btn)
        self.add_widget(self.hab_streak)

    def pressd(self, btn):
        try:
            self.root.remove_widget(self.dropmenu)
        except:
            pass    
        if btn.last_touch.button == 'right':
            if 'Dropdown' in str(self.root.children[0]):
                self.root.remove_widget(self.root.children[0])
            drop_pos = ((self.get_x(btn.last_touch.pos[0]),self.get_y(btn.last_touch.pos[1])))
            self.make_menu(btn, drop_pos)
            self.right_clicked_widget = btn


    def get_x(self, n):
        return n + 550
    
    def get_y(self, n):
        n = 20
        for _ in range(0, self.indx):
            n += 50
        return 550 - n

    def make_menu(self, btn, posi):
        self.dropmenu = DropdownClick(root=self.root, size_hint=(None,None), size=(150,100), pos=posi, edit=True, clicked_widget=btn, argus=self.argus)
        self.root.add_widget(self.dropmenu)

    def get_func(self,arg):
        self.func = arg


class TagButton(BoxLayout):
    btn = ObjectProperty()
    chk = ObjectProperty()
    def __init__(self, root, *args, **kwargs):
        super(TagButton,self).__init__(*args, **kwargs)
        self.root = root

    def check_tick(self, chk):
        if chk.active == False:
            chk.active = True
        else: 
            chk.active = False
        

class FolderButton(BoxLayout):
    folder_name = ObjectProperty()

    def __init__(self, txt, *args, **kwargs):
        super(FolderButton, self).__init__(*args, **kwargs)
        self.folder_name.text = txt

    def delete(self):
        self.parent.remove_widget(self)
        PROFILE['init']['image_folders'].remove(self.folder_name.text)
        PROFILE['init'] = PROFILE['init']


class PriorityButton(Button):
    def __init__(self, btn_color=None, *args,**kwargs):
        super(PriorityButton,self).__init__(*args,**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = btn_color
        self.size_hint=(None,None)
        self.size=(25,25)


class HabitdayButton(Button):
    def __init__(self, btn_text='', day=None, dialog=None, indx=None, *args,**kwargs):
        super(HabitdayButton,self).__init__(*args,**kwargs)
        self.indx = indx
        self.text = btn_text
        self.background_disabled_normal = ''
        self.background_normal = ''
        self.background_color = [.965,.965,.965,1]
        self.size_hint=(None,None)
        self.size=(30,30)
        self.color = (.965,.965,.965,1)
        self.day = day
        self.on_press = lambda: dialog.selected_habit_day(self)
        self.disabled = True


class ObjSwitch(MDSwitch):
    def __init__(self, btns, label, *args,**kwargs):
        super(ObjSwitch, self).__init__(*args,**kwargs)
        self.btns = btns
        self.label = label

    def switch(self):
        if self.active == True:
            for button in self.btns:
                button.background_color = [.7,.7,.7,1]
                button.color = [0,0,0,1]
                self.label.color = [0,0,0,1]
                button.disabled = False
        elif self.active == False:
            for button in self.btns:
                button.color = [.965,.965,.965,1]
                self.label.color = [.965,.965,.965,1]
                button.background_color = [.965,.965,.965,1]
                button.disabled = True


class MyIconButton(MDIconButton):
    c = ListProperty([0,0,0,1])
    disabled_t = ListProperty([0,0,0,1])
    def _set_b_color(self,arg):
        self.c = arg
        if arg == [0.992, 0.901, 0.525,1]:
            self.disabled_t = [0.69, 0.552, 0.011,1]
        else:
            self.disabled_t = [0,0,0,1]


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


class ArchivedMilestoneButton(Button):
    disabled_t = ListProperty([0.69, 0.552, 0.011,1])


class MilestonesButton(BoxLayout):
    def __init__(self, root, *args, indx=None, name=None, active=None, progress=None, text='', archive=False, reward=None, m_category=None, **kwargs):
        super(MilestonesButton,self).__init__(*args,**kwargs)
        self.root = root
        self.indx = indx
        self.active = active
        self.archive = archive
        self.name = name.replace(' ', '_')
        self.progress = progress
        self.reward = reward
        self.claimed = False
        self.m_category = m_category
        self.label = text.replace('%r%', f'{self.reward}').replace('%p%', f'({self.progress[0]}/{self.progress[1]})').replace('%n%', f'{self.progress[1]}')
        
        self.btn = ArchivedMilestoneButton(text=self.label, size_hint=(1,None), height=75, markup=True, halign='left', background_normal='', background_color=(.3,.3,.3,1))
        if self.disabled:
            self.btn.background_color = root.disabled_c
        self.btn.on_press = lambda: self.pressed(self.btn, self.archive)
        self.btn.text_size = 750,None
        self.add_widget(self.btn)

    def pressed(self, btn, archive=False):
        if btn.last_touch.button == 'left':
            try:
                self.remove_widget(self.dropmenu)
            except:
                pass
            if archive:
                if not self.claimed:
                    txt = btn.text
                    txt += ' - Claimed!'
                    btn.text = txt
                    btn.background_color = self.root.disabled_c
                    btn.color = self.root.disabled_t
                    # btn.disabled = True
                    # save to ARCHIVE
                    ARCHIVE[btn.parent.name]['claimed'] = True
                    ARCHIVE[btn.parent.name]['text'] = txt
                    ARCHIVE[btn.parent.name] = ARCHIVE[btn.parent.name]
                    self.claimed = True
                else:
                    btn.text = btn.text[:-11]
                    btn.background_color = (.3,.3,.3,1)
                    btn.color = (1,1,1,1)
                    ARCHIVE[btn.parent.name]['claimed'] = False
                    ARCHIVE[btn.parent.name]['text'] = btn.text
                    ARCHIVE[btn.parent.name] = ARCHIVE[btn.parent.name]
                    self.claimed = False

        elif btn.last_touch.button == 'right':
            
            try:
                self.remove_widget(self.dropmenu)
            except:
                pass
            if self.active == 'progress':
                drop_pos = (self.get_x(btn.last_touch.pos[0]),self.get_y(btn.last_touch.pos[1]))
                self.make_menu(btn, drop_pos)
                self.right_clicked_widget = btn

    def make_menu(self, btn, posi):
        self.dropmenu = MileDrop(size_hint=(None,None), size=(150,100), pos=posi, clicked_widget=btn, root=self.root)
        
        self.root.add_widget(self.dropmenu)

    
    def get_x(self, n):
        return n + 100
    
    def get_y(self, n):
        n = 20
        for _ in range(0, self.indx):
            n += 75
        return 500 - n

    def click(self,btn):
        return btn.last_touch.button

    def click_pos(self, btn):
        return btn.last_touch.pos


class MileDrop(StackLayout):
    b1 = ObjectProperty()
    b2 = ObjectProperty()

    def __init__(self, *args,  root=None, clicked_widget=None, **kwargs):
        super(MileDrop, self).__init__(*args, **kwargs)
        self.btn = clicked_widget
        self.root = root
        self.name = self.get_name()
        self.milestone = self.btn.parent.name
        self.reward = self.btn.parent.reward

    def change_reward(self):
        self.parent.remove_widget(self)
        content = BoxLayout(orientation='vertical')
        btn_box = BoxLayout()
        cancel_btn = Button(text='Cancel', on_press=lambda x: self.pop_cancel())
        save_btn = Button(text='Save', on_press=lambda x: self.pop_save())
        self.change_to = TextInput()

        btn_box.add_widget(save_btn)
        btn_box.add_widget(cancel_btn)
        content.add_widget(self.change_to)
        content.add_widget(btn_box)
        self.ron = MDDialog(title=f'Change Reward for: {self.name}',type='custom',content_cls=content, auto_dismiss=False)
        self.ron.open()
        Clock.schedule_once(lambda x: self.root.parent.autofocus(self.change_to), .2)

    def pop_save(self):
        self.btn.text = self.update_reward(self.change_to.text)
        MILESTONES[self.milestone]['reward'] = self.change_to.text
        MILESTONES[self.milestone]['text'] = self.btn.text
        MILESTONES[self.milestone] = MILESTONES[self.milestone]
        self.ron.dismiss()
        

    def update_reward(self, arg):
        rew = ''
        for x in self.btn.text:
            rew += x
            if rew.endswith('Reward:'):
                rew += ' '
                break
        rew += arg
        return rew


    def get_name(self):
        name = self.btn.text.replace(f'[size={MARKUP_SIZE}]', '&').replace('[/size]', '|')        
        new_name = ''
        for x in name:
            if x == '&':
                continue
            elif x == '|':
                break
            else:
                new_name += x
        return new_name if len(new_name) < 30 else new_name[:30] + '...'


    def pop_cancel(self):
        self.ron.dismiss()

    def cancel(self):
        self.parent.remove_widget(self)


class ObjectiveButton(BoxLayout):
    def __init__(self, root=None, obj_text=None, priority=None, habit=False, indx=None, *args,**kwargs):
        super(ObjectiveButton, self).__init__(*args,**kwargs)
        self.padding = [0,10,0,0]
        self.indx = indx
        self.root = root
        self.habit = habit
        self.streak = None
        self.done = False
        self.priority = priority
        self.obj_text = obj_text.replace(' ', '_')
        if self.habit == True:
            ic = 'reload'
        else:
            ic = ''
        self.obj_btn = Button(markup=True, text=obj_text,size_hint=(.8,None), color=(0,0,0,1),height=50, background_normal='', background_color=priority, background_disabled_normal='', disabled_color=root.disabled_t)
        self.hab_symb = MyIconButton(size_hint=(None,None), icon=ic)
        self.obj_check = MyIconButton(size_hint=(None,None), width= 400,height=50, icon='checkbox-blank')
        self.obj_check._set_b_color(priority)
        self.hab_symb._set_b_color(priority)


        self.hab_symb.on_press = lambda: self.pressd(self.obj_btn, self.obj_check, check=True)
        self.obj_btn.on_press = lambda: self.pressd(self.obj_btn, self.obj_check)
        self.obj_check.on_press = lambda: self.pressd(self.obj_btn, self.obj_check,check=True)
        self.add_widget(self.hab_symb)
        self.add_widget(self.obj_btn)
        self.add_widget(self.obj_check)

    def pressd(self, btn, chk, check=False):
        try:
            self.root.remove_widget(self.dropmenu)
        except:
            pass    
        if check:
            self.completed_objective(btn, chk)
        else:
            if btn.last_touch.button == 'left':
                self.completed_objective(btn,chk)
            elif btn.last_touch.button == 'right':
                if 'Dropdown' in str(self.root.children[0]):
                    self.root.remove_widget(self.root.children[0])
                drop_pos = ((self.get_x(btn.last_touch.pos[0]),self.get_y(btn.last_touch.pos[1])))
                self.make_menu(btn, drop_pos)
                self.right_clicked_widget = btn

    def get_x(self, n):
        return n + 200
    
    def get_y(self, n):
        n = 20
        for _ in range(0, self.indx):
            n += 50
        return 600 - n

    def completed_objective(self, btn, chk):
        self.completed()
        
        if self.done == True:
            if self.habit == True:
                HABITS[self.obj_text]['streak'] += 1
                if HABITS[self.obj_text]['skippable'] != 0:
                    HABITS[self.obj_text]['skippable'] -= 1
                HABITS[self.obj_text] = HABITS[self.obj_text]
                self.streak.text = str(int(self.streak.text) + 1)
            OBJECTIVES[f'{DATE_TODAY}-{self.obj_text}']['status'] = 'completed'
            OBJECTIVES[f'{DATE_TODAY}-{self.obj_text}'] = OBJECTIVES[f'{DATE_TODAY}-{self.obj_text}']
            DAILY[f'{DATE_TODAY}']['completed'] += 1
            DAILY[f'{DATE_TODAY}'] = DAILY[f'{DATE_TODAY}']
            PROFILE['init']['this_week'] += 1
            PROFILE['init']['this_month'] += 1
            PROFILE['init']['total'] += 1
            if PROFILE['init']['this_month'] > PROFILE['init']['best_month']:
                PROFILE['init']['best_month'] = PROFILE['init']['this_month']
            PROFILE['init'] = PROFILE['init']

            self.plus_hundred()
            if self.habit == True:
                try:
                    progress = MILESTONES[self.obj_text]['progress']
                    if  progress[0] < progress[1]:
                        MILESTONES[self.obj_text]['progress'] = (progress[0]+1, progress[1])
                        MILESTONES[self.obj_text] = MILESTONES[self.obj_text]
                        if progress[0] + 1 == progress[1]:
                            # make popup appear
                            self._make_popup()
                            MILESTONES[self.obj_text]['completed_date'] = f'{DATE_TODAY}'
                            MILESTONES[self.obj_text] = MILESTONES[self.obj_text]
                            text = f'[size={MARKUP_SIZE}]{self.obj_text} habit acquired![/size]\nReward: %r%'
                            ARCHIVE.put(self.obj_text, progress=MILESTONES[self.obj_text]['progress'], reward=MILESTONES[self.obj_text]['reward'], completed_date=MILESTONES[self.obj_text]['completed_date'], category=MILESTONES[self.obj_text]['category'], text=f'{text}', claimed=False)
                            year_progress = MILESTONES[f'{DATE_TODAY.year}-habits']['progress']
                            MILESTONES.delete(self.obj_text)
                            if year_progress[0] < year_progress[1]:
                                MILESTONES[f'{DATE_TODAY.year}-habits']['progress'] = (year_progress[0]+1,year_progress[1])
                                MILESTONES[f'{DATE_TODAY.year}-habits']['habit_list'].append(self.obj_text)
                                MILESTONES[f'{DATE_TODAY.year}-habits'] = MILESTONES[f'{DATE_TODAY.year}-habits']

                                if year_progress[0]+1 == year_progress[1]:
                                    MILESTONES[f'{DATE_TODAY.year}-habits']['completed_date'] = f'{DATE_TODAY}'
                                    MILESTONES[f'{DATE_TODAY.year}-habits'] = MILESTONES[f'{DATE_TODAY.year}-habits']
                                    text = f'[size={MARKUP_SIZE}]Acquired %n% new habits in {DATE_TODAY.year}![/size]\nReward: %r%'
                                    ARCHIVE.put(f'{DATE_TODAY.year}-habits', completed_date=f'{DATE_TODAY}', reward=MILESTONES[f'{DATE_TODAY.year}-habits']['reward'], progress=MILESTONES[f'{DATE_TODAY.year}-habits']['progress'], habit_list=MILESTONES[f'{DATE_TODAY.year}-habits']['habit_list'], category=MILESTONES[f'{DATE_TODAY.year}-habits']['category'], text=f'{text}', claimed=False)
                                    MILESTONES.delete(f'{DATE_TODAY.year}-habits')
                except:
                    pass  # habit acquired milestone most likely achieved already
            self.check_monthly_milestone()

        else:
            self.root.manager.popup = False
            if self.habit == True:
                HABITS[self.obj_text]['streak'] -= 1
                if HABITS[self.obj_text]['skippable'] != 0:
                    HABITS[self.obj_text]['skippable'] += 1
                HABITS[self.obj_text] = HABITS[self.obj_text]
                self.streak.text = str(int(self.streak.text) - 1)
            OBJECTIVES[f'{DATE_TODAY}-{self.obj_text}']['status'] = 'uncompleted'
            OBJECTIVES[f'{DATE_TODAY}-{self.obj_text}'] = OBJECTIVES[f'{DATE_TODAY}-{self.obj_text}']
            DAILY[f'{DATE_TODAY}']['completed'] -= 1
            DAILY[f'{DATE_TODAY}'] = DAILY[f'{DATE_TODAY}']
            PROFILE['init']['this_week'] -= 1
            PROFILE['init']['this_month'] -= 1
            PROFILE['init']['total'] -= 1
            PROFILE['init'] = PROFILE['init']

            self.plus_hundred(undo=True)
            if self.habit == True:
                if self.obj_text in ARCHIVE:
                    progress = ARCHIVE[self.obj_text]['progress']
                else:
                    progress = MILESTONES[self.obj_text]['progress']        
            
                if progress[0] == progress[1]:
                    # make popup appear

                    year_progress = ARCHIVE[f'{DATE_TODAY.year}-habits']['progress']
                    MILESTONES.put(self.obj_text, progress=progress, reward=ARCHIVE[self.obj_text]['reward'],completed_date=None, category='habit', text= f"[size={MARKUP_SIZE}]Acquire habit: {self.obj_text.replace('_',' ')} - %p%[/size]\nReward: %r%")
                    ARCHIVE.delete(self.obj_text)

                    if year_progress[0] == year_progress[1]:
                        progress = ARCHIVE[f'{DATE_TODAY.year}-habits']['progress']
                        reward = ARCHIVE[f'{DATE_TODAY.year}-habits']['reward']
                        hab_list = ARCHIVE[f'{DATE_TODAY.year}-habits']['habit_list']
                        categ = ARCHIVE[f'{DATE_TODAY.year}-habits']['category']
                        text = f'[size={MARKUP_SIZE}]Acquire %n% habits in {DATE_TODAY.year} - %p%[/size]\nReward: %r%'
                        MILESTONES.put(f'{DATE_TODAY.year}-habits', completed_date=None, reward=reward, progress=progress, habit_list=hab_list, category=categ, text=f'{text}')
                        ARCHIVE.delete(f'{DATE_TODAY.year}-habits')

                    MILESTONES[f'{DATE_TODAY.year}-habits']['progress'] = (year_progress[0]-1,year_progress[1])
                    MILESTONES[f'{DATE_TODAY.year}-habits']['habit_list'].remove(self.obj_text)
                    MILESTONES[f'{DATE_TODAY.year}-habits'] = MILESTONES[f'{DATE_TODAY.year}-habits']
                MILESTONES[self.obj_text]['progress'] = (progress[0]-1, progress[1])
                MILESTONES[self.obj_text] = MILESTONES[self.obj_text]
            self.check_monthly_milestone(undo=True)

    def _make_popup(self):
        self.root.manager.popup = True
        pop = Mypop(root=self.root, btn_text='Go to Milestones', text='Congratulations, you reached a Milestone!', font_size='18sp')
        pop.show()

    def completed(self):
        if self.done == True:
            self.done = False
        else:
            self.done = True
        if self.done == True:
            self.obj_btn.background_color = self.root.disabled_c
            self.obj_btn.color = self.root.disabled_t
            self.obj_check.icon = 'checkbox-marked'
            self.obj_check._set_b_color(self.root.disabled_c)
            self.hab_symb._set_b_color(self.root.disabled_c)
        else:
            self.hab_symb._set_b_color(self.priority)
            self.obj_btn.background_color = (self.priority)
            self.obj_btn.color = (0,0,0,1)
            self.obj_check.icon = 'checkbox-blank'
            self.obj_check._set_b_color(self.priority)

    def make_menu(self, btn, posi):
        self.dropmenu = DropdownClick(root=self.root, size_hint=(None,None), size=(150,100), pos=posi, clicked_widget=btn)
        self.root.add_widget(self.dropmenu)

    def set_streak(self, arg):
        self.streak = arg

    def getsize(self):
        return self.size

    def plus_hundred(self, undo=False):
        progress = MILESTONES['+100Objectives']['progress']
        if not undo:
            if progress[0] < progress[1]:
                MILESTONES['+100Objectives']['progress'] = (progress[0]+1, progress[1])
                MILESTONES['+100Objectives'] = MILESTONES['+100Objectives']
                if progress[0] + 1 == progress[1]:
                    self._make_popup()
                    nxt_prog = MILESTONES['+100Objectives']['progress']
                    MILESTONES['+100Objectives']['progress'] = (nxt_prog[0], nxt_prog[1]+100)
                    MILESTONES['+100Objectives']['text'] = f'[size={MARKUP_SIZE}]Road to {nxt_prog[1]+100} Objectives! - %p%[/size]\nReward: %r%'
                    MILESTONES['+100Objectives'] = MILESTONES['+100Objectives']
                    text = f'[size={MARKUP_SIZE}]Completed %n% Objectives![/size]\nReward: %r%'
                    ARCHIVE.put(f'{nxt_prog[0]}Objectives', progress=nxt_prog, reward=MILESTONES['+100Objectives']['reward'], completed_date=f'{DATE_TODAY}', category='n', text=f'{text}', claimed=False)
        else:
            if progress[0] == progress[1]-100:
                nxt_prog = MILESTONES['+100Objectives']['progress']
                MILESTONES['+100Objectives']['progress'] = (nxt_prog[0], nxt_prog[0])
                MILESTONES['+100Objectives']['text'] = f'[size={MARKUP_SIZE}]Road to {nxt_prog[1]-100} Objectives! - %p%[/size]\nReward: %r%'
                MILESTONES['+100Objectives'] = MILESTONES['+100Objectives']
                text = f'[size={MARKUP_SIZE}]Completed %n% Objectives![/size]\nReward: %r%'
                ARCHIVE.delete(f'{nxt_prog[0]}Objectives')
                MILESTONES['+100Objectives']['progress'] = (progress[0]-1, progress[1]-100)
            else:
                MILESTONES['+100Objectives']['progress'] = (progress[0]-1, progress[1])
            MILESTONES['+100Objectives'] = MILESTONES['+100Objectives']
            self.root.manager.popup = False

    def check_monthly_milestone(self, undo=False):
        mydate = f'{DATE_TODAY.year}-{DATE_TODAY.month}'
        if not undo:
            if MILESTONES[mydate]['completed_date'] != f'{DATE_TODAY}':
                progress = MILESTONES[mydate]['progress']
                if  progress[0] < progress[1]:
                    if MILESTONES[mydate]['last_progress'] != f'{DATE_TODAY}':
                        MILESTONES[mydate]['progress'] = (progress[0]+1,progress[1])
                        MILESTONES[mydate]['last_progress'] = f'{DATE_TODAY}'
                        MILESTONES[mydate]['last_completed'] = self.obj_text
                        MILESTONES[mydate] = MILESTONES[mydate]
                progress = MILESTONES[mydate]['progress']
                if progress[0] == progress[1]:    
                    self._make_popup()
                    MILESTONES[mydate]['completed_date'] = f'{DATE_TODAY}'
                    mnth = DATE_TODAY.strftime('%B')
                    text = f'[size={MARKUP_SIZE}]Monthly Objectives of {mnth} {DATE_TODAY.year} - %p%[/size]\nReward: %r%'
                    ARCHIVE.put(mydate, progress=progress, completed_date=f'{DATE_TODAY}', reward=MILESTONES[mydate]['reward'], category=MILESTONES[mydate]['category'], text=f'{text}', claimed=False, last_completed=self.obj_text)
                    MILESTONES.delete(mydate)
        else:
            self.root.manager.popup = False
            if mydate in ARCHIVE:
                progress = ARCHIVE[mydate]['progress']
                reward = ARCHIVE[mydate]['reward']

                MILESTONES.put(mydate, progress=(progress[0]-1,progress[1]), reward=reward, completed_date=None,last_progress=None,last_completed=None,category='monthly',text=f'[size={MARKUP_SIZE}]Complete 1 Objective each day - %p%[/size]\nReward: %r%')
                ARCHIVE.delete(mydate)
            else:
                progress = MILESTONES[mydate]['progress']
                if len(DAILY[f'{DATE_TODAY}']['objectives']) == 0:
                    MILESTONES[mydate]['progress'] = (progress[0]-1,progress[1])
                    MILESTONES[mydate] = MILESTONES[mydate]


class DropdownClick(StackLayout):
    obj_name = ObjectProperty()
    b1 = ObjectProperty()   # change color
    b2 = ObjectProperty()   # delete
    b3 = ObjectProperty()   # cancel
    color_box = ObjectProperty()

    def __init__(self, root, *args, edit=False, argus=None, clicked_widget=None, **kwargs):
        super(DropdownClick, self).__init__(*args, **kwargs)
        self.btn = clicked_widget
        self.root = root
        self.argus = argus
        self.displayhabit = edit
        if len(self.btn.text) < 17:
            self.obj_name.text = self.btn.text        
        else:
            self.obj_name.text = self.btn.text[:17] + '...'

        # if self.btn.parent.habit == True:
        #     self.b1.text = 'Skip'
        if self.displayhabit:
            self.b1.text = 'Edit'

    def edit(self):
        if self.b1.text == ' Edit ':
            colored_btns_layout = FloatLayout(size_hint=(None,None),size=(150,50), pos=self.b1.pos)
            btns_layout = BoxLayout(padding=(5,5),spacing=5, pos=(self.b1.pos[0]+150,self.b1.pos[1]-10))
            change_btn = Button(text='Change Name',pos=(self.b1.pos[0]+155,self.b1.pos[1]+25),size_hint=(None,None),size=(115,25), background_normal='', background_color=(0,0,0,0))
            change_btn.on_press= lambda: self.change_name()

            with btns_layout.canvas.before:
                Color(rgba=(.5,.5,.5,1))
                Rectangle(size=(125,60), pos=btns_layout.pos)
            c1=Button(size_hint=(None,None),size=(25,25), background_normal='', background_color=self.root.my_pink)
            c2=Button(size_hint=(None,None),size=(25,25), background_normal='', background_color=self.root.my_orange)
            c3=Button(size_hint=(None,None),size=(25,25), background_normal='', background_color=self.root.my_blue)
            c4=Button(size_hint=(None,None),size=(25,25), background_normal='', background_color=self.root.my_green)
            btns_layout.add_widget(c1)
            btns_layout.add_widget(c2)
            btns_layout.add_widget(c3)
            btns_layout.add_widget(c4)
            colored_btns_layout.add_widget(btns_layout)
            c1.on_press=lambda: self.update_color(c1.background_color, 1)
            c2.on_press=lambda: self.update_color(c2.background_color, 2)
            c3.on_press=lambda: self.update_color(c3.background_color, 3)
            c4.on_press=lambda: self.update_color(c4.background_color, 4)
            colored_btns_layout.add_widget(change_btn)
            self.add_widget(colored_btns_layout)

        elif self.b1.text == 'Edit':
            # check for completed amount since last skip
            # perhaps mark the objective with a skipped color
            # if habit recognizes skipped AND objectives to complete before skipable = 0 then doesn't ruin streak.
            # otherwise it goes back to streak 0.
            self.root.edit_objective(*self.argus)


    def pop_save(self):
        name = self.change_to.text.replace(' ', '_')
        name = f'{DATE_TODAY}-' + name
        old_name = f'{DATE_TODAY}-' + self.btn.text.replace(' ', '_')
        if self.change_to.text != '':
            status = OBJECTIVES[old_name]['status']
            priority = OBJECTIVES[old_name]['priority']
            habit = OBJECTIVES[old_name]['habit']
            OBJECTIVES.put(name, status=status, priority=priority, habit=habit)
            OBJECTIVES.delete(old_name)

            if old_name in DAILY[f'{DATE_TODAY}']['objectives']:
                DAILY[f'{DATE_TODAY}']['objectives'].remove(old_name)
                DAILY[f'{DATE_TODAY}']['objectives'].append(name)
                DAILY[f'{DATE_TODAY}'] = DAILY[f'{DATE_TODAY}']
            self.btn.text = self.change_to.text
            self.ron.dismiss()

    def delete(self):
        if not self.displayhabit:
            # delete the objective from the list, from the daily list, from objectives file
            name = f'{DATE_TODAY}-{self.btn.text}'.replace(' ', '_')
            OBJECTIVES.delete(name)
            DAILY[f"{DATE_TODAY}"]['objectives'].remove(name)
            DAILY[f"{DATE_TODAY}"] = DAILY[f"{DATE_TODAY}"]
            self.root.objectives_layout.remove_widget(self.btn.parent)
            self.cancel()
        else:
            # delete from ojbectives of today if its there, from daily list, if its there, from milestones and from habits.
            name = self.btn.text.replace(' ', '_')
            HABITS.delete(name)
            MILESTONES.delete(name)
            try:
                OBJECTIVES.delete(f'{DATE_TODAY}-{name}')
                DAILY[f'{DATE_TODAY}']['objectives'].remove(f'{DATE_TODAY}-{name}')
                DAILY[f'{DATE_TODAY}'] = DAILY[f'{DATE_TODAY}']
                for x in self.root.objectives_layout.children:
                    if x.children[1].text == self.btn.text:
                        self.root.objectives_layout.remove_widget(x)
                        break
            except:
                pass

            self.root.habits_layout.remove_widget(self.btn.parent)
            self.cancel()

    def update_color(self, color, indx):
        # update priority in objectives
        # update color
        self.btn.parent.children[0]._set_b_color(color)
        name = self.btn.text.replace(' ', '_')
        self.btn.parent.children[2]._set_b_color(color)
        OBJECTIVES[f'{DATE_TODAY}-{name}']['priority'] = indx
        OBJECTIVES[f'{DATE_TODAY}-{name}'] = OBJECTIVES[f'{DATE_TODAY}-{name}']
        self.btn.background_color = color
        self.cancel()

    def change_name(self):
        self.parent.remove_widget(self)
        content = BoxLayout(orientation='vertical')
        btn_box = BoxLayout()
        cancel_btn = Button(text='Cancel', on_press=lambda x: self.ron.dismiss())
        save_btn = Button(text='Save', on_press=lambda x: self.pop_save())
        self.change_to = TextInput(hint_text=self.btn.text)
        btn_box.add_widget(save_btn)
        btn_box.add_widget(cancel_btn)
        content.add_widget(self.change_to)
        content.add_widget(btn_box)
        self.ron = MDDialog(title=f'Change Name',type='custom',content_cls=content, auto_dismiss=False)
        self.ron.open()
        
        Clock.schedule_once(lambda x: self.root.parent.autofocus(self.change_to), .2)

    def cancel(self):
        self.parent.remove_widget(self)


class DiaryEntry(BoxLayout):
    btn = ObjectProperty()
    edit = ObjectProperty()
    delete = ObjectProperty()

    def __init__(self, entry_number, *args, **kwargs):
        super(DiaryEntry,self).__init__(*args, **kwargs)
        self.entry_n = entry_number
        self.MANAGER = None

    def edit_entry(self):
        from .screens import CreateEntry
        self.edit_page = CreateEntry()
        self.edit_page.edit = True
        self.edit_page.entry = self.entry_n
        self.edit_page.name='edit_page'
        self.edit_page.MANAGER = self.MANAGER
        self.MANAGER.add_widget(self.edit_page)
        self.MANAGER.current = 'edit_page'

    def delete(self):
        lay = BoxLayout(orientation='vertical',spacing=15)
        btns = BoxLayout()
        cancel = Button(text='Cancel')
        delete = Button(text='Delete', on_press=lambda x: self.confirm_delete())
        txt = Label(text=f'You are about to delete "{DIARY[str(self.entry_n)]["title"][:-4]}"', color=(0,0,0,1))
        self.pop = MDDialog(title=f'Are you sure you want to delete this?',type='custom',content_cls=lay, auto_dismiss=False)
        cancel.on_press = lambda: self.pop.dismiss()
        btns.add_widget(delete)
        btns.add_widget(cancel)
        lay.add_widget(txt)
        lay.add_widget(btns)
        self.pop.open()

    def confirm_delete(self):
        self.parent.remove_widget(self)
        for tag in ["lifestyle", "health", "family", "friends", "love", "work", "recipes"]:
            if DIARY[str(self.entry_n)][tag] == 1:
                DIARY['init'][tag].remove(self.entry_n)
        DIARY['init'] = DIARY['init']
        DIARY.delete(str(self.entry_n))
        shutil.rmtree(join(ENTRIES_FOLDER, str(self.entry_n)))
        self.pop.dismiss()

