# Codex Pets WorkBuddy 1.0.1 · Windows

## 中文

双击 Codex-Pets-WorkBuddy-1.0.1-Windows-x64-Setup.exe，按安装向导操作。支持 Windows 10/11 x64，无需安装 Python、Pillow 或其他开发工具；安装和运行可离线完成。默认仅安装到当前用户，不需要管理员权限。

在开始菜单中启动「豆包 Doubao」或「橘宝 Mikan」。右键宠物切换中文／英文、1×／1.5×／2× 显示大小（默认 2×）以及互动项目。宠物和文字背景透明。两只可同时运行。

可选任务跟随：开始菜单 → Codex Pets WorkBuddy → 启用 WorkBuddy 任务跟随。重启或恢复 WorkBuddy，按客户端提示审阅并信任 hooks 后生效。停用入口可移除此安装目录的配置。升级自 Python 源码版时，请先在旧目录运行 disable-task-link.cmd，避免重复配置。

卸载可使用 Windows 设置 → 应用，或开始菜单中的卸载入口。卸载会移除本安装目录注册的 hooks，保留个人偏好与本机事件数据。数据位于 %LOCALAPPDATA%/CodexPetsWorkBuddy，可由 CODEX_PETS_DATA 指定其他位置。不会收集聊天、提示词、工具参数或输出。

免安装版：完整解压 Portable ZIP，双击 CodexPets.exe。启动橘宝可使用 CodexPets.exe --pet mikan。保持所有文件与子目录完整。可选任务跟随配置命令为 CodexPets.exe --configure-hooks enable；停用使用 disable。移动目录前先停用旧目录配置。

## English

Run Codex-Pets-WorkBuddy-1.0.1-Windows-x64-Setup.exe and follow the wizard. Windows 10/11 x64 is supported. Python and Pillow runtimes are bundled; developer tools and network access are not required. The default installation is per-user and does not require administrator access.

Start Doubao or Mikan from the Start menu. Right-click the pet to switch Chinese/English, choose 1×/1.5×/2× size (2× default), and interact. Backgrounds and text areas are transparent. Both pets may run together.

Optional task integration: Start menu → Codex Pets WorkBuddy → Enable WorkBuddy task integration. Restart/resume WorkBuddy and review/trust the added hooks. The disable shortcut removes this installation's entries. When migrating from the Python edition, disable its old hooks first to avoid duplicate entries.

Uninstall through Windows Settings → Apps. Uninstallation removes this installation's registered hooks and retains personal preferences and local event data. Data stays in %LOCALAPPDATA%/CodexPetsWorkBuddy, overridable with CODEX_PETS_DATA. Chats, prompts, tool arguments and outputs are not collected.

Portable edition: extract the full ZIP and run CodexPets.exe. Use CodexPets.exe --pet mikan to start Mikan. Keep all files and directories together. Optional integration uses CodexPets.exe --configure-hooks enable or disable. Disable old hooks before moving the folder.

[Project / 项目主页](https://github.com/RobertsVault/Codex-Pets)


WorkBuddy 接入：用户级配置位于 ~/.workbuddy/settings.json。启用时合并并备份现有配置，停用仅移除此目录的接收程序。收到首个真实事件前，宠物显示“等待事件”。Stop 表示本轮响应结束，不代表整个项目已完成。单次工具错误不会自动当作整项任务失败。

WorkBuddy integration uses ~/.workbuddy/settings.json with backup and merge. Only this installation is removed when disabled. The companion shows awaiting events until an actual event arrives. Stop means the response ended, not that an entire project succeeded. Tool errors alone do not indicate overall failure.
