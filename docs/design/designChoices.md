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
