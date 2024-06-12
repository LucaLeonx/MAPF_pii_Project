import time
from typing import List

import psutil
from description.benchmarkdescription import TestDescription
from result.action import WaitAction, MoveAction, AppearAction, DisappearAction, Action
from result.testrun import TestRun

from description.graph import Node


class TestInspector(object):
    """
        The TestInspector is responsible for registering the results of
        the solution of a test instance, in particular the computed
        action plan
    """

    def __init__(self, test_description: TestDescription):
        """
            Object initializer

            Parameters
            ----------
            test_description : TestDescription
                The description of the test instance to keep track of
        """
        self._test_description = test_description
        self._action_list = []
        self._current_position = {entity.name: None for entity in self._test_description.entities}
        self._test_solved = False
        self._memory_used = None
        self._start_time = None
        self._end_time = None

        for entity in self._test_description.entities:
            if entity.has_start_position():
                self.register_appearance(0, entity.name, entity.start_position)

    @property
    def test_description(self) -> TestDescription:
        """
            The description of the inspected test instance
        """
        return self._test_description

    @property
    def action_list(self) -> List[Action]:
        """
            The list of action which are part of the plan
            provided for this test instance
        """
        return self._action_list

    def register_action(self, action: Action):
        """
            Register the specified action in the plan
            for the given test instance

            Parameters
            ----------
            action : Action
                The action to be registered
        """
        self._action_list.append(action)

    def _register_move_with_description(self, timestep: int, entity_name: str, end_position: Node,
                                        description: str = ""):
        self.register_action(
            MoveAction(timestep, entity_name, self._current_position[entity_name], end_position, description))
        self._current_position.update({entity_name: end_position})

    def register_move(self, timestep: int, entity_name: str, end_position: Node):
        """
            Register the move action of the specified entity in the plan

            Parameters
            ----------
            timestep : int
                The timestep at which the action is executed
            entity_name : str
                The name of the entity performing the action
            end_position: Node
                The final position of the entity after the move
        """
        self._register_move_with_description(timestep, entity_name, end_position)

    def register_move_left(self, timestep, entity_name):
        """
            Register the left movement of one cell of an entity in the plan

            Warning
            -------
            This method must be used only if the map of
            the test is a GridGraph. Otherwise, this may lead to undefined benchmark results.
            Moreover, the method will raise an exception
            if the end position of the entity is outside the grid
            (e.g. it has negative coordinates)

            Parameters
            ----------
            timestep : int
                The timestep at which the action is executed
            entity_name : str
                The name of the entity performing the action
        """
        current_position = self._current_position[entity_name]
        end_position = Node(coords=(current_position.x - 1, current_position.y))
        self._register_move_with_description(timestep, entity_name, end_position, description="MoveLeft")

    def register_move_right(self, timestep, entity_name):
        """
            Register the right movement of one cell of an entity in the plan

            Warning
            -------
            This method must be used only if the map of
            the test is a GridGraph. Otherwise, this may lead to undefined benchmark results.
            Moreover, the method will raise an exception
            if the end position of the entity is outside the grid
            (e.g. it has negative coordinates)

            Parameters
            ----------
            timestep : int
                The timestep at which the action is executed
            entity_name : str
                The name of the entity performing the action
        """
        current_position = self._current_position[entity_name]
        end_position = Node(coords=(current_position.x + 1, current_position.y))
        self._register_move_with_description(timestep, entity_name, end_position, description="MoveRight")

    def register_move_up(self, timestep, entity_name):
        """
            Register the up movement of one cell of an entity in the plan

            Warning
            -------
            This method must be used only if the map of
            the test is a GridGraph. Otherwise, this may lead to undefined benchmark results.
            Moreover, the method will raise an exception
            if the end position of the entity is outside the grid
            (e.g. it has negative coordinates)

            Parameters
            ----------
            timestep : int
                The timestep at which the action is executed
            entity_name : str
                The name of the entity performing the action
        """
        current_position = self._current_position[entity_name]
        end_position = Node(coords=(current_position.x, current_position.y + 1))
        self._register_move_with_description(timestep, entity_name, end_position, description="MoveUp")

    def register_move_down(self, timestep, entity_name):
        """
            Register the up movement of one cell of an entity in the plan

            Warning
            -------
            This method must be used only if the map of
            the test is a GridGraph. Otherwise, this may lead to undefined benchmark results.
            Moreover, the method will raise an exception
            if the end position of the entity is outside the grid
            (e.g. it has negative coordinates)

            Parameters
            ----------
            timestep : int
                The timestep at which the action is executed
            entity_name : str
                The name of the entity performing the action
        """
        current_position = self._current_position[entity_name]
        end_position = Node(coords=(current_position.x, current_position.y - 1))
        self._register_move_with_description(timestep, entity_name, end_position, description="MoveDown")

    def register_wait(self, timestep: int, entity_name: str):
        """
            Register the wait action of the specified entity in the plan

            Parameters
            ----------
            timestep : int
                The timestep at which the wait is done
            entity_name : str
                The name of the entity waiting
        """
        self._action_list.append(WaitAction(timestep, entity_name, self._current_position[entity_name]))

    def register_appearance(self, timestep: int, entity_name: str, position: Node):
        """
            Register the appearance of the specified entity in the plan

            Parameters
            ----------
            timestep : int
                The timestep at which the entity appears
            entity_name : str
                The name of the appearing entity
            position : Node
                The position at which the entity appears
        """

        self._current_position.update({entity_name: position})
        self._action_list.append(AppearAction(timestep, entity_name, start_position=None, end_position=position))

    def register_disappearance(self, timestep: int, entity_name: str):
        """
            Register the disappearance of the specified entity in the plan

            Parameters
            ----------
            timestep : int
                The timestep at which the entity disappears
            entity_name : str
                The name of the disappearing entity
        """
        self._action_list.append(DisappearAction(timestep,
                                                 entity_name,
                                                 start_position=self._current_position[entity_name]))
        self._current_position.update({entity_name: None})

    def mark_as_solved(self):
        """
            Mark the test instance as solved
        """
        self._test_solved = True

    def start_profiling(self):
        """
            Start the profiling of runtime information of the program
        """
        self._process_reference = psutil.Process()
        self._start_time = time.perf_counter_ns()

    def end_profiling(self):
        """
            Stop the profiling of runtime information of the program
            and register the results
        """
        if self._process_reference:
            self._memory_used = self._process_reference.memory_info().rss
            self._end_time = time.perf_counter_ns()

    def get_result(self) -> TestRun:
        """
            Return a TestRun instance with the registered results
            for the current test

            Returns
            -------
            TestRun
                The registered results of the current test instance
        """
        time_elapsed = None
        memory_used = None
        if self._end_time:
            time_elapsed = (self._end_time - self._start_time) / 1_000_000
            memory_used = self._memory_used / 1024
        else:
            time_elapsed = None
        return TestRun(self._test_description, self._action_list, self._test_solved,
                       time_elapsed,
                       memory_used)
