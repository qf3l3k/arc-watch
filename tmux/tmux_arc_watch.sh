#!/bin/bash

session='arc'
script_folder='/opt/arc_watch'

/usr/bin/tmux start-server

# Initiate session and create first windows for system purposes
/usr/bin/tmux new-session -d -s $session -n dashboard
/usr/bin/tmux send-keys "cd ${script_folder}; watch -c -n30 'python arc_watch.py -d'" C-m


# Run arc_watch fix and refresh every 30 minutes
/usr/bin/tmux new-window -n 'fixer'
/usr/bin/tmux send-keys "cd ${script_folder}; watch -c -n1800 'python arc_watch.py -f'" C-m


# Display arc_watch log file
/usr/bin/tmux new-window -n 'log'
/usr/bin/tmux send-keys "cd ${script_folder} tail -f logs/arc_watch.log" C-m


/usr/bin/tmux -2 attach -t $session
