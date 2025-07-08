#!/bin/bash

source ~/.bashrc

TASK_NAME="iros_pack_in_the_supermarket"

echo "================================="
echo "Running VLA inference for task: $TASK_NAME"
echo "================================="

# Function to cleanup background processes
cleanup() {
    echo -e "\nCleaning up background processes..."
    pkill -f "task_benchmark|teleop|replay|infer|isaac-sim|omni|omni_python|raise|ros" || true
    exit 0
}

# Trap Ctrl+C and other signals
trap cleanup SIGINT SIGTERM

echo "Starting VLA inference pipeline..."

# Start server in background
echo "Starting Isaac Sim server..."
/isaac-sim/python.sh server/source/genie.sim.lab/raise_standalone_sim.py  --headless --record_video --record_img &
SERVER_PID=$!

# Wait for server to initialize
sleep 90

# Start client in background
echo "Starting benchmark client..."
/isaac-sim/python.sh benchmark/task_benchmark.py --task_name $TASK_NAME --policy_class=BaselinePolicy --record &
CLIENT_PID=$!

# Wait for client to initialize
sleep 50

# Start VLA inference
echo "Starting VLA model inference..."
cd AgiBot-World && /isaac-sim/python.sh scripts/infer.py --task_name $TASK_NAME &
INFER_PID=$!

echo -e "\nAll processes started. Press Ctrl+C to stop all processes..."

# Wait for any process to finish or user interruption
wait $INFER_PID

# Cleanup when done
cleanup 
