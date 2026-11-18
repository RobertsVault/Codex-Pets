# Codex Pets · 橘宝与豆包

[中文安装教程](#中文安装教程) · [English setup](#english-setup) · [v1.1.0 Release](https://github.com/RobertsVault/Codex-Pets/releases/tag/v1.1.0)

**橘宝 Mikan** 与 **豆包 Doubao**，提供原生 Codex 宠物包和 Windows 独立桌面伙伴。原生版使用多帧姿态；独立版提供每只 12 类细致动画、真实迈腿跑步、16 个转头方向、中英切换及 1×／1.5×／2× 显示尺寸，默认 2×。宠物背景与文字栏透明。

**Mikan** and **Doubao** are available as native Codex pets and a standalone Windows companion. Native pets use multi-frame poses. The companion adds twelve detailed animation states per pet, articulated running, sixteen head directions, Chinese/English switching and 1×/1.5×/2× display sizes (2× by default), with transparent backgrounds and text areas.

![Running and head turns](media/animations.gif)

| 版本 / Edition | 要求 / Requirements | 下载 / Download |
| --- | --- | --- |
| 原生宠物 / Native pets | 支持 v2 自定义宠物的 Codex 客户端 / v2-compatible Codex client | [Native ZIP](https://github.com/RobertsVault/Codex-Pets/releases/download/v1.1.0/Codex-Pets-1.1.0-Native.zip) |
| Windows 独立版 / Windows companion | Windows 10/11 x64，无需另装 Python / Python bundled | [Setup / Portable](https://github.com/RobertsVault/Codex-Pets/releases/tag/v1.1.0) |
| WorkBuddy 适配版 / WorkBuddy companion | Windows 10/11 x64，无需另装 Python / Python bundled | [Setup / Portable](https://github.com/RobertsVault/Codex-Pets/releases/tag/v1.1.0) |

[MIT License](LICENSE)

### v1.1.0

更新橘宝与豆包的动画素材，统一身体尺寸、比例和配色，改进摸头、握爪、摸肚皮及玩球动作的表现；原生版保留清晰的待机眨眼。随包附带独立的 Original-Artwork 目录，保留 1.0.0 原画素材。修复 WorkBuddy 在 PowerShell 执行环境下无法启动任务跟随的问题；升级后重新启用一次 WorkBuddy 任务跟随。

Updated Mikan and Doubao animations with consistent body size, proportions and colors, and clearer head-pat, paw-shake, belly-rub and ball-play actions. Native pets retain their idle blink. Original 1.0.0 artwork is included in a separate Original-Artwork directory. Fixed task integration failing to start when WorkBuddy executes hooks through PowerShell; re-enable WorkBuddy task integration after upgrading.

### 动画 / Animations

| 宠物 / Pet | 工作与休息 / Tasks and rest | 互动 / Interactions |
| --- | --- | --- |
| 橘宝 Mikan | ![Mikan tasks](media/mikan-tasks.gif) | ![Mikan interactions](media/mikan-interactions.gif) |
| 豆包 Doubao | ![Doubao tasks](media/doubao-tasks.gif) | ![Doubao interactions](media/doubao-interactions.gif) |

上述细致动画展示独立版表现。原生版按客户端固定帧表播放，动作集合与持续时间有所不同。

Detailed animation previews show the standalone edition. Native playback follows the client's fixed frame table and has a different action set and timing.

## 中文安装教程

### 1. 原生宠物版

1. 下载 **Native ZIP**，完整解压，不要直接在压缩包中运行。
2. Windows 双击 `install.cmd`，无需 Python 或管理员权限。
3. 在支持 v2 自定义宠物的 Codex 客户端中刷新宠物列表，选择 **橘宝 Mikan** 或 **豆包 Doubao**。若素材被缓存，重新选择宠物或重启客户端。

默认安装到 `~/.codex/pets`；设置 `CODEX_HOME` 时使用其 `pets` 子目录。安装器会将已有宠物备份到同级 `pet-backups`。从仓库源码安装时，进入 `native/` 运行相同文件。自定义安装位置：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Destination "目标目录"
```

`sh install.sh` 可用于有兼容客户端的 macOS/Linux 环境，尚未在这些系统实测；它不是 macOS 独立应用。

原生版的播放时长、任务触发、鼠标悬停、注视、拖动和界面语言由 Codex 客户端控制，素材包不能改变这些规则。

卸载时先关闭宠物，再删除安装目录中的 `mikan` 和 `doubao`。恢复旧版时，将 `pet-backups` 中所需备份复制回 `pets` 并改回对应名称。

### 2. Windows 独立桌面版

1. 从 v1.1.0 Release 下载 **Codex Windows x64 Setup** 并安装，无需另装 Python、Pillow 或开发工具，可离线安装与运行。
2. 从开始菜单 → **Codex Pets** 启动豆包或橘宝；默认仅安装到当前用户，无需管理员权限。
3. 免安装版请完整解压 **Portable ZIP**，运行 `CodexPets.exe`；启动橘宝使用 `CodexPets.exe --pet mikan`。保留所有文件与子目录。
4. 右键 → **语言 / Language → 中文 / English**，随时切换文字。
5. 右键 → **显示大小 → 1× / 1.5× / 2×**，默认 2×。宠物、字体和可交互区域同步缩放，选择随每只宠物保存。

两只宠物可同时运行，也可与原生版共存。[安装与卸载说明](standalone/windows/INSTALL.md)。从源码启动仍需 Python 3.11+、Tcl/Tk 与 Pillow，进入 `standalone/windows/` 后使用 cmd 脚本；也可指定启动语言：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\launch.ps1 -Mode doubao -Language en
```

单击摸头、双击玩球、中键喂食；拖动可移动窗口，右键打开互动菜单，Esc 退出。摸头、喂食、握爪和摸肚皮至少展示 5 秒；玩球、跑步和散步至少 6 秒；睡觉至少 10 秒。主动选择另一项互动可以替换当前互动。跑步会移动窗口并在屏幕边缘转向。

工作和等待持续展示到状态改变；完成、审阅、失败保持至少 10 秒，新活动任务可优先切入。任务状态优先于互动和闲逛。自动散步默认关闭；空闲时可跟随附近鼠标逐步转头。右键可以关闭自动散步、视线跟随或细致动画，也可以手动选择任务状态。

### 3. 可选：连接 Codex 任务

1. 保持独立版运行，从开始菜单 → Codex Pets 选择「启用 Codex 任务跟随」（源码版使用 `enable-task-link.cmd`）。
2. 安装器合并用户级 `hooks.json` 并备份已有文件，保留其他 hooks。重新启动／恢复 Codex，按客户端提示审阅并信任新增 hooks；CLI 可使用 `/hooks`。
3. 提交请求进入工作；工具批准请求进入等待；工具继续执行恢复工作；本轮停止后展示完成；中断或会话结束回到空闲。
4. 开始菜单中的「停用 Codex 任务跟随」只移除此安装目录注册的 hooks（源码版使用 `disable-task-link.cmd`）。迁移目录或更换 Python 路径前，在旧目录禁用后再从新目录启用。

联动只消费宠物启动后收到的状态事件，不读取聊天记录。多会话时等待优先于工作，活动任务优先于闲逛。普通文字问题不一定触发批准 hook，工具报错也不一定代表整个任务失败；这两类状态可手动选择。客户端支持及授权情况会影响实际联动。若退出异常导致状态未清除，可右键清除任务状态。

### 4. 数据与常见问题

位置、语言、尺寸偏好、状态事件与错误日志保存在 `%LOCALAPPDATA%/CodexPets`；`CODEX_PETS_DATA` 可指定其他目录。事件仅包含状态、哈希化会话／任务标识和时间，不保存提示词、工具参数、输出、账户或密钥，也不读取 transcript。安装版自带依赖，可离线安装与运行；源码版首次安装 Pillow 需要联网。

若没有窗口，确认安装文件或便携目录完整，并检查上述本机目录中的错误日志；源码版另需检查 Python/Tcl/Tk/Pillow。首次启动、客户端重启后或未信任 hooks 时，空闲状态不代表任务联动已经启用。

### 5. WorkBuddy 适配版

从 v1.1.0 Release 下载文件名包含 **WorkBuddy** 的 Setup 或 Portable ZIP。开始菜单 → Codex Pets WorkBuddy 中可启动宠物及启用／停用 WorkBuddy 任务跟随；便携版使用 `CodexPets.exe --configure-hooks enable` 或 `disable`。

启用时合并并备份 `~/.workbuddy/settings.json`，重启 WorkBuddy 并按客户端提示审阅 hooks。数据保存在 `%LOCALAPPDATA%/CodexPetsWorkBuddy`，与 Codex 版分开。语言、尺寸和互动方式相同；移动目录前先停用旧配置。[详细说明](adapters/workbuddy/windows/INSTALL.md)。

## English setup

### 1. Native pets

1. Download **Native ZIP** and extract it fully.
2. On Windows, run `install.cmd`. Python and administrator access are not required.
3. Refresh pets in a v2-compatible Codex client and choose **Mikan** or **Doubao**. Reselect the pet or restart the client if artwork is cached.

The default destination is `~/.codex/pets`, or `CODEX_HOME/pets` when configured. Existing pets are backed up to the sibling `pet-backups` directory. From source, use `native/`. The PowerShell command above supports a custom destination.

`sh install.sh` is included for compatible macOS/Linux clients but has not been tested there. This does not constitute a released macOS standalone application. Native duration, triggers, hover/gaze reactions, dragging and UI language belong to the Codex client.

To uninstall, close the pet and remove its `mikan` or `doubao` directory. To restore a backup, copy it from `pet-backups` into `pets` under the original name.

### 2. Windows companion

1. Download the **Codex Windows x64 Setup** from v1.1.0 Release. Python, Pillow and developer tools need no separate installation; installation and runtime work offline.
2. Start Doubao or Mikan from Start menu → **Codex Pets**. Installation is per-user and requires no administrator privileges.
3. For portable use, extract the complete **Portable ZIP** and run `CodexPets.exe`, or `CodexPets.exe --pet mikan` for Mikan. Keep all files and subdirectories together.
4. Right-click → **Language / 语言 → English / 中文**.
5. Right-click → **Display size → 1× / 1.5× / 2×** (default). The pet, text and interactive area scale together. Preferences are saved per pet.

Both pets can run together and coexist with native pets. See [installation and uninstallation](standalone/windows/INSTALL.md). Source launchers under `standalone/windows/` still require Python 3.11+, Tcl/Tk and Pillow. The launch command above can set the startup language.

Click for head pats, double-click to play ball, middle-click for a snack, drag to reposition, or right-click for all actions. Esc quits. Most interactions last at least 5 seconds; running, walking and playing ball last at least 6 seconds; sleeping lasts at least 10 seconds. A new deliberate interaction may replace the current one. Running moves the window and turns at screen edges.

Working and waiting remain visible until changed. Results stay for at least 10 seconds unless a new active task supersedes them. Tasks take priority over interactions and roaming. Idle roaming is off by default. Pointer tracking gradually turns the head only while idle. The menu can toggle roaming, pointer tracking or detailed animation, and lets you choose states manually.

### 3. Optional task integration

Run the companion, then choose Start menu → Codex Pets → Enable Codex task integration (source edition: `enable-task-link.cmd`). This merges user-level hooks while preserving other entries and backing up the previous file. Restart/resume Codex and review/trust the new hooks when prompted; the CLI provides `/hooks`.

Prompt submission starts work; tool approval requests show waiting; tool activity resumes work; a stopped turn shows completion; interrupt/session end clears the state. Only events received after launch are consumed. No transcript is read. Multiple sessions prioritize waiting over working. Plain-text questions and overall task failure cannot always be inferred from hook events; manual state selection is available. Actual integration depends on client support and authorization.

Choose Disable Codex task integration in the Start menu to remove only this installation's hooks (source edition: `disable-task-link.cmd`). Disable the old location before moving the application or changing Python paths, then enable from the new location. Clear tasks from the menu if a crashed client leaves stale state.

### 4. Privacy and troubleshooting

Settings, language, size preferences, minimal events and error logs stay in `%LOCALAPPDATA%/CodexPets`, or `CODEX_PETS_DATA` when set. Events contain only a state, hashed session/task identifiers and a timestamp. No prompts, tool arguments, outputs, transcripts, credentials or account identifiers are collected or uploaded. The installer bundles dependencies for offline installation and runtime. First-time Pillow installation for the source edition requires network access.

If no window opens, check that the installed or portable files are complete and inspect the local error log; source users should also verify Python/Tcl/Tk/Pillow. Idle state alone does not mean hooks are connected, especially before trust is granted or after restarting the client.

### 5. WorkBuddy companion

Download a Setup or Portable ZIP containing **WorkBuddy** in its filename from v1.1.0 Release. Start pets and enable/disable integration from Start menu → Codex Pets WorkBuddy. Portable integration uses `CodexPets.exe --configure-hooks enable` or `disable`.

Configuration is merged into `~/.workbuddy/settings.json` with backup. Restart WorkBuddy and review hooks as prompted. Local data stays in `%LOCALAPPDATA%/CodexPetsWorkBuddy`, separately from Codex. Language, size and interaction controls are shared. Disable old hooks before moving directories. See [the setup guide](adapters/workbuddy/windows/INSTALL.md).



Community project; not an official OpenAI release. / 社区项目，与 OpenAI 官方发行无关。
