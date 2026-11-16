# Windows desktop companion / Windows 独立桌面版

安装标准 Python 3.10+（含 Tcl/Tk 与 Python Launcher），无需第三方依赖。完整解压后双击 `start-doubao.cmd` 或 `start-mikan.cmd`。右键 → 语言 / Language → 中文 / English，随时切换并保存偏好。工作／等待持续展示，结果保持 10 秒，互动至少 5 秒，跑步至少 6 秒。自动散步默认关闭。

Install standard Python 3.10+ with Tcl/Tk and Python Launcher. No third-party packages are required. Extract fully, run `start-doubao.cmd` or `start-mikan.cmd`, and right-click → Language / 语言 to switch English/Chinese. Working and waiting persist; results last 10 seconds; interactions last at least 5 seconds; running lasts at least 6 seconds. Idle roaming is off by default.

可选任务联动：运行宠物后执行 `enable-task-link.cmd`，重启／恢复 Codex 并按提示信任新增 hooks。执行 `disable-task-link.cmd` 可移除此目录的联动配置。迁移目录前先禁用旧配置。不会自动信任 hooks，也不会改动批准决策。

Optional task integration: run `enable-task-link.cmd`, restart/resume Codex, then review/trust the new hooks. Use `disable-task-link.cmd` from this directory to remove its integration. Disable the old location before moving it. Trust and approval decisions are never bypassed.

数据与错误日志保存在 `%LOCALAPPDATA%/CodexPets`，可用 `CODEX_PETS_DATA` 覆盖。不读取 transcript，不记录聊天、工具参数或输出，不发送网络请求。真实客户端事件联动需验收；普通文字等待与任务失败不保证自动识别。

Data and error logs stay in `%LOCALAPPDATA%/CodexPets`, overridable with `CODEX_PETS_DATA`. No transcripts, chat content, tool arguments or outputs are collected. No network requests are made. Real task integration requires client verification; plain-text waiting and task failure are not always inferred automatically.

[完整中英教程 / Full bilingual guide](https://github.com/RobertsVault/Codex-Pets#readme)
