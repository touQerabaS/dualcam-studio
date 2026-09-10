$ErrorActionPreference = 'Stop'
$decoderPath = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'dist-preview\DualCam Studio\_internal\preview-worker\PreviewDecoder.exe'))
if (-not (Test-Path -LiteralPath $decoderPath -PathType Leaf)) { throw 'Build the complete preview app before allowing its receiver.' }
$ruleName = 'DualCam-GoPro-Preview-8554'
$existingRule = Get-NetFirewallRule -Name $ruleName -ErrorAction SilentlyContinue
if ($existingRule) {
    $existingProgram = ($existingRule | Get-NetFirewallApplicationFilter).Program
    if ($existingProgram -ne $decoderPath) { throw 'A different app already owns this firewall rule name.' }
    $existingRule | Remove-NetFirewallRule -ErrorAction Stop
}
New-NetFirewallRule -Name $ruleName -DisplayName 'DualCam: GoPro preview only' -Direction Inbound -Action Allow -Enabled True -Profile Any -Program $decoderPath -Protocol UDP -LocalPort 8554 -RemoteAddress 10.5.5.9 -ErrorAction Stop | Out-Null
# Windows creates explicit block rules when its first-run network prompt is dismissed.
# Disable only this exact receiver's UDP block; default inbound filtering remains on.
$changedRules = @()
Get-NetFirewallRule -Direction Inbound -Action Block -Enabled True | ForEach-Object {
    $candidate = $_
    $application = $candidate | Get-NetFirewallApplicationFilter
    if ($application.Program -eq $decoderPath) {
        $portFilter = $candidate | Get-NetFirewallPortFilter
        if ($portFilter.Protocol -eq 'UDP' -or $portFilter.Protocol -eq 17) {
            $candidate | Disable-NetFirewallRule -ErrorAction Stop
            $changedRules += $candidate.Name
        }
    }
}
[pscustomobject]@{ AllowedProgram = $decoderPath; RemoteAddress = '10.5.5.9'; UdpPort = 8554; DisabledConflictingRules = $changedRules } | ConvertTo-Json
