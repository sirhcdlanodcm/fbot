# Push friendbot image to Docker Hub (PowerShell).
# Prereqs: docker login
# Usage:
#   .\scripts\push-dockerhub.ps1 -DockerHubUser yourhubusername
#   .\scripts\push-dockerhub.ps1 -DockerHubUser yourhubusername -Tag 2026-03-29

param(
    [Parameter(Mandatory = $true)]
    [string] $DockerHubUser,
    [string] $Tag = (Get-Date -Format "yyyy-MM-dd"),
    [string] $ImageName = "friendbot"
)

$ErrorActionPreference = "Stop"
# PSScriptRoot = .../fbot/scripts -> repo root is parent
$repoRoot = Split-Path $PSScriptRoot -Parent
Set-Location $repoRoot

$fullImage = "${DockerHubUser}/${ImageName}:${Tag}"
Write-Host "Building $ImageName ..."
docker build -t $ImageName .
Write-Host "Tagging $fullImage ..."
docker tag "${ImageName}:latest" $fullImage
Write-Host "Pushing $fullImage ..."
docker push $fullImage
Write-Host "Done. Use this image in Azure: $fullImage"
