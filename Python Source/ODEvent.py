from datetime import timedelta
from sqlite3 import Error
import Proxy, ProxyType

def createTables():
    Tables = ["""
    CREATE TABLE if not exists "Dominion" (
    "random_clicks"  INTEGER NOT NULL DEFAULT 0,
    "random_timing"  INTEGER NOT NULL DEFAULT 0,
    "username"  TEXT DEFAULT '',
    "password"  TEXT DEFAULT '',
    "show_window"  INTEGER NOT NULL DEFAULT 1,
    "use_proxy"  INTEGER DEFAULT 0,
    "browser_agent"  TEXT DEFAULT 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/6.0)',
    "proxy_address"  TEXT DEFAULT '',
    "sound"  INTEGER NOT NULL DEFAULT 0,
    "use_session"  INTEGER DEFAULT 0,
    "manual_login"  INTEGER DEFAULT 0,
    "race"  TEXT DEFAULT 0,
    "safe_run"  INTEGER NOT NULL DEFAULT 0,
    "hide_browser_window"  INTEGER NOT NULL DEFAULT 0,
    "server"  TEXT
    );""",
     """
    CREATE TABLE if not exists "Events" (
    "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "event_date"  TEXT,
    "event_type"  TEXT,
    "insert_data"  TEXT,
    "maximum_possible"  INTEGER DEFAULT 0,
    "status"  TEXT DEFAULT No,
    "repeating"  INTEGER DEFAULT 0,
    "repeat_time"  INTEGER,
    "repeat_end"  TEXT
    );
    """ ]
    for single in Tables:
            try:
               query(single,1)
            except EOFError as e:
                print(e)





if len(query("Select * from Dominion")) == 0:
    query("Insert into Dominion (sound) values (?)", 1, [0])

def dominion_config():
    dominion_conf = query(f"Select * from [Dominion] ")
    return dominion_conf[0]


def build_chrome_options():
    options = webdriver.ChromeOptions()
    options.accept_untrusted_certs = True
    options.assume_untrusted_cert_issuer = True
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    return options


def render_units(type):
    if type == "Human":
        return ["Spearmen", "Archer", "Knight", "Cavalry"]
    elif type == "Dwarf":
        return ["Soldier", "Miner", "Cleric", "Warrior"]
    elif type == "Wood Elf":
        return ["Ranger", "Longbowman", "Mystic", "Druid"]
    elif type == "Halfling":
        return ["Slinger", "Defender", "Staff Master", "Master Thief"]
    elif type == "Merfolk":
        return ["Mermen", "Sirens", "Kraken", "Leviathan"]
    elif type == "Sylvan":
        return ["Satyr", "Sprite", "Dryad", "Centaur"]
    elif type == "Gnome":
        return ["Suicide Squad", "Tinker", "Rockapult", "Juggernaut"]
    elif type == "Firewalker":
        return ["Fire Sprite", "Flamewolf", "Phoenix", "Salamander"]
    elif type == "Spirits":
        return ["Phantom", "Banshee", "Ghost", "Spectre"]
    elif type == "Goblin":
        return ["Raider", "Shaman", "Hobgoblin", "Wolf Rider"]
    elif type == "Troll":
        return ["Brute", "Ogre", "Basher", "Smasher"]
    elif type == "Dark Elf":
        return ["Swordsman", "Gargoyle", "Adept", "Spirit Warrior"]
    elif type == "Undead":
        return ["Skeleton", "Ghoul", "Progeny", "Vampire"]
    elif type == "Lycanthrope":
        return ["Scavenger", "Ratman", "Werewolf", "Garou"]
    elif type == "Kobold":
        return ["Grunt", "Underling", "Beast", "Overlord"]
    elif type == "Lizardfolk":
        return ["Reptile", "Serpent", "Chameleon", "Lizardmen"]
    elif type == "Icekin":
        return ["Icebeast", "Snow Witch", "FrostMage", "Ice Elemental"]
    elif type == "Orc":
        return ["Savage", "Guard", "Voodoo Magi", "Bone Breaker"]
    elif type == "Nomad":
        return ["Fighter", "Crossbowman", "Blademaster", "Valkyrie"]
    elif type == "The Nox":
        return ["Imp", "Fiend", "Nightshade", "Lich"]
    else:
        return ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Spies", "Wizards", "Archmages"]


def render_races():
    return ["Good Races", "------------------", "Human", "Dwarf", "Wood Elf", "Halfling", "Merfolk", "Sylvan", "Gnome",
            "Firewalker", "Spirits",
            "------------------", "Goblin", "Troll", "Dark Elf", "Undead", "Lycanthrope", "Kobold", "Lizardfolk",
            "Icekin", "Orc", "Nomad", "The Nox"]


def date_format(date):
    return date.strftime("%d/%m/%y %H:%M")


def sound(type=0):
    if dominion_config()[8] == 1:
        if not sys.platform.startswith('win'):
            sg.PopupError('Sorry, you gotta be on Windows to hear sound')
        else:
            if type == 0:
                return winsound.PlaySound("media/flip.wav", 1)
            elif type == 1:
                return winsound.PlaySound("media/gold.wav", 1)
            elif type == 2:
                return winsound.PlaySound("media/butcher.wav", 1)
            elif type == 3:
                return winsound.PlaySound("media/error.wav", 1)
            elif type == 4:
                return winsound.PlaySound("media/click.wav", 1)


def field_fill_delay():
    if dominion_config()[1] == 1:
        return time.sleep(random.randint(10, 20) / 10)

def get_number(number):
    number = str(number)
    if not number.isnumeric():
        return 0
    else:
        return number


def get_row(selected):
    return query(f"Select * from [Events] order by event_date asc limit 1 offset {selected}")


def event_list(type=0):
    clientTable = []
    if type == 1:
        for everyRecord in query(f"Select * from [Events] where completed=0 order by event_date asc"):
            clientTable.append(  # Columns in Event Table
                [everyRecord[0],  # ID
                 everyRecord[1],  # event_date
                 everyRecord[2],  # event_type
                 everyRecord[3],  # insert_data
                 everyRecord[4],  # #maximum_possible
                 everyRecord[5],  # status
                 everyRecord[6],  # repeating
                 everyRecord[7],  # repeat_time
                 everyRecord[8],  # repeat_end
                 everyRecord[9]  # attempts
                 ]
            )
    else:
        for everyRecord in query(f"Select * from [Events] order by event_date asc"):
            maximum = " - "
            repeater = " - "
            repeat_end = " - "
            repeat_interval = " - "
            if everyRecord[4] == 1:
                maximum = "Yes"
            if everyRecord[6] == 1:
                repeater = "Yes"
                repeat_interval = " {} minute".format(everyRecord[7])
                repeat_end = everyRecord[8]

            clientTable.append(  # Columns in Event Table
                [everyRecord[0],  # ID
                 everyRecord[1],  # event_date
                 everyRecord[2],  # event_type
                 everyRecord[3],
                 maximum,
                 repeater,  # repeating
                 repeat_interval,  # repeat_time
                 repeat_end,  # repeat_end
                 everyRecord[5]  # status
                 ]
            )
    return clientTable


def ev_data():
    data = event_list(1)
    data = str(data[0][3]).split(",")
    near = []
    for each in data:
        near.append(each.split(":"))
    return near


def update_table(mainwindow):
    mainwindow.FindElement("_all_events_table_").Update(event_list())


def botter():

    driver = webdriver.Chrome('chromedriver.exe', options=build_chrome_options())

    while dominion_config()[12] == 1:
        if dominion_config()[13]:
            driver.set_window_position(-2000, 0)
        else:
            driver.set_window_position(0, 0)

        sound(2)
        field_fill_delay()

        while True:

                    all_cookies = driver.get_cookies()
                    cookies = {}

                    for s_cookie in all_cookies:
                        cookies[s_cookie["name"]] = s_cookie["value"]


                    if each_event[6] == 0:
                        try:
                            driver.find_element_by_css_selector(".alert-success")
                        except:
                            error =1
                            query("Update Events set status='Error', attempt =1, completed =1 where id=?", 1, [each_event[0]])
                            next_attempt = date_format(datetime.datetime.now() + timedelta(minutes=60))
                            query(
                                f"Insert into Events (event_date,event_type,insert_data,maximum_possible,status,repeating,repeat_time,repeat_end, attempts) "
                                f"values (?,?,?,?,?,?,?,?,?)", 1,
                                [
                                    next_attempt,
                                    each_event[2],
                                    each_event[3],
                                    each_event[4],
                                    "Attempt:%s | ID:%s" % (each_event[9],each_event[0]),
                                    each_event[6],
                                    each_event[7],
                                    each_event[8],
                                    (each_event[9] +1)
                                ])
                        if error == 0:

                            query("Update Events set status='Completed', completed=1 where id=?", 1, [each_event[0]])
                    else:
                        if date_format(datetime.datetime.now()) < each_event[8]:
                            start_time_new = date_format(
                                datetime.datetime.now() + timedelta(minutes=each_event[7]))
                            query(f"Update Events set event_date =?, status='Repeating' where id=?", 1,
                                  [start_time_new, each_event[0]])
                        else:
                            query(f"Update Events set status='Completed', completed=1 where id=?", 1, [each_event[0]])
                    sound(1)
                    time.sleep(1)

                    if dominion_config()[13]:
                        driver.set_window_position(-2000, 0)
                    else:
                        driver.set_window_position(0, 0)
                    if dominion_config()[12] == 2:
                        driver.close()




driver_shut = 0
server_list = [
    "https://beta.opendominion.net/",
    "https://odarena.com/",
]

########################################################################################################
# ------ Menu Definition ------ #
Events_Header = ["#   ",
                 "Starting Date",
                 "Event Name",
                 "                     Actions                    ",
                 "Use Maximum" ,
                 "Use Repeater",
                 "Repeat Interval",
                 "Ending Time",
                 "Completed"]


# ------ Menu Definition ------ #
TopMenu = [
    ['&Add Events',
      ['&Explore Land', '&Construct Buildings', '&Re-zone Land', '&Improvements','!--------------------', '&BLACK OPS', '&Military', 'Invade',
       '!--------------------','Magic', 'Espionage'],
#     ['&Repeating ',
#      ['&Explore Land', '&Construct Buildings', '&Re-zone Land', '&Improvements','!--------------------', '&BLACK OPS', '&Military', 'Invade',
#       '!--------------------','Magic', 'Espionage']]
      ],
    ['&Load Events'],
    ['&Properties',
     ['Login', 'System']],
     ['&Notifications'],
    ['&Help', ['&How To','&Changes','&About']]]

if len(event_list()) == 0:
    display_list = [['', '', '', '', '', '','','','']]
else:
    display_list = event_list()



# Main Window Layout
layout = [[sg.Menu(TopMenu, tearoff=False, pad=(20, 1))],
          [
              sg.Btn(tooltip="Start The Program",image_filename="media/battlenet.png", key="_start_program_",button_color=("#d4d0c8", "#d4d0c8")),
              sg.T("", background_color="#d4d0c8",pad=(2,2),),
              sg.Btn(tooltip="Refresh the window",image_filename="media/refresh.png",key="Refresh",button_color=("#d4d0c8", "#d4d0c8")),
              sg.T("", background_color="#d4d0c8",pad=(2,2),),
              sg.Btn(tooltip="Stop The Program",image_filename="media/battlenetoff.png", key="_stop_program_",button_color=("#d4d0c8", "#d4d0c8")),
              sg.T("", background_color="#d4d0c8", pad=(2, 2), ),
              sg.Btn(tooltip="Close Browser window",image_filename="media/tray_down.png", key="_hide_br_window_",button_color=("#d4d0c8", "#d4d0c8")),
           ],
          [sg.Table(
        alternating_row_color='lightblue',
        justification="left",
        auto_size_columns=True,
        background_color='#555',
        bind_return_key=True,
        num_rows=30,
        hide_vertical_scroll=True,
        key="_all_events_table_",
        values=display_list,
        headings=Events_Header,
    )
          ]]
###################################################################################################################
####################################################################################################################
# Main Window
Main_Window = sg.Window('Open Dominion Event Handler  v0.1.23  05/12/2019  ', icon="media/osnologo.ico",
                   element_justification="left",
                   auto_size_buttons=True,
                   background_color="#d4d0c8",
                   use_default_focus=True,
                   return_keyboard_events=True,
                   right_click_menu=['&Right', ['&Refresh','&Export All','&Delete All']],
                   text_justification="left",
                    resizable=True,
                    debugger_enabled=False,
                   ).Layout(layout).Finalize()



def gui():

    # Start The Display GUI PART and Database Updates ####################################################################
    while True:
        event, values = Main_Window.Read(timeout=7000)
        sg.PopupAnimated(None)
        if event in ['Exit', None]:
                sound(3)
                break

        update_table(Main_Window)

        if event == "_go_tray_":
            sound(4)
            Main_Window.Minimize()

        if event == "_hide_br_window_":
            sound(4)
            updates = dominion_config()[13] ^ 1
            query(f"Update dominion set hide_browser_window = {updates}", 1)
            Main_Window.FindElement("_hide_br_window_").Update(button_color=sg.COLOR_SYSTEM_DEFAULT)

        #IF an event from table is clicked, fire up the popup
        if len(values['_all_events_table_']) > 0:
            selectedEvent = values['_all_events_table_']

        if event == "Refresh":
            sound(4)
            update_table(Main_Window)

        if event == "Delete:46":
            sound(1)
            delete_row = sg.PopupYesNo("Are you sure that you want to delete this record?",title="",button_color=sg.COLOR_SYSTEM_DEFAULT,keep_on_top=True,icon="media/question.ico")
            if delete_row == "Yes":
                query("Delete from Events where id ={}".format(get_row(values['_all_events_table_'][0])[0][0]), 1)
                update_table(Main_Window)
                sound()
        if event == "Delete All":
            sound(1)
            query("Delete from Events",1)
            update_table(Main_Window)

        if event == "Changes":
            sound(3)
            Changes_layout = [[sg.Frame("", element_justification="center", layout=(
                [
                    [sg.Image(filename="media/opendominion.png")],
                    [sg.T("""
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        Open Dominion Event Handler

        GUI  v.0.1.23 -  05.12.2019

        r00tme

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
              
        TODO:
            - Detailed logs / Text file to contain all the activity

            """

             , pad=(10, 10), justification="center")]

                ]))]]

            # Main Window
            Changes_Window = sg.Window('Changes and Bugs Information', icon="media/info.ico",

                                     text_justification="left",
                                     element_justification="center",
                                     element_padding=(5, 5)
                                     , debugger_enabled=False,
                                     ).Layout(Changes_layout).Finalize()
            event, values = Changes_Window.Read()

        # About
        if event == "About":
            sound(3)
            About_layout = [[sg.Frame("",element_justification="center",layout=(
                [
                    [sg.Image(filename="media/opendominion.png")],
          [sg.T("""+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                   
    Open Dominion Event Handler
    
    GUI  v.0.1.23 -  05.12.2019
    
    r00tme
    """,justification="center")],
     [sg.Button(button_text="Bug Report", button_color=sg.COLOR_SYSTEM_DEFAULT, size=(10, 1),
                      key="_open_git_link_")]   ,
    [sg.T("""
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    MIT License
    Copyright (c) 2019 Zdravko Georgiev 
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE. """,pad=(10,10), justification="center")]

                ]))]]

            # Main Window
            About_Window = sg.Window('About Information', icon="media/info.ico",

                                     text_justification="left",
                                     element_justification="center",
                                     element_padding=(5,5)
                                     ,debugger_enabled=False,
                                     ).Layout(About_layout).Finalize()
            event, values = About_Window.Read()
        if event == "_open_git_link_":
            webdriver.Chrome('chromedriver.exe', options=build_chrome_options()).get("https://github.com/r00tmebaby/OpenDominion-Event-Handler")
        # Add Login Settings
        if event == "Login":
            sound(3)

            LoginLayout = [
                [sg.Frame("", element_justification="left", pad=(5, 5), layout=(
                    [sg.T("Username"), sg.InputText(default_text=dominion_config()[2], pad=(10, 10), size=(27, 1),
                                                    key="_set_login_username_")],
                    [sg.T("Password"),
                     sg.InputText(default_text=dominion_config()[3], password_char="*", pad=(10, 10), size=(27, 1),
                                  key="_set_login_password_")],)
                          )],
                [sg.Checkbox("Use Session",default=dominion_config()[9], pad=(2, 2), size=(10, 1), key="_try_use_session_"),
                 sg.Checkbox("Manual Login",default=dominion_config()[10], pad=(2, 2), size=(10, 1), key="_try_login_manual_")],
                [sg.Button(image_filename="media/blue_accept_ok.png", button_color=('#FFF', '#d4d0c8'),
                           key="_add_login_credentials_", pad=(5, 5))]]

            Login_Window = sg.Window('Login Settings', icon="media/login.ico",
                                     element_justification="center",
                                     auto_size_buttons=True,
                                     background_color="#d4d0c8",
                                     use_default_focus=True,
                                     text_justification="left",
                                     keep_on_top=True,
                                     debugger_enabled=False
                                     ).Layout(LoginLayout).Finalize()

            event, values = Login_Window.Read()
            if event == "_add_login_credentials_":
                sound(1)
                query("Update [Dominion] set username=?, password= ?, use_session=?,manual_login=?", 1,
                      [values['_set_login_username_'], values['_set_login_password_'],values['_try_use_session_'],values['_try_login_manual_'] ])
                Login_Window.Close()

        # [sg.DropDown(brlist,default_value=dominion_config[0][6],pad=(5,5), size=(90,3))]
        # Add System Settings
        if event == "System":
            sound(3)

            Sysyem_Layout = [[sg.Frame("Advanced Configuration", pad=(10, 10), element_justification="left", layout=([
                # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                [sg.Frame("Change User Agent", pad=(15, 15), layout=(
                    [sg.DropDown(brlist, key="_set_browser_agent_", default_value=dominion_config()[6], pad=(5, 5),
                                 size=(40, 10))],
                    [sg.Checkbox("Show Browser Window", key="_set_window_show_", default=dominion_config()[4],
                                 size=(20, 1))],
                    [sg.Checkbox("Use Proxy", key="_set_checkbox_proxy_", default=dominion_config()[5], size=(10, 1)),
                     sg.Input(pad=(5, 5), default_text=dominion_config()[7], key="_set_proxy_proxy_", size=(25, 1))
                     ],))],
                [sg.Frame("Game Settings",size=(30,1), pad=(15, 15),layout=(
                    [sg.T("Server Link"),
                      sg.DropDown(server_list, default_value=dominion_config()[14], key="_select_system_server_",
                                  size=(30, 15), readonly=True)],
                    [sg.T("Your Race"),
                      sg.DropDown(render_races(),default_value=dominion_config()[11],key="_select_race_system_",size=(20,15),readonly=True)]
                ))],
                [sg.Frame("Bot Behaviour", pad=(15, 15), layout=(
                    [sg.Checkbox("Enable Sound", key="_set_sound_on_", default=dominion_config()[8], size=(35, 1))],
                    [sg.Checkbox("Use Fake Clicks", key="_set_fake_clicks_", default=dominion_config()[0], size=(35, 1))],
                    [sg.Checkbox("Use Random Delay", key="_set_random_delay_", default=dominion_config()[1],
                                 size=(30, 1))]))
                 ]]))
                              ],
                             [sg.T(" " * 46),
                              sg.Button(image_filename="media/blue_accept_ok.png", button_color=('#FFF', '#d4d0c8'),
                                        key="_save_system_settings_", pad=(5, 5)), sg.T(" " * 46), ]]

            System_Window = sg.Window('System Settings', icon="media/system.ico",
                                      element_justification="left",
                                      auto_size_buttons=True,
                                      use_default_focus=True,
                                      text_justification="left",
                                      keep_on_top=True,
                                      debugger_enabled=False,
                                      ).Layout(Sysyem_Layout).Finalize()

            event, values = System_Window.Read()
            if event == "_save_system_settings_":
                sound(1)
                query(
                    "Update Dominion set random_clicks=?, random_timing=?,show_window=?,browser_agent=?,use_proxy=?,proxy_address=?, sound=?,race=?,server =?",
                    1,
                    [
                        values['_set_fake_clicks_'],
                        values['_set_random_delay_'],
                        values['_set_window_show_'],
                        values['_set_browser_agent_'],
                        values['_set_checkbox_proxy_'],
                        values['_set_proxy_proxy_'],
                        values['_set_sound_on_'],
                        values['_select_race_system_'],
                        values['_select_system_server_']
                    ]
                    )
                System_Window.Close()

        ## Add Static Event Explore Land ##############################################################################
        if event == "Explore Land":
            sound()

            ExploreLAnd = [
                    [sg.Frame("", element_justification="center", pad=(5, 5), layout=(
                        [sg.Frame("Timers", layout=(
                        [sg.T("Date Format DD/MM/YY 24:00")],
                        [sg.T("Start Time",),sg.InputText(default_text=date_format(datetime.datetime.now()), pad=(10, 10), size=(15, 1), key="_starting_date_update_explore_",tooltip="Use this timer to set a static event time")],
                        [sg.T("End Time",),sg.InputText(default_text=date_format(datetime.datetime.now()), pad=(10, 10), size=(15, 1),key="_ending_date_update_explore_",tooltip="Use this timer to set when the repeater will stop")],
                        [sg.T("Repeat",),sg.Checkbox("",tooltip="Check this box to use the repeater",key="_repeat_explore_use_"),sg.T("every"),
                         sg.Input("0", pad=(10, 10), size=(5, 1), key="_repeat_explore_min_"),sg.T("minutes")
                         ]))],
                        [sg.Frame("Explore Land", pad=(25, 25),element_justification="center", layout=([
                            [sg.Checkbox("Explore Maximum Possible",pad=(10, 10), key="_explore_max_possible_")],
                            [sg.T(size=(30, 1), text="   Terrain                     Explore For", background_color="#fff",
                                  pad=(2, 2))],
                            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                            [sg.T(size=(10, 1), text="Plain"),
                             sg.Input(pad=(5, 5), default_text=0, key="_plain_explore_", size=(15, 1))],
                            [sg.T(size=(10, 1), text="Mountains"),
                             sg.Input(pad=(5, 5), default_text=0, key="_mountains_explore_", size=(15, 1))],
                            [sg.T(size=(10, 1), text="Swamp"),
                             sg.Input(pad=(5, 5), default_text=0, key="_swamp_explore_", size=(15, 1))],
                            [sg.T(size=(10, 1), text="Cavern"),
                             sg.Input(pad=(5, 5), default_text=0, key="_cavern_explore_", size=(15, 1))],
                            [sg.T(size=(10, 1), text="Forest"),
                             sg.Input(pad=(5, 5), default_text=0, key="_forest_explore_", size=(15, 1))],
                            [sg.T(size=(10, 1), text="Hill"),
                             sg.Input(pad=(5, 5), default_text=0, key="_hill_explore_", size=(15, 1))],
                            [sg.T(size=(10, 1), text="Water"),
                             sg.Input(pad=(5, 5), default_text=0, key="_water_explore_", size=(15, 1))],
                            [sg.Button(image_filename="media/blue_accept_ok.png", button_color=("#d4d0c8", "#FFF"),
                                       key="_add_time_explore_btn_", pad=(5, 5))]
                             ]))]
                    ))]]


            exploreland_window = sg.Window('Explore Land', icon="media/explore.ico"
                                                                "",
                                           element_justification="center",
                                           auto_size_buttons=True,
                                           background_color="#d4d0c8",
                                           use_default_focus=True,
                                           text_justification="left",
                                           keep_on_top=True,
                                           debugger_enabled=False,
                                           ).Layout(ExploreLAnd).Finalize()

            event, values = exploreland_window.Read()

            if event == "_add_time_explore_btn_":
                json_explore_data = """Plain: %s, Mountains: %s, Swamp: %s, Cavern: %s, Forest: %s, Hill: %s,  Water: %s""" % (
                    get_number(values['_plain_explore_']),
                    get_number(values['_mountains_explore_']),
                    get_number(values['_swamp_explore_']),
                    get_number(values['_cavern_explore_']),
                    get_number(values['_forest_explore_']),
                    get_number(values['_hill_explore_']),
                    get_number(values['_water_explore_'])
                )
                sound(1)
                query("Insert into [Events] (event_date,event_type,insert_data,maximum_possible,repeat_end,repeat_time,repeating)"
                      " values (?,?,?,?,?,?,?)", 1,
                      [
                          values['_starting_date_update_explore_'],
                          "Explore Land",
                          json_explore_data,
                          values["_explore_max_possible_"],
                          values['_ending_date_update_explore_'],
                          values['_repeat_explore_min_'],
                          values['_repeat_explore_use_'],
                      ])
                exploreland_window.Close()
                update_table(Main_Window)

        ## Add Static Event Construct Buildings ##############################################################################
        if event == "Construct Buildings":
            sound()
            ConstructLand = [
                [sg.Frame("",  pad=(10, 10), layout=(
                    [
                        [sg.Frame("Timers",pad=(10, 10), layout=(

                            [sg.T("Date Format DD/MM/YY 24:00")],
                            [sg.T("Start Time"),
                             sg.InputText(default_text=date_format(datetime.datetime.now()), pad=(10, 10), size=(15, 1),
                                          key="_starting_date_construct_")],
                            [sg.T("End Time"),
                             sg.InputText(default_text=date_format(datetime.datetime.now()), pad=(10, 10), size=(15, 1),
                                          key="_end_date_construct_")],
                            [sg.T("Repeat"), sg.Checkbox("", key="_repeat_add_construct_"), sg.T("every"),
                             sg.Input("0", pad=(10, 10), size=(5, 1), key="_repeat_add_construct_min_"), sg.T("minutes")
                             ]

                        ))],

                        [sg.Frame("Construct Buildings", pad=(10, 10), layout=([
                            [sg.Checkbox("Build Maximum Possible", pad=(5, 5), key="_build_max_possible_")],
                            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                            [sg.Frame("", background_color="#FFF", pad=(15, 15), layout=(
                                [[sg.Frame("Plain", pad=(15, 15), layout=(
                                    [sg.T(size=(10, 1), text="Alchemy"),
                                     sg.Input(default_text=0, key="_construct_alchemy__", size=(10, 1))],
                                    [sg.T(size=(10, 1), text="Farm"),
                                     sg.Input(default_text=0, key="_construct_farm__", size=(10, 1))],
                                    [sg.T(size=(10, 1), text="Smithy"),
                                     sg.Input(default_text=0, key="_construct_smithy__", size=(10, 1))],
                                    [sg.T(size=(10, 1), text="Masonry"),
                                     sg.Input(default_text=0, key="_construct_masonry__", size=(10, 1))],
                                ))],

                                 [sg.Frame("Mountain", pad=(15, 15), layout=(
                                     [sg.T(size=(10, 1), text="Ore Mine"),
                                      sg.Input(default_text=0, key="_construct_ore_mine_", size=(10, 1))],
                                     [sg.T(size=(10, 1), text="Gryphon Nest"),
                                      sg.Input(default_text=0, key="_construct_gryphon_nest__", size=(10, 1))],
                                 ))],
                                 [sg.Frame("Swamp", pad=(15, 15), layout=(
                                     [sg.T(size=(10, 1), text="Tower"),
                                      sg.Input(default_text=0, key="_construct_tower__", size=(10, 1))],
                                     [sg.T(size=(10, 1), text="Wizard Guild"),
                                      sg.Input(default_text=0, key="_construct_wizguild__", size=(10, 1))],
                                     [sg.T(size=(10, 1), text="Temple"),
                                      sg.Input(default_text=0, key="_construct_temple__", size=(10, 1))],
                                 ))],

                                 ])),
                             sg.Frame("", background_color="#FFF", pad=(15, 15), layout=(
                                 [[sg.Frame("Cavern", pad=(15, 15), layout=(
                                     [sg.T(size=(10, 1), text="Diamond Mine"),
                                      sg.Input(default_text=0, key="_construct_diam_mine__", size=(10, 1))],
                                     [sg.T(size=(10, 1), text="School"),
                                      sg.Input(default_text=0, key="_construct_school__", size=(10, 1))],
                                 ))],
                                  [sg.Frame("Forest", pad=(15, 15), layout=(
                                      [sg.T(size=(10, 1), text="Lumberyard"),
                                       sg.Input(default_text=0, key="_construct_lumberyard__", size=(10, 1))],
                                      [sg.T(size=(10, 1), text="Forest Heaven"),
                                       sg.Input(default_text=0, key="_construct_forest_hven__", size=(10, 1))],
                                  ))],
                                  [sg.Frame("Hill", pad=(15, 15), layout=(
                                      [sg.T(size=(10, 1), text="Home"),
                                       sg.Input(default_text=0, key="_construct_home__", size=(10, 1))],
                                      [sg.T(size=(10, 1), text="Factory"),
                                       sg.Input(default_text=0, key="_construct_factory__", size=(10, 1))],
                                      [sg.T(size=(10, 1), text="Guard Tower"),
                                       sg.Input(default_text=0, key="_construct_gtower__", size=(10, 1))],
                                      [sg.T(size=(10, 1), text="Shrine"),
                                       sg.Input(default_text=0, key="_construct_shrine__", size=(10, 1))],
                                      [sg.T(size=(10, 1), text="Barracks"),
                                       sg.Input(default_text=0, key="_construct_baracks__", size=(10, 1))],
                                  ))],
                                  [sg.Frame("Special", pad=(15, 15), layout=(
                                      [sg.T(size=(10, 1), text="Mycelia"),
                                       sg.Input(default_text=0, key="_construct_mycelia__", size=(10, 1))],

                                  ))],
                                  ])),
                             ], [sg.Frame("Water", background_color="#FFF", pad=(15, 15), layout=(
                                [sg.T(size=(10, 1), pad=(10, 10), text="Docks"),
                                 sg.Input(default_text=0, key="_construct_docs__", size=(10, 1))],

                            ))],[sg.T(" " * 60),
                             sg.Button(image_filename="media/blue_accept_ok.png", button_color=("#d4d0c8", "#FFF"),
                                       key="_add_time_construct_button_", pad=(5, 5))]
                        ]), )

                         ],
                    ])
                          )]]
            Construct_window = sg.Window('Construct Buildings', icon="media/construct.ico",
                                         element_justification="left",
                                         auto_size_buttons=True,
                                         background_color="#d4d0c8",
                                         use_default_focus=True,
                                         text_justification="left",
                                         keep_on_top=True,
                                         debugger_enabled=False,
                                         ).Layout(ConstructLand).Finalize()

            event, values = Construct_window.Read()
            if event == "_add_time_construct_button_":
                json_construct_data = "\
    Alchemy:%s,Farm:%s,Smithy:%s,Masonry:%s,Ore Mine:%s,Gryphon Nest:%s,Tower:%s,\
    Wizard Guild:%s,Temple:%s,Diamond Mine:%s,School:%s,Lumberyard:%s,Forest Heaven:%s,\
    Home:%s,Factory:%s,Guard Tower:%s,Shrine:%s,Barracks:%s,Mycelia:%s,Docks:%s\
                " % (
                    get_number(values['_construct_alchemy__']),
                    get_number(values['_construct_farm__']),
                    get_number(values['_construct_smithy__']),
                    get_number(values['_construct_masonry__']),
                    get_number(values['_construct_ore_mine_']),
                    get_number(values['_construct_gryphon_nest__']),
                    get_number(values['_construct_tower__']),
                    get_number(values['_construct_wizguild__']),
                    get_number(values['_construct_temple__']),
                    get_number(values['_construct_diam_mine__']),
                    get_number(values['_construct_school__']),
                    get_number(values['_construct_lumberyard__']),
                    get_number(values['_construct_forest_hven__']),
                    get_number(values['_construct_home__']),
                    get_number(values['_construct_factory__']),
                    get_number(values['_construct_gtower__']),
                    get_number(values['_construct_shrine__']),
                    get_number(values['_construct_baracks__']),
                    get_number(values['_construct_mycelia__']),
                    get_number(values['_construct_docs__'])
                )
                sound(1)
                query("Insert into [Events] (event_date,event_type,insert_data,maximum_possible,repeat_end,repeat_time,repeating) "
                      "values (?,?,?,?,?,?,?)", 1,
                      [
                          values['_starting_date_construct_'],
                          "Construct Land",
                          json_construct_data,
                          values["_build_max_possible_"],
                          values["_end_date_construct_"],
                          values["_repeat_add_construct_min_"],
                          values["_repeat_add_construct_"]
                       ])
                Construct_window.Close()
                update_table(Main_Window)
     #################################################################################################################################

    # Event ADD Military Menu
        if event == "Military":
            sound()

            MilitaryLayout = [
                [sg.Frame("", element_justification="center", pad=(5, 5), layout=(
                    [sg.Frame("Timers", layout=(
                        [sg.T("Date Format DD/MM/YY 24:00")],
                        [sg.T("Start Time"), sg.InputText(default_text=date_format(datetime.datetime.now()), pad=(10, 10), size=(15, 1),
                                                          key="_starting_date_add_military_")],
                        [sg.T("End Time"), sg.InputText(default_text=date_format(datetime.datetime.now()), pad=(10, 10), size=(15, 1),
                                                        key="_ending_date_add_military_")],
                        [sg.T("Repeat"), sg.Checkbox("", key="_repeat_add_military_"), sg.T("every"),
                         sg.Input("0", pad=(10, 10), size=(5, 1), key="_repeat_add_military_min_"), sg.T("minutes")
                         ]))],
                    [sg.Frame("Units To Train", pad=(25, 25),element_justification="center", layout=([
                        [sg.Checkbox("Add Maximum Possible", pad=(10, 10), key="_add_military_max_possible_")],
                        [sg.T(size=(30, 1), text="      Military Name          Add Number", background_color="#fff",
                              pad=(10, 10))],
                        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                        [sg.T(size=(10, 1), text=render_units(dominion_config()[11])[0]),
                         sg.Input(pad=(5, 5), default_text=0, key="_add_military_unit_1_", size=(10, 1))],
                        [sg.T(size=(10, 1), text=render_units(dominion_config()[11])[1]),
                         sg.Input(pad=(5, 5), default_text=0, key="_add_military_unit_2_", size=(10, 1))],
                        [sg.T(size=(10, 1), text=render_units(dominion_config()[11])[2]),
                         sg.Input(pad=(5, 5), default_text=0, key="_add_military_unit_3_", size=(10, 1))],
                        [sg.T(size=(10, 1), text=render_units(dominion_config()[11])[3]),
                         sg.Input(pad=(5, 5), default_text=0, key="_add_military_unit_4_", size=(10, 1))],
                        [sg.T(size=(10, 1), text="Spies"),
                         sg.Input(pad=(5, 5), default_text=0, key="_add_military_unit_5_", size=(10, 1))],
                        [sg.T(size=(10, 1), text="Wizzards"),
                         sg.Input(pad=(5, 5), default_text=0, key="_add_military_unit_6_", size=(10, 1))],
                        [sg.T(size=(10, 1), text="Archmages"),
                         sg.Input(pad=(5, 5), default_text=0, key="_add_military_unit_7_", size=(10, 1))],
                        [sg.Button(image_filename="media/blue_accept_ok.png", button_color=("#d4d0c8", "#FFF"),
                                   key="_add_time_military_btn_", pad=(5, 5))]
                    ]))]
                ))]]

            military_window = sg.Window('Military Adder', icon="",
                                           element_justification="center",
                                           auto_size_buttons=True,
                                           background_color="#d4d0c8",
                                           use_default_focus=True,
                                           text_justification="left",
                                           keep_on_top=True,
                                           debugger_enabled=False,
                                           ).Layout(MilitaryLayout).Finalize()

            event, values = military_window.Read()

            if event == "_add_time_military_btn_":
                json_military_data = """%s: %s, %s: %s, %s: %s, %s: %s, Spies: %s,  Wizzards: %s, Archmages: %s""" % (
                   render_units(dominion_config()[11])[0],
                   get_number(values['_add_military_unit_1_']),
                   render_units(dominion_config()[11])[1],
                   get_number(values['_add_military_unit_2_']),
                   render_units(dominion_config()[11])[2],
                   get_number(values['_add_military_unit_3_']),
                   render_units(dominion_config()[11])[3],
                   get_number(values['_add_military_unit_4_']),
                   get_number(values['_add_military_unit_5_']),
                   get_number(values['_add_military_unit_6_']),
                   get_number(values['_add_military_unit_7_'])
                )
                sound(1)
                query(
                    "Insert into [Events] (event_date,event_type,insert_data,maximum_possible,repeat_end,repeat_time,repeating)"
                    " values (?,?,?,?,?,?,?)", 1,
                    [
                        values['_starting_date_add_military_'],
                        "Military Train",
                        json_military_data,
                        values["_add_military_max_possible_"],
                        values['_ending_date_add_military_'],
                        values['_repeat_add_military_min_'],
                        values['_repeat_add_military_'],
                    ])
                military_window.Close()
                update_table(Main_Window)

    # Cast Magic Menu
        if event == "Magic":
            sound()
            MilitaryLayout = [
                [sg.Frame("", element_justification="center", pad=(5, 5), layout=(
                    [sg.Frame("Timers", layout=(
                        [sg.T("Date Format DD/MM/YY 24:00")],
                        [sg.T("Start Time"), sg.InputText(default_text=date_format(datetime.datetime.now()), pad=(10, 10), size=(15, 1),
                                                          key="_starting_date_cast_magic_")],
                        [sg.T("End Time"), sg.InputText(default_text=date_format(datetime.datetime.now()), pad=(10, 10), size=(15, 1),
                                                        key="_ending_date_cast_magic_")],
                        [sg.T("Repeat"), sg.Checkbox("", key="_repeat_cast_magic_"), sg.T("every"),
                         sg.Input("0", pad=(10, 10), size=(5, 1), key="_repeat_cast_magic_time_"), sg.T("minutes")
                         ]))],
                    [sg.Frame("Magic to cast", pad=(25, 25),element_justification="left", layout=([
                        [sg.Checkbox("Gaia's Watch", pad=(10, 10), key="_cast_gaias_watch_")],
                        [sg.Checkbox("Mining Strength", pad=(10, 10), key="_cast_mining_strength_")],
                        [sg.Checkbox("Harmony", pad=(10, 10), key="_cast_harmony")],
                        [sg.Checkbox("Fool's Gold", pad=(10, 10), key="_cast_fools_gold_")],
                        [sg.Checkbox("Surreal Perception", pad=(10, 10), key="_cast_surreal_perception_")],
                        [sg.Checkbox("Energy Mirror", pad=(10, 10), key="_cast_energy_mirror_")],
                        [sg.Checkbox("Race Special", pad=(10, 10), key="_cast_special_race_magic_")],
                    ]))],
                    [sg.Button(image_filename="media/blue_accept_ok.png", button_color=("#d4d0c8", "#FFF"),
                               key="_add_time_magic_cast_btn_", pad=(5, 5))]
                ))]]

            military_window = sg.Window('Magic Caster', icon="",
                                           element_justification="left",
                                           auto_size_buttons=True,
                                           background_color="#d4d0c8",
                                           use_default_focus=True,
                                           text_justification="left",
                                           keep_on_top=True,
                                           debugger_enabled=False,
                                           ).Layout(MilitaryLayout).Finalize()

            event, values = military_window.Read()

            if event == "_add_time_magic_cast_btn_":
                json_magic_data = """Gaias Watch: %s,  Mining Strength: %s, Harmony: %s,Fool's Gold: %s, Surreal Perception: %s, Energy Mirror: %s, Race Special: %s""" % (
                    get_number(values['_cast_gaias_watch_']),
                    get_number(values['_cast_mining_strength_']),
                    get_number(values['_cast_harmony']),
                    get_number(values['_cast_fools_gold_']),
                    get_number(values['_cast_surreal_perception_']),
                    get_number(values['_cast_energy_mirror_']),
                    get_number(values['_cast_special_race_magic_']),
                )
                sound(1)
                query(
                    "Insert into [Events] (event_date, event_type, insert_data, repeat_end, repeat_time, repeating)"
                    " values (?,?,?,?,?,?)", 1,
                    [
                        values['_starting_date_cast_magic_'],
                        "Magic Cast",
                        json_magic_data,
                        values['_ending_date_cast_magic_'],
                        values['_repeat_cast_magic_'],
                        values['_repeat_cast_magic_time_']
                    ])
                military_window.Close()
                update_table(Main_Window)
    ###############################################################################################################
    ## WebDriver Static Events Logic ##############################################################################

        if event == "_start_program_":
            if len(event_list(1)) > 0:
                query("Update dominion set safe_run = 1", 1)
                threading.Thread(target=botter).start()
            else:
                sound(3)
                sg.PopupError("The event list is empty or all tasks are completed",
                              button_color=(sg.COLOR_SYSTEM_DEFAULT),
                              icon="media/system.png",
                              auto_close=True,
                              auto_close_duration=1,
                              no_titlebar=True,
                              keep_on_top=True
                              )

        elif event == "_stop_program_":
            query("Update dominion set safe_run = 2",1)

if __name__ == "__main__":
   gui()