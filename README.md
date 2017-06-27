```
pip install -r requirements.txt
kernprof -l debug.py
python -m line_profiler debug.py.lprof

Timer unit: 1e-06 s

Total time: 50.3281 s
File: debug.py
Function: recursive_func at line 12

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    12                                           @profile
    13                                           def recursive_func(val):
    14      4089        14667      3.6      0.0      if val == 0:
    15                                                   return val
    16      4089         7725      1.9      0.0      if val < 1:
    17         1       304861 304861.0      0.6          sleep(.30)
    18         1           45     45.0      0.0          return val + recursive_func(val + 1)
    19      4088         6012      1.5      0.0      elif val < 5:
    20         6      1215549 202591.5      2.4          sleep(.20)
    21         6          143     23.8      0.0          return val + recursive_func(val * 2)
    22      4082         6599      1.6      0.0      elif val < 100:
    23      4066     46994745  11558.0     93.4          sleep(.01)
    24      4066       117915     29.0      0.2          return val + recursive_func(val + .2)
    25        16           23      1.4      0.0      elif val > 1000:
    26         3       308707 102902.3      0.6          sleep(.10)
    27         3           96     32.0      0.0          return val + recursive_func(val / 100)
    28                                               else:
    29        13      1350919 103916.8      2.7          sleep(.10)
    30        13           89      6.8      0.0          return val

Total time: 50.3895 s
File: debug.py
Function: my_func at line 36

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    36                                           @profile
    37                                           def my_func():
    38        14           32      2.3      0.0      for val in data_array:
    39        13     50389430 3876110.0    100.0          recursive_func(val)
```

While looking to debug the code to determine what too so long (50 seconds), you might see the longest sleep time at `sleep(.30)` and think that was the top optimization; however, it's much better to focus efforts on optimizing lines 23 and 24.


Using cProfile:
```
python -m cProfile debug.py

8186 function calls (4110 primitive calls) in 50.445 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:989(_handle_fromlist)
        1    0.000    0.000   50.444   50.444 debug.py:1(<module>)
  4089/13    0.073    0.000   50.444    3.880 debug.py:12(recursive_func)
        1    0.000    0.000   50.444   50.444 debug.py:36(my_func)
        2    0.000    0.000    0.000    0.000 debug.py:5(profile)
        1    0.000    0.000   50.445   50.445 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
     4089   50.372    0.012   50.372    0.012 {built-in method time.sleep}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

We call time.sleep a huge number of times and it winds up being a large amount of time, although only 0.012 seconds per call.
We can sort by interesting statistics by using `-s`

```
python -m cProfile -s cumtime debug.py

8186 function calls (4110 primitive calls) in 50.321 seconds

Ordered by: cumulative time

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
1    0.000    0.000   50.321   50.321 {built-in method builtins.exec}
1    0.000    0.000   50.321   50.321 debug.py:1(<module>)
1    0.000    0.000   50.321   50.321 debug.py:36(my_func)
4089/13    0.072    0.000   50.321    3.871 debug.py:12(recursive_func)
4089   50.249    0.012   50.249    0.012 {built-in method time.sleep}
1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:989(_handle_fromlist)
1    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
2    0.000    0.000    0.000    0.000 debug.py:5(profile)
1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

Abbreviations can be used for any key names, as long as the abbreviation is unambiguous. The following are the keys currently defined:

Valid Arg	Meaning
'calls'	call count
'cumulative'	cumulative time
'cumtime'	cumulative time
'file'	file name
'filename'	file name
'module'	file name
'ncalls'	call count
'pcalls'	primitive call count
'line'	line number
'name'	function name
'nfl'	name/file/line
'stdname'	standard name
'time'	internal time
'tottime'	internal time
```

Finally, we can write cProfile out to an output for future manipulation

```
python -m cProfile debug.py -o profiling
python
>> import pstats
>> p = pstats.Stats('profiling')
>> p.strip_dirs().sort_stats('ncalls').print_stats(5)
Tue Jun 27 17:40:38 2017    profiling

         8186 function calls (4110 primitive calls) in 50.406 seconds

   Ordered by: call count
   List reduced from 9 to 5 due to restriction <5>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     4089   50.327    0.012   50.327    0.012 {built-in method time.sleep}
  4089/13    0.080    0.000   50.406    3.877 debug.py:12(recursive_func)
        2    0.000    0.000    0.000    0.000 debug.py:5(profile)
        1    0.000    0.000   50.406   50.406 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}


<pstats.Stats object at 0x10a507c88>
```
