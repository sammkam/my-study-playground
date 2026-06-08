# [プラットフォーム名: Tryhackme Blizzard  [HS-SQL-01] Writeup

## 📌 概要 (Scenario & Info)
- **難易度:** `[medium]`
- **カテゴリ:** `[Windows]`
- **シナリオ:** 
```
A critical alert was detected on one of Health Sphere Solutions' database servers, highlighting the company's early challenges in securing its network. 
Since the security controls are still being established, alerts have only come from servers, and only network-level events are being audited, it's essential to manually investigate both servers and workstations to connect the dots and fully understand the incident.
```

| Alert Timestamp	| Alert Name	|Alert Description | Host Name |
| --- | --- | --- | --- |
| 03/24/2024 19:55:29	| POTENTIAL_DATA_EXFIL_DETECTED	| A high bandwidth outbound connection from HS-SQL-01 has been detected. |	HS-SQL-01 |

- **使用ツール/ガイド:
```
In addition, your team has prepared the following items to assist your investigation:

Standalone tools in the C:\Tools directory.
Tools prepared as desktop shortcuts.
Investigation Guide

As part of your playbook, you are tasked to determine the following information during the investigation:

Determine any unusual login attempts to the database server. >> イベントビューア
Note any suspicious binaries executed within the server. >> イベントビューア, レジストリ、Amchace
Look for typical persistence mechanisms deployed in the server. >> イベントビューア, レジストリ、タスクスケジューラ
The IT team has also shared that the infected database server is set up for internal access only and is not yet linked to other systems, as it is still in the setup phase. This information could help narrow down potential sources of the threat.
```

---

## ⏱️ タイムライン (Incident Timeline)
※調査を進めながら、判明した攻撃の時系列を埋めていく（DFIRで最も重要な要素）。

| 日時 (UTC / JST) | イベント内容 (何が起きたか) | 関連アーティファクト・証拠 |
| :--- | :--- | :--- |
| `[2024-03-24 19:38:48]` | 初期アクセス (Initial Access) | `[RDPアクセス(dbadmin)]` |
| `[YYYY/MM/DD HH:MM:SS]` | ペイロードのダウンロード | `[例: Sysmon Event ID 1]` |
| `[YYYY/MM/DD HH:MM:SS]` | 横展開・権限昇格 | `[例: Security.evtx (ID 4624)]` |
| `[YYYY/MM/DD HH:MM:SS]` | 横展開・権限昇格 | `[例: Security.evtx (ID 4624)]` |
| `[YYYY/MM/DD HH:MM:SS]` | 横展開・権限昇格 | `[例: Security.evtx (ID 4624)]` |
| `[2024-03-24 19:55:29]` | POTENTIAL_DATA_EXFIL_DETECTED | `[例: Security.evtx (ID 4624)]` |


---

## 🛠️ 分析したアーティファクト (Artifacts Analyzed)
提供されたファイル群の中で、調査のキーになったものを記録する。
- **`[C:\Windows\System32\winevt\Logs\Microsoft-Windows-TerminalServices-RemoteConnectionManager%4Operational.evtx]`:** `[ログイン履歴の確認]`
- **`[ファイル名 / ログの名前]`:** `[例: 実行されたコマンドライン引数の確認]`

---

## 📝 設問と回答 (Tasks & Answers)
CTFのタスクごとに、どのように答えを導き出したか（思考プロセスとコマンド）を記録する。

### Task X: [When did the attacker access this machine from another internal machine? (format: MM/DD/YYYY HH:MM:SS)]
- **回答:** `[03/24/2024 19:38:48]`
- **アプローチ・証拠:**
  - `[Microsoft-Windows-TerminalServices-RemoteConnectionManager%4Operational.evtx]`
  - `[上記よりアクセスのあるユーザ(\dbadmin)の1149ログを確認。]`
---

### Task X: [What is the full file path of the binary used by the attacker to exfiltrate data?]
- **回答:** `[回答]`
- **アプローチ・証拠:**
  - `[どのように特定したか]`

---


### Task X: [What email is used by the attacker to exfiltrate sensitive data?]
- **回答:** `[回答]`
- **アプローチ・証拠:**
  - `[どのように特定したか]`

---


### Task X: [Where did the attacker store a persistent implant in the registry? Provide the registry value name.]
- **回答:** `[回答]`
- **アプローチ・証拠:**
  - `[どのように特定したか]`

---


### Task X: [Aside from the registry implant, another persistent implant is stored within the machine. When did the attacker implant the alternative backdoor? (format: MM/DD/YYYY HH:MM:SS)]
- **回答:** `[回答]`
- **アプローチ・証拠:**
  - `[どのように特定したか]`

---

### Task X: [設問文をここに書く]
- **回答:** `[回答]`
- **アプローチ・証拠:**
  - `[どのように特定したか]`

---


### Task X: [設問文をここに書く]
- **回答:** `[回答]`
- **アプローチ・証拠:**
  - `[どのように特定したか]`

---


### Task X: [設問文をここに書く]
- **回答:** `[回答]`
- **アプローチ・証拠:**
  - `[どのように特定したか]`

---

### Task X: [設問文をここに書く]
- **回答:** `[回答]`
- **アプローチ・証拠:**
  - `[どのように特定したか]`

---

### Task X: [設問文をここに書く]
- **回答:** `[回答]`
- **アプローチ・証拠:**
  - `[どのように特定したか]`

---

## 🎯 まとめ・防衛側の教訓 (Lessons Learned & MITRE ATT&CK)
攻撃の全体像と、現場で活かせる防御策をまとめる。

- **特定した攻撃手法 (MITRE ATT&CK):**
  - `[例: Initial Access: T1190 (Exploit Public-Facing Application)]`
  - `[例: Execution: T1059.001 (PowerShell)]`
- **検知・防御策 (もし実際の現場だったらどう防ぐか):**
  - `[例: Webアプリケーションの脆弱性パッチを適用する。]`
  - `[例: Tempフォルダからの未署名バイナリの実行を制限する。]`