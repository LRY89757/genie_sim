#!/bin/bash

# Check if correct number of arguments provided
if [ $# -lt 2 ]; then
    echo "Usage: bash scripts/scene_capture/capture_task_variants.sh <gpu_num> <task_json_path> [num_variants] [output_dir]"
    echo "Example: bash scripts/scene_capture/capture_task_variants.sh 0 benchmark/ader/eval_tasks/iros_stamp_the_seal.json 5"
    echo "Example: bash scripts/scene_capture/capture_task_variants.sh 0 benchmark/ader/eval_tasks/iros_stamp_the_seal.json 10 my_variants"
    echo "Example: bash scripts/scene_capture/capture_task_variants.sh 1 benchmark/ader/eval_tasks/curobo_restock_supermarket_items.json 10 my_variants"
    exit 1
fi

# Set CUDA device and task parameters
export CUDA_VISIBLE_DEVICES=$1
TASK_JSON_PATH=$2
NUM_VARIANTS=${3:-5}
OUTPUT_DIR=${4:-"task_variants"}

echo "Using GPU: $1"
echo "Task JSON: $2"
echo "Number of variants: $NUM_VARIANTS"
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
    pkill -f "task_scene_capture_variants.py" 2>/dev/null || true
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

# Run task variant capture
echo "Capturing scene images from $NUM_VARIANTS variants..."
/isaac-sim/python.sh scripts/scene_capture/task_scene_capture_variants.py \
    --task_json "$TASK_JSON_PATH" \
    --num_variants "$NUM_VARIANTS" \
    --output_dir "$OUTPUT_DIR" \
    --client_host "localhost:50051"

CAPTURE_EXIT_CODE=$?

# Show results if successful
if [ $CAPTURE_EXIT_CODE -eq 0 ]; then
    echo ""
    echo "=== Variant Capture Complete ==="
    TASK_NAME=$(basename "$TASK_JSON_PATH" .json)
    RESULT_DIR="$OUTPUT_DIR/$TASK_NAME"
    
    if [ -d "$RESULT_DIR" ]; then
        echo "Results saved to: $RESULT_DIR"
        echo "Variants generated:"
        ls -la "$RESULT_DIR" | grep "variant_" | wc -l | xargs echo "  Total variants:"
        echo ""
        echo "Sample images from variant_0:"
        if [ -d "$RESULT_DIR/variant_0" ]; then
            ls -la "$RESULT_DIR/variant_0" | grep -E "\.(jpg|png)$" | head -6
        fi
    fi
fi

# Cleanup
cleanup

# Exit with capture script's exit code
exit $CAPTURE_EXIT_CODE 
