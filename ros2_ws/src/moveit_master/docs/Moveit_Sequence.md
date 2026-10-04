/home/artem/robotics/neura_chess/ros2_ws/src/lara5_moveit_config/config/lara5.srdf stores memotized joint-space positions of the arms


# injecting PlanningScene objects data into targets
- happens once in a pick and place action


# objects properties retrieved from PlanningScene
- reads using PlanningSceneInterface getObjects function
    - type (object_recognition_msgs/ObjectType)
    - pose



# Dictionary of objects properties
- stored as .yaml in /config of package: no need to recompile the package for new parameters to take effect
- retrieving: 
    - by type of object, known from moveit_msgs/CollisionObject.msg