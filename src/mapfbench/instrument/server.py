import zmq

from mapfbench.description import Scenario, Plan
from mapfbench.instrument import PlanRecorder
from mapfbench.instrument.connection import ClientSocket, ServerSocket


class BenchmarkServer:
    def __init__(self, scenarios: list[Scenario], connection_address: str):
        self._connection_address = connection_address
        self._socket = ServerSocket(connection_address)
        self._scenarios = list(scenarios)
        self._scenarios_num = len(self._scenarios)
        self._assigned_scenarios = []
        self._plans = []
        self._stop = True

    def start(self):
        self._stop = False
        self._socket.start()

        while not self._stop:
            # This allows the server to check for stop in case messages do not arrive
            # Timeout in seconds

            request = self._socket.receive_message()
            request_type = request["label"]

            if request_type == "random_scenario":
                if len(self._scenarios) == 0:
                    reply = self._socket.send_message("finished")
                else:
                    scenario = self._scenarios.pop()
                    self._assigned_scenarios.append(scenario)
                    reply = self._socket.send_message("scenario", scenario.encode())
            elif request_type == "result":
                self._plans.append(Plan.decode(request["content"]))

                if len(self._plans) == self._scenarios_num:
                    self._stop = False
                    reply_message = "finished"
                else:
                    reply_message = "done"

                reply = self._socket.send_message(reply_message, scenario.encode())
            else:
                reply = self._socket.send_message("error")

            print(self.status)

        self.stop()
        return self._plans

    def stop(self):
        self._stop = True
        self._socket.stop()

    @property
    def plans(self):
        return self._plans

    @property
    def status(self) -> dict[str, int]:
        return {"Running": not self._stop, "Number of scenarios": self._scenarios_num,
                "Assigned": len(self._assigned_scenarios), "Done": len(self._plans)}


class BenchmarkClient:
    def __init__(self, connection_address: str):
        self._connection_address = connection_address
        self._socket = ClientSocket(connection_address)
        self._requested_scenarios = []

    def start(self):
        self._socket.start()

    def request_scenario(self) -> PlanRecorder:
        request = self._socket.send_message("random_scenario")
        reply = self._socket.receive_message()

        if reply["label"] == "finished":
            raise TestsFinishedException("All tests have been assigned")
        elif reply["label"] == "scenario":
            scenario = Scenario.decode(reply["content"])
            self._requested_scenarios.append(scenario)
            return PlanRecorder(scenario)
        else:
            raise InvalidMessageException("Invalid message received. label: {}, content: {}".format(reply["label"],
                                                                                                    reply["content"]))

    def submit_plan(self, recorder: PlanRecorder):
        request = self._socket.send_message("result", recorder.plan.encode())
        reply = self._socket.receive_message()
        if reply["label"] == "finished":
            raise TestsFinishedException("All tests have been finished")

    @property
    def requested_scenarios(self) -> list[Scenario]:
        return self._requested_scenarios

    def stop(self):
        self._socket.stop()


class TestsFinishedException(Exception):
    pass


class InvalidMessageException(Exception):
    pass
