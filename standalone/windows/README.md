# Windows companion / Windows 独立桌面版

1.1.0 免 Python 安装包和便携版见 [安装说明](INSTALL.md)。以下为可选的源码运行方式。 / For the 1.1.0 self-contained installer and portable edition, see [setup](INSTALL.md). The following instructions apply to optional source execution.

安装标准 Python 3.11+（含 Tcl/Tk 与 Python Launcher），完整解压后运行 start-doubao.cmd 或 start-mikan.cmd。首次缺少 Pillow 时会联网安装。右键切换中英语言及 1×／1.5×／2× 显示大小，默认 2×，偏好自动保存。背景与文字栏透明。

Install Python 3.11+ with Tcl/Tk and Python Launcher. Extract fully and run start-doubao.cmd or start-mikan.cmd. Missing Pillow is installed on first launch. Right-click to switch Chinese/English and 1×/1.5×/2× sizes (default 2×). Preferences are saved; backgrounds and text areas are transparent.

可选联动：enable-task-link.cmd 合并并备份用户 hooks，需在 Codex 中审阅并信任后生效。disable-task-link.cmd 移除此目录的联动。迁移目录前先禁用旧配置。

Optional integration: enable-task-link.cmd merges and backs up hooks; review/trust them in Codex. disable-task-link.cmd removes this directory's integration. Disable old hooks before moving the application.

本机数据保存在 %LOCALAPPDATA%/CodexPets，可用 CODEX_PETS_DATA 覆盖。运行时不联网；首次安装依赖除外。不记录聊天、工具参数或输出。

Local data stays in %LOCALAPPDATA%/CodexPets, overridable with CODEX_PETS_DATA. Runtime is offline except dependency installation. Chats, tool arguments and outputs are not recorded.

[完整安装教程 / Full setup guide](https://github.com/RobertsVault/Codex-Pets#readme)
