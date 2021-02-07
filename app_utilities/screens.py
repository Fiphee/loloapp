from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from .my_paths import DAILY, DIARY, OBJECTIVES, HABITS, ARCHIVE, MILESTONES, PROFILE, TEST_FOLDER, TEST_IMAGES, TEST_THUMBS, TEMP, ENTRIES_FOLDER
from kivymd.uix.dialog import MDDialog
from .dates import DATE_TODAY, DAY_NAME
from . import custom_buttons
# from .custom_buttons import ObjectiveButton, DisplayHabit, MilestonesButton, MileDrop, ArchivedMilestoneButton, ImageButton, FolderButton, DiaryEntry
from .fileselect import FileSelector, FileLoader, FolderSelect, TagsList
from kivy.clock import Clock
from kivy.uix.stacklayout import StackLayout
from os.path import isdir, join
import os
import shutil
from kivy.core.window import Window
from .search import SearchTags, EntrySearch
# from .popups import Popup, Snackbar, Mypop, ViewEntry, CreateObjective
from . import popups
from PIL import Image as pil_img
from kivymd.uix.snackbar import Snackbar
from kivy.uix.popup import Popup

global DIARY

class SideNav(StackLayout):
    pass

class ScreenOne(Screen, Widget):
    obj_color = ListProperty([.8,.8,.8,1])
    my_pink = ListProperty([1.0, 0.529, 0.749, 1])
    my_orange = ListProperty([1.0, 0.709, 0.396, 1])
    my_blue = ListProperty([0.396, 0.752, 1.0, 1])
    my_green = ListProperty([0.607, 0.925, 0.498, 1])
    disabled_t = ListProperty([0.69, 0.552, 0.011,1])
    disabled_c = ListProperty([0.992, 0.901, 0.525,1])

    highlight = ListProperty([0.6, 1.0, 0.6, 1])

    r = ListProperty([0.69, 0.552, 0.011,1])
    r2 = ListProperty([.101,.101,.101,1])
    
    b = ObjectProperty()
    main_container = ObjectProperty()
    habits_layout = ObjectProperty()
    # sidenav = ObjectProperty()
    profile_info_box = ObjectProperty()
    profile_picture_btn = ObjectProperty()
    edit_profile = ObjectProperty()
    create_objective_btn = ObjectProperty()
    create_habit_btn = ObjectProperty()
    diary_btn = ObjectProperty()
    objectives_layout = ObjectProperty()
    habit_list = {}
    habit = False
    right_clicked_widget = None
    
    def __init__(self,*args,**kwargs):
        super(ScreenOne, self).__init__(*args,**kwargs)
        self.priority_colors = {1:self.my_pink,2:self.my_orange,3:self.my_blue,4:self.my_green}
        Clock.schedule_once(lambda x: self.load_habits())
        self.start = True

    def load_habits(self):
        self.habits_layout.clear_widgets()
        self.habit_list = {}
        try:
            indx = 0
            for x in HABITS:
                if x == 'init':
                    continue
                name = x
                streak = str(HABITS[name]['streak'])
                the_day = HABITS[name]['started']
                days = HABITS[name]['repeats']
                priority = HABITS[name]['priority']
                han = custom_buttons.DisplayHabit(root=self, hab_text=name.replace('_', ' '), indx=indx, streak=streak, size_hint_y=None, height=50, argus=[name, self, True, the_day, days, priority, True, ])
                self.habits_layout.add_widget(han)
                for d in days:
                    if days[d] == DAY_NAME:
                        if f'{DATE_TODAY}' not in DAILY:
                            DAILY.put(f'{DATE_TODAY}', objectives=[], completed=0)
                        if f'{DATE_TODAY}-{x}' not in DAILY[f'{DATE_TODAY}']['objectives']:
                            OBJECTIVES.put(f'{DATE_TODAY}-{x}', status='uncompleted', priority=priority, habit=True)
                            DAILY[f'{DATE_TODAY}']['objectives'].append(f'{DATE_TODAY}-{x}')
                            DAILY[f'{DATE_TODAY}'] = DAILY[f'{DATE_TODAY}'] 
                indx += 1
                self.habit_list[x] = han.hab_streak
        except:
            pass
        if self.start:
            Clock.schedule_once(lambda x: self.load_objectives())
            self.start == False

    def load_objectives(self):
        self.objectives_layout.clear_widgets()
        try:
            indx = 1
            for i in range(2):
                if i == 0:
                    c = 'uncompleted'
                else:
                    c = 'completed'
                for x in DAILY[f'{DATE_TODAY}']['objectives']:
                    if OBJECTIVES[x]['status'] != c:
                        continue
                    name = x.split('-')
                    name = name[-1]
                    if OBJECTIVES[x]['habit'] == True:
                        habit = True
                    else: 
                        habit = False
                    priority = self.priority_colors[OBJECTIVES[x]['priority']]
                    obj = custom_buttons.ObjectiveButton(root=self, obj_text=name.replace('_', ' '), priority=priority, size_hint_y=None, height=50, indx=indx, habit=habit)
                    if OBJECTIVES[x]['habit'] == True:
                        obj.set_streak(self.habit_list[name])
                    if OBJECTIVES[x]['status'] == 'completed':
                        obj.completed()
                    self.objectives_layout.add_widget(obj)
                    indx += 1
        except:
            pass

    def make(self):
        obj = custom_buttons.ObjectiveButton(obj_text='Ey', size_hint_y=None, height=50)
        self.objectives_layout.add_widget(obj)

    def edit_objective(self, name, root, edit, date_picked, days, priority, habit):
        editing = popups.CreateObjective(name=name, root=root, edit=True, date_picked=date_picked, days=days, priority=priority, habit=habit,)
        ron = MDDialog(title='Name', type='custom', content_cls=editing, auto_dismiss=False)
        editing._set_pop(ron)
        ron.open()
    
    def create_objective(self, habit=None):
        pop = popups.CreateObjective(root=self, habit=habit)
        pop.days = {}
        ron = MDDialog(title='Name',type='custom',content_cls=pop, auto_dismiss=False)
        pop._set_pop(ron)
        ron.open()

    def _make_popup(self):
        self.manager.popup = True
        pop = popups.Mypop(root=self, btn_text='Go to Milestones', text='Congratulations, you reached a Milestone!', font_size='18sp')
        pop.show()

    def debug(self):
        # self._make_popup()
        pass
    
    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        if 'Dropdown' in str(self.children[0]):
            position = self.children[0].pos
            if touch.x < position[0] or touch.x > position[0] + 150 and touch.y > position[1] + 200 or touch.y < position[1]:
                self.remove_widget(self.children[0])

    def popup(self):
        self.manager.current = 'milestones'


class Milestones(Screen):
    obj_color = ListProperty([.8,.8,.8,1])
    my_pink = ListProperty([1.0, 0.529, 0.749, 1])
    my_orange = ListProperty([1.0, 0.709, 0.396, 1])
    my_blue = ListProperty([0.396, 0.752, 1.0, 1])
    my_green = ListProperty([0.607, 0.925, 0.498, 1])
    disabled_c = ListProperty([0.992, 0.901, 0.525,1])
    disabled_t = ListProperty([0.69, 0.552, 0.011,1])
    highlight = ListProperty([0.6, 1.0, 0.6, 1])
    
    archived_btn = ObjectProperty()
    in_progress_btn = ObjectProperty()
    b = ObjectProperty()
    main_container = ObjectProperty()
    sidenav = ObjectProperty()
    profile_info_box = ObjectProperty()
    profile_picture_btn = ObjectProperty()
    edit_profile = ObjectProperty()
    create_objective_btn = ObjectProperty()
    diary_btn = ObjectProperty()
    milestones_list = ObjectProperty()
    active = None
    popup = None

    def on_pre_enter(self):
        self.popup = self.manager.popup     

    def on_enter(self):
        if self.popup:
            try:
                self.load_archived()
            except:
                pass
            self.manager.popup = False
        else:
            try:
                self.load_milestones()
            except:
                pass

    def load_archived(self):
        self.active = 'completed'
        self.archived_btn.color = [.5,.5,.5,1]
        self.archived_btn.background_color = self.highlight
        self.in_progress_btn.background_color = [.5,.5,.5,1]
        self.in_progress_btn.color = [1,1,1,1]
        self.milestones_list.clear_widgets()
        for i in range(2):
            if i == 0:
                cl = False
            else:
                cl = True
            for x in ARCHIVE:
                if x == 'init':
                    continue
                if ARCHIVE[x]['claimed'] == cl:
                    rew = ARCHIVE[x]['reward']
                    prog = ARCHIVE[x]['progress']
                    m_t = str(ARCHIVE[x]['category'])
                    text = str(ARCHIVE[x]['text'])
                    milestone = custom_buttons.MilestonesButton(self, active='completed', disabled=cl, name=x, text=text, archive=True, progress=prog, reward=rew, m_category=m_t, size_hint_y=None, height=75)

                    self.milestones_list.add_widget(milestone)
            
    def load_milestones(self):
        self.active = 'progress'
        self.archived_btn.color = [1,1,1,1]
        self.archived_btn.background_color = [.5,.5,.5,1]
        self.in_progress_btn.background_color = self.highlight
        self.in_progress_btn.color = [.5,.5,.5,1]
        self.milestones_list.clear_widgets()
        indx = 0
        for x in MILESTONES:
            if x == 'init':
                continue
            if MILESTONES[x]['completed_date'] == None:
                prog = MILESTONES[x]['progress']
                rew = MILESTONES[x]['reward']
                m_t = MILESTONES[x]['category']
                text = str(MILESTONES[x]['text'])
                milestone = custom_buttons.MilestonesButton(self, name=x, text=text, active='progress', progress=prog, reward=rew, m_category=m_t, size_hint_y=None, height=75, indx=indx)
                self.milestones_list.add_widget(milestone)
                indx += 1

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        if 'MileDrop' in str(self.children[0]):
            position = self.children[0].pos
            if touch.x < position[0] or touch.x > position[0] + 150 and touch.y > position[1] + 200 or touch.y < position[1]:
                self.remove_widget(self.children[0])


class CreateEntry(Screen):
    paper_color = ListProperty([0.945, 0.882, 0.752, 1])
    img_box = ObjectProperty()
    add_image = ObjectProperty()
    entry_title = ObjectProperty()
    content = ObjectProperty()
    n = NumericProperty(8)
    highlight = ListProperty([0.6, 1.0, 0.6, 1])
    MANAGER = None

    def __init__(self, edit=False, entry=None, manager=None, *args,**kwargs):
        super(CreateEntry,self).__init__(*args,**kwargs)
        Clock.schedule_once(lambda x: self.load_slots(),.2)
        self.MANAGER = manager
        self.edit = edit
        self.entry = entry
        self.next_gallery_slot = 0
        self.tag_list = set()
        self.pics = {}
        self.currently_shown = None
        self.old_tags = []
        
    def on_leave(self):
        shutil.rmtree(TEST_FOLDER)
        self.MANAGER.remove_widget(self)
        from .my_paths import get_profile, get_diary
        global DIARY
        DIARY = get_diary()
        global PROFILE
        PROFILE = get_profile()
        if not self.edit:
            self.MANAGER.add_widget(CreateEntry(name='create_entry', manager=self.MANAGER))
        del(self)


    def on_enter(self):
        if not isdir(TEST_FOLDER):
            os.mkdir(TEST_FOLDER)
            os.mkdir(TEST_IMAGES)
            os.mkdir(TEST_THUMBS)

        if self.edit:
            self.load_entry_details()

    def load_entry_details(self):
        entry = str(self.entry)
        title = DIARY[entry]['title'][:-4]
        content = DIARY[entry]['content']
        thumbs = DIARY[entry]['thumbnails']
        pics = DIARY[entry]['pics']
        self.entry_title.text = title
        text = ''
        with open(join(DIARY[entry]['path'], content)) as txt:
            for character in txt:
                text += character
        self.content.text = text

        self.old_tags = []
        tags = ["lifestyle", "health", "family", "friends", "love", "work", "recipes"]
        for tag in tags:
            if DIARY[entry][tag] == 1:
                self.tag_check(tag.capitalize(), True)
                self.old_tags.append(tag)
        for img in range(0,len(pics)):
            self.add_new_slot(pics[img], thumbs[img])

    def _add_img(self):
        if len(PROFILE['init']['image_folders']) == 0:
            popups.Mypop(root=self, btn_text='Select folders here', text="You don't have any image folders saved. Please select folders to search images in", size_hint_x=.8).show()
            return 0
        file_select = FileSelector()
        file_select.root = self
        self.add_widget(file_select)
        file_select.show()

    def popup(self):
        self._pick_folders()

    def save(self, edit=False):
        if not self.edit:
            entry_n = PROFILE['init']['last_diary'] 
            entry_n += 1
        else:
            entry_n = str(self.entry) 
            old_pics = DIARY[entry_n]['pics']
            old_thumbs = DIARY[entry_n]['thumbnails']
        

        entry_folder = join(ENTRIES_FOLDER, f'{entry_n}')
        images_folder = join(entry_folder, 'images')
        thumbnails_folder = join(images_folder, 'thumbs')
        
        # create folders for the entry
        if not self.edit:
            os.mkdir(entry_folder)
            os.mkdir(images_folder)
            os.mkdir(thumbnails_folder)
        else:
            os.remove(join(entry_folder, DIARY[entry_n]['title']))

        title = f'{self.entry_title.text}.txt'           
        content = join(entry_folder, title)
        # save text content to file
        with open(title, 'w') as txt:
            txt.write(self.content.text)
        shutil.move(title, entry_folder, title)

        # save image and thumbnails to entry folder
        pics = []
        thumbnails = []
        for image in self.img_box.children:
            if hasattr(image, 'indx') and image.pic != '':
                full_pic = join(images_folder, image.get_name(image.img))
                thmb = join(thumbnails_folder, image.get_name(image.pic))
                with pil_img.open(image.img) as im:
                    im.save(full_pic)
                with pil_img.open(image.pic) as thumb:
                    thumb.save(thmb)
                pics.insert(0, full_pic)
                thumbnails.insert(0, thmb)

        # save infos to json storage
        if not self.edit:
            DIARY.put(entry_n, title=title, content=content, path=entry_folder, pics=pics, thumbnails=thumbnails, date_created=f'{DATE_TODAY}', date_deleted=None, lifestyle=0, health=0, family=0, friends=0, love=0, work=0, recipes=0, day=f"{DATE_TODAY.strftime('%A')}", month=f"{DATE_TODAY.strftime('%B')}")
            
        else:
            DIARY[entry_n]['title'] = title
            DIARY[entry_n]['content'] = content
            DIARY[entry_n]['pics'] = pics
            DIARY[entry_n]['thumbnails'] = thumbnails
            self.delete_unused_images(old_pics, pics)
            self.delete_unused_images(old_thumbs, thumbnails)
        for tag in self.tag_list:
            DIARY[entry_n][tag.lower()] = 1
            if not self.edit:
                DIARY['init'][tag.lower()].append(entry_n)
            else:
                if tag.lower() in self.old_tags:
                    self.old_tags.remove(tag.lower())
                    continue
                taglist = DIARY['init'][tag.lower()]
                if len(taglist) == 0:
                    DIARY['init'][tag.lower()].append(int(entry_n))
                else:
                    DIARY['init'][tag.lower()] = self._insert_entry_in_taglist(taglist, entry_n)
        for tag in self.old_tags:
            DIARY['init'][tag.lower()].remove(int(entry_n))
            DIARY[entry_n][tag.lower()] = 0

        DIARY[entry_n] = DIARY[entry_n]

        if not self.edit:
            PROFILE['init']['last_diary'] += 1
            DIARY['init']['total'] += 1
        PROFILE['init'] = PROFILE['init']
        DIARY['init'] = DIARY['init']
        Snackbar(text='Entry Successfully saved!').show()
        self.MANAGER.current = 'diary'

    def delete_unused_images(self, old, new):
        for img in old:
            if img not in new:
                os.remove(img)

    def _insert_entry_in_taglist(self, tag, n):
        n = int(n)
        my_list = tag[:]
        L = 0
        R = len(my_list) - 1
        if n < my_list[L]:
            my_list.insert(L, n)
            return my_list
        elif n > my_list[R]:
            my_list.append(n)
            return my_list

        found_spot = False
        while not found_spot:
            mid = L + (R-L)// 2
            left = mid - 1
            right = mid + 1
            if my_list[mid] > n:
                if my_list[left] < n:
                    my_list.insert(mid, n)
                    found_spot = True
                    return my_list
                R = mid
            elif my_list[mid] < n:
                if my_list[right] > n:
                    my_list.insert(right, n) 
                    found_spot = True                   
                    return my_list
                L = mid
        
    def _check_in(self, tag, entry_n):
        L = 0 
        R = len(tag)-1
        while L <= R:
            mid = L + (R-L)//2
            if tag[mid] == entry_n:
                return mid
            elif tag[mid] < entry_n:
                L = mid + 1
            elif tag[mid] > entry_n:
                R = mid - 1
        else:
            return -1


    def do(self):
        print('doy')

    def load_slots(self):
        self.img_box.add_widget(custom_buttons.ImageButton(indx=0, root=self))
        self.img_box.add_widget(custom_buttons.ImageButton(indx=1, root=self))
        self.img_box.add_widget(custom_buttons.ImageButton(indx=2, root=self))
        self.img_box.add_widget(custom_buttons.ImageButton(indx=3, root=self))
        self.img_box.slots = 4

    def add_new_slot(self, source, thumb):
        if self.next_gallery_slot != self.img_box.slots:
            img = self.img_box.children[self.get_indx(self.next_gallery_slot)]
            img.pic = thumb
            img.img = source  
        else:
            img = custom_buttons.ImageButton(indx=self.img_box.slots, root=self)
            img.pic = thumb
            img.img = source
            self.img_box.add_widget(img)
            self.img_box.slots += 1
        self.pics[self.next_gallery_slot] = source
        self.next_gallery_slot += 1

    def get_indx(self, n):
        return (self.img_box.slots - n) -1          # true parent/child index

    def _pick_folders(self):
        self.folder_layout = FolderSelect(root=self)
        self.parent.add_path = True
        self.my_pop = Popup(title='Manage Image Folders', content=self.folder_layout, size_hint=(.5,.75), auto_dismiss=False, separator_color= (.1,.1,.1,1), separator_height='1dp', title_align='center')
        self.my_pop.open()
        for folder in PROFILE['init']['image_folders']:
            self._add_folder(folder)

    def _add_folder(self, folder):
        display_folder = custom_buttons.FolderButton(folder)
        self.folder_layout.listed_folders.add_widget(display_folder)
        
    def show_tags(self, root, pos=None):
        self.add_widget(TagsList(root=root, pos=pos))

    def tag_check(self, tag, state):
        if state == True:
            self.tag_list.add(tag)
        else:
            self.tag_list.remove(tag)


class Diary(Screen):
    diary_list = ObjectProperty()
    search_area = ObjectProperty()
    search_box = ObjectProperty()
    obj_color = ListProperty([.8,.8,.8,1])
    now_on_screen = None
    search_tags = []
    search_list = DIARY
    num_of_entries = DIARY['init']['total']

    def __init__(self, *args, **kwargs):
        super(Diary,self).__init__(*args, **kwargs)
        Clock.schedule_once(lambda x: self.search_area.add_widget(SearchTags(root=self, manager=self.parent)))
        Window.bind(on_key_down=self._on_keyboard_down)

    def on_enter(self):
        from .my_paths import get_diary, get_profile
        global DIARY
        DIARY = get_diary()
        global PROFILE
        PROFILE = get_profile()
        self.diary_list.clear_widgets()
        self.currently_loaded = DIARY['init']['total']
        self.search_list = DIARY
        self.load_more()
        if self.now_on_screen != None:
            self.view._update_infos()

    def show_entries(self):
        up_to = self.currently_loaded - 20
        if up_to < 0:
            up_to = 0
        for entry in range(self.currently_loaded,up_to,-1):
            try:
                self.add_entry(entry)
            except:
                pass  # in case an entry was deleted it can skip over it
        self.currently_loaded = up_to

    def load_more(self):
        if self.search_list == DIARY:
            self.show_entries()
        else:
            for _ in range(20):
                try:
                    entry = self.search_list.pop(-1)
                    self.add_entry(entry)
                except:
                    pass

    def add_entry(self, entry):
        DIARY[f'{entry}']['title']
        shown_entry = custom_buttons.DiaryEntry(entry)
        shown_entry.MANAGER = self.MANAGER
        shown_entry.btn.text = self._make_entry_text(f'{entry}') 
        shown_entry.btn.on_press = lambda entry=entry: self.view_entry(entry)
        self.diary_list.add_widget(shown_entry)

    def view_entry(self, entry_n):
        self.view = popups.ViewEntry(self, self.MANAGER)
        self.view.entry = entry_n
        self.add_widget(self.view)
        self.view.show()

    def _make_entry_text(self, entry_n):
        created = DIARY[entry_n]['date_created']
        title = DIARY[entry_n]['title'][:-4]
        return f'{created}  -  {title}'

    def search(self):
        self.diary_list.clear_widgets()
        self.currently_loaded = 0
        query = self.search_box.text
        self._search(self.search_tags, query)


    def _search(self, search_in, query):
        try:
            del(self.search_utils)
        except:
            pass
        self.search_utils = EntrySearch(search_in, query)   
        queries = self.search_utils.separate_queries()
        entries = self.search_utils.get_entry_list(queries)
        self.search_list = entries
        self.load_more()
        Clock.schedule_once(lambda x: self.focus_search(),.1)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.search_box.focus and keycode == 40:  # 40 - Enter key pressed
            self.search()

    def focus_search(self):
        self.search_box.focus = True