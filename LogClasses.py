import pandas as pd
from matplotlib import pyplot as plt


class ChatLog():
    def __init__(self):
        self.chat_folder = ''
        self.chat_file_name = ''
        self.session_cuttoff = 50
        self._chat_file = ''
        self.chat_log = ''
        self._sessions = []
        self.special_sessions = {}
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
            if current_session != '' and current_session not in self.special_sessions:
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
        self.player_names.append('ALL')

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
            return 'NPC:' + player
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
            if df['Roll'] != '':
                return 'Roll:GM'
            return'info'
        return 'not listed'
    
    def check_font_type(self, df):
        text_type = df['Text Type']
        text = df['Text']
        if text_type == 'Emote':
            return 'emote'
        if 'NPC' in text_type:
            return 'npc'
        if text_type == 'OoC':
            return 'ooc'
        if text_type == 'GM Text':
            if text.split(':')[0] == 'GM':
                return 'gmplayer'
            return 'gmtext'
        if 'Player' in text_type:
            return 'player'
        if 'Whisper' in text_type:
            return 'whisper'
        if text_type == 'info' or 'Roll' in text_type:
            return 'info'
        if text_type == 'not listed':
            return 'info'
    
    def check_player_text(self, df):
        font_type = df['Font Type']
        new_text = df['New Text']
        if font_type == 'player':
            player = df['Text Type'].replace('Player:', '')
            image = f'<p><img src="../Assets/Images/{player.replace(' ', '')}.png" alt="{player}"></p>'
            strong = f'<p><strong>{player}</strong></p>'
            new_text = new_text.replace(f'{player}: ', '')
            new_text = new_text.replace('[D]', '<div class="row">')
            new_text = new_text.replace('[di]', f'<div class="image">{image}</div>')
            new_text = new_text.replace('[dn]', f'<div class="name">{strong}</div>')
            new_text = new_text.replace('[dt]', '<div>')
            new_text = new_text.replace('[/D]', '</div></div>')
            return new_text
        if font_type == 'npc':
            npc = df['Text Type'].replace('NPC:', '')
            image = '<p><img src="../Assets/Images/PlaceHolder.png"></p>'
            strong = f'<p><strong>{npc}</strong></p>'
            new_text = new_text.replace(f'{npc}: ', '')
            new_text = new_text.replace('[D]', '<div class="row">')
            new_text = new_text.replace('[di]', f'<div class="image">{image}</div>')
            new_text = new_text.replace('[dn]', f'<div class="name">{strong}</div>')
            new_text = new_text.replace('[dt]', '<div>')
            new_text = new_text.replace('[/D]', '</div></div>')
            return new_text
        if font_type == 'gmplayer':
            image = '<p><img src="../Assets/Images/PlaceHolder.png"></p>'
            strong = f'<p><strong>GM</strong></p>'
            new_text = new_text.replace(f'GM: ', '')
            new_text = new_text.replace('[D]', '<div class="row">')
            new_text = new_text.replace('[di]', f'<div class="image">{image}</div>')
            new_text = new_text.replace('[dn]', f'<div class="name">{strong}</div>')
            new_text = new_text.replace('[dt]', '<div>')
            new_text = new_text.replace('[/D]', '</div></div>')
            return new_text
        new_text = new_text.replace('[D]', '')
        new_text = new_text.replace('[di]', '')
        new_text = new_text.replace('[dn]', '')
        new_text = new_text.replace('[dt]', '')
        new_text = new_text.replace('[/D]', '')
        return new_text

    def set_text_type(self):
        self._sessions_df['Text Type'] = self._sessions_df.apply(self.check_text_type, axis=1)
        self._sessions_df['Font Type'] = self._sessions_df.apply(self.check_font_type, axis=1)

    def set_new_text(self):
        self._sessions_df['New Text'] = self._sessions_df.apply(lambda x: f'[D][di][dn][dt]<p class="{x['Font Type']}">{x['Text']}</p>[/D]', axis=1)
        self._sessions_df['New Text'] = self._sessions_df.apply(self.check_player_text, axis=1)

    def set_players(self):
        self._sessions_df = self._sessions_df.fillna('')
        self._sessions_df['Players'] = self._sessions_df.apply(lambda x: x['Text'].split(':')[0] if '=' in x['Roll'] else '', axis=1)

    def set_header_footer(self, css_file):
        self.html_header = ['<!DOCTYPE html>', '<html>', '<head>', f'<link rel="stylesheet" href="{css_file}">', '</head>', '<body>', '<div>']
        self.html_footer = ['</div>', '</body>', '</html>']

    def add_header(self):
        for line in self.html_header:
            self._html_body.append(line)

    def add_footer(self):
        for line in self.html_footer:
            self._html_body.append(line)

    def plot_player_rolls(self, player=''):
        filename = 'Total'
        roll_bins = [0,10,20,30,40,50,60,70,80,90,100]
        roll_df = self._sessions_df[self._sessions_df['Roll'].str.contains('d100')][['Roll', 'Text Type']].copy()
        roll_df = roll_df[~roll_df['Text Type'].str.contains('Roll:GM')]
        if player != '':
            roll_df = roll_df[roll_df['Text Type'].str.contains(f'Roll:{player}')]
            filename = player.replace(' ', '')
        roll_df['Roll#'] = roll_df['Roll'].str.split(' = ').str[-1].astype(int)
        roll_df = roll_df[roll_df['Roll#'] <= 100]
        roll_df['Roll##'] = (roll_df['Roll#']/5).round().astype(int)*5
        count_df = roll_df.groupby(['Roll##'])['Roll##'].size().reset_index(name='counts')
        count_df = count_df.sort_values(['Roll##'])
        ax = roll_df.plot(kind='hist', bins=20, x='Roll#', legend=False, color="#C7D9DD", xticks=roll_bins, rwidth=0.95)
        if player == '': player = 'Total'
        ax.set_title(f'{player} D100 Rolls ({len(roll_df)})', color="#fefbd8", size=14)
        ax.set_facecolor("#0F171C")
        ax.set_ylabel('Number of Rolls', color="#fefbd8", size=14)
        ax.set_xlabel('D100 Roll', color="#fefbd8", size=14)
        ax.tick_params(color="#fefbd8", labelcolor="#fefbd8", labelsize=14)
        fig = ax.get_figure()
        fig.patch.set_alpha(0)
        fig.savefig(f'Rooms/Assets/Images/{filename}Roll.png')
        plt.close(fig)
        return
    
    def plot_rolls(self):
        self.plot_player_rolls()
        for player in self.player_names:
            if player != 'ALL': self.plot_player_rolls(player=player)
        return
    
    def set_player_skills(self, player):
        play_skill_df = self._sessions_df[(self._sessions_df['Text'].str.contains(r'\[SKILL\]')) & (self._sessions_df['Text Type'].str.contains(f'Roll:{player}'))][['Text', 'Text Type']].copy()
        play_skill_df['Skill'] = play_skill_df['Text'].str.split(r'\[SKILL\] ').str[1].str.split(r' \(').str[0]
        count_df = play_skill_df.groupby(['Skill'])['Skill'].size().reset_index(name='counts')
        count_df['Skill#'] = count_df['Skill'] + ':' + count_df['counts'].astype(str)
        return count_df['Skill#'].to_list()
    
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
        self._html_body.append('<li><a href="Rooms/ChatLogs/DiceRolls.html">Dice Rolls</a></li>')
        for player in self.player_names:
            if player == 'ALL':
                self._html_body.append('<li><a href="Rooms/ALL.html">Secret Room (GM)</a></li>')
            else:
                self._html_body.append(f'<li><img src="Rooms/Assets/Images/{player.replace(' ', '')}.png" alt="{player}"><a href="Rooms/{player.replace(' ', '')}.html">{player}\'s Room</a></li>')
        self._html_body.append('</ul>')
        self.add_footer()
        self.write_html_file('Lobby.html', self._html_body)
        _temp = 'temp'

    def create_session_ledger(self):
        self._sessions.sort()
        self.set_header_footer('Rooms/Assets/fgstyles.css')
        self._html_body = []
        self.add_header()
        for session in self._sessions:
            self._html_body.append(f'<h3>Session Date: {session}</h3>')
            sess_df = self._sessions_df[self._sessions_df['Session'] == session].copy()
            sess_df = sess_df[sess_df['Text Type'] == 'GM Text']
            sess_df['New Text'] = sess_df.apply(lambda x: x['New Text'].replace('.../Assets/Images/PlaceHolder.png', 'Rooms/Assets/Images/PlaceHolder.png'), axis=1)
            sess_list = sess_df['New Text'].to_list()
            for text in sess_list:
                self._html_body.append(text)
        self.add_footer()
        self.write_html_file('SessionLedger.html', self._html_body)
        _temp = 'temp'

    def create_session(self, session='', player=''):
            self.set_header_footer('../Assets/fgstyles.css')
            self._html_body = []
            self.add_header()
            if player == 'ALL':
                self._html_body.append(f'<h3>You Begin To Read Everyones Adventures From {session}</h3>')
                sess_df = self._sessions_df[self._sessions_df['Session'] == session].copy()
            else:
                self._html_body.append(f'<h3>You Begin To Read {player}\'s Adventures From {session}</h3>')
                sess_df = self._sessions_df[self._sessions_df['Session'] == session].copy()
                allowed_types = f'{player.replace(' ', '')}|Roll|Player|info|Text|OoC|Emote|NPC'
                sess_df = sess_df[sess_df['Text Type'].str.contains(allowed_types)]
                sess_df = sess_df[~sess_df['Text Type'].str.contains('Roll:GM')]
            sess_df = sess_df.sort_values(by=['idx'])
            sess_list = sess_df['New Text'].to_list()
            for text in sess_list:
                self._html_body.append(text)
            self.add_footer()
            self.write_html_file(f'Rooms/ChatLogs/{player.replace(' ', '')}_{session}.html', self._html_body)

    def create_player_session(self):
        for session in self._sessions:
            for player in self.player_names:
                self.create_session(session=session, player=player)
        return
    
    def create_player_rooms(self):
        for player in self.player_names:
            self.set_header_footer('Assets/fgstyles.css')
            self._html_body = []
            self.add_header()
            if player == 'ALL':
                self._html_body.append(f'<h1>You Have Entered The Secret Room</h1>')
            else:
                self._html_body.append(f'<h1>You Have Entered {player}\'s Room</h1>')
            self._html_body.append('<h3>Choose an adventure to read</h3>')
            self._html_body.append('<ul>')
            self._sessions.sort(reverse=True)
            for session in self._sessions:
                self._html_body.append(f'<li><a href="ChatLogs/{player.replace(' ', '')}_{session}.html">Adventures From: {session}</a></li>')
            self._html_body.append('</ul>')
            if player != 'ALL':
                player_skills = self.set_player_skills(player)
                self._html_body.append('<br>')
                self._html_body.append('<table>')
                self._html_body.append('<tr>')
                self._html_body.append('<th>Skill</th>')
                self._html_body.append('<th>Uses</th>')
                self._html_body.append('</tr>')
                for skill in player_skills:
                    s_list = skill.split(':')
                    self._html_body.append('<tr>')
                    self._html_body.append(f'<td>{s_list[0]}</td>')
                    self._html_body.append(f'<td>{s_list[1]}</td>')
                    self._html_body.append('</tr>')
                self._html_body.append('</table>')
            self.add_footer()
            self.write_html_file(f'Rooms/{player.replace(' ', '')}.html', self._html_body)
            _temp = 'temp'

    def create_session_rolls(self):
        self.set_header_footer('../Assets/fgstyles.css')
        self._html_body = []
        self.add_header()
        self._html_body.append('<h1>You Look At The Totally Normal And Random Dice Rolls (D100)</h1>')
        self._html_body.append('<div class="row"><div>')
        self._html_body.append('<img class="roll" src="../Assets/Images/TotalRoll.png" alt="Total">')
        self._html_body.append('</div></div>')
        new_row = True
        for player in self.player_names:
            if new_row:
                self._html_body.append('<div class="row">')
            self._html_body.append('<div>')
            self._html_body.append(f'<img class="roll_img" src="../Assets/Images/{player.replace(' ', '')}.png" alt="{player}"><img class="roll" src="../Assets/Images/{player.replace(' ', '')}Roll.png" alt="{player}">')
            self._html_body.append('</div>')
            if not new_row:
                self._html_body.append('</div>')
            new_row = not new_row
        self.add_footer()
        self.write_html_file('Rooms/ChatLogs/DiceRolls.html', self._html_body)

    def create_rolls_csv(self):
        roll_df = self._sessions_df[self._sessions_df['Roll'].str.contains('=')][['Session', 'Text', 'Roll', 'Text Type']].copy()
        roll_df['Dice'] = roll_df['Roll'].str.split(' = ').str[0]
        roll_df['Roll'] = roll_df['Roll'].str.split(' = ').str[1]
        roll_df = roll_df[['Session', 'Text', 'Text Type', 'Dice', 'Roll']]
        roll_df.to_csv(f'{self.chat_folder}\\DiceRolls.csv', index=False)

