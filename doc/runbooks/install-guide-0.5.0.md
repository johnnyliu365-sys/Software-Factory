# Software Factory 0.5.0 安裝與排錯指南

給第一次安裝 Software Factory 的人。照順序做，每一步都有「怎麼確認成功」。遇到問題時，先看第 5 節的對照表。

- 版本：0.5.0
- 發佈 commit：`<發佈後填入>`
- 插件包 repo：`johnnyliu365-sys/software-factory-plugin`
- 這份指南不在插件包裡。插件包自己的 README 是正式說明；兩邊不一致時，以插件包的 README 為準，並請回報給作者。

## 1. 開始前

| 項目 | 要求 | 怎麼確認 |
| --- | --- | --- |
| Git | 已安裝。Windows 請裝 Git for Windows（含 Git Bash） | `git --version` |
| Claude Code（要用 Claude 時） | 已安裝並登入。作者測試的版本是 2.1.332 | `claude --version` |
| Codex（要用 Codex 時） | 已安裝並登入，而且有 `codex plugin add` 指令。作者測試的版本是 0.166.0 與 0.172.0 | `codex --version` |
| 網路 | 能連到 github.com 與 raw.githubusercontent.com | 用瀏覽器開這兩個網址 |
| 舊版 | 如果裝過 johnny-ai-skill（0.4.x），先照第 4 節移除 | 第 4 節的檢查指令 |

**Windows 的一個重點：** 終端機面板裡每個「Run」按鈕都在新的 shell 執行，前一行的 `cd` 不會帶到下一行。需要在某個資料夾裡執行的指令，請把 `cd` 和指令寫在同一行，用 `;` 隔開。

## 2. 安裝：Claude Code

依序執行，每行一個指令：

```bash
claude plugin marketplace add https://raw.githubusercontent.com/johnnyliu365-sys/software-factory-plugin/marketplace/.claude-plugin/marketplace.json
```

```bash
claude plugin install software-factory@software-factory --scope user
```

**確認成功**

1. 執行下面的指令。清單裡要有 `software-factory@software-factory`，版本 0.5.0，狀態 enabled。

   ```bash
   claude plugin list
   ```

2. 開一個**新的** session（或輸入 `/reload-plugins`），在任一專案裡問：「P0 權限規則是什麼？」
   - 正常：它讀了插件的 `AGENTS.md`，回答 P0 的內容，並註明檔案、章節與版本。過程中沒有用 grep 或全文搜尋找規則。
   - 不正常：它用搜尋找規則，或說找不到。看第 5 節 C1。
3. 選做：在 Claude Code **終端機**裡輸入 `/hooks`，應該看得到 Software Factory 的 SessionStart hook。桌面 app 沒有 `/hooks`。

## 3. 安裝：Codex

依序執行，每行一個指令：

```bash
codex plugin marketplace add johnnyliu365-sys/software-factory-plugin --ref marketplace
```

```bash
codex plugin add software-factory@software-factory --json
```

**必做：在終端機信任 hook 一次。** 安裝或每次更新之後，在終端機進到你平常用 Codex 的專案資料夾，執行 codex（Windows PowerShell 範例，資料夾換成你的）：

```powershell
cd C:\path\to\your-project; codex
```

它詢問是否信任 Software Factory 的 hook 時選信任，然後輸入 `/quit` 離開。Codex 桌面 app 不會問這個問題；沒有在終端機信任過，hook 就不會生效。

**確認成功**

1. 執行下面的指令。`software-factory@software-factory` 這一筆的 version 是 0.5.0，installed 與 enabled 都是 true。

   ```bash
   codex plugin list --marketplace software-factory --json
   ```

2. 確認 hook 真的有跑（PowerShell，在同一個專案資料夾；會用掉一點點用量）：

   ```powershell
   codex exec --skip-git-repo-check -s read-only "Answer exactly OK." 2>&1 | Select-String "hook:"
   ```

   - 正常：出現 `hook: SessionStart Completed`。
   - 不正常：出現 `hook: SessionStart Failed`。看第 5 節 X1。
3. 開一個新的 Codex 對話（終端機或桌面 app 都可以），問：「P0 權限規則是什麼？」
   - 正常：它讀了插件的 `AGENTS.md` 後回答。Codex 可能先查一下它自己的記憶檔，這是 Codex 內建的行為，不算錯。
   - 不正常：它在專案裡用 `rg` 或其他搜尋找規則。看第 5 節 X1。

## 4. 從舊版 johnny-ai-skill 換過來

新舊兩版同時裝著時，新版一開工就會停下來，請你先移除舊版。

**檢查有沒有舊版**

```bash
claude plugin list
```

```bash
codex plugin list --json
```

清單裡有 `johnny-ai-skill@johnny-ai-skill`，就是還裝著舊版。

**移除（Claude Code）**：先看清單上它的 Scope 是 user、project 還是 local。

- user 範圍，直接執行：

  ```bash
  claude plugin uninstall johnny-ai-skill@johnny-ai-skill --scope user
  ```

  ```bash
  claude plugin marketplace remove johnny-ai-skill
  ```

- project 或 local 範圍：到當初安裝的那個專案資料夾裡執行，並把 `--scope user` 換成 `--scope project` 或 `--scope local`。Windows PowerShell 範例：

  ```powershell
  cd C:\path\to\that-project; claude plugin uninstall johnny-ai-skill@johnny-ai-skill --scope local
  ```

**移除（Codex）**

```bash
codex plugin remove johnny-ai-skill@johnny-ai-skill --json
```

```bash
codex plugin marketplace remove johnny-ai-skill --json
```

第二個指令如果回 `marketplace johnny-ai-skill is not configured or installed`，代表當初沒有登記 marketplace，不影響結果。用 `codex plugin list --json` 確認舊版已經不在清單裡即可。

移除後，開一個**新的** session 再開始工作。

## 5. 排錯對照表

先找你看到的現象，照「處理」做；做完再回到第 2 或第 3 節的「確認成功」。

| 編號 | 現象 | 原因 | 處理 |
| --- | --- | --- | --- |
| A1 | agent 一開場就說「舊版 johnny-ai-skill 還裝著」，然後停下來 | 新舊兩版同時裝著，這是設計好的保護 | 照第 4 節移除舊版，開新的 session |
| A2 | 照指示移除舊版，清單裡還是有它 | 舊版裝在 project 或 local 範圍，`--scope user` 移不掉 | 第 4 節的 project／local 做法：到那個專案資料夾裡、換 `--scope` |
| A3 | Codex 移除 marketplace 時出現 `not configured or installed` | 那份舊版當初沒有登記 marketplace | 不影響；用 `codex plugin list --json` 確認舊版已不在 |
| C1 | Claude 查規則時用搜尋，或回答時沒提到插件的 `AGENTS.md` | session 是在安裝前開的，或插件沒啟用 | `claude plugin list` 確認 enabled；開新的 session 再問一次 |
| C2 | 指定專案時沒有跳出安裝提示 | Claude Code 移除插件後會留下一筆「已拒絕」紀錄 | 直接執行第 2 節的 install 指令；這筆紀錄不會擋明確的安裝 |
| C3 | 插件裝到了別的專案，或在錯的資料夾裡生效 | `cd` 和安裝指令分在兩個 Run 按鈕執行，`cd` 沒帶過去 | 把 `cd` 和指令寫在同一行；用 `claude plugin list` 看 Scope 和專案 |
| X1 | Codex 查規則時用 `rg` 搜尋；或 `codex exec` 顯示 `hook: SessionStart Failed` | hook 還沒在終端機信任過，或插件更新後要重新信任；桌面 app 不會問 | 照第 3 節「必做」在終端機執行一次 codex 並選信任，再做第 3 節確認 2 |
| X2 | `codex plugin add` 不存在 | Codex 版本太舊 | 更新 Codex（`codex update`），再確認 `codex --version` |
| U1 | 更新後行為沒變，還是舊的說明 | 版本號相同時，主機沿用舊的快取 | 先移除插件；再刪除快取資料夾（Claude：`%USERPROFILE%\.claude\plugins\cache\software-factory`，Codex：`%USERPROFILE%\.codex\plugins\cache\software-factory`）；最後重新安裝。Codex 裝好後要再在終端機信任一次 |
| W1 | Windows 上 hook 的訊息沒有出現，且電腦沒有 Git Bash | 沒有 Git Bash 時，Claude Code 會改用 Windows PowerShell 執行 hook，這是正常的 | 先照 C1 確認；仍不行再回報 |
| W2 | 手動輸入 `bash` 進到的是 Linux 環境 | Windows 上直接打 `bash` 會開到 WSL，不是 Git Bash | 用 Git Bash 本身，或用 PowerShell 照本指南的指令操作 |
| N1 | `marketplace add` 失敗、逾時或 404 | 網路連不到 GitHub，或 repo 名稱打錯 | 確認第 1 節的網路項目；指令整行複製，不要手打 |

## 6. 移除 Software Factory

Claude Code：

```bash
claude plugin uninstall software-factory@software-factory --scope user
```

```bash
claude plugin marketplace remove software-factory
```

Codex：

```bash
codex plugin remove software-factory@software-factory --json
```

```bash
codex plugin marketplace remove software-factory --json
```

## 7. 回報問題時請附上

- 作業系統與版本，例如 Windows 11。
- `claude --version`、`codex --version` 的輸出。
- `claude plugin list` 或 `codex plugin list --json` 中 software-factory 那一段的輸出。
- 第 5 節對照表的編號（如果有對到），以及你做了哪些處理。
- 畫面截圖：問「P0 權限規則是什麼？」時，把 agent 讀檔、執行指令的那一段展開。

**請不要附上**：密碼、API key、token、`auth.json` 或任何登入資料，也不要附上你自己專案的機密內容。
