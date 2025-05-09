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
                         'Folder assets refreshed']
chat_obj.player_names = ['Carmen Santamonica', 'Carl Handy', 'Professor Plato', 'Lillian Lovell']
chat_obj.fonts = [['880000', 'Emote'],
                  ['660066', 'Game Info'],
                  ['261A12', 'Player'],
                  ['000000', 'GM Text'],
                  ['005500', 'OoC'],
                  ['000066', 'Character'],
                  ['DA8ADB', 'Game Info'],
                  ['63F7ED', 'Emote'],
                  ['FFFFFF', 'GM Text'],
                  ['FFE6AB', 'Character'],
                  ['66CC66', 'OoC']]
chat_obj.fonts_theme = [['DA8ADB', 'Game Info'],
                        ['63F7ED', 'Emote'],
                        ['000000', 'GM Text'],
                        ['261A12', 'Player'],
                        ['FFE6AB', 'Character'],
                        ['66CC66', 'OoC']]
chat_obj.read_file()
chat_obj.set_sessions()
chat_obj.split_chat_text()
chat_obj.remove_bad_sessions()
chat_obj.remove_bad_lines()
chat_obj.set_text_type()
chat_obj.update_fonts()
chat_obj.create_new_log()
temp = 'temp'
