#!/bin/bash
# This file contains multiple runnable commands for AgiBot World Challenge tasks
# Uncomment the line you want to run, or copy and run it directly
# If one episode doesn't work, try another one from the same task

# Clear Table in the Restaurant:
./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/clear_table_in_the_restaurant/2810125/3336152/A2D0015AB00061/12056564 iros_clear_table_in_the_restaurant
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/clear_table_in_the_restaurant/2810125/3336136/A2D0015AB00061/12056439 iros_clear_table_in_the_restaurant
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/clear_table_in_the_restaurant/2810125/3336055/A2D0015AB00061/12055991 iros_clear_table_in_the_restaurant
#
# Clear the Countertop Waste:
./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/clear_the_countertop_waste/2810083/3327562/A2D0015AB00061/12040721 iros_clear_the_countertop_waste
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/clear_the_countertop_waste/2810083/3328278/A2D0015AB00061/12041429 iros_clear_the_countertop_waste
#
# Heat the Food in the Microwave (requires extraction):
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/heat_the_food_in_the_microwave/<task_id>/<job_id>/<robot_id>/<episode_id> iros_heat_the_food_in_the_microwave
#
# Make a Sandwich (requires extraction):
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/make_a_sandwich/<task_id>/<job_id>/<robot_id>/<episode_id> iros_make_a_sandwich
#
# Open Drawer and Store Items (10 episodes available):
./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/open_drawer_and_store_items/2810096/3329474/A2D0015AB00061/12042598 iros_open_drawer_and_store_items
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/open_drawer_and_store_items/2810096/3329671/A2D0015AB00061/12042790 iros_open_drawer_and_store_items
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/open_drawer_and_store_items/2810096/3329800/A2D0015AB00061/12042914 iros_open_drawer_and_store_items
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/open_drawer_and_store_items/2810096/3329501/A2D0015AB00061/12042623 iros_open_drawer_and_store_items
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/open_drawer_and_store_items/2810096/3329936/A2D0015AB00061/12043054 iros_open_drawer_and_store_items
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/open_drawer_and_store_items/2810096/3329603/A2D0015AB00061/12042723 iros_open_drawer_and_store_items
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/open_drawer_and_store_items/2810096/3329895/A2D0015AB00061/12043013 iros_open_drawer_and_store_items
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/open_drawer_and_store_items/2810096/3329728/A2D0015AB00061/12042844 iros_open_drawer_and_store_items
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/open_drawer_and_store_items/2810096/3330169/A2D0015AB00061/12043282 iros_open_drawer_and_store_items
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/open_drawer_and_store_items/2810096/3329692/A2D0015AB00061/12042813 iros_open_drawer_and_store_items
#
# Pack in the Supermarket (10 episodes available):
./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pack_in_the_supermarket/2810137/3335888/A2D0015AB00061/12055136 iros_pack_in_the_supermarket
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pack_in_the_supermarket/2810137/3335888/A2D0015AB00061/12055122 iros_pack_in_the_supermarket
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pack_in_the_supermarket/2810137/3335897/A2D0015AB00061/12055187 iros_pack_in_the_supermarket
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pack_in_the_supermarket/2810137/3335897/A2D0015AB00061/12055193 iros_pack_in_the_supermarket
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pack_in_the_supermarket/2810137/3335953/A2D0015AB00061/12055452 iros_pack_in_the_supermarket
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pack_in_the_supermarket/2810137/3335879/A2D0015AB00061/12055065 iros_pack_in_the_supermarket
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pack_in_the_supermarket/2810137/3335879/A2D0015AB00061/12055073 iros_pack_in_the_supermarket
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pack_in_the_supermarket/2810137/3335879/A2D0015AB00061/12055059 iros_pack_in_the_supermarket
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pack_in_the_supermarket/2810137/3335899/A2D0015AB00061/12055186 iros_pack_in_the_supermarket
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pack_in_the_supermarket/2810137/3336113/A2D0015AB00061/12056305 iros_pack_in_the_supermarket
#
# Pack Moving Objects from Conveyor (requires extraction):
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pack_moving_objects_from_conveyor/<task_id>/<job_id>/<robot_id>/<episode_id> iros_pack_moving_objects_from_conveyor
#
# Pickup Items from the Freezer (requires extraction):
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/pickup_items_from_the_freezer/<task_id>/<job_id>/<robot_id>/<episode_id> iros_pickup_items_from_the_freezer
#
# Restock Supermarket Items:
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/restock_supermarket_items/2810085/3327951/A2D0015AB00061/12041099 iros_restock_supermarket_items
./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/restock_supermarket_items/2810085/3327924/A2D0015AB00061/12041071 iros_restock_supermarket_items
#
# Stamp the Seal:
# ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/stamp_the_seal/2810130/3335579/A2D0015AB00061/12053448 iros_stamp_the_seal
./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/stamp_the_seal/2810130/3335579/A2D0015AB00061/12053451 iros_stamp_the_seal
#   ./replay_agibot_trajectory.sh AgiBotWorldChallenge-2025/Manipulation-SimData/stamp_the_seal/2810130/3335579/A2D0015AB00061/12053447 iros_stamp_the_seal
#

# First, check what Isaac Sim processes are running:
ps aux | grep -E "raise_standalone_sim|replay_state|isaac-sim" | grep -v grep

# Kill all Isaac Sim server processes:
pkill -9 -f "raise_standalone_sim.py"
