# Separate live authorization is required. Propagate the Python status unchanged.
param(
    [Parameter(Mandatory=$true)][string]$Manifest,
    [Parameter(Mandatory=$true)][string]$ManifestSha256,
    [Parameter(Mandatory=$true)][string]$Output,
    [switch]$ExecuteLive
)
$ErrorActionPreference = 'Stop'
if (-not $ExecuteLive) {
    throw 'Explicit -ExecuteLive and separate user authorization are required.'
}
& ./.venv/Scripts/python.exe -B -m tools.validation.preference_gate_smoke `
    --manifest $Manifest --manifest-sha256 $ManifestSha256 --output $Output --execute-live
$smokeExitCode = $LASTEXITCODE
exit $smokeExitCode
