from datetime import timedelta
from sqlite3 import Error
from selenium.webdriver.common.proxy import Proxy, ProxyType

import datetime, os, sys, time, numpy, random, winsound, platform, subprocess, sqlite3, threading

if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

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



def conn(db = r"dominion.db"):
        global conns
        try:
            conns = sqlite3.connect(db, check_same_thread=False)
        except Error as e:
            exit(e)
        finally:
            return conns


''' Select Query Type 0, insert, update and delete is type 1, default 0'''
def query(task: object, type: object = 0, params: object = "", how_many: object = 0, conn: object = conn()) -> object:
    cur = conn.cursor()
    try:
        if type == 1:
          cur.execute(task, params)
          conn.commit()
        else:
            cur.execute(task)
            if how_many == 1:
               return cur.fetchone()
            else:
               return cur.fetchall()

    except sqlite3.Error as e:
        exit(e)

createTables()



if len(query("Select * from Dominion")) == 0:
    query("Insert into Dominion (sound) values (?)", 1, [0])

def dominion_config():
    dominion_conf = query(f"Select * from [Dominion] ")
    return dominion_conf[0]


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


def generate_random_clicks():
    links = [
        dominion_config()[14] + 'dominion/status',
        dominion_config()[14] + 'dominion/advisors',
        dominion_config()[14] + 'dominion/bonuses',
        dominion_config()[14] + 'dominion/explore',
        dominion_config()[14] + 'dominion/construct',
        dominion_config()[14] + 'dominion/rezone',
        dominion_config()[14] + 'dominion/improvements',
        dominion_config()[14] + 'dominion/bank',
        dominion_config()[14] + 'dominion/military',
        dominion_config()[14] + 'dominion/invade',
        dominion_config()[14] + 'dominion/magic',
        dominion_config()[14] + 'dominion/espionage',
        dominion_config()[14] + 'dominion/search',
        dominion_config()[14] + 'dominion/council',
        dominion_config()[14] + 'dominion/op-center',
        dominion_config()[14] + 'dominion/government',
        dominion_config()[14] + 'dominion/realm',
        dominion_config()[14] + 'dominion/rankings/land',
        dominion_config()[14] + 'dominion/town-crier',
        dominion_config()[14] + 'scribes/races',
        dominion_config()[14] + 'scribes/construction',
        dominion_config()[14] + 'dominion/advisors/military',
        dominion_config()[14] + 'dominion/advisors/construct',
        dominion_config()[14] + 'dominion/advisors/statistics',
        dominion_config()[14] + 'dominion/advisors/land',
        dominion_config()[14] + 'dominion/advisors/production'
    ]
    return numpy.random.choice(numpy.roll(links, random.randint(0, 999999)), size=random.randint(2, 20), replace=False)


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

    while dominion_config()[12] == 1:
        if dominion_config()[13]:
            driver.set_window_position(-2000, 0)
        else:
            driver.set_window_position(0, 0)

        sound(2)
        field_fill_delay()
        if int(dominion_config()[9]) == 0 and int(dominion_config()[10]) == 0:
            try:
                driver.get(dominion_config()[14] + "auth/login")
                field_fill_delay()
                driver.find_element_by_id("email").send_keys(dominion_config()[2])
                field_fill_delay()
                driver.find_element_by_id("password").send_keys(dominion_config()[3])
                driver.find_element_by_name("remember").click()
                field_fill_delay()
                driver.find_element_by_css_selector(".btn.btn-primary").click()

            except IOError as e:
                exit("The program can login to the website ERROR:%s" % e)
        elif int(dominion_config()[10]) == 1 and int(dominion_config()[9]) == 0:
            driver.get(dominion_config()[14] + "auth/login")
            sg.Popup(
                "You have 10 minutes to login, after successful login. Close the window and restart the program,"
                "You can then uncheck the /manual login/ button and check /use session/. "
                "At the next run the program will try to use the saved credentials")
            time.sleep(1000)
        elif int(dominion_config()[9]) == 1 and int(dominion_config()[10]) == 0:
            pass
        while True:
            if dominion_config()[12] == 2:
                driver.close()
            if dominion_config()[13]:
                driver.set_window_position(-2000, 0)
            else:
                driver.set_window_position(0, 0)
            for each_event in event_list(1):
                if dominion_config()[0] == 1:
                    for each_fake_click in generate_random_clicks():
                        driver.get(each_fake_click)
                        time.sleep(random.randint(30, 300) / 10)
                        if date_format(datetime.datetime.now()) >= each_event[1]:
                            break
                events_config = []
                for k in query(f"Select * from [Events_Config]"):
                    if k[1] == each_event[2]:
                        events_config.append(k)

                if events_config[0][1] == "Magic Cast":
                    print(dominion_config()[14] + events_config[0][2])
                    break
                else: #FOR THE FORM FIELDS TO FILL
                    if events_config[0][1] == each_event[2] and date_format(datetime.datetime.now()) >= each_event[1]:
                       # try:
                        driver.get(dominion_config()[14] + events_config[0][2])
                        error = 0

                        form_fields = str(events_config[0][4]).split(",")
                        for i in range(0, len(form_fields)):
                            try:
                              driver.find_element_by_name(form_fields[i]).is_displayed()
                            except:
                                continue

                            max_possible = driver.find_element_by_name(form_fields[i]).get_attribute("placeholder")

                            if  max_possible == '0':
                                max_possible = driver.find_element_by_name(form_fields[i]).get_attribute("max")


                            if int(ev_data()[i][1]) > 0:

                                if int(each_event[4]) == 1 and max_possible > ev_data()[i][1]:
                                    driver.find_element_by_name(form_fields[i]).send_keys(max_possible)
                                else:
                                    driver.find_element_by_name(form_fields[i]).send_keys(ev_data()[i][1])
                            field_fill_delay()

                        try:
                            driver.find_element_by_xpath(events_config[0][3]).click()
                        except:
                            driver.find_element_by_css_selector("body > div > div > section > div.row > div.col-sm-12.col-md-9 > div > form > div.box-footer > button").click()

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

brlist = [
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; yie11; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-G930F Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_4; de-de) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.2 Safari/525.20.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1",
    "Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-G900F Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla / 5.0(compatible; bingbot / 2.0; +http://www.bing.com/bingbot.htm)",
    "AdsBot-Google (+http://www.google.com/adsbot.html)",
    "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
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