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
^j::
text := "httppp"
MsgBox % LC_UrlEncode(text)
return

MessageBoxW(hWnd,Text, Caption,Options)
{
	return DllCall("MessageBoxW", "Int",hWnd, "Str", Text, "Str", Caption, "Int",Options)
}

http_get(text)
{
    whr := ComObjCreate("WinHttp.WinHttpRequest.5.1")
    u_text := LC_UrlEncode(text)
    url := "http://localhost:8088/translator?content=" u_text "&dst=zh&encoding=utf-16"
    whr.Open("GET", url, true)
    whr.Send()
    whr.WaitForResponse()
}

; Modified by GeekDude from http://goo.gl/0a0iJq
LC_UriEncode(Uri, RE="[0-9A-Za-z]") {
	VarSetCapacity(Var, StrPut(Uri, "UTF-8"), 0), StrPut(Uri, &Var, "UTF-8")
	While Code := NumGet(Var, A_Index - 1, "UChar")
		Res .= (Chr:=Chr(Code)) ~= RE ? Chr : Format("%{:02X}", Code)
	Return, Res
}

LC_UriDecode(Uri) {
	Pos := 1
	While Pos := RegExMatch(Uri, "i)(%[\da-f]{2})+", Code, Pos)
	{
		VarSetCapacity(Var, StrLen(Code) // 3, 0), Code := SubStr(Code,2)
		Loop, Parse, Code, `%
			NumPut("0x" A_LoopField, Var, A_Index-1, "UChar")
		Decoded := StrGet(&Var, "UTF-8")
		Uri := SubStr(Uri, 1, Pos-1) . Decoded . SubStr(Uri, Pos+StrLen(Code)+1)
		Pos += StrLen(Decoded)+1
	}
	Return, Uri
}

;----------------------------------

LC_UrlEncode(Url) { ; keep ":/;?@,&=+$#."
	return LC_UriEncode(Url, "[0-9a-zA-Z:/;?@,&=+$#.]")
}

LC_UrlDecode(url) {
	return LC_UriDecode(url)
}