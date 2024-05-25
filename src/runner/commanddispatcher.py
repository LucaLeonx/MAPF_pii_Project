from runner.exceptions import ElementNotFoundException


class CommandDispatcher(object):

    def __init__(self, function_associations):
        self._function_associations = function_associations

    def execute(self, function_name, arguments):
        if function_name not in self._function_associations:
            raise ElementNotFoundException(f"Function {function_name} not found")

        return self._function_associations[function_name](arguments)

