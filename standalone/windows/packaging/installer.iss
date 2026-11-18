#ifndef BundleDir
  #error BundleDir must point to the bundled application
#endif
#ifndef OutputDir
  #define OutputDir "."
#endif
[Setup]
AppId={{EF0C2534-2278-4C71-9D3C-788236728B61}
AppName=Codex Pets
AppVersion=1.1.0
AppPublisher=RobertsVault
AppPublisherURL=https://github.com/RobertsVault/Codex-Pets
AppSupportURL=https://github.com/RobertsVault/Codex-Pets
DefaultDirName={localappdata}\Programs\Codex Pets
DefaultGroupName=Codex Pets
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
OutputDir={#OutputDir}
OutputBaseFilename=Codex-Pets-1.1.0-Windows-x64-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\CodexPets.exe
SetupIconFile={#BundleDir}\CodexPets.ico
LicenseFile={#BundleDir}\LICENSE
AppMutex=Local\CodexPets_doubao,Local\CodexPets_mikan
CloseApplications=yes
RestartApplications=no
SetupLogging=no
VersionInfoVersion=1.1.0.0
VersionInfoCompany=RobertsVault
VersionInfoDescription=Codex Pets installer

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[CustomMessages]
english.Doubao=Doubao
english.Mikan=Mikan
english.EnableHooks=Enable Codex task integration
english.DisableHooks=Disable Codex task integration
english.DesktopIcons=Create desktop shortcuts
english.StartPet=Start Doubao
chinesesimplified.Doubao=豆包 Doubao
chinesesimplified.Mikan=橘宝 Mikan
chinesesimplified.EnableHooks=启用 Codex 任务跟随
chinesesimplified.DisableHooks=停用 Codex 任务跟随
chinesesimplified.DesktopIcons=创建桌面快捷方式
chinesesimplified.StartPet=启动豆包

[Tasks]
Name: "desktopicon"; Description: "{cm:DesktopIcons}"; Flags: unchecked

[Files]
Source: "{#BundleDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{cm:Doubao}"; Filename: "{app}\CodexPets.exe"; Parameters: "--pet doubao"
Name: "{group}\{cm:Mikan}"; Filename: "{app}\CodexPets.exe"; Parameters: "--pet mikan"
Name: "{group}\{cm:EnableHooks}"; Filename: "{app}\CodexPets.exe"; Parameters: "--configure-hooks enable"
Name: "{group}\{cm:DisableHooks}"; Filename: "{app}\CodexPets.exe"; Parameters: "--configure-hooks disable"
Name: "{group}\{cm:UninstallProgram,Codex Pets}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{cm:Doubao}"; Filename: "{app}\CodexPets.exe"; Parameters: "--pet doubao"; Tasks: desktopicon
Name: "{autodesktop}\{cm:Mikan}"; Filename: "{app}\CodexPets.exe"; Parameters: "--pet mikan"; Tasks: desktopicon

[Run]
Filename: "{app}\CodexPets.exe"; Parameters: "--pet doubao"; Description: "{cm:StartPet}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
Filename: "{app}\CodexPets.exe"; Parameters: "--configure-hooks disable --quiet"; RunOnceId: "RemoveTaskHooks"; Flags: runhidden waituntilterminated

[InstallDelete]
Type: files; Name: "{app}\原画素材\README.md"
Type: files; Name: "{app}\原画素材\SHA256SUMS.txt"
Type: files; Name: "{app}\原画素材\文件清单.csv"
Type: files; Name: "{app}\原画素材\橘宝\mikan.png"
Type: files; Name: "{app}\原画素材\豆包\ball.png"
Type: files; Name: "{app}\原画素材\豆包\begging.png"
Type: files; Name: "{app}\原画素材\豆包\celebrate.png"
Type: files; Name: "{app}\原画素材\豆包\coding.png"
Type: files; Name: "{app}\原画素材\豆包\eating.png"
Type: files; Name: "{app}\原画素材\豆包\idle.png"
Type: files; Name: "{app}\原画素材\豆包\petting.png"
Type: files; Name: "{app}\原画素材\豆包\roll.png"
Type: files; Name: "{app}\原画素材\豆包\sleep.png"
Type: files; Name: "{app}\原画素材\豆包\sniff-left.png"
Type: files; Name: "{app}\原画素材\豆包\sniff.png"
Type: dirifempty; Name: "{app}\原画素材\橘宝"
Type: dirifempty; Name: "{app}\原画素材\豆包"
Type: dirifempty; Name: "{app}\原画素材"
Type: files; Name: "{app}\素材说明.md"
