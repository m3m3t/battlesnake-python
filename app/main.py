import bottle
import os
import random

class Strategy(enum):
    SCARED
    HUNGRY

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

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    
    my_id = data["you"]
    board_width = data['width']
    board_height = data['height']
    me = Snake(my_id, board_height, board_width)
    
    blockades =  map(lambda x: extend_head(x,me), data["snakes"])
    blockades = blockades[0]
    
    food.sort(key=lambda xy: abs(xy[0] - me.head[0]) + abs(xy[1] - me.head[1])) 
    food = food[:3]
    
    move = me.gather_food(food, blockades)
    #move = me.run_free(food, blockades)

    # TODO: Do things with data
    
    directions = ['up', 'down', 'left', 'right']
    move = random.choice(directions)
    print move 
    return {
        'move': move,
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
