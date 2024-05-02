# Client Server Communication - design choices

Two components are required to run the tests
- Runner (Server): Provides the tests to the executors
- Inspector (Client) : Requests the tests to the Runner and records the result provided by the executor

We assume that each executor uses the same program (algorithm).
Different algorithms should be analyzed in different benchmark runs
One component should in charge of appending the algorithm label to each TestResult

The server provides one or more tests according to
the preferences of the client (even all of them).
The same test must be provided only once.

After having issued all the tests, the server closes.
The clients are informed of this by their own connection

## Server Commands
- ping() : Ping the server
- request_test(testName) : Returns the TestDescription with the given name 
- request_random_Test() : Return one random test not assigned
- assign_test(testName) : Get one test assigned (don't return the value)