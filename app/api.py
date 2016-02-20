
class MOVE(object):
    NORTH = "north"
    EAST = "east"
    WEST = "west"
    SOUTH = "south"

class SEND(object):
    GET   = {
                "color": "#FF0000",
                "head": "http://www.clker.com/cliparts/D/i/A/w/J/R/snake-no-white-drule-hi.png",
            }
    START = {
                "taunt": "Let's rock!"
            }
    MOVE = {
                "move" : "north",
                "taunt": "Let's rock!"
           }

RESPONSE = {
                "game": "hairy-cheese",
                "mode": "advanced",
                "turn": 0,
                "height": 20,
                "width": 30,
                "snakes": [
                            #<Snake Object>, <Snake Object>, ...
                          ],
                "food": [],
                "walls": [],  // Advanced Only
                "gold": []    // Advanced Only
            
             }
STATE = 
        {
            "id": "3fc52e17-4dcf-48df-b2b7-c5f69838e92f",
            "name": "Well Documented Snake",
            "status": "alive",
            "message": "Moved north",
            "taunt": "Let's rock!",
            "age": 56,
            "health": 83,
            "coords": [ [1, 1], [1, 2], [2, 2] ],
            "kills": 4,
            "food": 12,
            "gold": 2
        }
