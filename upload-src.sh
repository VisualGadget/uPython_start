#!/usr/bin/env -S ./venv/bin/rshell --port /dev/ttyUSB0 --rts 0 --dtr 0 --file

rsync --mirror ./src /pyboard  # never remove /pyboard from dest!
repl~ import machine~ machine.soft_reset()
