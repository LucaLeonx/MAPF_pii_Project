from runner.exceptions import ElementNotAvailableException


class Action(object):

    def __init__(self, timestep, subject, start_position=None, end_position=None, description=""):
        self._timestep = timestep
        self._subject = subject
        self._start_position = start_position
        self._end_position = end_position
        self._description = description

    @property
    def timestep(self):
        return self._timestep

    @property
    def subject(self):
        return self._subject

    @property
    def start_position(self):
        if self._start_position is None:
            raise ElementNotAvailableException("This action doesn't have an initial position")

        return self._start_position

    @property
    def end_position(self):
        if self._end_position is None:
            raise ElementNotAvailableException("This action doesn't have a final position")

        return self._end_position

    @property
    def description(self):
        return self._description


class MoveAction(Action):
    def __init__(self, timestep, subject, start_position, end_position, description=""):
        Action.__init__(self, timestep, subject, start_position, end_position, description)


class WaitAction(Action):
    def __init__(self, timestep, subject, description=""):
        Action.__init__(self, timestep, subject, None, None, description)


class AppearAction(Action):
    def __init__(self, timestep, subject, start_position, description=""):
        Action.__init__(self, timestep, subject, start_position, None, description)


class DisappearAction(Action):
    def __init__(self, timestep, subject, description=""):
        Action.__init__(self, timestep, subject, None, None, description)
        
