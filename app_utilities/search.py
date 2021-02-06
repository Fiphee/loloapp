import re
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.uix.button import Button
from .my_paths import DIARY


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

        except Exception:
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


class SearchTags(BoxLayout):
    obj_color = ListProperty([.5,.5,.5,1])
    highlight = ListProperty([0.6, 1.0, 0.6, 1])
    def __init__(self, root=None, manager=None, *args, **kwargs):
        super(SearchTags,self).__init__(*args, **kwargs)
        self.spacing = 2.5
        self.MANAGER = manager
        self.root = root
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
