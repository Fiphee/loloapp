from os.path import join, isdir
import os
import ntpath
from kivy.storage.jsonstore import JsonStore



data_dir = os.getenv('APPDATA')
app_folder = join(data_dir, 'loloapp')

if not isdir(app_folder):
    os.mkdir(app_folder)    
    os.mkdir(join(app_folder, 'entries'))
    os.mkdir(join(app_folder, 'misc'))
    os.mkdir(join(app_folder, 'temp'))

MANAGER = None

DAILY = JsonStore(join(app_folder, 'daily.json'))
OBJECTIVES = JsonStore(join(app_folder, 'objectives.json'))
HABITS = JsonStore(join(app_folder, 'habits.json'))
MILESTONES = JsonStore(join(app_folder, 'milestones.json'))
PROFILE = JsonStore(join(app_folder, 'profile.json'))
ARCHIVE = JsonStore(join(app_folder, 'archive.json'))
DIARY = JsonStore(join(app_folder, 'diary.json'))
ENTRIES_FOLDER = join(app_folder, "entries")
TEMP = join(app_folder, 'temp')
TEST_FOLDER = join(ENTRIES_FOLDER, 'current')
TEST_IMAGES = join(TEST_FOLDER, 'images')
TEST_THUMBS = join(TEST_IMAGES, 'thumbs')