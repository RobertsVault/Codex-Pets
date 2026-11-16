# Native pets / 原生宠物包

Windows：完整解压后双击 `install.cmd`，在兼容 v2 的 Codex 客户端中刷新宠物列表。无需 Python 或管理员权限。默认安装到 `~/.codex/pets`，支持 `CODEX_HOME`。旧版备份保存在同级 `pet-backups`。原生播放时长和触发由客户端控制。

Windows: extract fully, run `install.cmd`, then refresh pets in a v2-compatible Codex client. No Python or administrator access is required. Defaults to `~/.codex/pets`; respects `CODEX_HOME`. Existing pets are backed up in the sibling `pet-backups` directory. Timing and triggers are controlled by the client.

`sh install.sh` 供兼容 macOS/Linux 客户端使用，未在这些系统实测。 / The shell installer is included for compatible macOS/Linux clients but has not been tested there.

卸载：关闭宠物后移除 `pets/mikan`、`pets/doubao`；需要时从 `pet-backups` 恢复并改回原名。 / Uninstall: close the pets, remove their installed directories, or restore backups under the original names.

[完整中英教程 / Full bilingual guide](https://github.com/RobertsVault/Codex-Pets#readme)
