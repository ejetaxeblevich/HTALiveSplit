import os
import time
import re
import traceback
import socket
import psutil
import json
from pathlib import Path
import sys
from datetime import datetime

# -*- coding: utf-8 -*-

LOG_OUTPUT = Path(
    f"HTALiveSplitLOG\\HTALiveSplit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_OUTPUT, "a", encoding="utf-8") as f:
        f.write(line + "\n")
        f.flush()


log("HTALiveSplit v1.2 Startup...")


def load_json(path):
    for encoding in ("utf-8", "utf-8-sig", "cp1251"):
        try:
            with open(path, encoding=encoding) as f:
                return json.load(f)
        except UnicodeDecodeError:
            pass

    raise RuntimeError(f"Cannot read {path}")


BASE_DIR = Path(sys.argv[0]).resolve().parent
CONFIG_FILE = BASE_DIR / "HTALiveSplit_config.json"

log(f"Loading config {CONFIG_FILE}...")

config = load_json(CONFIG_FILE)

GAME_LOG = ['\\exmachina.log', '\\emarcade.log']
LOG_FILE = ""

GAME_FOLDER_EXE = config["GLOBALPATH_EXMACHINA_EXE"]
GAME_EXE = str(Path(GAME_FOLDER_EXE).name)
GAME_FOLDER = str(Path(GAME_FOLDER_EXE).parent)

SPLITS_FILE = config["GLOBALPATH_SPLITS"]
HOST = config["LIVESPLIT_HOST"]
PORT = config["LIVESPLIT_PORT"]

LS_ISPAUSE_LOADLEVEL = config["LIVESPLIT_PAUSE_WhenLevelLoading"]
LS_ISPAUSE_LOADSAVE = config["LIVESPLIT_PAUSE_WhenSaveLoading"]
LS_ISPAUSE_DOSAVE = config["LIVESPLIT_PAUSE_WhenGameSaving"]

LS_START = config["LIVESPLIT_TCP_COMMAND_START"]
LS_RESET = config["LIVESPLIT_TCP_COMMAND_RESET"]
LS_PAUSE = config["LIVESPLIT_TCP_COMMAND_PAUSE"]
LS_RESUME = config["LIVESPLIT_TCP_COMMAND_RESUME"]
LS_GETTIMERPHASE = config["LIVESPLIT_TCP_COMMAND_GETTIMERPHASE"]
LS_GETTIMER = config["LIVESPLIT_TCP_COMMAND_GETTIMER"]
LS_SPLIT = config["LIVESPLIT_TCP_COMMAND_SPLIT"]

M_LEVEL = config["MATCH_LEVEL"]
M_QUEST = config["MATCH_QUEST"]
M_SAVED = config["MATCH_SAVED"]

M_LOADING_LEVEL_START = config["MATCH_LOADING_LEVEL_START"]
M_LOADING_LEVEL_END = config["MATCH_LOADING_LEVEL_END"]
M_LOADING_SAVE_START = config["MATCH_LOADING_SAVE_START"]
M_LOADING_SAVE_END = config["MATCH_LOADING_SAVE_END"]
M_SAVING_START = config["MATCH_SAVING_START"]
M_SAVING_END = config["MATCH_SAVING_END"]
M_LOG_END = config["MATCH_EXMACHINA_LOG_END"]

log(f'Config: GAME_EXE {GAME_FOLDER_EXE}')
log(f'Config: SPLITS_FILE {SPLITS_FILE}')
log(f'Config: HOST {HOST}')
log(f'Config: PORT {PORT}')

log(f"Loading splits {SPLITS_FILE}...")

splits = load_json(SPLITS_FILE)

START_MAP = splits["LOCALPATH_EXMACHINA_FIRSTLEVEL"]
MAINMENU_MAP = splits["LOCALPATH_EXMACHINA_MAINMENULEVEL"]
SPLIT_QUESTS = splits["SPLIT_QUESTS"]
SPLIT_LEVELS = splits["SPLIT_LEVELS"]
SPLIT_CUSTOM = splits["SPLIT_CUSTOM"]

log(f'Splits: START_MAP {START_MAP}')
log(f'Splits: MAINMENU_MAP {MAINMENU_MAP}')
log(f'Splits: SPLIT_QUESTS {SPLIT_QUESTS}')
log(f'Splits: SPLIT_LEVELS {SPLIT_LEVELS}')
log(f'Splits: SPLIT_CUSTOM {SPLIT_CUSTOM}')

game = None
last_game_state = None
last_log_state = None

sock = None
last_sock_state = None

started = False
wait_for_start = False
loading_map = False
loading_save = False
saving = False

last_quest = ""
last_custom_log = ""
levels = []

quest_complete_re = re.compile(rf"{M_QUEST}")
loading_level_re = re.compile(rf"{M_LEVEL}")
saving_level_re = re.compile(rf"{M_SAVED}")


def find_game():
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == GAME_EXE:
            return proc
    return None

def get_game():
    global game
    global last_game_state
    global LOG_FILE
    while True:
        game = find_game()
        if game:
            log(f"Game exe found: {game.cmdline()}")
            for logfile in GAME_LOG:
                LOG_FILE = GAME_FOLDER + logfile
                if os.path.exists(LOG_FILE):
                    log(f"Game log found: {LOG_FILE}")
                    break

            if last_game_state!=True:
                last_game_state = True
                log("[GAME OPENED]")
            return game
        else:
            if last_game_state!=False:
                last_game_state = False
                log("Waiting for game process...")
            
            time.sleep(1)
    
def game_running():
    global game
    try:
        return game.status()
    except psutil.NoSuchProcess:
        return False
        


def open_log():
    global game
    global last_log_state
    global LOG_FILE
    while not os.path.exists(LOG_FILE):
        if last_log_state!=False:
            last_log_state = False
            log("Waiting for log file...")
        if not game_running():
            log("[GAME CLOSED]")
            game = get_game()
            
        time.sleep(1)
        
    last_log_state = True
    log("Log found")
    return open(LOG_FILE, "r", encoding="utf-8", errors="ignore")

def connect_livesplit():
    global sock
    global last_sock_state
    while True:
        try:
            sock = socket.create_connection((HOST, PORT))
            sock.settimeout(0.5)

            log("Connected to LiveSplit")
            last_sock_state = True
            return True
        except Exception as e:
            if last_sock_state!=False:
                last_sock_state = False
                log(f"LiveSplit not found: {e}")
            
            sock = None
            time.sleep(1)

def livesplit(command):
    global sock
    global last_sock_state
    if sock is None:
        connect_livesplit()
    
    #log("LiveSplit >", command)

    while True:
        try:
            sock.sendall((command + "\r\n").encode())
            return sock.recv(1024).decode().strip()
        except socket.timeout:
            return "<nothing>"
        except (BrokenPipeError,
                ConnectionResetError,
                ConnectionAbortedError,
                OSError) as e:
            if last_sock_state!=False:
                log(f"Lost LiveSplit connection: {e}")

            try:
                sock.close()
            except:
                pass

            sock = None
            connect_livesplit()

def livesplit_split():
    livesplit(LS_SPLIT)
    if livesplit(LS_GETTIMERPHASE) == "Ended":
        final_time = livesplit(LS_GETTIMER)
        log(f"[RUN COMPLETE] {final_time}")

def clean_cache():
    global started
    global wait_for_start
    global loading_map
    global loading_save
    global saving
    global last_quest
    global last_custom_log
    global levels
    started = False
    wait_for_start = False
    loading_map = False
    loading_save = False
    saving = False
    last_custom_log = ""
    last_quest = ""
    levels = []

########################################################

game = get_game()

f = open_log()

f.seek(0, os.SEEK_END)

connect_livesplit()
livesplit(LS_GETTIMERPHASE)
livesplit(LS_RESET)

last_process_check = time.monotonic()


while True:
    try:
        if time.monotonic() - last_process_check >= 1:
            last_process_check = time.monotonic()

            if not game_running():
                log("[GAME CLOSED]")
                livesplit(LS_PAUSE)
                
                game = get_game()
                f = open_log()
                f.seek(0)
                livesplit(LS_RESUME)
                livesplit(LS_RESET)
                
        line = f.readline()
        if not line:
            try:
                current_size = os.path.getsize(LOG_FILE)
            except FileNotFoundError:
                current_size = -1

            current_pos = f.tell()

            if current_size >= 0 and current_pos > current_size:
                log("Log recreated, reopening...")
                livesplit(LS_RESET)
                
                clean_cache()

                f.close()
                f = open_log()
                f.seek(0)

            time.sleep(0.05)
            continue


        ################### LiveSplit ###################
        line = line.strip()

        if M_LOADING_LEVEL_START in line and not loading_map:
            loading_map = True
            log("[LOAD MAP START]")
            if started and LS_ISPAUSE_LOADLEVEL:
                livesplit(LS_PAUSE)
        elif M_LOADING_LEVEL_END in line and loading_map:
            loading_map = False
            log("[LOAD MAP END]")
            if wait_for_start:
                wait_for_start = False
                started = True
                log("[START RUN]")
                livesplit(LS_START)
            elif started and LS_ISPAUSE_LOADLEVEL:
                livesplit(LS_RESUME)
            
        if M_LOADING_SAVE_START in line and not loading_save:
            loading_save = True
            log("[LOAD SAVE START]")
            if started and LS_ISPAUSE_LOADSAVE:
                livesplit(LS_PAUSE)
        elif M_LOADING_SAVE_END in line and loading_save:
            loading_save = False
            loading_map = False
            log("[LOAD SAVE&MAP END]")
            if started and LS_ISPAUSE_LOADSAVE:
                livesplit(LS_RESUME)
            
        if M_SAVING_START in line and not saving:
            saving = True
            log("[SAVING START]")
            if started and LS_ISPAUSE_DOSAVE:
                livesplit(LS_PAUSE)
        match = saving_level_re.search(line)
        if (M_SAVING_END in line or match) and saving:
            saving = False
            log("[SAVING END]")
            if started and LS_ISPAUSE_DOSAVE:
                livesplit(LS_RESUME)
            
        match = loading_level_re.search(line)
        if match:
            level = match.group(1)
            log(f"[LEVEL] {level}")
            
            level_l = level.lower()

            if level_l == START_MAP.lower() and not started:
                wait_for_start = True
                livesplit(LS_RESET)
                log("[WAITING FOR START RUN]")
                
            if (level_l not in levels) and (level in SPLIT_LEVELS) and started:
                levels.append(level)
                log("[SPLIT BY LEVEL]")
                livesplit_split()
                
            if level_l == MAINMENU_MAP.lower() and started:
                clean_cache()
                log("[STOP RUN]")
                livesplit(LS_PAUSE)
                
        match = quest_complete_re.search(line)
        if match:
            quest = match.group(1)
            log(f"[QUEST COMPLETE] {quest}")
            if quest!=last_quest and started and quest in SPLIT_QUESTS:
                last_quest = quest
                log("[SPLIT BY QUEST]")
                livesplit_split()
                
        for custom_log in SPLIT_CUSTOM:
            if custom_log in line and custom_log!=last_custom_log and started:
                last_custom_log = custom_log
                log(f"[SPLIT BY CUSTOM LOG] {custom_log}")
                livesplit_split()
        
        if M_LOG_END in line and started:
            clean_cache()
            log("[STOP RUN]")
            livesplit(LS_PAUSE)
                
    except Exception:
        traceback.print_exc()

        try:
            f.close()
        except:
            pass

        time.sleep(1)
        f = open_log()