import pandas as pd


class ChatLog():
    def __init__(self):
        self.chat_folder = ''
        self.chat_file_name = ''
        self.session_cuttoff = 50
        self._chat_file = ''
        self.chat_log = ''
        self.sessions = []
        self.remove_lines = ''
        self.player_names = []
        self._font_list = []
        self.fonts = []
        self.fonts_theme = []
        self.html_header = []
        self.html_footer = []
        self._sessions_df = pd.DataFrame()

    def read_file(self):
        self._chat_file = self.chat_folder + '\\' + self.chat_file_name
        with open(self._chat_file , 'r') as chat:
            self.chat_log = chat.readlines()

    def set_sessions(self):
        current_session = ''
        chat_sessions = set()
        sessions_log = []
        for lines in self.chat_log:
            if 'Session started' in lines:
                current_session = lines.split('"')[1]
            if current_session != '':
                chat_sessions.add(current_session)
                sessions_log.append([current_session, lines])
        self.sessions = list(chat_sessions)
        self.sessions.sort()
        self._sessions_df = pd.DataFrame(sessions_log)
        self._sessions_df.columns = ['Session', 'Chat Log']

    def split_chat_text(self):
        self._sessions_df['Font'] = self._sessions_df['Chat Log'].str.split('="#').str[1].str.split('">').str[0]
        self._sessions_df['Text'] = self._sessions_df['Chat Log'].str.split('</').str[0].str.split('>').str[-1]
        self._sessions_df['Roll'] = self._sessions_df['Chat Log'].str.split(r'> \[').str[1].str.split(r'\]').str[0]
        self._sessions_df = self._sessions_df.fillna('')
        self._font_list = list(pd.unique(self._sessions_df['Font']))

    def remove_bad_sessions(self):
        count_df = self._sessions_df.groupby(['Session'])['Session'].size().reset_index(name='counts')
        self._sessions_df = self._sessions_df.merge(count_df, how='left', on='Session')
        self._sessions_df = self._sessions_df[self._sessions_df['counts'] > self.session_cuttoff]

    def remove_bad_lines(self):
        for lines in self.remove_lines:
            self._sessions_df = self._sessions_df[~self._sessions_df['Text'].str.startswith(lines)]
        self._sessions_df = self._sessions_df[~self._sessions_df['Chat Log'].str.startswith('<br')]

    def check_text_type(self, df):
        text = df['Text']
        font = df['Font']
        text_type = 'not listed'
        for fonts in self.fonts:
            if font in fonts:
                if font == 'FFFFFF':
                    if text.split(':')[0] in self.player_names:
                        text_type = 'Player'
                    else:
                        text_type = 'GM Text'
                else:
                    text_type = fonts[1]
        return text_type

    def set_text_type(self):
        self._sessions_df['Text Type'] = self._sessions_df.apply(self.check_text_type, axis=1)

    def update_fonts(self):
        theme_df = pd.DataFrame(self.fonts_theme)
        theme_df.columns = ['New Font', 'Text Type']
        self._sessions_df = self._sessions_df.merge(theme_df, how='left', on='Text Type')
        self._sessions_df['New Log'] = self._sessions_df.apply(lambda x: x['Chat Log'].replace(x['Font'], x['New Font']), axis=1)

    def set_players(self):
        self._sessions_df = self._sessions_df.fillna('')
        self._sessions_df['Players'] = self._sessions_df.apply(lambda x: x['Text'].split(':')[0] if '=' in x['Roll'] else '', axis=1)

    def set_header_footer(self):
        if not self.html_header:
            self.html_header = ['<!DOCTYPE html>', '<html>', '<body>']
            self.html_footer = ['<\\body>', '<\html>']
    
    def create_new_log(self):
        new_log = ''.join(self._sessions_df['New Log'].to_list())
        with open('test_log.html', 'w') as file:
            file.writelines(new_log)

    