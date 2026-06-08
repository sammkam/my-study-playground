# [プラットフォーム名: HTB Sherlocks等] [マシンの名前] Writeup

## 📌 概要 (Scenario & Info)
- **難易度:** `[Easy / Medium / Hard]`
- **カテゴリ:** `[例: Windows / Linux / Network / Memory / Malware]`
- **シナリオ:** `[例: Webサーバーが侵害され、ランサムウェアが展開された。提供されたアーティファクトから原因を特定せよ。]`
- **使用ツール:** `[例: Event Viewer, Chainsaw, Wireshark, Registry Explorer, KAPE]`

---

## ⏱️ タイムライン (Incident Timeline)
※調査を進めながら、判明した攻撃の時系列を埋めていく（DFIRで最も重要な要素）。

| 日時 (UTC / JST) | イベント内容 (何が起きたか) | 関連アーティファクト・証拠 |
| :--- | :--- | :--- |
| `[YYYY/MM/DD HH:MM:SS]` | 初期アクセス (Initial Access) | `[例: IISアクセスログ]` |
| `[YYYY/MM/DD HH:MM:SS]` | ペイロードのダウンロード | `[例: Sysmon Event ID 1]` |
| `[YYYY/MM/DD HH:MM:SS]` | 横展開・権限昇格 | `[例: Security.evtx (ID 4624)]` |

---

## 🛠️ 分析したアーティファクト (Artifacts Analyzed)
提供されたファイル群の中で、調査のキーになったものを記録する。
- **`[ファイル名 / ログの名前]`:** `[何を見るために使ったか。例: ログイン履歴の確認]`
- **`[ファイル名 / ログの名前]`:** `[例: 実行されたコマンドライン引数の確認]`

---

## 📝 設問と回答 (Tasks & Answers)
CTFのタスクごとに、どのように答えを導き出したか（思考プロセスとコマンド）を記録する。

### Task 1: 攻撃者が最初に侵入に成功した時刻は？
- **回答:** `[YYYY-MM-DD HH:MM:SS]`
- **アプローチ・証拠:**
  - IISのアクセスログ (`u_exYYMMDD.log`) を確認。
  - 不審なPOSTリクエストがあり、ステータスコード200（成功）が返っている時間を特定。

### Task 2: 攻撃者がドロップしたマルウェアのハッシュ値は？
- **回答:** `[SHA256ハッシュなど]`
- **アプローチ・証拠:**
  - `Sysmon` ログの Event ID 1 (プロセス作成) をフィルター。
  - `Temp` フォルダで実行された `payload.exe` のハッシュ値を抽出。

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