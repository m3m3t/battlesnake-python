import search


class Snake:
    def __init__(self, _myid, _height, _width):
        self.myid = _myid
        self._length = 10 #TODO: ?
        self._health = 100
        self._grid = search.SquareGrid(_height, _width)
        #self._position = (0,0)

    def gather_food(self, food, obstacles):
        self._grid.obstacles = obstacles
        move = search.get_move(self._grid, self.head, food)
        return move

    def on_offense(self):
        pass

    def on_defense(self):
        pass

    def health(self):
        return self._health


    def status(self):
        return self._health / self._length

    def length(self):
        return self._length
    
    @property
    def myid(self):
        return self._myid
    @myid.setter
    def myid(self, _myid):
        self._myid = _myid

    @property
    def head(self):
        return self._position

    @head.setter
    def head(self, pos):
        self._position = pos

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, turn):
        self._turn = turn
