Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

batchPath = fso.GetParentFolderName(WScript.ScriptFullName) & "\verbose_launch_numl_toolkit_pyqt5.bat"

shell.Run Chr(34) & batchPath & Chr(34), 0
