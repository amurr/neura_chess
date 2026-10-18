# Calibration and precision pick-and-place: lessons learned

Lessons from making the Lara5 + SO-101 (LeRobot) gripper pick and place chess pieces in Isaac
Sim to millimetre accuracy. Written so the same process can be reused on other high-precision
tasks and robots (Lara5, Franka FR3). The chess numbers are examples; the method is the point.


## 1. Order of work

Errors stack up along a chain. Fix them from the base outwards, and measure each link before
tuning anything after it.

```
world / board / objects  →  robot base  →  joint tracking  →  flange  →  TCP
        →  gripper contact mechanics  →  carry  →  release  →  final object pose
```

1. **Frames and object positions agree everywhere** (sim scene, planning scene, perception).
2. **The robot reaches its commanded poses** (controller tolerances, drive gains, sag).
3. **The TCP is the real working point** (tool geometry).
4. **The planning model matches what physically collides** (collision geometry).
5. **The grasp holds** (contact mechanics, forces, friction).
6. **Release leaves the object where intended** (place mechanics).
7. **Only then calibrate the remaining systematic offsets** from measured outcomes.

On this project, every early failure came from steps 1–4, not from grasp parameters:

- the board was 2 cm off between Isaac and ROS (corner vs centre convention);
- kings and queens were swapped in Isaac;
- MoveIt pieces floated 1 cm above the board;
- MoveIt never checked collisions with pieces, because an STL loader kept 1 triangle per mesh.

No amount of grasp tuning could have fixed any of those.


## 2. Frames and conventions

- **Write down every convention explicitly**: what a calibration point means (corner or centre,
  top surface or mid-thickness), axis directions, file/rank mapping, mirroring. Two
  descriptions of "a1 at (0.27, −0.16)" disagreed by half a square.
- **Keep one source of truth** for scene geometry. Derive the sim scene, the planning scene and
  the hover/grasp poses from it, instead of keeping separate constants in each place.
- **Check with a known object**: place one object, read its pose from every system (sim
  ground truth, planning scene, FK of the robot touching it), and compare to < 1 mm.
- **Object order and identity**: verify which object is where (king/queen swap), not just that
  "something is on every square".


## 3. TCP

- **Plan for the point that does the work, not the flange.** For a parallel or one-sided
  gripper, a good TCP is the fingertip on the contact face. Here it is the tip of the static
  SO-101 finger, on its inner face: `lara5_tcp` in the URDF, the end of the SRDF `arm` chain.
- **Measure the TCP from the CAD/mesh, not from a guess**, e.g. the lowest point of the finger
  mesh and the inner-face plane. Record how it was measured in the URDF comment.
- **Give it the gripper's axes**: x from the fixed to the moving finger, z back up the fingers.
  Then "piece centre at (r, 0, 0) in the TCP frame" is a direct statement about the grasp.
- **Keep the gripper links separate from the TCP** in software: the links allowed to touch a
  grasped object hang below the gripper mount, not below the TCP (a leaf link with no
  geometry).
- **Check it**: FK of the TCP in your own IK code, MoveIt's TF and the simulator must agree
  (here to 0.1 mm), and a pure Cartesian move must move the TCP by exactly the commanded amount.
- **Franka FR3**: `franka_description` already has `fr3_hand_tcp` (between the fingertips,
  0.1034 m from the flange). For one-sided pushing or edge grasps, define your own TCP on
  the finger face the same way. The Franka Hand is a true parallel gripper, so the slanted-jaw
  problems in section 6 mostly disappear. Its grasp force is commanded directly (`grasp` action
  with force/epsilon), not through position overshoot.


## 4. Make the model match what physically collides

- **Simulators approximate collision meshes.** Isaac/PhysX turns every mesh into a convex hull,
  by default limited to 64 vertices.
  - The convex hull of the SO-101 wrist mesh closed the gap between the fingers. Fix: fitted
    box primitives per finger segment in the URDF.
  - 64-vertex hulls shaved narrow features (the pawn's neck and head). Fix: hull vertex limit
    255 (`PhysxConvexHullCollisionAPI`).
- **Compute grasp parameters from the geometry the simulator actually collides with** (the
  same hulls, the same primitives), not from the visual mesh.
  `lara5_moveit/scripts/compute_piece_grasps.py` does this from the Isaac USD assets.
- **Give the planner the same geometry.** MoveIt piece meshes are generated from the Isaac
  hulls, so a pose MoveIt calls collision-free is collision-free in Isaac.
- **Check self-collision settings after editing articulations.** Re-applying
  `PhysxArticulationAPI` re-enabled self-collision, and the jaw's hub overlapped link6's hull:
  PhysX kept pushing the jaw shut, which looked like a weak gripper.
- **Test the collision checker with states that must collide.** Ask MoveIt
  (`/check_state_validity`) whether a pose with the fingers inside an object is valid. It said
  "valid" for everything here, which exposed the one-triangle-per-mesh STL bug.


## 5. Getting the arm to the commanded pose

- **Controller goal tolerances decide when a step "arrived".** With 0.02 rad per joint the
  controller declared success with the TCP ~1 cm high, and the gripper closed too early.
  Use per-joint tolerances matched to the lever arm: 0.005 rad on joints 1–3, 0.015 on the
  wrist joints.
- **Measure the static offset** (gravity sag, drive stiffness) at representative poses before
  setting tolerances. Here it was ~0.008 rad on joint 5, systematic and repeatable.
- **Simulator drive units**: USD angular drive stiffness and damping are per degree.
  2000 N·m/deg is very stiff; damping above critical slows settling.
- **Trust velocities only if they mean something.** Isaac's joint velocity for a jaw pressed
  still against an object read 0.07–3 rad/s. Stall detection and the "stopped" checks need
  velocities computed from position change (`isaac_state_velocity` relay).
- **On the real robot**: compliance, backlash and payload change the offsets. Measure them on
  the hardware (sections 9 and 10); don't copy simulation numbers.


## 6. Grasp mechanics: the part that takes most of the time

Positioning to 0.5 mm is the easy part. Whether the object ends up where planned depends on
contact mechanics.

**Geometry of the grip**
- **Grip above the centre of mass.** Two point contacts below it make an inverted pendulum and
  the piece swings over. Contacts above it make it hang.
- **Avoid cones and spheres between the fingers.** Squeezing a cone or a ball pushes it out of
  the grip, up or down along the slope. Grip a cylindrical section if there is one.
- **Watch for hooks.** A finger tip that sits under a ball or flange holds the object like a
  hook instead of squeezing it. It survives the lift, then slides out during transport.
- **Wide objects with a pivoting jaw** (SO-101) are touched high up by a tilted face: tall
  pieces get a tipping moment and wedge forces. A parallel gripper (Franka Hand) avoids this.
- **Give the static finger clearance before closing** (1.5 mm here): it must not land on the
  object. But keep the gap small, because the object has to slide that far on the table
  before it's clamped, and tall objects tip instead.

**Force**
- **A position-controlled jaw squeezes only through overshoot past contact.** If the contact is
  near the joint limit (narrow objects), there is no squeeze left. If the target is reached,
  the force is zero.
- **A stiff drive saturates and chatters against the object**, and kicks light objects away.
  A soft spring with the target well past contact gives a steady, bounded force.
- **Close slowly** (time constant ~0.3 s). A jaw that slams in tips objects over before it
  squeezes.
- **Franka Hand**: use the `grasp` action with an explicit force (e.g. 5–20 N) and width
  epsilon; that's the direct equivalent of everything above.

**Friction**
- **Friction is a per-finger design choice.**
  - High friction on the static finger holds the object in place.
  - High friction on the moving jaw drags objects over when it opens, because its tip moves
    up along its arc.
  - A frictionless jaw lets the object rotate about the other contact and fall out.
- **Point contacts have no torsional friction in simulation.** Real pads do. Enable torsional
  patch friction (PhysX `torsionalPatchRadius`) or the gripped object swings about the axis
  between the fingers.
- **Cap the depenetration velocity** of small objects, or a slightly overlapping release
  shoots them away.

**Release**
- **Set the object down slightly lower** than it was picked (1 mm press) so a slightly tilted
  object lands on its base.
- **Open only as far as needed**, then **move the fixed finger off** the object before lifting.
  Otherwise the high-friction finger drags it up.
- **Check after the arm has left.** Many failures happen during release and retreat, not
  during the grasp.


## 7. The gripper body is part of the problem

- **The wrist above the fingers is usually wider than the gap between objects** (SO-101:
  46 × 48 mm, 66 mm above the fingertip, on a 40 mm grid). Grip height and approach direction
  must account for neighbouring objects, especially tall ones.
- **Have more than one grasp option per object type** and choose per move:
  - several grip heights (`higher` levels in the objects dictionary);
  - a second jaw direction (`{square}_hover_alt`, −60° instead of −45°).
  The orchestrator checks the wrist boxes against the neighbours' height profiles and takes
  the lowest option that clears both the pick and the place. MoveIt then checks every motion.
- **Point fingers into the free space.** On a grid, the diagonal is where the next object is
  farthest away (56.6 mm instead of 40 mm).


## 8. Calibrating systematic offsets

- **Calibrate on the final outcome, not on an intermediate measurement.** The position of the
  piece in the gripper while carried did not predict where it landed (the knight was carried
  3 mm off the model but landed within 0.4 mm). The calibration now uses:
  final position − target, in TCP axes, added to the offset that was used.
  Script: `articulation_orchestrator/scripts/calibrate_place_offsets.py`.
- **Calibrate only what is repeatable.** Look at the spread across repeated runs first.
  - Queen and rook: same direction every time, so calibration fixed them (→ ~2 mm).
  - Bishop: varied by 5+ mm, so one sample over-corrected it (12 mm the next round).
  - Use several samples, and exclude failed moves (toppled, off the square).
- **Calibrate in the tool frame** (TCP axes), because the error comes from the grasp, not the
  world. A world-frame offset only holds for one approach direction.
- **Re-verify after every calibration** with fresh runs.


## 9. Measuring: the test harness matters as much as the robot

- **Log everything with timestamps**: joint states, TCP pose (from TF), every step's start and
  end, and the ground-truth object poses (sim) or perception poses (real).
  `execution_logger` writes `arm.jsonl`, `steps.csv` and `isaac_pieces.jsonl` per move.
- **Trace failures over time**, e.g. object z and tilt versus jaw angle versus step. That's what
  revealed the swinging pawn, the hook under the ball and the drag on release. A single final
  number never explains a failure.
- **Check that the metric measures what you think.** The snapshot "tilt" included rotation
  about the vertical, so upright pieces looked tipped; true lean is the angle of the up axis.
  Cross-check with an independent quantity (the object's height above the table).
- **Make sure the system under test is the one you changed.** One round ran on the old sim
  because a relative launch path failed and the readiness check read the previous log.
  Before each round, check the process start time and the loaded parameter values.
- **One stack per machine.** Two ROS stacks with the same node names (two controller managers,
  two action servers) silently corrupt each other. Check with `ros2 action info` and
  `ros2 topic info /joint_states` (exactly one server / publisher).
- **Reset to a known state before every trial** (scene restore + resync of the planner's world
  model). Otherwise one failure cascades into every following trial.
- **Run every test at least twice.** Single runs misled me repeatedly; contact physics is not
  deterministic enough to judge from one sample.
- **Write down the best configuration seen so far** and revert to it when a change makes
  things worse. Changes that helped one object type often hurt another.


## 10. Fast iteration

- **Use the cheapest test that answers the question.**
  - Offline geometry/IK script: seconds. Grasp offsets, wrist clearances, reachability.
  - Mock MoveIt stack on its own ROS domain (`ROS_DOMAIN_ID=87`): ~2 min. Planning and
    collisions for a whole game, with no physics.
  - MoveIt state-validity queries: instant. "Is this grasp pose collision-free?" for many
    options at once.
  - Full simulation: ~5 min startup + ~2 min per move. Contact mechanics only.
- **Script the whole loop**: restart → wait for readiness → reset → move → snapshot → log.
- **Generate parameters from geometry, then measure and correct.** Hand-tuned numbers don't
  survive a change of object, gripper or robot.


## 11. Checklist for a new task or robot (Lara5, Franka FR3, …)

1. Scene frames: one source of truth; verify one known object in sim, planner and perception.
2. TCP: measured from CAD on the working surface; FK = TF = sim; Cartesian move moves it exactly.
3. Collision geometry: sim approximations (hulls, primitives) used for planning and grasp
   computation; self-collision settings checked; validity checker tested with known collisions.
4. Arm accuracy: static offsets measured; per-joint goal tolerances; "arrived" before each
   contact step.
5. Grasp per object type: grip height above the centre of mass on a cylindrical section; the
   finger clearance; a force set-point (Franka) or overshoot with a soft drive (position
   grippers); slow close; friction per finger.
6. Neighbours: the gripper body's footprint checked against nearby objects; several grip
   heights and approach directions.
7. Release: press, partial open, back off, lift; check after the arm has left.
8. Harness: logging, ground-truth snapshots, reset, readiness checks, single stack, two runs per
   test.
9. Calibration: final-outcome errors in tool axes, only for repeatable types, re-verify.
10. Real hardware: repeat steps 4, 8 and 9 on the robot; simulation offsets are a starting point.


## Status of the Lara5 chess setup (end of this session)

Isaac, start-position moves, rounds 19–24:

| Piece | Status | Error |
|---|---|---|
| Knight | reliable | 0.1–2 mm |
| Rook | reliable | 0.6–3.8 mm |
| Queen | reliable | ~2 mm after calibration |
| King | mostly reliable (fell twice in ~12 moves) | 0.9–6.7 mm |
| Bishop | works; placement not yet repeatable | 0.3–12 mm |
| White pawns | mostly reliable (~1 in 10 dropped) | usually 0.2–5.6 mm |
| Black pawns | mostly fail (gripped by the head, lost during transport) | — |

Not yet tested in Isaac: captures, mid-game positions, black pieces other than pawns.
