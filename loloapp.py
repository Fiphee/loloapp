from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics','width',1200)
Config.set('graphics','height',700)
Config.set('graphics', 'resizable', False)
import calendar
from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.animation import Animation, AnimationTransition
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.uix.stacklayout import StackLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.button import ButtonBehavior
from kivy.uix.colorpicker import ColorPicker
from kivymd.uix.button import MDRoundFlatButton, MDFlatButton, MDRectangleFlatIconButton, MDIconButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Rectangle
from kivymd.uix.dialog import MDDialog
from kivy.uix.textinput import TextInput
from datetime import date, datetime, timedelta
from kivy.storage.jsonstore import JsonStore
from kivy.uix.scrollview import ScrollView
from os.path import join, isdir
from kivy.clock import Clock
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivy.uix.popup import Popup
from kivymd.uix.picker import MDDatePicker
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.snackbar import Snackbar
from kivy.uix.image import Image
from datetime import date, datetime, timedelta
import shutil
from time import ctime
from PIL import Image as pil_img
import os
import ntpath
import re

data_dir = App().user_data_dir
app_folder = join(data_dir, 'loloapp')
if not isdir(app_folder):
    os.mkdir(app_folder)    
    os.mkdir(join(app_folder, 'entries'))
    os.mkdir(join(app_folder, 'misc'))
    os.mkdir(join(app_folder, 'temp'))

DATE_TODAY = date.today()
# o = timedelta(days=1)
# o = DATE_TODAY + o
# o = str(o).split(' ')
# DATE_TODAY = datetime.strptime(o[0], '%Y-%m-%d') 
# DATE_TODAY = datetime.strptime(DATE_TODAY, '%Y-%m-%d') 

DAY_NAME = DATE_TODAY.strftime('%A')
DAILY = JsonStore(join(app_folder, 'daily.json'))
OBJECTIVES = JsonStore(join(app_folder, 'objectives.json'))
HABITS = JsonStore(join(app_folder, 'habits.json'))
MILESTONES = JsonStore(join(app_folder, 'milestones.json'))
PROFILE = JsonStore(join(app_folder, 'profile.json'))
ARCHIVE = JsonStore(join(app_folder, 'archive.json'))
DIARY = JsonStore(join(app_folder, 'diary.json'))
ENTRIES_FOLDER = join(app_folder, "entries")

MARKUP_SIZE = 25
# temporary and other directories
TEMP = join(app_folder, 'temp')
TEST_FOLDER = join(ENTRIES_FOLDER, 'current')
TEST_IMAGES = join(TEST_FOLDER, 'images')
TEST_THUMBS = join(TEST_IMAGES, 'thumbs')


if f'{DATE_TODAY}' not in MILESTONES:
    MILESTONES.put(f'{DATE_TODAY}', progress=('',''), reward='', completed_date=None, category='daily', text=f'[size={MARKUP_SIZE}]Complete all objectives today[/size]\nReward: %r%')
try: 
    DAILY['init']['status']
except:
    DAILY.put('init', status='exists')
    DAILY.put(f'{DATE_TODAY}', objectives=[], completed=0)
    DIARY.put('init', lifestyle=[], health=[], family=[], friends=[], love=[], work=[], recipes=[], total=0)
    OBJECTIVES.put('init', status='exists')
    HABITS.put('init', status='exists')
    MILESTONES.put('init',status='exists')
    MILESTONES.put(f'{DATE_TODAY.year}-habits', progress=(0,4), reward='', completed_date=None, category='yearly', habit_list=[], text=f'[size={MARKUP_SIZE}]Acquire %n% habits in {DATE_TODAY.year} - %p%[/size]\nReward: %r%')
    MILESTONES.put('+100Objectives', reward='', progress=(0,100), completed_date=None, category='general', text=f'[size={MARKUP_SIZE}]Road to 100 Objectives! - %p%[/size]\nReward: %r%')
    MILESTONES.put(f'{DATE_TODAY.year}-{DATE_TODAY.month}', progress=(0,calendar.monthrange(DATE_TODAY.year, DATE_TODAY.month)[1]), reward='', completed_date=None, last_progress=None, last_completed=None, category='monthly', text=f'[size={MARKUP_SIZE}]Complete 1 Objective each day - %p%[/size]\nReward: %r%')

    PROFILE.put('init', checked_habits='unchecked', status='exists', this_month=0, this_week=0, best_month=0, total=0, this_year={}, reset_week=True, month=DATE_TODAY.month, year=DATE_TODAY.year, archive={}, username="User", profile_pic="", image_folders=[], last_diary=0)
    ARCHIVE.put('init', status='exists')

d = timedelta(days=-1)
d = DATE_TODAY + d
Y = d
d = str(d).split(' ')
YESTERDAY = d[0]
MAKE_POP = False
if YESTERDAY in MILESTONES:
    try:
        if DAILY[YESTERDAY]['completed'] == len(DAILY[YESTERDAY]['objectives']) and len(DAILY[YESTERDAY]['objectives']) != 0:
            yesterdays_day = datetime.strptime(YESTERDAY, '%Y-%m-%d')
            thistext = f"[size={MARKUP_SIZE}]You completed all Objectives set![/size] [size=18] {YESTERDAY} [/size]\nReward: %r%"
            ARCHIVE.put(f'{YESTERDAY}', progress=('',DAILY[YESTERDAY]['completed']),reward=MILESTONES[YESTERDAY]['reward'],completed_date=f'{YESTERDAY}', category='daily', text=thistext, claimed=False)
            MAKE_POP = True
    except:
        pass
    MILESTONES.delete(f'{YESTERDAY}')


if len(HABITS) > 1:
    if PROFILE['init']['checked_habits'] != YESTERDAY:
        for x in HABITS:
            if x == 'init':
                continue
            check = f'{YESTERDAY}-{x}'
            PROFILE['init']['checked_habits'] = YESTERDAY
            PROFILE['init'] = PROFILE['init']
            try:
                state = OBJECTIVES[check]['status']
                if state == 'uncompleted':
                    if HABITS[x]['skippable'] != 0:
                        HABITS[x]['streak'] = 0
                        HABITS[x] = HABITS[x]
                    else:
                        HABITS[x]['skippable'] = 5
                        HABITS[x] = HABITS[x]
            except:
                pass

if DAY_NAME == 'Monday':        # handle resetting of objectives done in the week on mondays
    if PROFILE['init']['reset_week'] == True:
        PROFILE['init']['this_week'] = 0
        PROFILE['init']['reset_week'] = False
        PROFILE['init'] = PROFILE['init']

elif DAY_NAME == 'Tuesday':     # set it up so next monday it knows to reset. This is to avoid reset twice on the same monday
    PROFILE['init']['reset_week'] = True
    PROFILE['init'] = PROFILE['init']
    
if DATE_TODAY.month != PROFILE['init']['month']:    # resets month objective count
    PROFILE['init']['this_year'][PROFILE['init']['month']] = PROFILE['init']['this_month']
    PROFILE['init']['month'] = DATE_TODAY.month
    PROFILE['init']['this_month'] = 0
    PROFILE['init'] = PROFILE['init']
    MILESTONES.put(f'{DATE_TODAY.year}-{DATE_TODAY.month}', progress=(0,calendar.monthrange(DATE_TODAY.year, DATE_TODAY.month)[1]), reward='', completed_date=None, last_progress=None, last_completed=None, category='monthly')

if DATE_TODAY.year != PROFILE['init']['year']:      # resets year objective count
    PROFILE['init']['archive'][PROFILE['init']['year']] = PROFILE['init']['this_year']
    PROFILE['init']['year'] = DATE_TODAY.year
    PROFILE['init']['this_year'] = {}
    PROFILE['init'] = PROFILE['init']


def __get_date(entity):
    date_pattern = r'^[0-9]+-[0-9]+-[0-9]+'
    check_date = re.match(date_pattern, entity)
    if check_date == None:
        return None,None,None
    entity_date_string = check_date.group()
    entity_date = datetime.strptime(entity_date_string, '%Y-%m-%d')
    return entity_date, datetime.strptime(YESTERDAY, '%Y-%m-%d'), entity_date_string

for obj in OBJECTIVES:
    if obj != 'init':
        dates = __get_date(obj)
        if dates[0] == None:
            continue
        if dates[0] < dates[1]:
            OBJECTIVES.delete(obj)
            if dates[2] in DAILY:
                DAILY.delete(dates[2])
for milestone in MILESTONES:
    dates = __get_date(milestone)
    if dates[0] == None:
        continue
    if dates[0] <= dates[1]:
        MILESTONES.delete(milestone)


Builder.load_string('''


<SideNav@StackLayout>:                                                    # Sidenav
    id: sidenav
    size_hint: .15, 1
    orientation: 'tb-lr'
    # Profile name, profile picture perhaps
    spacing: 5
    Label: #spacer
        size_hint: 1,.03

    BoxLayout:                                                  # Profile info box
        id: profile_info_box
        size_hint: 1,.3
        orientation: 'vertical'
        spacing: 10
        MDLabel:
            text: app.username
            padding: 10,10
            size_hint: 1,.15
            halign: 'center'
            font_size: '30px'
        Image:
            source: app.profile_pic
            size_hint_y: None
            width: 100
            allow_strech: False

        # Button:
        #     id: profile_picture_btn
        #     size_hint: 1,.7
        #     background_down: ''
        #     background_normal: app.profile_pic
        #     on_press: app.m.scr_one.debug()

        RoundedCutButton:
            id: edit_profile
            text: 'Change Name'
            size_hint:1,.1      
            on_press: app.change_name()    

    RoundedButton:                                                     # Home Btn
        id: milestones_btn
        text: 'Home'
        size_hint: 1,.05
        on_press:
            app.m.current = 'scr_one'

    RoundedButton:                                                     # Milestones Btn
        id: milestones_btn
        text: 'Milestones'
        size_hint: 1,.05
        on_press:
            app.m.current = 'milestones'

    RoundedButton:                                                     # Diary Btn
        id: diary_btn
        text: 'Diary'
        size_hint: 1,.05
        on_press:
            app.m.current = 'diary'

<RoundedButton@Button>:
    background_color: 0,0,0,0
    canvas.before:
        Color:
            rgba:(.3,.3,.3,1)
        RoundedRectangle:
            size:self.size
            pos:self.pos
            radius: [18]

<RoundedCutButton@Button>:
    background_color: 0,0,0,0
    canvas.before:
        StencilPush
        RoundedRectangle:
            size: self.size[0] -2, self.size[1]-2
            pos: self.pos[0] + 1, self.pos[1] + 1
            radius: [17]
        StencilUse
        Color:
            rgba:(.3,.3,.3,1)
        RoundedRectangle:
            size:self.size
            pos:self.pos
            radius: [18]
        StencilUnUse

        RoundedRectangle:
            size: self.size[0] -2, self.size[1]-2
            pos: self.pos[0] + 1, self.pos[1] + 1
            radius: [17]
        StencilPop
            
<Mypop@Snackbar>:
    snackbar_x: "20dp"
    snackbar_y: "20dp"
    size_hint_x: .6
    pos_hint: {"center_x":.7}
    duration: 4

<ArchivedMilestoneButton@Button>:
    background_disabled_normal: '' 
    disabled_color: root.disabled_t

<ObjSwitch@MDSwitch>:
    on_active:
        root.switch()

<MyIconButton@MDIconButton>:
    canvas.before:
        Color: 
            rgba: root.c
        Rectangle:
            size: self.size[0],self.size[0]+2
            pos: self.pos
    theme_text_color: 'Custom'
    text_color: root.disabled_t

<MileDrop@StackLayout>:
    b1: b1
    b2: b2
    canvas.before:
        Color:
            rgba: .5,.5,.5,1
        Rectangle:
            size: self.size
            pos: self.pos
    # obj_name: obj_name
    # Label:
    #     id: obj_name
    #     text: ''
    #     size_hint: 1,.25
    Button:
        id: b1
        text: 'Change Reward'
        size_hint: 1,.5   
        on_press:
            root.change_reward()
    Button:
        id: b2
        text: 'Cancel'
        size_hint: 1,.5
        on_press:
            root.cancel()

<DropdownClick@StackLayout>:
    b1: b1
    b2: b2
    b3: b3
    canvas.before:
        Color:
            rgba: .5,.5,.5,1
        Rectangle:
            size: self.size
            pos: self.pos
    obj_name: obj_name
    Label:
        id: obj_name
        text: ''
        size_hint: 1,.25
    Button:
        id: b1
        text: ' Edit '
        size_hint: 1,.25    
        on_press:
            root.edit()  
    Button:
        id: b2
        text: 'Delete'
        size_hint: 1,.25
        on_press:
            root.delete()
    Button:
        id: b3
        text: 'Cancel'
        size_hint: 1,.25
        on_press:
            root.cancel()

<ScreenOne>:
    habits_layout: habits_layout
    objectives_layout: objectives_layout
    
    BoxLayout:                                                          # main container
        id: main_container
        orientation: 'horizontal'
        spacing: 5
        padding: 5,0,0,0
        SideNav:
        
        BoxLayout:
            canvas.before:
                Color:
                    rgba: .7,.7,.7,1
                Rectangle:
                    size: self.size
                    pos: self.pos

            id: main_layout
            size_hint: .85, 1
            FloatLayout:                                                # float layout for main screen
                size_hint: 1,1
                # EffectWidget:
                #     size_hint: .5,.05
                #     FXAAEffect:
                #     RoundedButton:
                #         text: 'Test'

                BoxLayout:                                              # Objective layout
                    canvas.before:
                        Color:
                            rgba: root.obj_color
                        Rectangle:
                            size: self.size
                            pos: self.pos

                    # id: objectives_layout
                    orientation: 'vertical'
                    size_hint: None,None
                    size: 400,550
                    pos_hint: {'x':.05, 'y':.1}
                    BoxLayout:
                        padding: 15,0,15,0
                        pos_hint: {'top':1}
                        size_hint: 1,.1
                        Label:
                            text: "Today's Objectives"
                            font_size: '30px'
                        MDIconButton:
                            id: create_objective_btn
                            theme_text_color: 'Custom'
                            text_color: 1,1,1,1
                            pos_hint: {'center_y':.46}
                            icon: 'plus-circle'
                            user_font_size: '32sp'
                            on_press:
                                root.create_objective()
                    ScrollView:
                        size_hint: 1, .85
                        StackLayout:
                            size_hint_y: None
                            height: self.minimum_height
                            id: objectives_layout

                BoxLayout:                                              # Habits layout
                    canvas.before:
                        Color:
                            rgba: root.obj_color
                        Rectangle:
                            size: self.size
                            pos: self.pos
                    orientation: 'vertical'
                    size_hint: None,None
                    size: 400,550
                    pos_hint: {'x':.5, 'y':.1}
                    BoxLayout:
                        padding: 15,0,15,0
                        pos_hint: {'top':1}
                        size_hint: 1,.1
                        Label:
                            text: "Habits"
                            font_size: '30px'
                        MDIconButton:
                            id: create_habit_btn
                            theme_text_color: 'Custom'
                            text_color: 1,1,1,1
                            pos_hint: {'center_y':.46}
                            icon: 'plus-circle'
                            user_font_size: '32sp'
                            on_press:
                                root.create_objective(habit=True)
                    ScrollView:
                        size_hint: 1, .85
                        StackLayout:
                            size_hint_y: None
                            height: self.minimum_height
                            id: habits_layout

######################################################################################################################
################################################### DIARY ############################################################
######################################################################################################################

<DiaryEntry@BoxLayout>:
    btn: btn
    size_hint_y: None
    height: self.minimum_height
    Button:
        id: btn
        size_hint: .8,None
        height: 50
        text: ''
        halign: 'left'
        font_size: 18
        text_size: self.size[0]-25,25
    MDIconButton:
        id: edit
        icon:'file-document-edit'
        size_hint_y: None
        size: 50,50
        on_press: 
            root.edit_entry()

    MDIconButton:
        id: delete
        icon: 'close'
        size_hint_y: None
        size: 50,50
        on_press:
            root.delete()

<SearchTags@BoxLayout>:

<Diary>:
    diary_list: diary_list
    search_area: search_area
    search_box: search_box
    
    BoxLayout:                                                          
        id: main_container
        orientation: 'horizontal'
        spacing: 5
        padding: 5,0,0,0
        SideNav:
        BoxLayout:                                                      # Diary Layout
            canvas.before:
                Color:
                    rgba: .7,.7,.7,1
                Rectangle:
                    size: self.size
                    pos: self.pos

            id: main_layout
            size_hint: .85, 1
            FloatLayout:                                                # float layout for main screen
                size_hint: 1,1
                BoxLayout:                                              # main layout
                    canvas.before:
                        Color:
                            rgba: root.obj_color
                        Rectangle:
                            size: self.size
                            pos: self.pos

                    # id: objectives_layout
                    orientation: 'vertical'
                    size_hint: .96,None
                    size: 950,600
                    pos_hint: {'x':.02, 'y':.035}
                    BoxLayout:
                        orientation:'vertical'
                        BoxLayout:
                            canvas.before:
                                Color:
                                    rgba: .4,.4,.4,1
                                Rectangle:
                                    size: self.size
                                    pos: self.pos

                            id: top_bar
                            size_hint: 1,.15
                            MDIconButton:
                                icon: 'plus-circle'
                                user_font_size: '64sp'
                                theme_text_color: 'Custom'
                                text_color: 1,1,1,1
                                on_press:
                                    app.m.current = 'create_entry'
                            BoxLayout:    
                                BoxLayout:
                                    padding: 0,5,0,0
                                    id: search_area
                                    orientation: 'vertical'
                                    TextInput:
                                        id: search_box
                                        size_hint: 1,1
                                        multiline: False
                                        
                                    SearchTags:
                                        size_hint: 1,.1
 
                                MDIconButton:
                                    icon:'magnify'
                                    size_hint: None,None
                                    height: 80
                                    width: 80
                                    theme_text_color: 'Custom'
                                    text_color: 1,1,1,1
                                    on_press: root.search()
                        
                        ScrollView:
                            size_hint: 1, .85
                            StackLayout:
                                padding: 0,2,0,0
                                size_hint_y: None
                                height: self.minimum_height
                                spacing: 1.5
                                id: diary_list
                        Button:
                            text: 'Load more'
                            size_hint: 1,.1
                            on_press:
                                root.load_more()
                    
<TagButton@BoxLayout>:
    btn: btn
    chk: chk
    size_hint_y: None
    height: 35
    Button:
        id: btn
        background_normal: ''
        background_color: 0,0,0,0
        on_press: root.check_tick(chk)

    MDCheckbox:
        id: chk
        size_hint: None,None
        height: 35
        width: 35
        on_active: root.root.tag_check(btn.text, self.active)
        canvas.before:
            Color:
                rgba: 0,0,0,0
            Rectangle:
                pos: self.pos
                size: self.size
            
<TagsList@StackLayout>:
    
    size_hint: None,None
    height: 280
    width: 150
    canvas.before:
        Color:
            rgba: root.clr
        Rectangle:
            pos: self.pos
            size: self.size

<FolderButton@BoxLayout>:
    folder_name: folder_name
    size_hint_y: None
    height: 50
    Button:
        id: folder_name
        size_hint: .8,1
        disabled: True
        disabled_color: 1,1,1,1
    MDIconButton:
        icon: 'close'
        on_press: root.delete()

<FolderSelect@BoxLayout>:
    listed_folders: listed_folders
    orientation: 'vertical'
    ScrollView:
        size_hint: 1,.75
        StackLayout:
            id: listed_folders
            size_hint_y: None
            height: self.minimum_height
    BoxLayout:
        orientation: 'vertical'
        size: root.size
        pos: root.pos
        size_hint: 1,.2
        padding: 0,0,0,25
        MDIconButton:
            disabled: True
            pos_hint: {'center_x':.5}
            icon: 'upload'
            theme_text_color: 'Custom'
            text_color: 1,1,1,1

        MDLabel:
            halign: 'center'
            text: 'Drag and Drop Folder'
            size_hint_y: None
            height: 10
            color: 1,1,1,1

    Button:
        size_hint: 1,.12
        text: 'Close'
        background_color: .5,.5,.5,1
        on_press: root.close()

<_DisplayImage@BoxLayout>:
    img: img
    orientation: 'vertical'
    pos_hint: {'center_y':.5,'center_x':.5}
    size_hint: .8,.9
    Image:
        id: img

    BoxLayout: 
        padding: 400,0
        size_hint_y: .1
        pos_hint: {'center_x':.5}
        MDIconButton:
            icon: 'chevron-left'
            theme_text_color: 'Custom'
            text_color: 1,1,1,1
            on_press: root.change('left')
        MDIconButton:
            icon: 'close'
            theme_text_color: 'Custom'
            text_color: 1,1,1,1
            on_press: root.dismiss()
        MDIconButton:
            icon: 'chevron-right'
            theme_text_color: 'Custom'
            text_color: 1,1,1,1    
            on_press: root.change('right')

<ImageButton@Button>:
    size_hint: None,None
    height: 120
    width: 120
    background_normal: ''
    background_color: 0,0,0,0
    disabled: True
    canvas.before:
        Color:
            rgba: .8,.8,.8,1
        Rectangle:
            size:self.size
            pos:self.pos
            source: root.pic

<FileLoader@BoxLayout>:
    canvas.before:
        Color:
            rgba: 0,0,0,.5
        Rectangle:
            pos: self.pos
            size: self.size
    padding: 20,20
    loaded_images: loaded_images
    load_btn: load_btn
    show_selected: show_selected
    BoxLayout:
        canvas.before:
            Color:
                rgba: 0,0,0,.4
            Rectangle:
                pos: self.pos
                size: self.size
        size_hint: .5,1
        orientation: 'vertical'
        Image:
            id: show_selected
            size_hint: .98,.9
        Button:
            text: 'Add Image(s)'
            size_hint: 1,.1
            on_press:
                root.add_image()
    BoxLayout:
        size_hint: .5,1
        orientation: 'vertical'
        
        ScrollView:
            id: file_scroll
            size_hint: 1,.9
            GridLayout:
                id: loaded_images
                col_default_width: 115
                col_force_default: True
                row_default_height: 115
                row_force_default: True
                cols: 5
                rows: 0
                size_hint_y: None
                height: self.minimum_height #max(self.minimum_height, file_scroll.height)
            
        BoxLayout:
            size_hint: 1,.1
            Button:
                id: load_btn
                text: "Load More"
                on_press: root._load_more()
            Button:
                text: "Close"
                on_press: root.parent.dismiss()

<SelectorImage@Button>:
    background_normal: ''
    background_color: 0,.5,1,root.transp
    size_hint: None, None
    size: 110,110
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: root.thumb

<SelectorBox@BoxLayout>:

    FloatLayout:
        size: 50,50
        pos: root.pos

<CreateEntry>:
    content: text_editor                    # big text field
    img_box: img_box                            # image squares layout on the right 
    entry_title: title
    canvas.before:
        Color:
            rgba: root.paper_color
        Rectangle:
            size: self.size
            pos: self.pos

    StackLayout:
        add_image: add_image
        BoxLayout:
            padding: 20,20,20,20
            id: top_bar
            size_hint: 1,.13

            TextInput:
                id: title
                hint_text: 'Name'
                multiline: False
                size_hint: .35, 1
                background_color: root.paper_color
            Button:
                text: 'Tags'
                size_hint: .1,1
                on_press: root.show_tags(root, pos=[self.pos[0], self.pos[1]-280])
            Button:
                text: 'Select Folders'
                size_hint: .13,1
                on_press: root._pick_folders()
            Button:
                text: 'Save'
                size_hint: .13,1
                on_press: root.save()
            Button:
                size_hint: .13,1
                text: 'Back'
                on_press: 
                    app.m.current = 'diary'

        BoxLayout:
            padding: 20,5,0,20
            size_hint: 1,.85 
            ScrollView:
                size_hint: .875,1
                id: scrlv
                scroll_type: ['bars']
                BoxLayout:
                    id: box
                    size_hint: 1, None
                    height: max(self.minimum_height, scrlv.height)
                    
                    TextInput:
                        id: text_editor
                        size_hint: 1, None
                        height: max(self.minimum_height, scrlv.height)
                        markup: True
                        # background_color: root.paper_color
                        # source: root.im

            ScrollView:
                size_hint: .125,1
                id: scroll_images
                canvas.before:
                    Color:
                        rgba: .7,.7,.7,1
                    Rectangle:
                        size: self.size
                        pos: self.pos
                ImageBox:
                    id: img_box
                    padding: 14,14,10,14
                    spacing: 10
                    size_hint_y: None
                    height: self.minimum_height
                    MDIconButton:
                        id: add_image
                        size_hint: None,None
                        height: 120
                        width: 120
                        icon: 'plus'
                        on_press:
                            root._add_img()
                        canvas.before:
                            Color:
                                rgba: .8,.8,.8,1
                            Rectangle:
                                pos:self.pos
                                size:self.size

<EntryDisplayed@BoxLayout>:
    content: content
    img_box: img_box

    BoxLayout:
        padding: 20,5,0,20
        size_hint: 1,.85 
        ScrollView:
            size_hint: .875,1
            id: scrlv
            scroll_type: ['bars']
            BoxLayout:
                id: box
                size_hint: 1, None
                height: max(self.minimum_height, scrlv.height)
                
                TextInput:
                    id: content
                    size_hint: 1, None
                    height: max(self.minimum_height, scrlv.height)
                    markup: True
                    disabled: True
                    disabled_foreground_color: 0,0,0,1
                    background_color: app.paper_color
                    # source: root.im
        ScrollView:
            size_hint: .125,1
            id: scroll_images
 
            ImageBox:
                id: img_box
                padding: 14,0,10,14
                spacing: 10
                size_hint_y: None
                height: self.minimum_height


######################################################################################################################
################################################# MILESTONES #########################################################
######################################################################################################################

<Milestones>:
    main_container: main_container
    in_progress_btn: in_progress_btn
    archived_btn: archived_btn
    milestones_list: milestones_list
    BoxLayout:                                                          # main container
        id: main_container
        orientation: 'horizontal'
        spacing: 5
        padding: 5,0,0,0
        SideNav:
       
        BoxLayout:                                                      # Milestones Layout
            canvas.before:
                Color:
                    rgba: .7,.7,.7,1
                Rectangle:
                    size: self.size
                    pos: self.pos

            id: main_layout
            size_hint: .85, 1
            FloatLayout:                                                # float layout for main screen
                size_hint: 1,1
                BoxLayout:                                              # main layout
                    canvas.before:
                        Color:
                            rgba: root.obj_color
                        Rectangle:
                            size: self.size
                            pos: self.pos

                    orientation: 'vertical'
                    size_hint: .96,None
                    size: 950,600
                    pos_hint: {'x':.02, 'y':.035}
                    BoxLayout:
                        orientation:'vertical'
                        BoxLayout:
                            # canvas.before:
                            #     Color:
                            #         rgba: .4,.4,.4,1
                            #     Rectangle:
                            #         size: self.size
                            #         pos: self.pos

                            id: top_bar
                            size_hint: 1,.15
                            Button:
                                id: in_progress_btn
                                text: 'In Progress'
                                background_normal: ''
                                on_press: 
                                    root.load_milestones()
                            Button:
                                id: archived_btn
                                text: 'Completed'
                                background_normal: ''
                                on_press:
                                    root.load_archived()
                        ScrollView:
                            size_hint: 1, .85
                            StackLayout:
                                size_hint_y: None
                                height: self.minimum_height
                                id: milestones_list


<Manager>:
    id: screen_manager
    scr_one: scr_one
    diary: diary
    milestones: milestones
    create_entry: create_entry
    ScreenOne:
        id: scr_one
        name: 'scr_one'
        manager: screen_manager
    Milestones:
        id: milestones
        name: 'milestones'
        manager: screen_manager
    CreateEntry:
        id: create_entry
        name: 'create_entry'
        manager: screen_manager
    Diary:
        id: diary
        name: 'diary'
        manager: screen_manager

''')

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
        for x in range(0, self.indx):
            n += 50
        return 550 - n

    def make_menu(self, btn, posi):
        self.dropmenu = DropdownClick(root=self.root, size_hint=(None,None), size=(150,100), pos=posi, edit=True, clicked_widget=btn, argus=self.argus)
        self.root.add_widget(self.dropmenu)

    def get_func(arg):
        self.func = arg


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
        for x in range(0, self.indx):
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
            # self.obj_btn.disabled = True
            self.obj_btn.background_color = self.root.disabled_c
            self.obj_btn.color = self.root.disabled_t
            self.obj_check.icon = 'checkbox-marked'
            self.obj_check._set_b_color(self.root.disabled_c)
            # self.obj_check.disabled = True
            self.hab_symb._set_b_color(self.root.disabled_c)

            # self.hab_symb.disabled = True
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
                    # make popup yayy
                    self._make_popup()
                    nxt_prog = MILESTONES['+100Objectives']['progress']
                    MILESTONES['+100Objectives']['progress'] = (nxt_prog[0], nxt_prog[1]+100)
                    MILESTONES['+100Objectives']['text'] = f'[size={MARKUP_SIZE}]Road to {nxt_prog[1]+100} Objectives! - %p%[/size]\nReward: %r%'
                    MILESTONES['+100Objectives'] = MILESTONES['+100Objectives']
                    text = f'[size={MARKUP_SIZE}]Completed %n% Objectives![/size]\nReward: %r%'
                    ARCHIVE.put(f'{nxt_prog[0]}Objectives', progress=nxt_prog, reward=MILESTONES['+100Objectives']['reward'], completed_date=f'{DATE_TODAY}', category='n', text=f'{text}', claimed=False)
        else:
            if progress[0] == progress[1]-100:
                # make popup yayy
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
                    # make popup appear ayy gg
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
                categ = ARCHIVE[mydate]['category']

                MILESTONES.put(mydate, progress=(progress[0]-1,progress[1]), reward=reward, completed_date=None,last_progress=None,last_completed=None,category='monthly',text=f'[size={MARKUP_SIZE}]Complete 1 Objective each day - %p%[/size]\nReward: %r%')
                ARCHIVE.delete(mydate)
            else:
                progress = MILESTONES[mydate]['progress']
                if len(DAILY[f'{DATE_TODAY}']['objectives']) == 0:
                    MILESTONES[mydate]['progress'] = (progress[0]-1,progress[1])
                    MILESTONES[mydate] = MILESTONES[mydate]


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


class Test(BoxLayout):
    def __init__(self,root=None, name='', edit=False, priority=1, date_picked=str(DATE_TODAY), habit=False, days={}, *args,**kwargs):
        super(Test,self).__init__(*args,**kwargs)
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
    sidenav = ObjectProperty()
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
                han = DisplayHabit(root=self, hab_text=name.replace('_', ' '), indx=indx, streak=streak, size_hint_y=None, height=50, argus=[name, self, True, the_day, days, priority, True, ])
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
                    obj = ObjectiveButton(root=self, obj_text=name.replace('_', ' '), priority=priority, size_hint_y=None, height=50, indx=indx, habit=habit)
                    if OBJECTIVES[x]['habit'] == True:
                        obj.set_streak(self.habit_list[name])
                    if OBJECTIVES[x]['status'] == 'completed':
                        obj.completed()
                    self.objectives_layout.add_widget(obj)
                    indx += 1
        except:
            pass

    def make(self):
        obj = ObjectiveButton(obj_text='Ey', size_hint_y=None, height=50)
        self.objectives_layout.add_widget(obj)

    def edit_objective(self, name, root, edit, date_picked, days, priority, habit):
        editing = Test(name=name, root=root, edit=True, date_picked=date_picked, days=days, priority=priority, habit=habit,)
        ron = MDDialog(title='Name', type='custom', content_cls=editing, auto_dismiss=False)
        editing._set_pop(ron)
        ron.open()
    
    def create_objective(self, habit=None):
        pop = Test(root=self, habit=habit)
        pop.days = {}
        ron = MDDialog(title='Name',type='custom',content_cls=pop, auto_dismiss=False)
        pop._set_pop(ron)
        ron.open()

    def _make_popup(self):
        self.manager.popup = True
        pop = Mypop(root=self, btn_text='Go to Milestones', text='Congratulations, you reached a Milestone!', font_size='18sp')
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


class Mypop(Snackbar):
    def __init__(self, *args, root=None, btn_text=None, **kwargs):
        super(Mypop,self).__init__(*args,**kwargs)
        self.root = root
        self.btn_text = btn_text
        self.btn = Button(size_hint=(.35,1),background_normal='', background_color=root.highlight, text=self.btn_text, color=(.3,.3,.3,1), on_press=lambda x: self.root.popup())
        self.ids.box.add_widget(Image(source="", allow_stretch=False, keep_ratio=True, size_hint=(None,None), size=(40,40)))
        self.ids.box.add_widget(self.btn)
        self.ids.box.children[-1], self.ids.box.children[-2] = self.ids.box.children[-2], self.ids.box.children[-1] 


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
        for x in range(0, self.indx):
            n += 75
        return 500 - n

    def click(self,btn):
        return btn.last_touch.button

    def click_pos(self, btn):
        return btn.last_touch.pos


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
                    completed = ARCHIVE[x]['completed_date']
                    rew = ARCHIVE[x]['reward']
                    prog = ARCHIVE[x]['progress']
                    m_t = str(ARCHIVE[x]['category'])
                    text = str(ARCHIVE[x]['text'])
                    milestone = MilestonesButton(self, active='completed', disabled=cl, name=x, text=text, archive=True, progress=prog, reward=rew, m_category=m_t, size_hint_y=None, height=75)

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
                milestone = MilestonesButton(self, name=x, text=text, active='progress', progress=prog, reward=rew, m_category=m_t, size_hint_y=None, height=75, indx=indx)
                self.milestones_list.add_widget(milestone)
                indx += 1

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        if 'MileDrop' in str(self.children[0]):
            position = self.children[0].pos
            if touch.x < position[0] or touch.x > position[0] + 150 and touch.y > position[1] + 200 or touch.y < position[1]:
                self.remove_widget(self.children[0])


class DiaryEntry(BoxLayout):
    btn = ObjectProperty()
    edit = ObjectProperty()
    delete = ObjectProperty()

    def __init__(self, entry_number, *args, **kwargs):
        super(DiaryEntry,self).__init__(*args, **kwargs)
        self.entry_n = entry_number
        
    def edit_entry(self):
        self.edit_page = CreateEntry()
        self.edit_page.edit = True
        self.edit_page.entry = self.entry_n
        self.edit_page.name='edit_page'
        self.manager = MANAGER
        MANAGER.add_widget(self.edit_page)
        MANAGER.current = 'edit_page'

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
                DIARY['init'][tag].remove(entry_n)
        DIARY['init'] = DIARY['init']
        DIARY.delete(str(self.entry_n))
        shutil.rmtree(join(ENTRIES_FOLDER, str(self.entry_n)))
        self.pop.dismiss()

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
        Clock.schedule_once(lambda x: self.search_area.add_widget(SearchTags()))
        Window.bind(on_key_down=self._on_keyboard_down)

    def on_enter(self):
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
        shown_entry = DiaryEntry(entry)
        shown_entry.btn.text = self._make_entry_text(f'{entry}') 
        shown_entry.btn.on_press = lambda entry=entry: self.view_entry(entry)
        self.diary_list.add_widget(shown_entry)

    def view_entry(self, entry_n):
        self.view = ViewEntry(self)
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


class EntrySearch():
    days = ('monday', 'tuesday','wednesday','thursday','friday','saturday','sunday')
    months = ('january', 'february','march','april','may','june','july','august','september','october','november','december')
    pattern1 = r'^[0-9]+-[a-zA-Z]+-[a-zA-Z]+,*'
    pattern2 = r'^[0-9]+-[0-9]+-[a-zA-Z]+,*'
    pattern3 = r'^[0-9]+-[a-zA-Z]+,*'
    pattern4 = r'^[0-9]+-[0-9]+-[0-9]+,*'
    pattern5 = r'^[0-9]+-[0-9]+,*'
    pattern6 = r'^[0-9]+,*'
    pattern7 = r'[a-zA-Z]+-[a-zA-Z]+,*'
    pattern8 = r'[a-zA-Z]+,*'
    ptrns = [pattern1, pattern2, pattern3, pattern4, pattern5, pattern6, pattern7, pattern8]

    used_pattern = f'({")|(".join(ptrns)})'
    
    def __init__(self, tags, query):
        self.tags = tags
        self.query = query
        
    def get_entry_list(self, queries):
        length = len(self.tags)
        if queries.count('') == 3:
            if length == 0:
                return self.all_entries()                
        if length == 0 and queries.count('') < 3:
            return self.queried_list_no_tags(queries)
        elif length == 1:
            return self.queried_one_tag(self.tags[0], queries)
        elif length > 1:
            return self.queried_all_with_tags(self.tags, queries)

    def check_conditions(self, entry, queries):
        temp = None
        if queries.count('') == 3:
            return entry
        for indx, query in enumerate(queries):
            if query != '' and indx == 0:
                if query in DIARY[entry]['date_created']:
                    temp = entry
                else:
                    temp = None
                    break

            if query != '' and indx == 1:
                if self.check_day_and_month(entry, query):
                    temp = entry
                else:
                    temp = None
                    break
            if query != '' and indx == 2:
                if self.check_query_in_title(entry, query):
                    temp = entry
                else:
                    temp = None
                    break
 
        return temp

    def queried_all_with_tags(self, tags, queries):
        entries = []
        for entry in DIARY:
            if entry == 'init':
                continue
            temp = self.check_conditions(entry, queries)
            if temp != None:
                for tag in tags:
                    if DIARY[temp][tag] == 1:
                        entries.append(temp)
        return entries

    def all_entries(self):
        entries = []
        for entry in DIARY:
            if entry == 'init':
                continue
            else:
                entries.append(entry)
        return entries

    def queried_one_tag(self, tag, queries):
        entries = []
        for entry in DIARY['init'][tag]:
            temp = self.check_conditions(str(entry), queries)
            if temp != None:
                entries.append(temp)
        return entries
            
    def queried_list_no_tags(self, queries):
        entries = []
        for entry in DIARY:
            if entry == 'init':
                continue
            temp = self.check_conditions(str(entry), queries)
            if temp != None:
                entries.append(temp)
        return entries

    def check_day_and_month(self, entry, query):
        queries = query.split('-')
        if len(queries) == 1:
            if DIARY[entry]['day'] in query or DIARY[entry]['month'] in query:
                return True
        else:
            if DIARY[entry]['day'] in query and DIARY[entry]['month'] in query:
                return True
        return False

    def check_query_in_title(self, entry, query):
        if query in DIARY[entry]['title']:
            return True
        return False

    def separate_queries(self):
        queries = ['','','']
        regex = re.match(self.used_pattern, self.query, re.IGNORECASE)
        try:
            title_query = self.query[regex.span()[1]:]
            date_query = regex.group()
            if date_query.endswith(','):
                temp = date_query[:-1]
            else:
                temp = date_query
            if temp.isalpha():
                if temp not in self.months and temp not in self.days:
                    title_query = date_query + title_query
                    date_query = ''

        except Exception as e:
            title_query = self.query
            date_query = ''
        

        queries[2] = title_query
        indx = 0
        for char in date_query:
            if char == ',':
                break
            if char.isnumeric() or char == '-' and indx == 0:
                indx = 0
            else:
                indx = 1
            queries[indx] += char
        if queries[0].endswith('-'):
            queries[0] = queries[0][:-1]
        if queries[2].startswith(' '):
            queries[2] = queries[2][1:]

        return queries


class CreateEntry(Screen):
    paper_color = ListProperty([0.945, 0.882, 0.752, 1])
    img_box = ObjectProperty()
    add_image = ObjectProperty()
    entry_title = ObjectProperty()
    content = ObjectProperty()
    n = NumericProperty(8)
    highlight = ListProperty([0.6, 1.0, 0.6, 1])

    def __init__(self, edit=False, entry=None, *args,**kwargs):
        super(CreateEntry,self).__init__(*args,**kwargs)
        Clock.schedule_once(lambda x: self.load_slots(),.2)
        self.edit = edit
        self.entry = entry
        self.next_gallery_slot = 0
        self.tag_list = set()
        self.pics = {}
        self.currently_shown = None

    def on_leave(self):
        shutil.rmtree(TEST_FOLDER)
        if self.edit:
            MANAGER.remove_widget(self)
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
        tags = ["lifestyle", "health", "family", "friends", "love", "work", "recipes"]
        for tag in tags:
            if DIARY[entry][tag] == 1:
                self.tag_check(tag.capitalize(), True)
        for img in range(0,len(pics)):
            self.add_new_slot(pics[img], thumbs[img])

    def _add_img(self):
        if len(PROFILE['init']['image_folders']) == 0:
            Mypop(root=self, btn_text='Select folders here', text="You don't have any image folders saved. Please select folders to search images in", size_hint_x=.8).show()
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

        DIARY[entry_n] = DIARY[entry_n]

        if not self.edit:
            PROFILE['init']['last_diary'] += 1
            DIARY['init']['total'] += 1
        PROFILE['init'] = PROFILE['init']
        DIARY['init'] = DIARY['init']
        Snackbar(text='Entry Successfully saved!').show()

    def delete_unused_images(self, old, new):
        for img in old:
            if img not in new:
                os.remove(img)

    def do(self):
        print('doy')

    def load_slots(self):
        self.img_box.add_widget(ImageButton(indx=0, root=self))
        self.img_box.add_widget(ImageButton(indx=1, root=self))
        self.img_box.add_widget(ImageButton(indx=2, root=self))
        self.img_box.add_widget(ImageButton(indx=3, root=self))
        self.img_box.slots = 4

    def add_new_slot(self, source, thumb):
        if self.next_gallery_slot != self.img_box.slots:
            img = self.img_box.children[self.get_indx(self.next_gallery_slot)]
            img.pic = thumb
            img.img = source  
        else:
            img = ImageButton(indx=self.img_box.slots, root=self)
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
        # add to profile
        # add to popup
        display_folder = FolderButton(folder)
        self.folder_layout.listed_folders.add_widget(display_folder)
        
    def show_tags(self, root, pos=None):
        self.add_widget(TagsList(root=root, pos=pos))

    def tag_check(self, tag, state):
        if state == True:
            self.tag_list.add(tag)
        else:
            self.tag_list.remove(tag)


class FolderSelect(BoxLayout):
    listed_folders = ObjectProperty()

    def __init__(self, *args, root=None, **kwargs):
        super(FolderSelect,self).__init__(*args, **kwargs)
        self.root = root

    def _load_folders(self):
        for x in PROFILE['init']['image_folders']:
            self.listed_folders.add_widget(FolderButton(x))

    def close(self):
        self.root.my_pop.dismiss()
        self.root.parent.add_path = False


class FolderButton(BoxLayout):
    folder_name = ObjectProperty()

    def __init__(self, txt, *args, **kwargs):
        super(FolderButton, self).__init__(*args, **kwargs)
        self.folder_name.text = txt

    def delete(self):
        self.parent.remove_widget(self)
        PROFILE['init']['image_folders'].remove(self.folder_name.text)
        PROFILE['init'] = PROFILE['init']


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


class ImageHandler():
    def __init__(self, image_path):
        self.thumb = self._get_thumb(image_path)
        self.img_path = image_path
        self.name = ''

    def _crop_and_save_image(self, save=False):
        image = pil_img.open(self.img_path)
        if save:       
            new_path = join(TEST_IMAGES, self.get_filename(self.img_path))
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


class SelectorImage(Button):
    img = StringProperty()
    thumb = StringProperty()
    transp = NumericProperty(0)
    def __init__(self, root=None, *args, **kwargs):
        self.root = root
        super(SelectorImage,self).__init__(*args, **kwargs)


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
        

class TagsList(StackLayout):
    clr = ListProperty([.5,.5,.5,1])
    def __init__(self, root, pos=[0,0],*args, **kwargs):
        super(TagsList,self).__init__(*args, **kwargs)
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


class EntryDisplayed(BoxLayout):
    content = ObjectProperty()
    img_box = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(EntryDisplayed ,self).__init__(*args, **kwargs)
        self.next_gallery_slot = 0
        self.currently_shown = None
        self.pics = {}


class ViewEntry(ShowImage):
    def __init__(self, root, *args, **kwargs):
        super(ViewEntry ,self).__init__(*args, **kwargs)
        self.root = root
        self.entry = None
        self.dark_level = .9
        self.next_gallery_slot = 0
        self.currently_shown = None
        self.pics = {}
        self.root.now_on_screen = self.entry

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
        self.manager = MANAGER
        MANAGER.add_widget(self.edit_page)
        MANAGER.current = 'edit_page'
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


class SearchTags(BoxLayout):
    obj_color = ListProperty([.5,.5,.5,1])
    highlight = ListProperty([0.6, 1.0, 0.6, 1])
    def __init__(self, *args, **kwargs):
        super(SearchTags,self).__init__(*args, **kwargs)
        self.spacing = 2.5
        self.root = MANAGER.diary
        for tag in ["Lifestyle", "Health", "Family", "Friends", "Love", "Work", "Recipes"]:
            tagbtn = Button(text=tag, background_normal = '', background_color=self.obj_color)
            tagbtn.on_press = lambda tag=tag, tagbtn=tagbtn: self.pressed(tagbtn)
            self.add_widget(tagbtn)

    def pressed(self, btn):
        if btn.background_color == self.obj_color:
            btn.background_color = self.highlight
            btn.color = self.obj_color
            self.root.search_tags.append(btn.text.lower()) 

        else:
            btn.background_color = self.obj_color
            btn.color = (1,1,1,1)
            self.root.search_tags.remove(btn.text.lower())


class SideNav(StackLayout):
    pass
  

class Manager(ScreenManager):
    scr_one = ObjectProperty()
    diary = ObjectProperty()
    create_entry = ObjectProperty
    milestones = ObjectProperty()
    popup = False
    add_path = False

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
