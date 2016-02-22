import bottle
import os
from search import *
from snake import Snake

ID="3fc52e17-4dcf-48df-b2b7-c5f69838e92f"
CURRENT = None


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.jpg' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#00ff00',
        'head': head_url
    }

def get_taunt():
    return "yomomma"

@bottle.post('/start')
def start():
    data = bottle.request.json

    TURN = data["turn"]

    return {
        'taunt': get_taunt() 
    }

def last_dir(data):
    snakes = data["snakes"]
    for snake in snakes:
        if snake["id"] == ID:
            coords = snake["coords"]
            direction = [coords[0][0] - coords[1][0], coords[0][1] - coords [1][1]]

    if direction[0]!=0:
        if direction[0]>0:
            return "east"
        else:
            return "west"
    else:
        if direction[1]>0:
            return "south"
        else:
            return "north"


@bottle.post('/move')
def move():
    global CURRENT
    data = bottle.request.json

    grid = SquareGrid(data["height"], data["width"])
    snakes = [ snake["coords"] for snake in data["snakes"]  ]
    grid.snakes = [ tuple(y) for x in snakes for y in x]

    
    current = [ snake["coords"] for snake in data["snakes"] if snake["id"] == ID ][0]
    for i, coords in enumerate(snakes):
        if coords[0] != current[0]: #and coords[0] not in data["food"]:
            [x,y] = coords[0]
            grid.snakes.extend([(x+1, y), (x, y-1), (x-1, y), (x, y+1)])
    
    #print "Current location: ", current[0] 
    last_direction = last_dir(data)
    food = [ x for x in data["food"] if x not in grid.snakes ]
    move = get_move(grid,current[0], food, last_direction)

    print "attempting: ",move
    if move == "east" and last_direction == "west":
        move = last_direction
    elif move == "west" and last_direction == "east":
        move = last_direction
    elif move == "south" and last_direction == "north":
        move = last_direction
    elif move == "north" and last_direction == "south":
        move = last_direction
    CURRENT = move
    print "last direction",last_direction
    print "moving to: ",move 
    return {
        'move': move,
        'taunt': 'yomomma'
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'suckit'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
