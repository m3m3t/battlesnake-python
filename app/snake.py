
class Snake:
    def __init__(self, _id, position, turn):
        self._id = _id
        self._position = position
        self._turn = turn
    
    def id(self):
        return self.id
    
    def current(self):
        return self._position

    def turn(self):
        return self._turn

