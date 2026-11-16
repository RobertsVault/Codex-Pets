# Privacy / 隐私说明

Published source and edition ZIPs are assembled from an explicit file list. They exclude account configuration, hooks installed on a particular computer, credentials, chats, transcripts, runtime settings/events/logs, editor files, caches, generated source images, generation prompts, local inspection reports and developer runtime paths. PNGs carry no textual, EXIF or location metadata. Download ZIPs contain no Git history.

发布源码与分版 ZIP 按明确清单组装，不包含账户配置、本机安装的 hooks、凭证、聊天、transcript、运行设置／事件／日志、编辑器文件、缓存、生成中间图、提示词、本地检查报告或开发运行时路径。PNG 不含文本、EXIF 或位置信息。下载 ZIP 不含 Git 历史。

The optional hook consumes lifecycle input but persists only a state, hashed session/task identifiers and time. It does not persist prompts, arguments, outputs, raw account/session identifiers or transcript paths. Runtime data and diagnostic logs remain on the user's computer; no network calls are made by the companion. Hashes are pseudonymous identifiers, not a claim of mathematical anonymity.

可选 hooks 只持久化状态、哈希化会话／任务标识和时间，不保存 prompt、参数、输出、原始账户／会话标识或 transcript 路径。运行数据和诊断日志留在用户本机，桌面伙伴不发送网络请求。哈希标识属于假名化处理，不代表数学意义上的匿名。

GitHub repository history and contributor identity are separate from downloadable package contents and are governed by the account's GitHub commit settings. The copyright notice in the existing MIT license is preserved.

GitHub 提交历史与贡献者身份不同于安装包内容，取决于账号的 GitHub 提交设置；保留现有 MIT 许可证中的版权声明。
