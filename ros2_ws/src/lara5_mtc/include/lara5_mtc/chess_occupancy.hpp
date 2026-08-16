#pragma once

#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>

#include <nlohmann/json.hpp>

namespace lara5_mtc
{

struct SquarePose
{
  double x{ 0.0 };
  double y{ 0.0 };
  double z{ 0.0 };
  std::string type;
};

struct ChessMove
{
  std::string source;
  std::string target;
  std::string piece_type;
  double piece_diameter{ 0.018 };
  double piece_height{ 0.034 };
  std::string object_id;
};

nlohmann::json loadOccupancyFile(const std::string& path);

std::unordered_map<std::string, SquarePose> occupancySquarePoses(const nlohmann::json& occ);

ChessMove resolveChessMove(const nlohmann::json& occ,
                           const std::string& source_override,
                           const std::string& target_override);

std::string pieceObjectId(const std::string& square);

std::tuple<double, double> pieceCylinderDimensions(const std::string& piece_type);

SquarePose inferSquarePose(const nlohmann::json& occ,
                           const std::string& square,
                           const std::string& reference_square,
                           double square_size_m);

std::string defaultOccupancyPath();

}  // namespace lara5_mtc
