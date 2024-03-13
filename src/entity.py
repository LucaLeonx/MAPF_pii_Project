from optional import Optional

class Entity():

    def __init__(self, label, description="", start_position=None):
        self._label = label
        self._description = description
        self._position = Optional.of(start_position)
    
    def __eq__(self, other):
        if isistance(other, Entity):
            return self._label == other._label
        else: 
            return False

    def get_label(self):
        return self._label
    
    def get_description(self):
        return self._description
    
    def is_position_available(self):
        return self._position.is_present()

    def get_position(self):
        return self._position

    def set_position(self, new_node):
        self._position = Optional.of(new_node)

    def disappear(self):
        self.set_position(None)
    
    def is_colliding_with(self, other):
        return self.is_position_available() and other.is_position_available() and self.get_position() == other.get_position()

    

