import asyncio

import zmq
import zmq.asyncio

from mapfbench.description import Scenario


class BenchmarkServer:
    pass


class BenchmarkServer:
    def __init__(self, scenarios: list[Scenario], connection_address: str):
        self._connection_address = connection_address
        self._socket = zmq.asyncio.Socket(zmq.REP)
        self._scenarios = list(scenarios)
        self._scenarios_num = len(self._scenarios)
        self._assigned_scenarios = []
        self._plans = []
        self._stop = True

    async def start(self):
        self._stop = False
        self._socket.bind(self._connection_address)

        while not self._stop:
            # This allows the server to check for stop in case messages do not arrive
            # Timeout in seconds
            try:
                async with asyncio.timeout(1):
                    request = await self._socket.recv_multipart(copy=False)
            except TimeoutError:
                continue

            request_type = request[0]["type"]

            if request_type == "random_scenario":
                if len(self._scenarios) == 0:
                    reply = self._socket.send_multipart("finished", copy=False)
                else:
                    scenario = self._scenarios.pop()
                    self._assigned_scenarios.append(scenario)
                    reply = self._socket.send_multipart(scenario, copy=False)
            elif request_type == "result":
                self._plans.append(request[1])
                if len(self._plans) == self._scenarios_num:
                    self._stop = True
                    break
            else:
                reply = self._socket.send_multipart("error", copy=False)

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



