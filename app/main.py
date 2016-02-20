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

    return {
        'taunt': get_taunt() 
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    grid = SquareGrid(data["height"], data["width"])
    snakes = [ snake["coords"] for snake in data["snakes"]  ]
    grid.snakes = [ x for x snakes ]
    
    current = [ snake["coords"] for snake in data["snakes"] if snake["id"] == ID ][0]
    food = [ food for food in data["food"] ]
    
    print "Current location: ", current[0] 

    move = get_move(grid,current[0], food)

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
