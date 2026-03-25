param(
  [string]$ProjectRoot = "D:\Develop-project\agentLearning\pkb-core",
  [string]$StartTimeWorkday = "09:00",
  [string]$StartTimeNightly = "23:30"
)

$taskCommand = "powershell -NoProfile -ExecutionPolicy Bypass -Command `"cd '$ProjectRoot'; .\scripts\run_pipeline.ps1`""

schtasks /Create /TN "PKB_Pipeline_Every2Hours" /SC HOURLY /MO 2 /D MON,TUE,WED,THU,FRI /TR $taskCommand /ST $StartTimeWorkday /F
schtasks /Create /TN "PKB_Pipeline_Nightly" /SC DAILY /TR $taskCommand /ST $StartTimeNightly /F

Write-Host "Task Scheduler entries created:"
Write-Host "- PKB_Pipeline_Every2Hours"
Write-Host "- PKB_Pipeline_Nightly"
