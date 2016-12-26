TODO
====
* CHECK -- Add implementation for get_memory() and get_battery()
* CHECK -- Implement showing output per flags
* CHECK -- Store the output of duplicate flags somewhere for faster execution?
* CHECK -- Rebalance memory levels' coloring
* Move the Colors class to the global scope so that individual get_*()s can read from it if needed?
    * CHECK -- Alt: Add another param to colorize(), allowing arbitrary string colorization
    * Alt: Move the Colors class to the global scope and pass objects of it to the get_*()s, which will pass to colorize(). tmux_needed can then be handled outside of any function.
* CHECK -- Check for anomalous output from ``adb shell dumpsys cpuinfo`` (eg: ``-99% TOTAL: -20.-7% user + -69.-9% kernel + -1.-4% iowait + -2.-9% irq + -3.-9% softirq``) in get_cpu_percent
    * Investigate this bug(?) in android 7.1.1's dumpsys cpuinfo? (Very possibly out of scope for me and this project)
* CHECK -- Add flag and implementation for device choosing (may be difficult with just 1 device to test on...)
* Time dumpsys usage vs using ``cat`` and /proc/ & /sys/ targets
* Investigate and use exceptions in more locations?
* Better pass ``args.tmux_needed``
* Add indicator letter or symbols optionally in front of or around each action's output to better distinguish them?
* Add graphics (framerate?) and network indicators?
* Add support for custom color choices via a config file or individual switches?
* Add to the -h output to specified there that an "action" must be chosen.
* Finish `<README.rst>`_