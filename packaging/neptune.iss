[Setup]
AppId=fr.neptune.studio.vocal
AppName=Neptune
AppVersion={#Version}
AppVerName=Neptune {#Version}
DefaultDirName={localappdata}\Programs\Neptune
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0.19045
WizardStyle=modern
Compression=lzma2
SolidCompression=yes
OutputDir=..\dist
OutputBaseFilename=Neptune-{#Version}-Windows-x64-Setup
UninstallDisplayIcon={app}\runtime-{#Version}\pythonw.exe

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[CustomMessages]
french.DependencyError=Impossible d’installer les dépendances. Vérifie ta connexion et consulte le journal :
english.DependencyError=Dependencies could not be installed. Check your connection and see the log:
french.Launch=Ouvrir Neptune
english.Launch=Open Neptune
french.InstallNote=L’installation télécharge les dépendances et peut prendre plusieurs minutes.
english.InstallNote=Setup downloads dependencies and may take several minutes.

[Files]
Source: "..\dist\payload\*"; DestDir: "{tmp}\bootstrap"; Flags: dontcopy noencryption recursesubdirs
Source: "..\dist\payload\*"; DestDir: "{app}\runtime-{#Version}"; Excludes: "*.whl,install_dependencies.py,requirements-windows.txt"; Flags: ignoreversion recursesubdirs
Source: "..\src\*.py"; DestDir: "{app}\runtime-{#Version}\src"; Excludes: "pptx.py"; Flags: ignoreversion recursesubdirs
Source: "launch.pyw"; DestDir: "{app}\runtime-{#Version}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Neptune"; Filename: "{app}\runtime-{#Version}\pythonw.exe"; Parameters: """{app}\runtime-{#Version}\launch.pyw"""; WorkingDir: "{app}\runtime-{#Version}"

[Run]
Filename: "{app}\runtime-{#Version}\pythonw.exe"; Parameters: """{app}\runtime-{#Version}\launch.pyw"""; Description: "{cm:Launch}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\runtime-{#Version}\Lib\site-packages"
Type: files; Name: "{app}\runtime-{#Version}\Lib\installation.log"
Type: files; Name: "{app}\runtime-{#Version}\Lib\dependencies-ready"
Type: dirifempty; Name: "{app}\runtime-{#Version}\Lib"
Type: dirifempty; Name: "{app}\runtime-{#Version}"

[Code]
function UpdateReadyMemo(Space, NewLine, MemoUserInfoInfo, MemoDirInfo,
  MemoTypeInfo, MemoComponentsInfo, MemoGroupInfo, MemoTasksInfo: String): String;
begin
  Result := MemoDirInfo + NewLine + NewLine + CustomMessage('InstallNote');
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  Bootstrap, LibDir, Ready: String;
  ExitCode: Integer;
begin
  Result := '';
  LibDir := ExpandConstant('{app}\runtime-{#Version}\Lib');
  Ready := LibDir + '\dependencies-ready';
  if FileExists(Ready) then
    Exit;

  ExtractTemporaryFiles('{tmp}\bootstrap\*');
  Bootstrap := ExpandConstant('{tmp}\bootstrap');
  WizardForm.PreparingLabel.Caption := CustomMessage('InstallNote');
  WizardForm.PreparingLabel.Refresh;
  if not Exec(Bootstrap + '\python.exe',
    'install_dependencies.py "' + LibDir + '\site-packages"',
    Bootstrap, SW_HIDE, ewWaitUntilTerminated, ExitCode) or (ExitCode <> 0) then
    Result := CustomMessage('DependencyError') + #13#10 + LibDir + '\installation.log'
  else if not SaveStringToFile(Ready, 'ready', False) then
    Result := CustomMessage('DependencyError') + #13#10 + LibDir + '\installation.log';
end;
