# Client Server Communication - design choices

Two components are required to run the tests
- Runner (Server): Provides the tests to the executors
- Inspector (Client) : Requests the tests to the Runner and records the result provided by the executor

We assume that each executor uses the same program (algorithm).
Different algorithms should be analyzed in different benchmark runs
One component should be in charge of appending the algorithm label to each TestResult,
if comparing data from different benchmarks

The server provides one or more tests according to
the preferences of the client (even all of them).
The same test must be provided only once.

After having issued all the tests, the server closes.
The clients are informed of this by their own connection

## Server Commands
- ping() : Ping the server
- request_test(testName) : Returns the TestDescription with the given name 
- request_random_test() : Return one random test not assigned
- assign_test(testName) : Get one test assigned (don't return the value)
- submit_result(testName) : Submit the result of the given test. A test must be assigned before submitting 
  its result. 

Requests are sent by inserting in the title the command to run, and the corresponding parameters in the content 
of the message. Any misuse of the server commands will produce an error message (title: "Error", content: "Error description)
Correct response will return messages titled "OK", with the content containing the requested payload


