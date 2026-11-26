# AI 協作入口與索引

> 本檔相當於書的前言與目錄：只定義啟動順序、P0 與索引。流程與路由以
> [Workflow.md](Workflow.md) 為準；Code Review 的入口、證據與結論以
> [CodeReview.md](CodeReview.md) 為準；專業方法由 Router 指定的
> [`johnny-project-takeover`](skills/johnny-project-takeover/SKILL.md) reference 定義。

<a id="startup-order"></a>

## 啟動順序

除下方唯讀查詢外，在讀取 target source、執行工具或寫入前：

1. 讀取 target project 自己的 `AGENTS.md` 與本次 authority。
2. 讀 [Workflow 流程圖](Workflow.md#workflow-flow) 定位目前 stage。
3. 讀 [Router 路由表](Workflow.md#workflow-router)，取得唯一 action、owner、必要
   artifact refs、skill reference、typed return 與 continuation。
4. 完整讀取被指定的 skill reference；不要載入完整 Workflow、全部 references、
   library 或聊天歷史。
5. 完成一個動作後把 typed event 寫進受據，由下一個閘門腳本讀取狀態檔判定（Revision 04）；不得自行選下一關。

<a id="read-only-lookup"></a>

唯讀查詢（只問某份文件的內容、某張票的狀態或某條規則的寫法，不要求改動）不走上面的啟動順序；target project 自己的治理檔另有規定時從其規定。P0 照常適用：不讀取或回覆 Secret、正式 Log，不讀 target repository 以外或其他 worktree 的檔案。使用者指名確切檔案時只讀該檔；否則從該類文件的索引一次解析一條路徑到確切的 leaf。本插件規則的查詢，使用者未指名確切檔案時，先讀本檔「流程索引」，取情境欄符合問題的一列（同時符合 P0 列與其他列時取 P0 列；其餘同時符合多列時，取表中較上面的一列），依該列解析到一份 leaf：第二欄連到本檔一節時即該節，否則為第三欄中含該規則的 reference；只讀含該規則的那一節（已安裝的插件版本），並註明檔案、章節與版本。定位只經索引與其連結，不以關鍵字搜尋（grep、全文搜尋）或逐檔瀏覽來找；索引沒有該規則的列時，照本段「找不到該類索引」那一句回答找不到並列出已查的路徑。不為定位而讀 Workflow 或 Router，不載入整棵樹，不寫受據，不執行閘門腳本、測試或其他程式。票的狀態以目前 checkout 已提交的 leaf 為準，不以索引列、其他 worktree 或未提交的檔案為準；回答附上 leaf 路徑與 commit；需要受據或佇列才能判定時照實說明，不推斷。找不到該類索引、索引有歧義、leaf 不存在或索引與 leaf 記載的 revision 不符時，回答找不到並列出已查的路徑，不掃描、不憑記憶補答、不進入 Wayfinder。查詢中發現需要改動時，回報後停下；只有使用者要求改動，才走上面的啟動順序。問下一步、能否派工、整合或核准，屬於推進流程，不是唯讀查詢。

狀態只保存 metadata（識別碼、revision、digest、repo 相對路徑）；pending implementation
dispatch 以票面狀態列（含派工檔 digest）表示，並由受據與精確 artifact references 綁定；整合佇列列
只承載整合候選（Revision 04 R4-1、R4-7）。

找不到、讀不到、版本不符或索引競爭時，在 mutation 前
`HALT / ROUTE_REFERENCE_INVALID`，不得憑記憶補規則。

<a id="p0-source-type"></a>

## P0：原始碼型別

所有正式原始碼必須以 C++ 概念可讀的強型別表達資料意義、nullability、輸入／
輸出與有限領域狀態。外部動態輸入在邊界驗證、正規化並轉成具名型別；不得把
`Any`、隱含 `any`、未驗證動態物件或字串慣例向內傳遞。使用語言可用的 strict
checker；ticket schema、preflight 與 TDD 由 Router 指向：

- [`specification-ticketing.md`](skills/johnny-project-takeover/references/specification-ticketing.md)
- [`implementation-tdd.md`](skills/johnny-project-takeover/references/implementation-tdd.md)

違反此 P0 不得 dispatch、commit、review approve 或交接。

<a id="p0-permissions"></a>

## P0：權限與所有權

- 插件治理文件與 skills 只存在插件版本庫／bundle／安裝快取，不複製到 target
  project；完整規則見 [治理文件歸屬](Workflow.md#governance-document-ownership)。
- SPEC、ticket、Context、進度、審閱、程式與測試屬 target project，必須
  target-owned、target-versioned。
- reviewer 是唯一 Agent-to-Agent orchestrator；implementation owner 不得控制
  其他 Agent。角色、task、worktree、receipt 與 correction 規則見
  [Implementation role boundary](Workflow.md#role-boundary)。
- Agent 建立 worktree 一律放在 repository root 底下的 `.worktrees/<ticket-id>`，
  不得開在 repository 的同層或任何外部路徑。Claude Code harness 自建的
  `.claude/worktrees/` 同屬受認可位置。兩者都已列入 `.gitignore`，
  經 junction 或 reparse point 到達的路徑一律拒絕。
- Agent 只能修改與提交自己的 worktree。不得接收、輸出或保存明文 Secret。
  Secret、正式 Log、Provider 與 external effect 的詳細規則見
  [security-boundary](skills/johnny-project-takeover/references/security-boundary.md)。
- 未核准、未提交、聊天宣稱、截圖或其他 worktree 的檔案不能作為 implementation
  authority、review evidence 或 merge source。

## 流程索引

| 情境 | Workflow 入口 | Router 指向的詳細 reference |
| --- | --- | --- |
| 唯讀查詢本身的規則（怎麼查、查不到時怎麼回答） | [唯讀查詢](#read-only-lookup) | 不適用：規則即本檔該節 |
| P0 原始碼型別（強型別、外部輸入、strict checker） | [P0：原始碼型別](#p0-source-type) | [specification-ticketing](skills/johnny-project-takeover/references/specification-ticketing.md) + [implementation-tdd](skills/johnny-project-takeover/references/implementation-tdd.md) |
| P0 權限與所有權（治理文件歸屬、角色、worktree、Secret） | [P0：權限與所有權](#p0-permissions) | [implementation-authority](skills/johnny-project-takeover/references/implementation-authority.md) + [security-boundary](skills/johnny-project-takeover/references/security-boundary.md) |
| 啟動順序（動手前的讀取順序） | [啟動順序](#startup-order) | 不適用：規則即本檔該節 |
| target project 正式來源的標準位置 | [Target project 正式來源](#target-sources) | 不適用：規則即本檔該節 |
| 任一事件、完成、等待或 HALT | [Router](Workflow.md#workflow-router) | [router-control](skills/johnny-project-takeover/references/router-control.md) |
| POC/MVP/COMMERCIAL、模型或 lane 數量、staging | [Profile](Workflow.md#workflow-router) | [delivery-profile](skills/johnny-project-takeover/references/delivery-profile.md) |
| 架構 owner、supervisor、implementer 休眠／喚醒 | [Model lifecycle](Workflow.md#workflow-router) | [model-role-routing](skills/johnny-project-takeover/references/model-role-routing.md) |
| 最小 Context、旁路引用、能力選擇 | [Router Context](Workflow.md#workflow-router) | [context-routing](skills/johnny-project-takeover/references/context-routing.md) |
| artifact tree、Agent Context 建立／換票／關閉 | [Router Context](Workflow.md#workflow-router) | [artifact-tree-routing](skills/johnny-project-takeover/references/artifact-tree-routing.md) + [agent-context-lifecycle](skills/johnny-project-takeover/references/agent-context-lifecycle.md) |
| PRD／CHG 建立、取代、封存 | [Change control](Workflow.md#change-control) | [requirement-lineage](skills/johnny-project-takeover/references/requirement-lineage.md) |
| reusable module catalog 查找／分區 | [Router Context](Workflow.md#workflow-router) | [module-catalog-routing](skills/johnny-project-takeover/references/module-catalog-routing.md) |
| 外部能力(map／craft／reduction)admission、tier／target 適配 | [Router Context](Workflow.md#workflow-router) | [capability-admission](skills/johnny-project-takeover/references/capability-admission.md) |
| 新專案、需求、Bug、架構或變更 | [Discovery](Workflow.md#discovery) | [discovery-change](skills/johnny-project-takeover/references/discovery-change.md) |
| Browser/WebView/DOM/JavaScript 不可信資料 | [XSS gate](Workflow.md#xss-review) | [xss-review](skills/johnny-project-takeover/references/xss-review.md) |
| Secret、正式 Log、Provider、Webhook、外部 effect | [Security](Workflow.md#security) | [security-boundary](skills/johnny-project-takeover/references/security-boundary.md) |
| SPEC、ticket、DI、type preflight、dispatch | [Tickets](Workflow.md#tickets) | [specification-ticketing](skills/johnny-project-takeover/references/specification-ticketing.md) |
| 低階模型 ticket 拆分或 admission | [Tickets](Workflow.md#tickets) | [ticket-decomposition](skills/johnny-project-takeover/references/ticket-decomposition.md) |
| 正式 UI、Figma／截圖／brief／既有 design system | [Tickets](Workflow.md#tickets) | [ui-design-handoff](skills/johnny-project-takeover/references/ui-design-handoff.md) |
| Owner、Agent control、task/worktree、correction | [Role boundary](Workflow.md#role-boundary) | [implementation-authority](skills/johnny-project-takeover/references/implementation-authority.md) |
| TDD、strict type、smoke、completion | [Implementation](Workflow.md#implementation) | [implementation-tdd](skills/johnny-project-takeover/references/implementation-tdd.md) |
| TDD matrix 或獨立 review | [Review](Workflow.md#review-handoff) | [review-checks](skills/johnny-project-takeover/references/review-checks.md) + [CodeReview.md](CodeReview.md) |
| 實作語言決策或驗證 | [SPEC/Tickets](Workflow.md#specification) | [language-policy](skills/johnny-project-takeover/references/language-policy.md) |

## Router 返回規則

任何 implementation 或 docs-only commit 都先產生 `ACTION_COMPLETED` 與 evidence，
再由 Router 選下一步：

- `AUTO_CONTINUE`：執行唯一已宣告且不需新 authority 的下一動作。
- `WAIT_FOR_HUMAN`：只等待具名核准、owner 決策或不可逆 effect。
- `HALT`：來源、權限、能力、驗證、安全或 transition 不合法。

`ImplementationReturn.CHANGE_DETECTED` 必須產生 `REQUIREMENT_CHANGED`；不得在已核准
ticket 內猜測或擴張需求。

<a id="target-sources"></a>

## Target project 正式來源

完整啟用後，沿用 target project 既有同用途路徑；若無，標準位置為：

```text
CONTEXT.md
PRD.md
ProjectSchedule.md
doc/RequirementChangeLog.md
doc/requirements/active/<year>/<domain>/REQ-YYYYMMDD-NNN.md
doc/archive/requirements/<year>/ARCH-REQ-YYYYMMDD-NNN.md
doc/WorkProgressReport.md
doc/security-agent-boundary.md
doc/context/<feature>/<worktree-id>.md
doc/reviews/<feature>/<cluster>-code-review.md
doc/adr/ADR-YYYYMMDD-NNN-<slug>.md
modules/spec/<feature>.md
modules/tickets/<feature>/README.md
modules/tickets/<feature>/<ticket>.md
modules/element/<language>/<feature>/<ticket-id>/
library/MODULE_CATALOG.md
library/catalog/<capability-domain>/README.md
```

必要來源尚未建立時，只能讀取現況、列出缺口並進入 Wayfinder／Grill；未經 owner
authority 不得猜測內容或建立平行來源。
