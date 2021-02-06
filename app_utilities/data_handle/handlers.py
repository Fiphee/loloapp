import os
import calendar
from os.path import join, isdir
from ..dates import DATE_TODAY, DAY_NAME, YESTERDAY, PREVIOUS_MONTH
from ..my_paths import DAILY, DIARY, OBJECTIVES, HABITS, MILESTONES, PROFILE, ARCHIVE
import re
from datetime import datetime

MARKUP_SIZE = 25

class MakeStorage():
    def create(self):
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


class VerifyData():
    def check_milestones(self):
        if f'{DATE_TODAY}' not in MILESTONES:
            MILESTONES.put(f'{DATE_TODAY}', progress=('',''), reward='', completed_date=None, category='daily', text=f'[size={MARKUP_SIZE}]Complete all objectives today[/size]\nReward: %r%')

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

    def check_habits(self):
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
    
    def check_dates(self):
        if DAY_NAME == 'Monday':        # handle resetting of objectives done in the week on mondays
            if PROFILE['init']['reset_week'] == True:
                PROFILE['init']['this_week'] = 0
                PROFILE['init']['reset_week'] = False
                PROFILE['init'] = PROFILE['init']

        elif DAY_NAME == 'Tuesday':     # set it up so next monday it knows to reset. This is to avoid reset twice on the same monday
            PROFILE['init']['reset_week'] = True
            PROFILE['init'] = PROFILE['init']

        if DATE_TODAY.month != PROFILE['init']['month']:    # resets month objective count
            if PREVIOUS_MONTH in MILESTONES:
                MILESTONES.delete(PREVIOUS_MONTH)
            PROFILE['init']['this_year'][PROFILE['init']['month']] = PROFILE['init']['this_month']
            PROFILE['init']['month'] = DATE_TODAY.month
            PROFILE['init']['this_month'] = 0
            PROFILE['init'] = PROFILE['init']
            MILESTONES.put(f'{DATE_TODAY.year}-{DATE_TODAY.month}', progress=(0,calendar.monthrange(DATE_TODAY.year, DATE_TODAY.month)[1]), reward='', completed_date=None, last_progress=None, last_completed=None, category='monthly', text=f'[size={MARKUP_SIZE}]Complete 1 Objective each day - %p%[/size]\nReward: %r%')

        if DATE_TODAY.year != PROFILE['init']['year']:      # resets year objective count
            PROFILE['init']['archive'][PROFILE['init']['year']] = PROFILE['init']['this_year']
            PROFILE['init']['year'] = DATE_TODAY.year
            PROFILE['init']['this_year'] = {}
            PROFILE['init'] = PROFILE['init']

    def __get_date(self, entity):
        date_pattern = r'^[0-9]+-[0-9]+-[0-9]+'
        check_date = re.match(date_pattern, entity)
        try:
            if check_date.span()[1] != len(entity):
                return None,None,None
        except:
            pass
        if check_date == None:
            return None,None,None
        entity_date_string = check_date.group()
        entity_date = datetime.strptime(entity_date_string, '%Y-%m-%d')
        return entity_date, datetime.strptime(YESTERDAY, '%Y-%m-%d'), entity_date_string
    
    def handle_old_data(self):
        for obj in OBJECTIVES:
            if obj != 'init':
                dates = self.__get_date(obj)
                if dates[0] == None:
                    continue
                if dates[0] < dates[1]:
                    OBJECTIVES.delete(obj)
                    if dates[2] in DAILY:
                        DAILY.delete(dates[2])
        for milestone in MILESTONES:
            dates = self.__get_date(milestone)
            if dates[0] == None:
                continue
            if dates[0] <= dates[1]:
                MILESTONES.delete(milestone)
