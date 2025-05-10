from LogClasses import *

chat_obj = ChatLog()
chat_obj.chat_folder = 'C:\\Users\\zmcke\\OneDrive\\Documents\\Spooky House'
chat_obj.chat_file_name = 'chatlog.html'
chat_obj.remove_lines = ['Session started at',
                         'Fantasy Grounds -',
                         'Call of Cthulhu',
                         'Ruleset Conversion by',
                         '(LINK)',
                         'Core RPG ruleset',
                         'Universal Module extension',
                         "Fen's NPC Portrait Workaround",
                         'Story Template Custom Record Templates',
                         'FG Browser',
                         'Folder assets refreshed',
                         'Chatlog Explorer v',
                         'Token Height Indication v',
                         'SmiteWorks Core Dark',
                         'Clear Dead v',
                         'Host (v']
chat_obj.player_names = ['Carmen Santamonica', 'Carl Handy', 'Professor Plato', 'Lillian Lovell']
chat_obj.player_cleanup = [['Moguppo The Handyman', 'Carl Handy'], ['Mogstew', 'Carl Handy'], ['The Professor', 'Professor Plato']]
# chat_obj.fonts = [['880000', 'Emote'],
#                   ['660066', 'Game Info'],
#                   ['261A12', 'Player'],
#                   ['000000', 'GM Text'],
#                   ['005500', 'OoC'],
#                   ['000066', 'Character'],
#                   ['DA8ADB', 'Game Info'],
#                   ['63F7ED', 'Emote'],
#                   ['FFFFFF', 'GM Text'],
#                   ['FFE6AB', 'Character'],
#                   ['66CC66', 'OoC']]
chat_obj.emote_fonts = ['880000', '63F7ED']
chat_obj.info_fonts = ['660066', 'DA8ADB']
chat_obj.player_fonts = ['261A12', 'FFFFFF']
chat_obj.gmtext_fonts = ['000000', 'FFFFFF']
chat_obj.npc_fonts = ['000066', 'FFE6AB']
chat_obj.ooc_fonts = ['005500', '66CC66']
# chat_obj.fonts_theme = [['DA8ADB', 'Game Info'],
#                         ['63F7ED', 'Emote'],
#                         ['000000', 'GM Text'],
#                         ['261A12', 'Player'],
#                         ['FFE6AB', 'Character'],
#                         ['66CC66', 'OoC']]
chat_obj.read_file()
chat_obj.set_sessions()
chat_obj.split_chat_text()
chat_obj.clean_players()
chat_obj.remove_bad_sessions()
chat_obj.remove_bad_lines()
chat_obj.set_text_type()
chat_obj.set_new_text()
chat_obj.create_lobby()
chat_obj.create_session_ledger()
chat_obj.create_rooms()
chat_obj.create_player_session()
print('Completed')
temp = 'temp'
