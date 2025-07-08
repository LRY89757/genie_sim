#!/bin/bash

set -e

# env
export ROS_DISTRO=humble

# # zshrc
# echo "alias omni_python='/isaac-sim/python.sh'" >>~/.zshrc
# echo "alias run_server='omni_python server/source/genie.sim.lab/raise_standalone_sim.py'" >>~/.zshrc
# echo "alias run_client='omni_python benchmark/task_benchmark.py --task_name'" >>~/.zshrc
# echo "alias run_teleop='omni_python teleop/teleop.py --task_name'" >>~/.zshrc
# echo "alias run_replay='omni_python teleop/replay_state.py'" >>~/.zshrc

# echo "source /opt/ros/$ROS_DISTRO/setup.bash" >>~/.zshrc

# echo "export SIM_ASSETS=/mnt/amlfs-01/home/runyul/projects/genie_sim/GenieSimAssets" >>~/.zshrc
# echo "export SIM_REPO_ROOT=/mnt/amlfs-01/home/runyul/projects/genie_sim" >>~/.zshrc

# echo "export ROS_DISTRO=humble" >>~/.zshrc
# echo "export ROS_LOCALHOST_ONLY=1" >>~/.zshrc

# bashrc
echo "alias omni_python='/isaac-sim/python.sh'" >>~/.bashrc
echo "alias run_server='omni_python server/source/genie.sim.lab/raise_standalone_sim.py'" >>~/.bashrc
echo "alias run_client='omni_python benchmark/task_benchmark.py --task_name'" >>~/.bashrc
echo "alias run_teleop='omni_python teleop/teleop.py --task_name'" >>~/.bashrc
echo "alias run_replay='omni_python teleop/replay_state.py'" >>~/.bashrc

echo "source /opt/ros/$ROS_DISTRO/setup.bash" >>~/.bashrc

echo "export SIM_ASSETS=/mnt/amlfs-01/home/runyul/projects/genie_sim/GenieSimAssets" >>~/.bashrc
echo "export SIM_REPO_ROOT=/mnt/amlfs-01/home/runyul/projects/genie_sim" >>~/.bashrc

echo "export ROS_DISTRO=humble" >>~/.bashrc
echo "export ROS_LOCALHOST_ONLY=1" >>~/.bashrc

# you can add more customized cmds here

# setup ros2 environment
cd /opt/ros/$ROS_DISTRO/
source "/opt/ros/$ROS_DISTRO/setup.bash" --
# exec "$@"

# zsh
bash
