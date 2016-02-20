import bottle
import os
from search import *
from snake import Snake

ID="3fc52e17-4dcf-48df-b2b7-c5f69838e92f"
CURRENT

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#00ff00',
        'head': head_url
    }

def get_taunt():
    return "TODO"

@bottle.post('/start')
def start():
    data = bottle.request.json
    
    TURN = data["turn"]
    CURRENT = [ snake["coords"] for snake in data["snakes"] if data["snake"]["id "]== ID ][0]


    return {
        'taunt': get_taunt() 
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    GRID = SquareGrid(data["height"], data["width"])
    GRID.snakes = [ x for snake in data["snakes"] for x in data["snakes"]["coords"] ]

    FOOD = [ food for food in data["food"] ]

    move = get_move(grid)

    return {
        'move': move,
        'taunt': 'battlesnake-python!'
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
