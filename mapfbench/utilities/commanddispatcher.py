from customexceptions import ElementNotFoundException


class CommandDispatcher(object):

    def __init__(self, function_associations):
        self._function_associations = function_associations

    @property
    def function_names(self):
        return self._function_associations.keys()

    def execute(self, function_name, arguments=None):
        if function_name not in self._function_associations:
            raise ElementNotFoundException(f"Function {function_name} not found")

        if arguments is None:
            return self._function_associations[function_name]()
        else:
            return self._function_associations[function_name](arguments)

