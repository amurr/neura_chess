[] see https://claude.ai/chat/5a49730e-e9e3-4274-bf0a-96634b26af79 for moveit_master.cpp code

# 03.10: prompt for articulation_orchestrator.py code
coding style:
- in code, organise the funtions as i listed them here
- keep it as brief as possible
- kepp it human-readable


1.
PlanningSceneReader function:
- takes all objects from the PlanningScene
- retrieves the specified one
- retrieves its 3d pose, type (=name in dictionary)
- retireves specifications to pick and place it correctly from

1.2
PlanningSceneUpdater publishing meshs from /assets using /apply_planning_scene service

2.
define the action between task_coordinator node and control_node (one in moveit_master.cpp)

3.
DictionaryDataInjection:
- injects this data as arguments into action that will be sent to moveit_master.cpp


# moveit_master_1 contains simpliest version of action service translating python master node commands into MoveGroupInterface actions sent to move_group server node


# ArticulationOrchestrator Node client sends actions to moveit_master_1 server node
see articulation_orchestrator.py def main()

# PlanningSceneUpdater Node client
see main

# chess_board_server.py is for actions server receiving changes done/to do to chess board from the chess cv module: it uses PlanningSceneUpdater OR ArticulationOrchestrator to keep PlanningScene up to date