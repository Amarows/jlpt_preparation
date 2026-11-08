Set shell = CreateObject("WScript.Shell")
Set fileSystem = CreateObject("Scripting.FileSystemObject")
projectPath = fileSystem.GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = projectPath
shell.Environment("PROCESS")("JLPT_BIND") = "0.0.0.0"
shell.Run """" & projectPath & "\.venv\Scripts\pythonw.exe"" server.py", 0, False
