#!/usr/bin/env bash
# Reinstall everything in dependencies.txt onto this machine.
# Pod relaunch wipes all paths except /workspace — run this after each boot:
#   ./scripts/setup/install_dependencies.sh
#
# Installs optional_ros_pkg too (Isaac topic_based_ros2_control).
# Pass --skip-optional to omit those. Pass --dry-run to print apt packages only.
set -euo pipefail
# shellcheck source=/dev/null
source "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/_repo_root.sh"
DEPS="${ROOT}/dependencies.txt"
ROS_DISTRO="${ROS_DISTRO:-humble}"
SKIP_OPTIONAL=0
DRY_RUN=0

usage() {
  cat <<EOF
Usage: $0 [--skip-optional] [--dry-run]
Install apt packages for every entry in dependencies.txt (ROS 2 ${ROS_DISTRO}).
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-optional) SKIP_OPTIONAL=1 ;;
    --dry-run) DRY_RUN=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2 ;;
  esac
  shift
done

if [[ ! -f "$DEPS" ]]; then
  echo "ERROR: $DEPS not found" >&2
  exit 1
fi

if [[ "$(id -u)" -eq 0 ]]; then
  APT=(apt-get)
  SUDO=()
else
  APT=(sudo apt-get)
  SUDO=(sudo)
fi

export DEBIAN_FRONTEND=noninteractive
export TZ="${TZ:-Etc/UTC}"

ros_deb() {
  # rclcpp -> ros-humble-rclcpp
  echo "ros-${ROS_DISTRO}-$(echo "$1" | tr '_' '-')"
}

# extras so listed packages can actually run / build (not duplicated from the file)
BOOTSTRAP_PKGS=(
  curl
  gnupg
  lsb-release
  ca-certificates
  locales
  software-properties-common
  build-essential
  cmake
  python3
  python3-dev
  python3-pip
  python3-argcomplete
  python3-colcon-common-extensions
  "ros-${ROS_DISTRO}-rmw-cyclonedds-cpp"
  "ros-${ROS_DISTRO}-rmw-fastrtps-cpp"
  "ros-${ROS_DISTRO}-xacro"
  "ros-${ROS_DISTRO}-moveit-ros-move-group"
  "ros-${ROS_DISTRO}-moveit-planners-ompl"
  "ros-${ROS_DISTRO}-moveit-simple-controller-manager"
  "ros-${ROS_DISTRO}-moveit-configs-utils"
  "ros-${ROS_DISTRO}-moveit-task-constructor-capabilities"
  "ros-${ROS_DISTRO}-moveit-task-constructor-visualization"
)

declare -a PKGS=()

add_pkg() {
  local p="$1"
  [[ -z "$p" ]] && return 0
  local e
  for e in "${PKGS[@]+"${PKGS[@]}"}"; do
    [[ "$e" == "$p" ]] && return 0
  done
  PKGS+=("$p")
}

map_entry() {
  local kind="$1" name="$2"
  case "$kind" in
    cmd)
      case "$name" in
        ros2) add_pkg "ros-${ROS_DISTRO}-ros-base" ;;
        colcon) add_pkg python3-colcon-common-extensions ;;
        python3) add_pkg python3; add_pkg python3-dev ;;
        *)
          echo "WARN: no apt mapping for cmd $name" >&2
          ;;
      esac
      ;;
    deb)
      add_pkg "$name"
      ;;
    ros_pkg)
      add_pkg "$(ros_deb "$name")"
      ;;
    optional_ros_pkg)
      if [[ "$SKIP_OPTIONAL" -eq 1 ]]; then
        echo "skip optional ros $name"
      else
        add_pkg "$(ros_deb "$name")"
      fi
      ;;
    python)
      case "$name" in
        numpy) add_pkg python3-numpy ;;
        yaml) add_pkg python3-yaml ;;
        pytest) add_pkg python3-pytest ;;
        rclpy|launch|launch_ros|ament_index_python|tf2_ros|geometry_msgs|std_msgs|moveit_msgs)
          add_pkg "$(ros_deb "$name")"
          ;;
        *)
          echo "WARN: no apt mapping for python $name (will try pip later)" >&2
          ;;
      esac
      ;;
    *)
      echo "SKIP unknown kind $kind ($name)" >&2
      ;;
  esac
}

while read -r kind name extra; do
  [[ -z "${kind:-}" || "$kind" =~ ^# ]] && continue
  map_entry "$kind" "$name"
done < <(grep -v '^[[:space:]]*$' "$DEPS" | grep -v '^#')

for p in "${BOOTSTRAP_PKGS[@]}"; do
  add_pkg "$p"
done

echo "Packages to install (${#PKGS[@]}):"
printf '  %s\n' "${PKGS[@]}"

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "dry-run: not installing"
  exit 0
fi

echo "== apt sources / ROS ${ROS_DISTRO} =="
"${APT[@]}" update -qq
"${APT[@]}" install -y -qq curl gnupg lsb-release ca-certificates locales software-properties-common

if ! grep -q '^en_US.UTF-8' /etc/locale.gen 2>/dev/null; then
  sed -i 's/^# *en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen || true
  echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen
fi
locale-gen en_US.UTF-8 >/dev/null
update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 || true
export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

"${SUDO[@]}" add-apt-repository -y universe >/dev/null

KEYRING=/usr/share/keyrings/ros-archive-keyring.gpg
if [[ ! -f "$KEYRING" ]]; then
  echo "Adding ROS 2 apt key and repo..."
  curl -fsSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /tmp/ros-archive-keyring.gpg
  "${SUDO[@]}" mv /tmp/ros-archive-keyring.gpg "$KEYRING"
fi
CODENAME="$(. /etc/os-release && echo "${UBUNTU_CODENAME}")"
ARCH="$(dpkg --print-architecture)"
echo "deb [arch=${ARCH} signed-by=${KEYRING}] http://packages.ros.org/ros2/ubuntu ${CODENAME} main" \
  > /tmp/ros2.list
"${SUDO[@]}" mv /tmp/ros2.list /etc/apt/sources.list.d/ros2.list

"${APT[@]}" update -qq
echo "== apt install =="
"${APT[@]}" install -y "${PKGS[@]}"

echo "== verify =="
# shellcheck source=/dev/null
set +u
source "/opt/ros/${ROS_DISTRO}/setup.bash"
set -u
"${ROOT}/scripts/setup/check_dependencies.sh"
echo "Install OK. After a pod relaunch, run this script again (only /workspace persists)."
echo "Then: source /opt/ros/${ROS_DISTRO}/setup.bash && source ${ROOT}/ros2_ws/install/setup.bash"
