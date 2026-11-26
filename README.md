# Software Factory

作者：Johnny Liu（[@johnnyliu365-sys](https://github.com/johnnyliu365-sys)）。授權：Apache License 2.0，見 [LICENSE](LICENSE) 與 [NOTICE](NOTICE)。

## 1. Software Factory 是什麼、給誰用

Software Factory 是一個用 AI agent 做軟體的受治理控制平面：需求、規格、票、實作、獨立審查與整合各有固定的關卡，每一步由 gate script 讀取專案裡的狀態檔後決定，而不是由哪個 agent 憑記憶決定。

它目前給用 Claude Code 或 Codex 做專案的個人與小團隊。從 1.0 起，它的目標對象是企業。

## 2. 它會做什麼、不會做什麼

**它只讀寫你的專案裡的檔案，不把 repository 的內容交給別的服務。** 狀態在檔案裡：票、receipt 與 integration queue。Gate script 在你的電腦上讀這些檔案、印出下一步能做什麼；把 plugin 指向一個 repository，不等於把那個 repository 的內容交給它。

**它是外部控制平面，不是專案的依賴。** 它引導專案自己擁有的工作，但不會成為那個專案的 runtime、CI、hook、import、submodule 或 symlink 依賴。專案自己的 AGENTS.md 與治理檔優先於這個 plugin 的流程。

**派工走同一個 session 的原生委派。** 當票已經被核准、worktree 與 branch 已由審閱者建立，當前 session 的審閱者才用 Codex 原生的 collaboration.spawn_agent 建立唯一的、綁定這張票的實作者，並用 wait_agent 等待完成，等待期間不做 activity 或 status 輪詢。回傳後由審閱者做 review、反向突變與既有的 gate。model 與 effort 只從票與 profile 讀取。若原生委派或所選 profile 的能力不存在，只回傳 HALT / CODEX_NATIVE_DELEGATION_UNAVAILABLE，不得由審閱者代為實作，也不得改走另一條派工路徑。

**沒有任何自動喚醒。** 這個版本沒有 runner、訂閱或喚醒能力；交接已經 commit，但沒有任何自動化被啟動，所以要由 owner 通知審閱者。

**交付階段停在 POC**，直到被核准的產出與變更紀錄另行說明。MVP 與 COMMERCIAL 是 profile 控制的階段，兩者都不是 plugin 可以自己從「進度看起來不錯」推斷出來的目標。

## 3. 安裝：Claude Code

先確認電腦有 Git 與 Claude Code。依序執行這五個指令。前兩個安裝，第三個更新，第四個移除 plugin，第五個移除 marketplace。

```bash
claude plugin marketplace add https://raw.githubusercontent.com/johnnyliu365-sys/software-factory-plugin/marketplace/.claude-plugin/marketplace.json
```

```bash
claude plugin install software-factory@software-factory --scope user
```

```bash
claude plugin update software-factory@software-factory --scope user
```

```bash
claude plugin uninstall software-factory@software-factory --scope user
```

```bash
claude plugin marketplace remove software-factory
```

安裝完成後，重新開啟 Claude Code session，或輸入：

```text
/reload-plugins
```

## 4. 安裝：Codex

1. 執行 codex --version，確認版本。需要有 plugin add 這個指令：0.167.0-alpha.3.2 有，0.130.0-alpha.5 只列出 plugin marketplace。

```bash
codex --version
```

2. 加入 marketplace：

```bash
codex plugin marketplace add johnnyliu365-sys/software-factory-plugin --ref marketplace
```

3. 安裝 plugin：

```bash
codex plugin add software-factory@software-factory --json
```

4. 用下面的指令檢查版本。清單裡 software-factory@software-factory 這一筆的 version 應為 0.5.0，installed 與 enabled 都應為 true。

```bash
codex plugin list --marketplace software-factory --json
```

5. 要移除時，先移除 plugin，再移除 marketplace：

```bash
codex plugin remove software-factory@software-factory --json
```

```bash
codex plugin marketplace remove software-factory --json
```

## 5. 從舊版 johnny-ai-skill 換過來

舊版的 plugin id 是 johnny-ai-skill@johnny-ai-skill。先用各 host 自己的 remove 指令移除舊版，再照第 3 與第 4 節安裝新版。

新舊兩版同時裝著時，agent 可能照舊版的規則做事。新版開工的第一步會檢查這件事：看到舊版還在，就停下來請你先移除舊版，移除後再開一個新的 session。

Claude Code：

```bash
claude plugin uninstall johnny-ai-skill@johnny-ai-skill --scope user
```

```bash
claude plugin marketplace remove johnny-ai-skill
```

Codex：

```bash
codex plugin remove johnny-ai-skill@johnny-ai-skill --json
```

```bash
codex plugin marketplace remove johnny-ai-skill --json
```

在 Claude Code 2.1.332 上，用 uninstall 移除插件後，Claude Code 會在它自己的設定裡留下一筆「已拒絕」這個插件的紀錄；這筆紀錄沒有擋住之後明確的安裝。如果某個專案要求安裝 Software Factory 卻沒有跳出提示，直接執行第 3 節的安裝指令即可。

專案裡從早期版本複製過去的 AGENTS.md 與 Workflow.md，要換成 0.5.0 的版本。

## 6. 舊版 Level 2 runtime 的移除

0.4.x 另有一個 Level 2 runtime，安裝在 %LOCALAPPDATA%\JohnnyRouter。0.5.0 不再提供它，也沒有任何 Level 2 的安裝步驟。已經裝過的人，用它自己的 uninstall 移除：

```powershell
powershell -ExecutionPolicy Bypass -File "$env:LOCALAPPDATA\JohnnyRouter\launcher\johnny-router.ps1" uninstall
```

uninstall 移除什麼、留下什麼：

- 移除：根目錄下的 plugin、venv、launcher、runtime、queue 與 telemetry 這幾個資料夾，條件是每一個都帶有安裝時寫下的 .johnny-owned 標記，而且標記與帳本相符。全部移除後，再清掉安裝日誌與已空的根目錄。這個行為寫在 live_uninstall_composition.py；johnny-router.ps1 只負責把 uninstall 轉交給它。
- 留下：沒有 .johnny-owned 標記的資料夾，uninstall 視為不是它的，會停下並保留帳本；根目錄裡你自己放進去的任何東西，所以根目錄不空就不會被刪；下載來的安裝檔與 zip，它們在下載資料夾，不在根目錄；以及 Claude Code 與 Codex 裡的 plugin，那要用第 5 節的指令移除。

什麼時候可以手動刪除資料夾 %LOCALAPPDATA%\JohnnyRouter：只在 uninstall 跑不起來的時候，例如安裝失敗之後，留下的 install-journal.jsonl 擋住了重新安裝。這時先確認那個資料夾是你自己的，再手動刪除整個資料夾。

## 7. 第一次使用

從一個專案的需求走到驗收，依序做：

1. 在要做的專案資料夾開啟 Claude Code 或 Codex。專案可以是新的，也可以是做到一半的。
2. 用一句話說出這個 session 的目標，然後執行接手指令：

```text
/johnny-project-takeover 我要做的目標
```

3. 它先讀專案自己的 AGENTS.md 與治理檔，再用 Workflow.md 找出目前在哪一個階段，只做那一個階段合法的下一步。
4. 需求寫成需求紀錄，經你確認；再由需求產生規格，規格拆成票。每張票有固定欄位與邊界。
5. 每張票交給一個實作者，在自己的 worktree 與 branch 裡做；實作者的 model 與 effort 由票與 profile 決定。
6. 實作完成後，由獨立的審閱者審查，並做反向突變；通過後才用整合 script 合併。
7. 全部票整合後，由你驗收。沒有通過的地方，回到需求或票，不是直接改產出。

要挑選可重複使用的模組時，執行：

```text
/apply-reusable-modules
```

## 8. 它怎麼運作

- 狀態在檔案裡：票、receipt 與 integration queue。換一個 session 或換一個 agent，從檔案接續，不靠對話記憶。
- Gate script 決定每一步：派工檢查、證據檢查、整合、用量報告都是 script，輸出就是結論；agent 不自己宣布通過。
- 審查是獨立的：審閱者不是實作者，也不看實作者對自己的評價；反向突變證明測試真的會變紅。

規則的來源是 AGENTS.md、Workflow.md、CodeReview.md 與 modules/spec/workflow-governance.md。

每次開新的 session，插件會用一個 SessionStart hook 告訴 agent 規則檔在哪裡、查本插件規則的唯讀查詢要先查流程索引，以及舊版 johnny-ai-skill 還裝著時要先停下來；在 Claude Code 終端機裡輸入 /hooks 可以看到它。

## 9. 路線

0.5.0（這一版），然後是 wave 4，然後是 beta（除了部署以外的每一項 1.0 能力，跑在測試者自己的電腦上），然後是給企業的 1.0（自行架設，用 Docker Compose），之後再做 SaaS。

## 10. 作者與授權

- 作者：Johnny Liu（GitHub [@johnnyliu365-sys](https://github.com/johnnyliu365-sys)）
- 版本庫：<https://github.com/johnnyliu365-sys/software-factory-plugin>
- 授權：Apache License 2.0，全文見 [LICENSE](LICENSE)；著作權與歸屬聲明見 [NOTICE](NOTICE)。再散布或衍生作品須依 Apache 2.0 第 4(d) 條保留 NOTICE 的歸屬內容。
