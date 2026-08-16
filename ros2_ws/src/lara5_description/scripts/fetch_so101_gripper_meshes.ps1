# Download SO-101 gripper STL meshes (TheRobotStudio/SO-ARM100)
$ErrorActionPreference = "Stop"
$MeshDir = Join-Path $PSScriptRoot "..\lara5\meshes\so101" | Resolve-Path -ErrorAction SilentlyContinue
if (-not $MeshDir) {
    $MeshDir = (New-Item -ItemType Directory -Force -Path (Join-Path $PSScriptRoot "..\lara5\meshes\so101")).FullName
}
$Base = "https://raw.githubusercontent.com/TheRobotStudio/SO-ARM100/main/STL/SO101/Individual"
$files = @{
    "moving_jaw_so101_v1.stl" = "$Base/Moving_Jaw_SO101.stl"
    "wrist_roll_follower_so101_v1.stl" = "$Base/Wrist_Roll_Follower_SO101.stl"
}
foreach ($name in $files.Keys) {
    $out = Join-Path $MeshDir $name
    Write-Host "Downloading $name ..."
    Invoke-WebRequest -Uri $files[$name] -OutFile $out -UseBasicParsing
}
# Optional servo mesh from SO-100 parts pack
try {
    $stsUrl = "https://raw.githubusercontent.com/TheRobotStudio/SO-ARM100/main/STL/SO100/Individual/STS3215_03a_v1.stl"
    Invoke-WebRequest -Uri $stsUrl -OutFile (Join-Path $MeshDir "sts3215_03a_v1.stl") -UseBasicParsing
} catch {
    Write-Warning "STS3215 mesh not found; URDF uses cylinder fallback for servo visual."
}
Get-ChildItem $MeshDir | Format-Table Name, Length
