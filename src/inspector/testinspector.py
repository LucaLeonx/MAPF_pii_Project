from description.map.graph import Node
from result.action import WaitAction, MoveAction, AppearAction, DisappearAction
from result.testrun import TestRun


class TestInspector(object):
    def __init__(self, test_description):
        self._test_description = test_description
        self._action_list = []
        self._current_position = {entity.name: None for entity in self._test_description.entities}
        self._test_solved = False

        for entity in self._test_description.entities:
            if entity.has_start_position():
                self.register_appearance(0, entity.name, entity.start_position)

    @property
    def test_description(self):
        return self._test_description

    @property
    def action_list(self):
        return self._action_list

    def register_action(self, action):
        self._action_list.append(action)

    def _register_move_with_description(self, timestep, entity_name, end_position, description="Move"):
        self._current_position.update({entity_name: end_position})
        self.register_action(MoveAction(timestep, entity_name, end_position, description))

    def register_move(self, timestep, entity_name, end_position):
        self._register_move_with_description(timestep, entity_name, end_position)

    def register_move_left(self, timestep, entity_name):
        current_position = self._current_position[entity_name]
        end_position = Node(coords=(current_position.x - 1, current_position.y))
        self._register_move_with_description(timestep, entity_name, end_position, description="MoveLeft")

    def register_move_right(self, timestep, entity_name):
        current_position = self._current_position[entity_name]
        end_position = Node(coords=(current_position.x + 1, current_position.y))
        self._register_move_with_description(timestep, entity_name, end_position, description="MoveRight")

    def register_move_up(self, timestep, entity_name):
        current_position = self._current_position[entity_name]
        end_position = Node(coords=(current_position.x, current_position.y + 1))
        self._register_move_with_description(timestep, entity_name, end_position, description="MoveUp")

    def register_move_down(self, timestep, entity_name):
        current_position = self._current_position[entity_name]
        end_position = Node(coords=(current_position.x, current_position.y - 1))
        self._register_move_with_description(timestep, entity_name, end_position, description="MoveDown")

    def register_wait(self, timestep, entity_name):
        self._action_list.append(WaitAction(timestep, entity_name))

    def register_appearance(self, timestep, entity_name, start_position):
        self._current_position.update({entity_name: start_position})
        self._action_list.append(AppearAction(timestep, entity_name, start_position))

    def register_disappearance(self, timestep, entity_name):
        self._current_position.update({entity_name: None})
        self._action_list.append(DisappearAction(timestep, entity_name))

    def mark_as_solved(self):
        self._test_solved = True

    # def start_profiling()
    # def end_profiling()

    def get_result(self):
        return TestRun(self._test_description, self._action_list, self._test_solved)
