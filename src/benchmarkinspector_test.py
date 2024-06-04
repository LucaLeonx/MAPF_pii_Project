from connection.connectionconfig import TCPConnectionConfig
from inspector.benchmarkinspector import BenchmarkInspector
from description.map.graph import Node

if __name__ == "__main__":
    inspector = BenchmarkInspector(TCPConnectionConfig(host="localhost", port=9361))
    print("Creation done")
    inspector.start()
    test_inspector = inspector.request_random_test()
    print(test_inspector.test_description)
    test_inspector.register_move(1, "A1", Node(2))
    test_inspector.register_wait(1, "A2")
    test_inspector.mark_as_solved()
    inspector.submit_result(test_inspector)

