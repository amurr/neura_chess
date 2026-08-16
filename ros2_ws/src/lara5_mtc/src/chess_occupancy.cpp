#include "lara5_mtc/chess_occupancy.hpp"

#include <algorithm>
#include <cctype>
#include <fstream>
#include <stdexcept>

#include <ament_index_cpp/get_package_share_directory.hpp>

namespace lara5_mtc
{
namespace
{

std::string lower(std::string value)
{
  std::transform(value.begin(), value.end(), value.begin(),
                 [](unsigned char c) { return static_cast<char>(std::tolower(c)); });
  return value;
}

bool isChessSquare(const std::string& name)
{
  if (name.size() != 2)
  {
    return false;
  }
  return name[0] >= 'a' && name[0] <= 'h' && name[1] >= '1' && name[1] <= '8';
}

std::string firstString(const nlohmann::json& occ, std::initializer_list<const char*> keys)
{
  for (const char* key : keys)
  {
    if (occ.contains(key) && occ[key].is_string())
    {
      return lower(occ[key].get<std::string>());
    }
  }
  return {};
}

}  // namespace

nlohmann::json loadOccupancyFile(const std::string& path)
{
  std::ifstream input(path);
  if (!input)
  {
    throw std::runtime_error("cannot open occupancy file: " + path);
  }
  nlohmann::json data;
  input >> data;
  return data;
}

std::unordered_map<std::string, SquarePose> occupancySquarePoses(const nlohmann::json& occ)
{
  std::unordered_map<std::string, SquarePose> poses;

  if (occ.contains("squares") && occ["squares"].is_object())
  {
    for (const auto& [name, value] : occ["squares"].items())
    {
      if (!value.is_object())
      {
        continue;
      }
      SquarePose pose;
      pose.x = value.value("x", 0.0);
      pose.y = value.value("y", 0.0);
      pose.z = value.value("z", 0.0);
      if (value.contains("type") && value["type"].is_string())
      {
        pose.type = lower(value["type"].get<std::string>());
      }
      poses[lower(name)] = pose;
    }
    return poses;
  }

  for (const auto& [name, value] : occ.items())
  {
    if (!isChessSquare(name) || !value.is_object())
    {
      continue;
    }
    SquarePose pose;
    pose.x = value.value("x", 0.0);
    pose.y = value.value("y", 0.0);
    pose.z = value.value("z", 0.0);
    if (value.contains("type") && value["type"].is_string())
    {
      pose.type = lower(value["type"].get<std::string>());
    }
    poses[lower(name)] = pose;
  }
  return poses;
}

std::tuple<double, double> pieceCylinderDimensions(const std::string& piece_type)
{
  static const std::unordered_map<std::string, std::pair<double, double>> kDims = {
    { "pawn", { 0.018, 0.034 } },
    { "bishop", { 0.022, 0.047 } },
    { "knight", { 0.024, 0.049 } },
    { "rook", { 0.026, 0.044 } },
    { "queen", { 0.027, 0.058 } },
    { "king", { 0.029, 0.066 } },
  };
  const std::string type = lower(piece_type);
  const auto it = kDims.find(type);
  if (it != kDims.end())
  {
    return { it->second.first, it->second.second };
  }
  return { 0.018, 0.034 };
}

std::string pieceObjectId(const std::string& square)
{
  return "piece_" + lower(square);
}

SquarePose inferSquarePose(const nlohmann::json& occ,
                           const std::string& square,
                           const std::string& reference_square,
                           const double square_size_m)
{
  const auto poses = occupancySquarePoses(occ);
  const std::string sq = lower(square);
  const auto direct = poses.find(sq);
  if (direct != poses.end())
  {
    return direct->second;
  }

  const std::string ref = lower(reference_square);
  const auto ref_it = poses.find(ref);
  if (ref_it == poses.end())
  {
    throw std::runtime_error("cannot infer square '" + sq + "': reference '" + ref + "' missing");
  }

  SquarePose pose = ref_it->second;
  const int df = sq[0] - ref[0];
  const int dr = sq[1] - ref[1];
  pose.x += dr * square_size_m;
  pose.y += df * square_size_m;
  return pose;
}

ChessMove resolveChessMove(const nlohmann::json& occ,
                           const std::string& source_override,
                           const std::string& target_override)
{
  ChessMove move;
  move.source = !source_override.empty() ? lower(source_override)
                                         : firstString(occ, { "source", "from", "from_square" });
  move.target = !target_override.empty() ? lower(target_override)
                                         : firstString(occ, { "target", "to", "to_square" });
  if (move.source.empty())
  {
    move.source = "e2";
  }
  if (move.target.empty())
  {
    move.target = "e4";
  }

  const auto poses = occupancySquarePoses(occ);
  const auto source_it = poses.find(move.source);
  move.piece_type = (source_it != poses.end() && !source_it->second.type.empty()) ? source_it->second.type
                                                                                    : "pawn";
  std::tie(move.piece_diameter, move.piece_height) = pieceCylinderDimensions(move.piece_type);
  move.object_id = pieceObjectId(move.source);
  return move;
}

std::string defaultOccupancyPath()
{
  const std::string share = ament_index_cpp::get_package_share_directory("xyz_motion");
  return share + "/examples/standard_start.json";
}

}  // namespace lara5_mtc
