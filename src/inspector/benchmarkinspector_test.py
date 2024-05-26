from connection.connectionconfig import TCPConnectionConfig
from inspector.benchmarkinspector import BenchmarkInspector

if __name__ == "__main__":
    inspector = BenchmarkInspector(TCPConnectionConfig(host="localhost", port=9361))
    print("Creation done")
    inspector.start()
    test_inspector = inspector.request_test("Test1")
    print(test_inspector.test_description)
    test_inspector.mark_as_solved()
    inspector.submit_result(test_inspector)

