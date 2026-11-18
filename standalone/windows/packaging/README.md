# Building Windows binaries / 构建 Windows 程序

用户使用安装版或 Portable ZIP 时无需 Python。此目录仅用于从源码生成相同的可分发程序。

The installer and Portable ZIP require no external Python. This directory is for rebuilding distributable binaries from source.

在 Windows x64 上使用包含 Tcl/Tk 的 Python 3.12，创建隔离环境并安装 requirements-build.txt。安装官方 Inno Setup 7.1.1，然后执行：

Use Python 3.12 with Tcl/Tk on Windows x64, create a virtual environment and install requirements-build.txt. Install official Inno Setup 7.1.1, then run:

```powershell
python -m pip install --upgrade "pip>=26.2"
python -m pip install -r packaging/requirements-build.txt
python packaging/build.py --compiler "<ISCC.exe>" --work-dir build --output-dir dist
```

在 standalone/windows 目录运行。输出包含当前用户安装器、便携 ZIP 和 SHA256SUMS.txt。默认不进行代码签名；如需公开分发已签名程序，应使用自己的有效签名证书。构建日志和中间文件保留在指定 work-dir，不进入安装包。

Run from standalone/windows. Output includes a per-user installer, portable ZIP and SHA256SUMS.txt. Builds are unsigned by default; use your own valid signing certificate when signed distribution is required. Build logs and intermediate files stay in work-dir and are excluded from installation packages.

依赖许可证与版本说明随程序分发。没有自动发布、修改 GitHub 或更改 hooks 信任状态的构建步骤。

Dependency licenses and component versions are distributed with the application. Building does not publish, modify GitHub or change hook trust settings.
