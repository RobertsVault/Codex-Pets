# Privacy / 隐私说明

发布源码和 ZIP 仅包含运行代码、素材、安装器、使用说明及许可证，不包含本机账户配置、凭证、聊天、transcript、运行设置／事件／日志、缓存、提示词、生成中间图或本机绝对路径。PNG 无文本、EXIF 或位置元数据；ZIP 无 Git 历史。

Published source and ZIPs contain runtime code, artwork, installers, user documentation and the license. They exclude local account configuration, credentials, chats, transcripts, settings/events/logs, caches, prompts, intermediate artwork and machine-specific absolute paths. PNGs contain no textual, EXIF or location metadata. ZIPs contain no Git history.

可选 hooks 仅持久化状态、哈希化会话／任务标识与时间，不保存提示词、参数、输出、原始标识或 transcript 路径。哈希属于假名化标识。数据与错误日志留在用户本机，不包含在下载包内。程序运行时不联网；启动器首次安装 Pillow 时会访问 Python 软件包源。

Optional hooks persist only a state, hashed session/task identifiers and time, never prompts, arguments, outputs, raw identifiers or transcript paths. Hashes are pseudonymous identifiers. Runtime data and error logs stay on the user's machine and are excluded from downloads. Runtime makes no network requests; first-time Pillow installation contacts the Python package index.

保留现有 MIT 许可证及其版权声明。仓库提交身份与包内容分开管理。

The existing MIT license and copyright notice are preserved. Repository commit attribution is separate from package contents.
