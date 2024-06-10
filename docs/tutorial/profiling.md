# Profiling

Is it possible to record additional runtime information during the test,
in order to profile the performance of the program.

:::{warning}
The included profiling facilities are intended for providing ballpark estimates of the 
runtime of a program. NO definitive conclusions about the efficiency of a program must be drawn from them. 
Consider using an external [profiler](https://docs.python.org/3/library/profile.html#module-profile)
to determine more accurate performance information.
:::

The metrics recorded during profiling are:
- Total run time, using the built-in time module
- Resident Set Size, as a measure of memory usage. Obtained with psutil 

To profile the code, simply wrap the relevant part of the algorithm with

```{python}
test.start_profiling()
    # Find plan
test.end_profiling()    
```