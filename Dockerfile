# ROS 2 Humble + MoveIt 2 + Foxglove
#rviz2, xacro
# Talks to Isaac Sim 6.0.1 via isaacsim.ros2.bridge on the host (--net=host).
#
# Build:  docker build -t ros2-humble-isaacsim:6.0.1 .
# Run:    docker run --rm -it --net=host --ipc=host -e DISPLAY -e ROS_DOMAIN_ID=0 ros2-humble-isaacsim:6.0.1

FROM osrf/ros:humble-desktop-full

ENV DEBIAN_FRONTEND=noninteractive \
    ROS_DISTRO=humble \
    RMW_IMPLEMENTATION=rmw_fastrtps_cpp \
    FASTRTPS_DEFAULT_PROFILES_FILE=/root/.ros/fastdds.xml \
    ROS_DOMAIN_ID=0

SHELL ["/bin/bash", "-c"]

# MoveIt 2 + Foxglove + utilities for Isaac Sim DDS / robot bringup
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-rmw-fastrtps-cpp \
    ros-humble-topic-tools \
    ros-humble-xacro \
    ros-humble-robot-state-publisher \
    ros-humble-joint-state-publisher \
    ros-humble-joint-state-publisher-gui \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-controller-manager \
    ros-humble-foxglove-bridge \
    ros-humble-moveit \
    ros-humble-moveit-resources \
    ros-humble-moveit-configs-utils \
    ros-humble-moveit-ros-planning-interface \
    ros-humble-moveit-ros-perception \
    ros-humble-moveit-task-constructor-msgs \
    ros-humble-moveit-task-constructor-core \
    ros-humble-moveit-task-constructor-capabilities \
    ros-humble-moveit-task-constructor-visualization \
    python3-pip \
    tmux \
    && rm -rf /var/lib/apt/lists/*

# trimesh loads collision meshes for the planning scene. Pinned: 5.x needs a
# newer numpy than Humble ships and fails at import on numpy 1.21.
RUN python3 -m pip install --no-cache-dir 'trimesh==3.23.5'



# Fast DDS UDP profile required for reliable DDS with Isaac Sim ros2.bridge
RUN mkdir -p /root/.ros && printf '%s\n' \
    '<?xml version="1.0" encoding="UTF-8" ?>' \
    '<profiles xmlns="http://www.eprosima.com/XMLSchemas/fastRTPS_Profiles">' \
    '  <transport_descriptors>' \
    '    <transport_descriptor>' \
    '      <transport_id>UdpTransport</transport_id>' \
    '      <type>UDPv4</type>' \
    '    </transport_descriptor>' \
    '  </transport_descriptors>' \
    '  <participant profile_name="udp_transport_profile" is_default_profile="true">' \
    '    <rtps>' \
    '      <userTransports><transport_id>UdpTransport</transport_id></userTransports>' \
    '      <useBuiltinTransports>false</useBuiltinTransports>' \
    '    </rtps>' \
    '  </participant>' \
    '</profiles>' \
    > /root/.ros/fastdds.xml

COPY ros_entrypoint.sh /ros_entrypoint.sh
RUN chmod +x /ros_entrypoint.sh \
    && echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc \
    && echo "alias foxglove='ros2 launch foxglove_bridge foxglove_bridge_launch.xml port:=8765'" >> /root/.bashrc

WORKDIR /ros2_ws
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
