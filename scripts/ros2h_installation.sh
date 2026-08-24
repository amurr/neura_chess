#!/usr/bin/env bash
# ROS 2 Humble + MoveIt + Isaac Sim bridge packages. Ubuntu 22.04 (jammy) only.
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export TZ=Etc/UTC

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[1/4] Locale, universe, ROS 2 Humble apt repo (jammy)..."
sudo apt-get update
sudo apt-get install -y \
  locales curl gnupg lsb-release ca-certificates software-properties-common
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
sudo add-apt-repository -y universe

sudo curl -fsSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu jammy main" | \
  sudo tee /etc/apt/sources.list.d/ros2.list >/dev/null

echo "[2/4] Installing ROS 2 Humble, MoveIt, ros2_control, Isaac bridge..."
sudo apt-get update
sudo apt-get install -y \
  build-essential \
  cmake \
  nlohmann-json3-dev \
  python3 \
  python3-dev \
  python3-pip \
  python3-argcomplete \
  python3-colcon-common-extensions \
  python3-numpy \
  python3-yaml \
  python3-pytest \
  ros-dev-tools \
  ros-humble-desktop \
  ros-humble-ackermann-msgs \
  ros-humble-ament-index-python \
  ros-humble-control-msgs \
  ros-humble-controller-manager \
  ros-humble-geometry-msgs \
  ros-humble-gripper-controllers \
  ros-humble-joint-state-broadcaster \
  ros-humble-joint-trajectory-controller \
  ros-humble-launch \
  ros-humble-launch-ros \
  ros-humble-moveit-configs-utils \
  ros-humble-moveit-core \
  ros-humble-moveit-msgs \
  ros-humble-moveit-planners-ompl \
  ros-humble-moveit-ros-move-group \
  ros-humble-moveit-ros-planning-interface \
  ros-humble-moveit-simple-controller-manager \
  ros-humble-moveit-task-constructor-capabilities \
  ros-humble-moveit-task-constructor-core \
  ros-humble-moveit-task-constructor-visualization \
  ros-humble-position-controllers \
  ros-humble-rclcpp \
  ros-humble-rclpy \
  ros-humble-realtime-tools \
  ros-humble-rmw-cyclonedds-cpp \
  ros-humble-rmw-fastrtps-cpp \
  ros-humble-robot-state-publisher \
  ros-humble-std-msgs \
  ros-humble-tf2-eigen \
  ros-humble-tf2-geometry-msgs \
  ros-humble-tf2-ros \
  ros-humble-tf2-tools \
  ros-humble-topic-based-ros2-control \
  ros-humble-vision-msgs \
  ros-humble-xacro

echo "[3/4] Shell environment..."
touch "${HOME}/.bashrc"
grep -Fq "source /opt/ros/humble/setup.bash" "${HOME}/.bashrc" || \
  printf '\n# ROS 2 Humble\nsource /opt/ros/humble/setup.bash\n' >> "${HOME}/.bashrc"
grep -Fq "RMW_IMPLEMENTATION=rmw_fastrtps_cpp" "${HOME}/.bashrc" || \
  echo "export RMW_IMPLEMENTATION=rmw_fastrtps_cpp" >> "${HOME}/.bashrc"

echo "[4/4] Verify..."
set +u
# shellcheck source=/dev/null
source /opt/ros/humble/setup.bash
set -u
"${ROOT}/scripts/setup/check_dependencies.sh"

echo "ROS 2 Humble install complete."
echo "source /opt/ros/humble/setup.bash"
echo "source ${ROOT}/ros2_ws/install/setup.bash"
