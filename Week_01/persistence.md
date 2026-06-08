# [20260601] スタートアップとレジストリ サービス、スケジュールタスク

## 概要
- windowsのスタートアップは execution (ATT&CK ID: TA002) と persistence (ATT&CK ID: TA003)でよく使われる。
- 攻撃者は侵害したシステムをスケジュールタスクなどを利用してバックドアを残し、永続性の確保などをおこなう。
- SysinternalのAutorunsc等で自動起動されるすべてのプロセス(レジストリ、サービス、タスクなどが見れる。)
## チートシート

### [スタートアッププログラム、コマンドの確認]

```powershell
Get-CimInstance Win32_StartupCommand | Select-Object Name, command, Location, User | fl | tee autorun-cmds.txt
```
#### 見るポイント: [不審な名前、ファイルパス、ユーザ]

### [レジストリの調査　logon関連]
- HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\Userinit
    Windowsへのサインイン（ログオン）時にユーザーの初期環境を構築・起動するために使用される
- HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\Shell 
    Windowsにサインイン（ログオン）した直後に最初に起動するプログラム（シェル）を指定するレジストリ設定
```powershell
$winlogonPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"; "Userinit: $((Get-ItemProperty -Path $winlogonPath -Name 'Userinit').Userinit)"; "Shell: $((Get-ItemProperty -Path $winlogonPath -Name 'Shell').Shell)"
```
#### 見るポイント: [userinit.exe以外の不審なものがないか。]


### [動いているサービスの取得]

```powershell
 "Running Services:"; Get-CimInstance -ClassName Win32_Service | Where-Object { $_.State -eq "Running" } | Select-Object Name, DisplayName, State, StartMode, PathName, ProcessId | ft -AutoSize | tee services-active.txt
```
#### 見るポイント: [名前、説明、実行パスに不審点がないか]


### [動いていないサービス]

```powershell
"Non-Running Services:"; Get-CimInstance -ClassName Win32_Service | Where-Object { $_.State -ne "Running" } | Select-Object @{Name='Name'; Expression={if ($_.Name.Length -gt 22) { "$($_.Name.Substring(0,19))..." } else { $_.Name }}}, @{Name='DisplayName'; Expression={if ($_.DisplayName.Length -gt 45) { "$($_.DisplayName.Substring(0,42))..." } else { $_.DisplayName }}}, State, StartMode, PathName, ProcessId | Format-Table -AutoSize | Tee-Object services-idle.txt      
```
#### 見るポイント: [動いていないといけないセキュリティサービスなどが止まっていないか？]
impairing defences (ATT&CK ID: T1562)


### [アクティブなスケジュールタスク]

```powershell
$tasks = Get-CimInstance -Namespace "Root/Microsoft/Windows/TaskScheduler" -ClassName MSFT_ScheduledTask; if ($tasks.Count -eq 0) { Write-Host "No scheduled tasks found."; exit } else { Write-Host "$($tasks.Count) scheduled tasks found." }; $results = @(); foreach ($task in $tasks) { foreach ($action in $task.Actions) { if ($action.PSObject.TypeNames[0] -eq 'Microsoft.Management.Infrastructure.CimInstance#Root/Microsoft/Windows/TaskScheduler/MSFT_TaskExecAction') { $results += [PSCustomObject]@{ TaskPath = $task.TaskPath.Substring(0, [Math]::Min(50, $task.TaskPath.Length)); TaskName = $task.TaskName.Substring(0, [Math]::Min(50, $task.TaskName.Length)); State = $task.State; Author = $task.Principal.UserId; Execute = $action.Execute } } } }; if ($results.Count -eq 0) { Write-Host "No tasks with 'MSFT_TaskExecAction' actions found." } else { $results | Format-Table -AutoSize | tee scheduled-tasks.txt }
```
#### 見るポイント: []


## メモ・次回TODO
[ ]