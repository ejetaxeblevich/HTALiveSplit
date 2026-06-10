import os
import time
import re
import traceback
import socket
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


log("HTALiveSplit v1.0 Startup...")


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

LOG_FILE = config["GLOBALPATH_EXMACHINA_LOG"]
SPLITS_FILE = config["GLOBALPATH_SPLITS"]
HOST = config["LIVESPLIT_HOST"]
PORT = config["LIVESPLIT_PORT"]

LS_ISPAUSE_LOADLEVEL = config["LIVESPLIT_PAUSE_WhenLevelLoading"]
LS_ISPAUSE_LOADSAVE = config["LIVESPLIT_PAUSE_WhenSaveLoading"]
LS_ISPAUSE_DOSAVE = config["LIVESPLIT_PAUSE_WhenGameSaving"]

LS_START = config["LIVESPLIT_TCP_COMMAND_START"]
LS_STOP = config["LIVESPLIT_TCP_COMMAND_STOP"]
LS_RESET = config["LIVESPLIT_TCP_COMMAND_RESET"]
LS_PAUSE = config["LIVESPLIT_TCP_COMMAND_PAUSE"]
LS_RESUME = config["LIVESPLIT_TCP_COMMAND_RESUME"]
LS_GETTIMERPHASE = config["LIVESPLIT_TCP_COMMAND_GETTIMERPHASE"]
LS_GETTIMER = config["LIVESPLIT_TCP_COMMAND_GETTIMER"]
LS_SPLIT = config["LIVESPLIT_TCP_COMMAND_SPLIT"]

M_LOADING_LEVEL_START = config["MATCH_LOADING_LEVEL_START"]
M_LOADING_LEVEL_END = config["MATCH_LOADING_LEVEL_END"]
M_LOADING_SAVE_START = config["MATCH_LOADING_SAVE_START"]
M_LOADING_SAVE_END = config["MATCH_LOADING_SAVE_END"]
M_SAVING_START = config["MATCH_SAVING_START"]
M_SAVING_END = config["MATCH_SAVING_END"]

log(f'Config: LOG_FILE {LOG_FILE}')
log(f'Config: SPLITS_FILE {SPLITS_FILE}')
log(f'Config: HOST {HOST}')
log(f'Config: PORT {PORT}')

log(f"Loading splits {SPLITS_FILE}...")

splits= load_json(SPLITS_FILE)

START_MAP = splits["LOCALPATH_EXMACHINA_FIRSTLEVEL"]
MAINMENU_MAP = splits["LOCALPATH_EXMACHINA_MAINMENULEVEL"]
SPLITS = splits["SPLIT_QUESTS"]

log(f'Splits: START_MAP {START_MAP}')
log(f'Splits: MAINMENU_MAP {MAINMENU_MAP}')
log(f'Splits: SPLITS {SPLITS}')

sock = None

started = False
wait_for_start = False
loading_map = False
loading_save = False
saving = False
last_quest = ""

quest_complete_re = re.compile(r"Quest '(.+?)' is complete")
loading_level_re = re.compile(r"-- Loading Level: (.+?) --")
saving_level_re = re.compile(r"Game '(.+?)' saved.")


def open_log():
    while not os.path.exists(LOG_FILE):
        log("Waiting for log file...")
        time.sleep(1)

    log("Log found")
    return open(LOG_FILE, "r", encoding="utf-8", errors="ignore")

def connect_livesplit():
    global sock
    try:
        sock = socket.create_connection((HOST, PORT))
        log("Connected to LiveSplit")
    except Exception as e:
        log(f"LiveSplit not found: {e}")
        sock = None

def livesplit(command):
    global sock
    if sock is None:
        return
    
    #log("LiveSplit >", command)

    sock.sendall((command + "\r\n").encode())
    sock.settimeout(0.5)
    try:
        return sock.recv(1024).decode().strip()
    except:
        return "<nothing>"

def clean_cache():
    global started
    global wait_for_start
    global loading_map
    global loading_save
    global saving
    global last_quest
    started = False
    wait_for_start = False
    loading_map = False
    loading_save = False
    saving = False
    last_quest = ""
    
    livesplit(LS_STOP)

########################################################

f = open_log()

f.seek(0, os.SEEK_END)

connect_livesplit()
livesplit(LS_GETTIMERPHASE)
livesplit(LS_RESET)


while True:
    try:
        line = f.readline()
        if not line:
            try:
                current_size = os.path.getsize(LOG_FILE)
            except FileNotFoundError:
                current_size = -1

            current_pos = f.tell()

            if current_size >= 0 and current_pos > current_size:
                log("Log recreated, reopening...")
                
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
        if M_SAVING_END in line and saving:
            saving = False
            log("[SAVING END]")
            if started and LS_ISPAUSE_DOSAVE:
                livesplit(LS_RESUME)
            
        match = loading_level_re.search(line)
        if match:
            level = match.group(1)
            log(f"[LEVEL] {level}")

            if level.lower() == START_MAP.lower() and not started:
                wait_for_start = True
                livesplit(LS_RESET)
                log("[WAITING FOR START RUN]")
                
            if level.lower() == MAINMENU_MAP.lower() and started:
                clean_cache()
                log("[STOP RUN]")
                livesplit(LS_STOP)
                
        match = quest_complete_re.search(line)
        if match:
            quest = match.group(1)
            log(f"[QUEST COMPLETE] {quest}")
            if quest!=last_quest and started and quest in SPLITS:
                last_quest = quest
                livesplit(LS_SPLIT)
                
                if livesplit(LS_GETTIMERPHASE) == "Ended":
                    final_time = livesplit(LS_GETTIMER)
                    log(f"[RUN COMPLETE] {final_time}")

    except Exception:
        traceback.print_exc()

        try:
            f.close()
        except:
            pass

        time.sleep(1)
        f = open_log()