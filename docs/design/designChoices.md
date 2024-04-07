# Design choices

Server: provides the tests to the algorithms
Algorithm: receive the tests and runs them

Each algorithm program is identified by a string
identifier. It must be defined within the code of
the algorithm, in the server


TestRun characterized by:
- id, given by the server
- algorithm, given by the runner

Benchmarks are aggregated by algorithms
The server provides one or more tests according to
the preferences of the client (even all of them).
The same test cannot be provided to the same
algorithm twice.

Once the server has calculated all the tests in a
benchmark for all the algorithms, it stops and 
generates the test_run results.

RequestTest(name=optional)
RequestBenchmark(name=optional)

# Test server and client

- A test is a MAPF problem to solve
- A benchmark is a suit of tests, to be solved by the same algorithm
- Tests are not distinguished by a name in a benchmark. However, the BenchMark runner assigns an ID
  to them
- The server provides a test to a client on request. No guarantees are made on which test is given
- Depending on the kind of request, the server may or may not send the test description to the client

- The client can request one or more tests, through the TestInspector
- Once it has finished a test, it can pass the results of a given test back to the server

- Problems with parallelism
- It must be possible to manage the case where the client is unable to solve the test (probably timeout)
