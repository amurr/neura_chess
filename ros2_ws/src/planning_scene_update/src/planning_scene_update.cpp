/**
 * Publishes chess_board.obj and a pawn.stl sitting on the board top.
 *
 *   ros2 run planning_scene_update planning_scene_update
 */

#include <memory>
#include <stdexcept>
#include <string>

#include <geometric_shapes/mesh_operations.h>
#include <geometric_shapes/shapes.h>
#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/pose.hpp>
#include <shape_msgs/msg/mesh.hpp>
#include <moveit_msgs/msg/collision_object.hpp>
#include <moveit_msgs/msg/planning_scene.hpp>

static const std::string FRAME_ID = "world";
static const std::string BOARD_MESH = "package://lara5_moveit/meshes/chess_board.obj";
static const std::string PAWN_MESH =
  "package://lara5_moveit/meshes/chess_pieces/collision_hulls/pawn.stl";

// Board OBJ is a 0.02 m slab centered at its pose, so the top face is +0.01 m.
static const double BOARD_X = 0.5;
static const double BOARD_Y = 0.0;
static const double BOARD_Z = 0.0;
static const double BOARD_TOP_Z = BOARD_Z + 0.01;

shape_msgs::msg::Mesh loadMesh(const std::string & uri)
{
  std::unique_ptr<shapes::Mesh> raw(shapes::createMeshFromResource(uri));
  if (!raw) {
    throw std::runtime_error("failed to load mesh " + uri);
  }

  shape_msgs::msg::Mesh mesh;
  mesh.vertices.resize(raw->vertex_count);
  for (unsigned i = 0; i < raw->vertex_count; ++i) {
    mesh.vertices[i].x = raw->vertices[3 * i + 0];
    mesh.vertices[i].y = raw->vertices[3 * i + 1];
    mesh.vertices[i].z = raw->vertices[3 * i + 2];
  }
  mesh.triangles.resize(raw->triangle_count);
  for (unsigned i = 0; i < raw->triangle_count; ++i) {
    mesh.triangles[i].vertex_indices[0] = raw->triangles[3 * i + 0];
    mesh.triangles[i].vertex_indices[1] = raw->triangles[3 * i + 1];
    mesh.triangles[i].vertex_indices[2] = raw->triangles[3 * i + 2];
  }
  return mesh;
}

moveit_msgs::msg::CollisionObject makeMeshObject(
  const std::string & id, const std::string & uri, double x, double y, double z)
{
  geometry_msgs::msg::Pose pose;
  pose.position.x = x;
  pose.position.y = y;
  pose.position.z = z;
  pose.orientation.w = 1.0;

  moveit_msgs::msg::CollisionObject obj;
  obj.header.frame_id = FRAME_ID;
  obj.id = id;
  obj.meshes.push_back(loadMesh(uri));
  obj.mesh_poses.push_back(pose);
  obj.operation = moveit_msgs::msg::CollisionObject::ADD;
  return obj;
}

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = rclcpp::Node::make_shared("planning_scene_update");
  auto pub = node->create_publisher<moveit_msgs::msg::PlanningScene>(
    "/planning_scene", rclcpp::QoS(1).transient_local());

  rclcpp::Rate rate(10);
  while (rclcpp::ok() && pub->get_subscription_count() == 0) {
    rclcpp::spin_some(node);
    rate.sleep();
  }

  moveit_msgs::msg::PlanningScene scene;
  scene.is_diff = true;
  try {
    scene.world.collision_objects.push_back(
      makeMeshObject("chess_board", BOARD_MESH, BOARD_X, BOARD_Y, BOARD_Z));
    scene.world.collision_objects.push_back(
      makeMeshObject("pawn", PAWN_MESH, BOARD_X, BOARD_Y, BOARD_TOP_Z));
  } catch (const std::exception & e) {
    RCLCPP_ERROR(node->get_logger(), "%s", e.what());
    rclcpp::shutdown();
    return 1;
  }

  pub->publish(scene);
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
