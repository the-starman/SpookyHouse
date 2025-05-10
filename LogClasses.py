import pandas as pd


class ChatLog():
    def __init__(self):
        self.chat_folder = ''
        self.chat_file_name = ''
        self.session_cuttoff = 50
        self._chat_file = ''
        self.chat_log = ''
        self._sessions = []
        self.remove_lines = ''
        self.player_names = []
        self.player_cleanup = []
        self._font_list = []
        self.emote_fonts = []
        self.info_fonts = []
        self.player_fonts = []
        self.gmtext_fonts = []
        self.npc_fonts = []
        self.ooc_fonts = []
        self.fonts_theme = []
        self.html_header = []
        self.html_footer = []
        self._html_body = []
        self._sessions_df = pd.DataFrame()

    def read_file(self):
        self._chat_file = self.chat_folder + '\\' + self.chat_file_name
        with open(self._chat_file , 'r') as chat:
            self.chat_log = chat.readlines()

    def set_sessions(self):
        current_session = ''
        sessions_log = []
        for lines in self.chat_log:
            if 'Session started' in lines:
                current_session = lines.split('"')[1]
            if current_session != '':
                sessions_log.append([current_session, lines])
        self._sessions_df = pd.DataFrame(sessions_log)
        self._sessions_df.columns = ['Session', 'Chat Log']
        self._sessions_df['idx'] = self._sessions_df.index

    def split_chat_text(self):
        self._sessions_df['Font'] = self._sessions_df['Chat Log'].str.split('="#').str[1].str.split('">').str[0]
        self._sessions_df['Text'] = self._sessions_df['Chat Log'].str.replace(' /><b', '')
        self._sessions_df['Text'] = self._sessions_df['Text'].str.split('">').str[1]
        self._sessions_df['Text'] = self._sessions_df['Text'].str.replace('</font>', '')
        self._sessions_df['Text'] = self._sessions_df['Text'].str.replace('<br />', '')
        self._sessions_df['Roll'] = self._sessions_df['Chat Log'].str.split(r'> \[').str[1].str.split(r'\]').str[0]
        self._sessions_df = self._sessions_df.fillna('')
        self._font_list = list(pd.unique(self._sessions_df['Font']))

    def clean_players(self):
        for player in self.player_cleanup:
            self._sessions_df['Text'] = self._sessions_df['Text'].str.replace(player[0], player[1])

    def remove_bad_sessions(self):
        count_df = self._sessions_df.groupby(['Session'])['Session'].size().reset_index(name='counts')
        self._sessions_df = self._sessions_df.merge(count_df, how='left', on='Session')
        self._sessions_df = self._sessions_df[self._sessions_df['counts'] > self.session_cuttoff]
        self._sessions = list(pd.unique(self._sessions_df['Session']))

    def remove_bad_lines(self):
        for lines in self.remove_lines:
            self._sessions_df = self._sessions_df[~self._sessions_df['Text'].str.startswith(lines)]
        self._sessions_df = self._sessions_df[~self._sessions_df['Chat Log'].str.startswith('<br')]

    def check_text_type(self, df):
        text = df['Text']
        font = df['Font']
        player = text.split(':')[0]
        if font in self.emote_fonts:
            return 'Emote'
        if font in self.npc_fonts:
            return 'NPC'
        if font in self.ooc_fonts:
            return'OoC'
        if font in self.player_fonts:
            if player in self.player_names:
                return 'Player:' + player
            return'GM Text'
        if font in self.gmtext_fonts:
            return'GM Text'
        if font in self.info_fonts:
            if text.startswith(' -&#62;'):
                return 'Whisper->' + player.split('; ')[-1].replace(' ', '')
            if player in self.player_names:
                if ' [' in text:
                    return 'Roll:' + player
                return 'Whisper<-' + player.replace(' ', '')
            return'info'
        return 'not listed'
    
    def check_font_type(self, df):
        text_type = df['Text Type']
        text = df['Text']
        if text_type == 'Emote':
            return 'emote'
        if text_type == 'NPC':
            return 'npc'
        if text_type == 'OoC':
            return 'ooc'
        if text_type == 'GM Text':
            if text.split(':')[0] == 'GM':
                return 'player'
            return 'gmtext'
        if 'Player' in text_type:
            return 'player'
        if 'Whisper' in text_type or 'Roll' in text_type:
            return 'info'
        if text_type == 'info':
            return 'info'
        if text_type == 'not listed':
            return 'info'
    
    def check_player_text(self, df):
        text_type = df['Text Type']
        new_text = df['New Text']
        if 'Player:' in text_type:
            player = text_type.replace('Player:', '')
            new_text = new_text.replace(f'{player}', '')
            new_text = new_text.replace('">', f'"><img src="../Assets/Images/{player.replace(' ', '')}.png" alt="{player}"><strong>{player}</strong>')
            return new_text
        if text_type == 'NPC':
            npc = new_text.split(':')[0]
            new_text = new_text.replace(f'{npc}', f'<strong>{npc}</strong>')
            return new_text
        return new_text

    def set_text_type(self):
        self._sessions_df['Text Type'] = self._sessions_df.apply(self.check_text_type, axis=1)
        self._sessions_df['Font Type'] = self._sessions_df.apply(self.check_font_type, axis=1)

    def set_new_text(self):
        self._sessions_df['New Text'] = self._sessions_df.apply(lambda x: f'<p class="{x['Font Type']}">{x['Text']}</p>', axis=1)
        self._sessions_df['New Text'] = self._sessions_df.apply(self.check_player_text, axis=1)

    def set_players(self):
        self._sessions_df = self._sessions_df.fillna('')
        self._sessions_df['Players'] = self._sessions_df.apply(lambda x: x['Text'].split(':')[0] if '=' in x['Roll'] else '', axis=1)

    def set_header_footer(self, css_file):
        self.html_header = ['<!DOCTYPE html>', '<html>', '<head>', f'<link rel="stylesheet" href="{css_file}">', '</head>', '<body>']
        self.html_footer = ['</body>', '</html>']

    def add_header(self):
        for line in self.html_header:
            self._html_body.append(line)

    def add_footer(self):
        for line in self.html_footer:
            self._html_body.append(line)
    
    def write_html_file(self, file_name, html_body):
        with open(file_name, 'w') as file:
            for lines in html_body:
                file.write(lines + '\n')

    def create_lobby(self):
        self.set_header_footer('Rooms/Assets/fgstyles.css')
        self._html_body = []
        self.add_header()
        self._html_body.append('<h1>You Have Entered The Spooky House Lobby</h1>')
        self._html_body.append('<h3>Choose a room to enter or view the session ledger</h3>')
        self._html_body.append('<ul>')
        self._html_body.append('<li><a href="SessionLedger.html">Session Ledger</a></li>')
        for player in self.player_names:
            self._html_body.append(f'<li><img src="Rooms/Assets/Images/{player.replace(' ', '')}.png" alt="{player}"><a href="Rooms/{player.replace(' ', '')}.html">{player}\'s Room</a></li>')
        self._html_body.append('</ul>')
        self.add_footer()
        self.write_html_file('Lobby.html', self._html_body)
        _temp = 'temp'

    def create_session_ledger(self):
        self.set_header_footer('Rooms/Assets/fgstyles.css')
        self._html_body = []
        self.add_header()
        for session in self._sessions:
            self._html_body.append(f'<h3>Session Date: {session}</h3>')
            sess_df = self._sessions_df[self._sessions_df['Session'] == session].copy()
            sess_df = sess_df[sess_df['Text Type'] == 'GM Text']
            sess_list = sess_df['New Text'].to_list()
            for text in sess_list:
                self._html_body.append(text)
        self.add_footer()
        self.write_html_file('SessionLedger.html', self._html_body)
        _temp = 'temp'

    def create_player_session(self):
        for player in self.player_names:
            for session in self._sessions:
                self.set_header_footer('../Assets/fgstyles.css')
                self._html_body = []
                self.add_header()
                self._html_body.append(f'<h3>You Begin To Read {player}\'s Adventures From {session}</h3>')
                sess_df = self._sessions_df[self._sessions_df['Session'] == session].copy()
                allowed_types = f'{player.replace(' ', '')}|Roll|Player|info|Text|OoC|Emote|NPC'
                sess_df = sess_df[sess_df['Text Type'].str.contains(allowed_types)]
                sess_df = sess_df.sort_values(by=['idx'])
                sess_list = sess_df['New Text'].to_list()
                for text in sess_list:
                    self._html_body.append(text)
                self.add_footer()
                self.write_html_file(f'Rooms/ChatLogs/{player.replace(' ', '')}_{session}.html', self._html_body)
        return

    def create_rooms(self):
        for player in self.player_names:
            self.set_header_footer('Assets/fgstyles.css')
            self._html_body = []
            self.add_header()
            self._html_body.append(f'<h1>You Have Entered {player}\'s Room</h1>')
            self._html_body.append('<h3>Choose an adventure to read</h3>')
            self._html_body.append('<ul>')
            for session in self._sessions:
                self._html_body.append(f'<li><a href="ChatLogs/{player.replace(' ', '')}_{session}.html">{player}\'s Adventures On: {session}</a></li>')
            self.add_footer()
            self.write_html_file(f'Rooms/{player.replace(' ', '')}.html', self._html_body)
        _temp = 'temp'

    