# Client Server Communication - design choices

There are three components:
- Distributor: It distributes the tests to the clients
- Client: Get and executes the tests. 
- Collector : Collects the results of the tests and signals when everything is done

We make the following assumptions:

- The Distributor provides the tests randomly to the clients
- The Distributor may give each test only once. If it finishes them, it closes.
- The client execute all the same program (they attach the same identifier).  
  If someone wants to test different algorithms on the same 
  tests, it must run a different Distributor and Collector for them.
- If someone wants to handle the tests in different format and order, or
  with specific granularity regarding parallelism, it can just dump results
  in the Collector. If properly configured, it will figure out when all the tests have been run.
  However, it should be somehow possible to convert the internal test format to the one we provide
- Because of the design of the ZeroMQ library, each client should use only one BenchmarkInspector.
  or let each thread inside it create its own.
- The TestInspector should be able to handle CTRL-C and other closing signals from the application.

- The Collector receives the benchmark to be run, so it knows when all the tests have been run.

- For now, we assume that the Clients and the Distributor close on their own, when they have finished their job
  (no more tests to be run). In the future, there may be a mechanism to let the Collector signal the other clients that
  all tests have been done (DONE), or that there was a timeout (TIMEOUT)


## Old design choices

Server: provides the tests to the algorithms
Algorithm: receive the tests and runs them

Each algorithm program is identified by a string
identifier. It must be defined within the code of
the algorithm, in the server

TestRun characterized by:
- id, given by the Distributor
- algorithm, given by the Client

Results may be aggregated by algorithm,
by the filters in the Calculator stage

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
