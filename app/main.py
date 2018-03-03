import bottle
import os
import random
import numpy as np
from snake import Snake

"""
class Strategy:
    SCARED
    HUNGRY
"""

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
    data = bottle.request.json
    
    my_id = data["you"]["id"]
    my_len = data["you"]["length"]
    my_health = data["you"]["health"]
    
    board_food = len(data["food"]["data"])
    board_width = data['width']
    board_height = data['height']
   
    print "health={}  len={}   food={}".format(my_health, my_len, board_food) 

    # TODO: Do things with data
    me = Snake(my_id, board_height, board_width)
    
    blockades =  map(lambda x: extend_head(x,me), data["snakes"]["data"])
    blockades = list(set([ y for x in blockades for y in x ]))

    food = [ (c["x"],c["y"]) for c in data["food"]["data"] ] 
    food.sort(key=lambda xy: abs(xy[0] - me.head[0]) + abs(xy[1] - me.head[1])) 
        
    if my_health < 75 or my_len < 5:
        move = me.gather_food(food[:3], blockades)
    else:
        #blockades.extend(food)
        move = me.go_chase(blockades)

    #directions = ['up', 'down', 'left', 'right']
    #move = random.choice(directions)
    return {
        'move': move,
        'taunt': 'battlesnake-python!'
    }

def extend_head(snake, me):
    coords = [ (c["x"],c["y"]) for c in snake["body"]["data"] ] 
    #print "Have snake: {} -> {}".format(snake["id"], coords)
    head = (x,y) = coords[0]

    #print "head = ( {}, {} )".format(x,y)
    if snake["id"] == me.myid:
        me.head = head
        me.tail = coords[-1] 
        #me.chase.append(coords[-1])
        return coords

    me.chase.append(coords[-1]) 
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
        host=os.getenv('IP', '127.0.0.1'),
        port=os.getenv('PORT', '8080'),
        debug = True)
