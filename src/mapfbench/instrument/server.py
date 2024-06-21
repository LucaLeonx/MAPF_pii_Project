import zmq

from mapfbench.description import Scenario, Plan
from mapfbench.instrument import PlanRecorder
from mapfbench.instrument.connection import Socket


class BenchmarkServer:
    def __init__(self, scenarios: list[Scenario], connection_address: str):
        self._connection_address = connection_address
        self._socket = Socket(connection_address)
        self._scenarios = list(scenarios)
        self._scenarios_num = len(self._scenarios)
        self._assigned_scenarios = []
        self._plans = []
        self._stop = True

    async def start(self):
        self._stop = False
        self._socket.start()

        while not self._stop:
            # This allows the server to check for stop in case messages do not arrive
            # Timeout in seconds

            request =

            request_type = request[0]

            if request_type == "random_scenario":
                if len(self._scenarios) == 0:
                    reply = self._socket.send_multipart("finished", copy=False)
                else:
                    scenario = self._scenarios.pop()
                    self._assigned_scenarios.append(scenario)
                    reply = await self._socket.send_multipart(msgpack.dumps(scenario.encode()), copy=False)
            elif request_type == "result":
                self._plans.append(Plan.decode(msgpack.loads(request[1])))
                if len(self._plans) == self._scenarios_num:
                    self._stop = True
                    break
            else:
                reply = await self._socket.send_multipart("error", copy=False)

        return self._plans

    def stop(self):
        self._stop = True

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
        self._context = zmq.asyncio.Context()
        self._socket = self._context.socket(zmq.REQ)
        self._requested_scenarios = []

    def start(self):
        self._socket.connect(self._connection_address)

    async def request_scenario(self, max_timeout: int = 10) -> PlanRecorder:
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())  # Avoid warnings
        reply = None
        try:
            request = self._socket.send_multipart("random_scenario", copy=False)
            fut = self._socket.recv_multipart(copy=False)
            reply = await asyncio.wait_for(fut, timeout=max_timeout)
        except TimeoutError:
            raise TimeoutError("Request timed out")

        if reply[0] == "finished":
            raise TestsFinishedException("All tests have been assigned")
        else:
            scenario = Scenario.decode(msgpack.loads(reply[1]))
            self._requested_scenarios.append(scenario)
            return PlanRecorder(scenario)

    async def submit_plan(self, recorder: PlanRecorder, timeout: int = 10):
        try:
            async with asyncio.timeout(timeout):
                request = await self._socket.send_multipart(msgpack.dumps(recorder.plan.encode()), copy=False)
        except TimeoutError:
            raise TimeoutError("Request timed out")

    @property
    def requested_scenarios(self) -> list[Scenario]:
        return self._requested_scenarios





class TestsFinishedException(Exception):
    pass

