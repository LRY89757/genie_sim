#!/bin/bash

# Script to replay AgiBot World Challenge trajectories
# Usage: ./replay_agibot_trajectory.sh <episode_path> [task_name]
#
# Example commands:
# 
# Clear Table in the Restaurant:
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/clear_table_in_the_restaurant/2810125/3336152/A2D0015AB00061/12056564 iros_clear_table_in_the_restaurant
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/clear_table_in_the_restaurant/2810125/3336136/A2D0015AB00061/12056439 iros_clear_table_in_the_restaurant
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/clear_table_in_the_restaurant/2810125/3336055/A2D0015AB00061/12055991 iros_clear_table_in_the_restaurant
#
# Clear the Countertop Waste:
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/clear_the_countertop_waste/2810083/3327882/A2D0015AB00061/12041032 iros_clear_the_countertop_waste
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/clear_the_countertop_waste/2810083/3328278/A2D0015AB00061/12041429 iros_clear_the_countertop_waste
#
# Heat the Food in the Microwave (requires extraction):
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/heat_the_food_in_the_microwave/<task_id>/<job_id>/<robot_id>/<episode_id> iros_heat_the_food_in_the_microwave
#
# Make a Sandwich (requires extraction):
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/make_a_sandwich/<task_id>/<job_id>/<robot_id>/<episode_id> iros_make_a_sandwich
#
# Open Drawer and Store Items (10 episodes available):
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/open_drawer_and_store_items/2810096/3329474/A2D0015AB00061/12042598 iros_open_drawer_and_store_items
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/open_drawer_and_store_items/2810096/3329671/A2D0015AB00061/12042790 iros_open_drawer_and_store_items
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/open_drawer_and_store_items/2810096/3329800/A2D0015AB00061/12042914 iros_open_drawer_and_store_items
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/open_drawer_and_store_items/2810096/3329501/A2D0015AB00061/12042623 iros_open_drawer_and_store_items
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/open_drawer_and_store_items/2810096/3329936/A2D0015AB00061/12043054 iros_open_drawer_and_store_items
#
# Pack in the Supermarket (10 episodes available):
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pack_in_the_supermarket/2810137/3335888/A2D0015AB00061/12055136 iros_pack_in_the_supermarket
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pack_in_the_supermarket/2810137/3335888/A2D0015AB00061/12055122 iros_pack_in_the_supermarket
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pack_in_the_supermarket/2810137/3335897/A2D0015AB00061/12055187 iros_pack_in_the_supermarket
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pack_in_the_supermarket/2810137/3335897/A2D0015AB00061/12055193 iros_pack_in_the_supermarket
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pack_in_the_supermarket/2810137/3335953/A2D0015AB00061/12055452 iros_pack_in_the_supermarket
#
# Pack Moving Objects from Conveyor (requires extraction):
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pack_moving_objects_from_conveyor/<task_id>/<job_id>/<robot_id>/<episode_id> iros_pack_moving_objects_from_conveyor
#
# Pickup Items from the Freezer (requires extraction):
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pickup_items_from_the_freezer/<task_id>/<job_id>/<robot_id>/<episode_id> iros_pickup_items_from_the_freezer
#
# Restock Supermarket Items:
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/restock_supermarket_items/2810085/3327951/A2D0015AB00061/12041099 iros_restock_supermarket_items
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/restock_supermarket_items/2810085/3327924/A2D0015AB00061/12041071 iros_restock_supermarket_items
#
# Stamp the Seal:
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/stamp_the_seal/2810130/3335579/A2D0015AB00061/12053448 iros_stamp_the_seal
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/stamp_the_seal/2810130/3335579/A2D0015AB00061/12053451 iros_stamp_the_seal
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/stamp_the_seal/2810130/3335579/A2D0015AB00061/12053447 iros_stamp_the_seal
#
# To find available episodes:
#   find AgiBotWorldChallenge-2025/Manipulation-SimData/<task_name> -name "state.json" -path "*/parameters/camera/*" | sed 's|/parameters/camera/state.json||'

# Check if episode path is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <episode_path> [task_name]"
    echo "Example: $0 AgiBotWorldChallenge-2025/Manipulation-SimData/clear_table_in_the_restaurant/2810125/3335477/A2D0015AB00061/12052353 iros_clear_table_in_the_restaurant"
    exit 1
fi

EPISODE_PATH=$1
TASK_NAME=${2:-"iros_clear_table_in_the_restaurant"}  # Default task name

# Validate paths
STATE_FILE="${EPISODE_PATH}/parameters/camera/state.json"
TASK_FILE="teleop/tasks/${TASK_NAME}.json"

if [ ! -f "$STATE_FILE" ]; then
    echo "Error: State file not found: $STATE_FILE"
    exit 1
fi

if [ ! -f "$TASK_FILE" ]; then
    echo "Error: Task file not found: $TASK_FILE"
    exit 1
fi

echo "=== Replaying AgiBot World Challenge Trajectory ==="
echo "Episode: $EPISODE_PATH"
echo "Task: $TASK_NAME"
echo "State file: $STATE_FILE"
echo "Task file: $TASK_FILE"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Cleaning up..."
    if [ ! -z "$SERVER_PID" ]; then
        echo "Stopping server (PID: $SERVER_PID)..."
        kill $SERVER_PID 2>/dev/null
        wait $SERVER_PID 2>/dev/null
    fi
}

# Set trap to cleanup on exit
trap cleanup EXIT INT TERM

# Start the server in the background
echo "Starting simulation server..."
/isaac-sim/python.sh server/source/genie.sim.lab/raise_standalone_sim.py --disable_physics --record_img --record_video &
SERVER_PID=$!

# Wait for server to be ready
echo "Waiting for server to initialize..."
sleep 10  # Adjust this based on your system's startup time

# Check if server is still running
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "Error: Server failed to start"
    exit 1
fi

echo "Server is ready!"
echo ""

# Run the replay
echo "Starting trajectory replay..."
/isaac-sim/python.sh teleop/replay_state.py \
    --task_file "$TASK_FILE" \
    --state_file "$STATE_FILE" \
    --record

echo ""
echo "Replay completed!"

# The cleanup function will be called automatically on exit 
