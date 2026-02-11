# Set sleep (standby) to Never on AC and DC
cmd /c "powercfg /change standby-timeout-ac 0 && powercfg /change standby-timeout-dc 0" | Out-Null
Write-Output "Sleep set to Never (AC + battery)."
