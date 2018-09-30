^y::
WinActive("A")                           ; sets last found window
ControlGetFocus, ctrl
if (RegExMatch(ctrl, "A)Edit\d+"))       ; attempt copying without clipboard
    ControlGet, text, Selected,, %ctrl%  
else {                                   ; fallback solution
    clipboardOld := Clipboard            ; backup clipboard
    Send, ^c                             ; copy selected text to clipboard
    if (Clipboard != clipboardOld) {
        text := Clipboard                ; store selected text
        Clipboard := clipboardOld        ; restore clipboard contents
    }
}
MsgBox % text
return

^j::
cmd := "cmd.exe /q /c dir"
MsgBox % ComObjCreate("WScript.Shell").Exec(cmd).StdOut.ReadAll()
return
