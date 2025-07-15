#!/bin/bash

# Check if correct number of arguments provided
if [ $# -lt 2 ]; then
    echo "Usage: bash scripts/scene_capture/capture_task_scene.sh <gpu_num> <task_json_path> [output_dir]"
    echo "Example: bash scripts/scene_capture/capture_task_scene.sh 0 benchmark/ader/eval_tasks/iros_stamp_the_seal.json"
    exit 1
fi

# Set CUDA device and task parameters
export CUDA_VISIBLE_DEVICES=$1
TASK_JSON_PATH=$2
OUTPUT_DIR=${3:-"scene_images"}

echo "Using GPU: $1"
echo "Task JSON: $2"
echo "Output directory: $OUTPUT_DIR"

# Function to cleanup background processes
cleanup() {
    if [ "$CLEANUP_RUNNING" = "true" ]; then
        return
    fi
    export CLEANUP_RUNNING=true
    
    echo -e "\nCleaning up background processes..."
    
    # Kill specific Isaac Sim and related processes, but not this script
    pkill -f "raise_standalone_sim.py" 2>/dev/null || true
    pkill -f "task_scene_capture.py" 2>/dev/null || true
    pkill -f "task_benchmark.py" 2>/dev/null || true
    pkill -f "teleop" 2>/dev/null || true
    pkill -f "isaac-sim" 2>/dev/null || true
    pkill -f "omni_python" 2>/dev/null || true
    pkill -f "omni\.python" 2>/dev/null || true
    
    # Kill the server process if we have its PID
    if [ ! -z "$SERVER_PID" ]; then
        kill $SERVER_PID 2>/dev/null || true
    fi
    
    echo "Cleanup completed"
    exit 0
}

# Trap Ctrl+C and other signals
trap cleanup SIGINT SIGTERM

# Check if task JSON file exists
if [ ! -f "$TASK_JSON_PATH" ]; then
    echo "Error: Task JSON file not found: $TASK_JSON_PATH"
    exit 1
fi

# Start Isaac Sim server in background
echo "Starting Isaac Sim server..."
/isaac-sim/python.sh server/source/genie.sim.lab/raise_standalone_sim.py --headless &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for Isaac Sim server to initialize..."
sleep 45

# Check if server is still running
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "Error: Isaac Sim server failed to start"
    exit 1
fi

echo "Isaac Sim server started successfully"

# Run task scene capture
echo "Capturing scene images..."
/isaac-sim/python.sh scripts/scene_capture/task_scene_capture.py \
    --task_json "$TASK_JSON_PATH" \
    --output_dir "$OUTPUT_DIR" \
    --client_host "localhost:50051"

CAPTURE_EXIT_CODE=$?

# Cleanup
cleanup

# Exit with capture script's exit code
exit $CAPTURE_EXIT_CODE 
