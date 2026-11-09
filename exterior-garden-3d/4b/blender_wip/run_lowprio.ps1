# Run ONE Blender job at IDLE priority with 2 threads (shared machine).
# Usage (Git Bash):  BLARGS='-P build_scene.py -- grime C:/.../x.blend' powershell -ExecutionPolicy Bypass -File run_lowprio.ps1 C:/.../job.log
param([string]$Log)
$B = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
$argline = '-b --factory-startup -t 2 ' + $env:BLARGS
$p = Start-Process -FilePath $B -ArgumentList $argline -PassThru -NoNewWindow -RedirectStandardOutput $Log -RedirectStandardError ($Log + '.err')
try { $p.PriorityClass = 'Idle' } catch {}
$p.WaitForExit()
exit $p.ExitCode
