import bottle
import os
import random

import numpy as np
from app.snake import Snake

"""
class Strategy:
    SCARED
    HUNGRY
"""

me = None

@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data
    me = Snake(my_id, board_height, board_width)

    {
        "color": "#FF0000",
        "secondary_color": "#00FF00",
        "head_url": "http://placecage.com/c/100/100",
        "taunt": "OH GOD NOT THE BEES",
        "head_type": "tongue",
        "tail_type": "curled"
    }


    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url
    }


@bottle.post('/move')
def move():
    global me
    data = bottle.request.json
    
    my_id = data["you"]
    board_width = data['width']
    board_height = data['height']
   # me = Snake(my_id, board_height, board_width)
    
    blockades =  map(lambda x: extend_head(x,me), data["snakes"]["data"])
    blockades = blockades[0]
   
    #TODO: strategy based on:
    # Number of snakes still on the board
    # Number of food on the board (calculate spawn frequency)
    # My current health
    # Do:
    #   - not eating : turn food into obstacles so I don't grow too big
    #   - remove last tail of other snakes (since it will be gone when I move)
    food.sort(key=lambda xy: abs(xy[0] - me.head[0]) + abs(xy[1] - me.head[1])) 
    food = food[:3]
    
    move = me.gather_food(food, blockades)
    #move = me.run_away(food, blockades)

    
    #directions = ['up', 'down', 'left', 'right']
    #move = random.choice(directions)
    print move 
    return {
        'move': move,
        'taunt': 'battlesnake-python!'
    }

def extend_head(snake, me):
    coords = map(tuple, snake["body"]["data"])
    #print "Have snake: {} -> {}".format(snake["id"], coords)
    head = (x,y) = coords[0][:2]
    #print "{} == {}".format(snake["id"], me.myid)

    if snake["id"] == me.myid:
        #print "Setting head position to {}".format(head)
        me.head = head
        return coords
    
    coords.extend([(x+1, y), (x, y-1), (x-1, y), (x, y+1)])
    return coords

def manhattan(xy):
    (x1,y1) = xy
    (x2,y2) = my_snake.head
    dx = abs(x1-x2)
    dy = abs(y1-y2)
    return dx + dy

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
