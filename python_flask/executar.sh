#!/bin/bash

SESSION_NAME="app"

if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    tmux attach-session -t $SESSION_NAME
else
    tmux new-session -d -s $SESSION_NAME
fi

tmux send-keys -t 0 C-c
tmux send-keys -t 0 "./iniciarApp.sh" C-m