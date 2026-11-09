# Low-priority, 2-thread Blender launcher: waits while 2+ blender.exe are running (another agent may be rendering).
param([string]$Script, [string]$Log, [string]$Extra = "")
$b = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
while (@(Get-Process blender -ErrorAction SilentlyContinue).Count -ge 2) { Start-Sleep -Seconds 30 }
$args2 = @("-b", "--factory-startup", "-t", "2", "-P", $Script, "--") + ($Extra -split " " | Where-Object { $_ })
$p = Start-Process -FilePath $b -ArgumentList $args2 -RedirectStandardOutput $Log -RedirectStandardError "$Log.err" -PassThru -NoNewWindow
try { $p.PriorityClass = 'Idle' } catch {}
$p.WaitForExit()
"EXIT $($p.ExitCode)"
