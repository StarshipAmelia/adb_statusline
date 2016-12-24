TODO
====
* CHECK -- Add implementation for get_memory() and get_battery()
* CHECK -- Implement showing output per flags
* CHECK -- Store the output of duplicate flags somewhere for faster execution?
* Add flag and implementation for device choosing (may be difficult with just 1 device to test on...)
* Move the Colors class to the global scope so that individual get_*()s can read from it if needed?
    * Alt: Add another param to colorize(), allowing arbitrary string colorization
* Time dumpsys usage vs using ``cat`` and /proc/ & /sys/ targets
* Investigate and use exceptions in more locations?
* Check for anomalous output from ``adb shell dumpsys cpuinfo`` (eg: ``-99% TOTAL: -20.-7% user + -69.-9% kernel + -1.-4% iowait + -2.-9% irq + -3.-9% softirq``) in get_cpu_percent
    * Investigate this bug(?) in android 7.1.1's dumpsys cpuinfo? (Very possibly out of scope for me and this project)
* Rebalance memory levels' coloring
* Better pass ``args.tmux_needed``