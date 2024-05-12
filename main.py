from map import *
from globals import *
from civ import *
from unit import *
from APIcalls import *
from time import sleep
import json
import google.generativeai as genai
import google.api_core
import curses
import sys

debug_file = open("debug.log", "a")
log_file = open("output.log", "a")
sys.stdout = log_file
sys.stderr = debug_file

responses = []
context = [
{"role": "system", "content": init_prompt }
]

def addUnit(unit, civ, map):
    civ.units[unit.name] = unit # TODO HANDLE MULTIPLE UNITS OF SAME TYPE

def main(stdscr):
    # Initializing game
    player_civ = Civ("player")
    ai_civ = Civ("opponent")
    terrainMap = Map(10, 10)
    terrainMap.generate_terrain("preset")
    addUnit(Unit('warrior', 0, 'player', [0, 0]), player_civ, terrainMap)
    addUnit(Unit('warrior', 1, 'opponent', [9, 9]), ai_civ, terrainMap)

    #Initializing model
    GOOGLE_API_KEY='AIzaSyD3CTe6s7RIWeQKVfrUaaGVEkteYOa7eKU'
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    currTurn = 1

    curses.curs_set(0)  # Hide cursor
    curses.start_color()  # Enable color
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.addstr(0, 0, "Welcome to Civilization!", curses.A_BOLD)
    stdscr.addstr(2, 0, "Press any key to continue...", curses.A_NORMAL)
    stdscr.getch()
    while currTurn < maxTurns:
        stdscr.clear()
        stdscr.addstr("YEAR " + str(currTurn) + "\n")
        terrainMap.print_map_player(stdscr)
        print("PLAYER MOVE")
        stdscr.refresh()
        for name, unit in player_civ.units.items():
            key = stdscr.getch()
            if (key == ord('w')): # TODO BOUND CHECKING
                unit.coordinates[1] -= 1
            if (key == ord('s')):
                unit.coordinates[1] += 1
            if (key == ord('d')):
                unit.coordinates[0] += 1
            if (key == ord('a')):
                unit.coordinates[0] -= 1
            else:
                continue #TODO INVALID INPUT THING
        for city in player_civ.cities:
            pass
        request = make_request(context, terrainMap, ai_civ.cities, ai_civ.units)
        response = get_response(model, request)
        if response is not None:
            responses.append(response)
        else:
            print("Gemini Error!")
        currTurn += 1



if __name__ == "__main__":
    curses.wrapper(main)