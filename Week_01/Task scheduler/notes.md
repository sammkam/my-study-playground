# Notes

## 概要
スケジュールタスクはシステムのスタートアップ時や指定された時間などで実行され、攻撃者に永続性の確保などに使われる。
また、特定のアカウント配下での実行を指定することで権限昇格などで利用されることもある。

## ATT&CK
- T1053.005

## 何のために使われるか
- Execution, Persistence, Privilege Escalation

## 仕組み
1. タスクが作成される
2. トリガーが設定される（logon / time / startup）
3. 指定コマンドが実行される
4. Task Schedulerサービスが管理するため正規プロセスに紛れる

## 攻撃者による作成方法
- schtasks.exe /Task scheduler GUI
- powershell (Set-ScheduledTask) 別途アクション、トリガーの設定が必要
```powershell
# タスクのアクション（実行するスクリプト）
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File C:\Scripts\backup.ps1"
# タスクのトリガー（毎日AM3:00に実行）
$trigger = New-ScheduledTaskTrigger -Daily -At 3am
# タスクを作成して登録
Register-ScheduledTask -TaskName "DailyBackup" -Action $action -Trigger $trigger -Description "毎日3時にバックアップを実行"
```
-XMLファイルのインポートなど。(タスクは基本的にXMLで管理されるため: C:\Windows\System32\Tasks)
```xml
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2025-01-12T13:01:28.2421594</Date>
    <Author>SAM2025\samka</Author>
    <URI>\python news</URI>
  </RegistrationInfo>
  <Principals>
    <Principal id="Author">
      <UserId>S-1-5-21-2168476006-2914628034-xxxxxxxx-1001</UserId>
      <LogonType>S4U</LogonType>
    </Principal>
  </Principals>
  <Settings>
    <DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
    <Enabled>false</Enabled>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
  </Settings>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2025-01-13T08:00:00</StartBoundary>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Actions Context="Author">
    <Exec>
      <Command>C:\Users\x\AppData\Local\Programs\Python\Python313\python.exe</Command>
      <Arguments>C:\Users\x\Desktop\workspace\python\secnews\index.py</Arguments>
    </Exec>
  </Actions>
</Task>
```
- *SchRpcRegisterTask* 実行したいコマンドを含む新しいタスクをリモートで登録することもできる impaketなどやC#のNew-Objectを利用。

## 重要ポイント
- 見逃しやすい点 :"hidden"スケジュールタスクも作れる。これはマニュアルクエリなどで確認できないものもある。(schtasks /query)

## 確認ポイント

### イベントログ
#### security
- 4698 : タスクの作成。
    名前、実行プロセスを確認
    Task Authorを確認し、アドミン権限を持っているユーザやシステム(AUTHORITY/SYSTEM)かなどを見る
- 4699: タスク削除
- 4702 : 既存のタスクの変更
#### TaskScheduler/Operational
-  106 : タスク登録イベント
    タスク名が確認できる
- 140 : 既存のタスクの変更
- 141 : タスク削除
-  201 : タスクの実行
    実行パスの確認ができる。

### 調査の流れ
1. 4698でタスク作成を確認
2. タスク名と実行コマンドを取得
3. 201で実際に実行されたか確認
4. 実行ファイルのパスを確認
5. 作成ユーザと実行ユーザを確認
6. Sysmon Event ID 1でプロセス実行を追跡

#### memo
基本的にセキュリティログのほうが多くの情報を保持しているが、攻撃者によって削除されてしまっている場合などに
TaskScheduler/Operationalは有効。


### TODO:
- schetask の引数の理解
- powershellのタスク作成/削除
- Register-ScheduledTaskで検証する
- Event ID 4698を取得する
- Sysmon Event ID 1を確認する