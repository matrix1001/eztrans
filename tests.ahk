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
http_get(text)
return

MessageBoxW(hWnd,Text, Caption,Options)
{
	return DllCall("MessageBoxW", "Int",hWnd, "Str", Text, "Str", Caption, "Int",Options)
}

http_get(text)
{
    ; Example: Download text to a variable:
    whr := ComObjCreate("WinHttp.WinHttpRequest.5.1")
    url := "http://localhost:8088/translator?content=" text "&dst=zh"
    whr.Open("GET", url, true)
    whr.Send()
    whr.WaitForResponse()
}