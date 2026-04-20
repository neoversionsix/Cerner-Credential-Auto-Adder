#Requires AutoHotkey v2.0
#SingleInstance Force

; =========================================================
; Credential Tool (AHK v2)
; - GUI runs normally
; - Worker runs in a separate process: --worker ...
; - Instant stop: GUI STOP button OR F12 kills the worker process immediately
; - Emergency: Ctrl+Alt+F12 exits the whole app
;
; Compile to EXE later with Ahk2Exe (no AHK needed on target PCs).
; =========================================================

; ---------- CONFIG (edit if needed) ----------
global TARGET_WIN_TITLE := "User Maint"
global USERNAME_TEXT    := "credentialbox"

global SHORT_DELAY_MS := 200
global LONG_DELAY_MS  := 1000

; ---------- MODE SWITCH ----------
global IsWorker := (A_Args.Length >= 1 && A_Args[1] = "--worker")

; Set hotkeys per mode
if (IsWorker) {
    Hotkey("F12",   (*) => ExitApp())   ; instant stop (worker self-terminates)
    Hotkey("Pause", (*) => ExitApp())
} else {
    Hotkey("F12",   (*) => StopRun())   ; instant stop (kills worker)
    Hotkey("^!F12", (*) => ExitApp())   ; emergency exit app
}

if (IsWorker) {
    WorkerMain()
    ExitApp
}

; =========================================================
; GUI PROCESS
; =========================================================
global WorkerPID := 0
global LogPath := A_Temp "\CredentialTool.log"
global LogPos := 0

; Clear previous session log so GUI starts fresh
try FileDelete(LogPath)

global g, edDay, edMonth, edYear, edCount, btnStart, btnStop, logBox

g := Gui(, "Credential Script (AHK v2)")
g.SetFont("s10", "Segoe UI")

g.AddText(, "Start Day:")
edDay := g.AddEdit("w80 Number", "1")

g.AddText("x+m", "Start Month:")
edMonth := g.AddEdit("w80 Number", "1")

g.AddText("x+m", "Start Year:")
edYear := g.AddEdit("w100 Number", "2026")

g.AddText("xm y+m", "Credentials to Add:")
edCount := g.AddEdit("w120 Number", "10")

btnStart := g.AddButton("xm y+m w140 h32", "Start")
btnStart.OnEvent("Click", (*) => StartRun())

btnStop := g.AddButton("x+m w420 h70", "CLICK TO TERMINATE SCRIPT")
btnStop.SetFont("s14 Bold", "Segoe UI")
btnStop.OnEvent("Click", (*) => StopRun())

g.AddText("xm y+m", "Hotkeys: F12 = stop instantly | Ctrl+Alt+F12 = exit app")

logBox := g.AddEdit("xm y+m w700 h260 ReadOnly -Wrap")
logBox.Value := ""

g.OnEvent("Close", (*) => (StopRun(), ExitApp))

SetTimer(MonitorWorkerAndLog, 250)
g.Show()

; ---------- GUI FUNCTIONS ----------
StartRun() {
    global WorkerPID, LogPath, LogPos, btnStart
    global edDay, edMonth, edYear, edCount

    if (WorkerPID && ProcessExist(WorkerPID)) {
        Log("Already running. Press F12 or click STOP to terminate.")
        return
    }

    day   := IntegerSafe(edDay.Value)
    month := IntegerSafe(edMonth.Value)
    year  := IntegerSafe(edYear.Value)
    count := IntegerSafe(edCount.Value)

    if (day <= 0 || month <= 0 || year <= 0 || count <= 0) {
        MsgBox("Please enter valid positive numbers.")
        return
    }

    ; reset log
    try FileDelete(LogPath)
    LogPos := 0

    quotedLog := '"' LogPath '"'
    args := "--worker " day " " month " " year " " count " " quotedLog

    if (A_IsCompiled) {
        cmd := '"' A_ScriptFullPath '" ' args
    } else {
        cmd := '"' A_AhkPath '" "' A_ScriptFullPath '" ' args
    }

    Run(cmd, , "Hide", &pid)
    WorkerPID := pid

    btnStart.Enabled := false
    Log("Started worker PID " WorkerPID ". Target window title: " TARGET_WIN_TITLE)
}

StopRun() {
    global WorkerPID, btnStart
    if (WorkerPID && ProcessExist(WorkerPID)) {
        try ProcessClose(WorkerPID)  ; <-- instant kill
        Log("STOP: worker killed (PID " WorkerPID ").")
    }
    WorkerPID := 0
    btnStart.Enabled := true
}

MonitorWorkerAndLog() {
    global WorkerPID, LogPath, LogPos, btnStart

    ; tail log
    if FileExist(LogPath) {
        try {
            f := FileOpen(LogPath, "r")
            if (f.Length > LogPos) {
                f.Seek(LogPos, 0)
                chunk := f.Read()
                LogPos := f.Pos
                if (chunk != "")
                    Log(chunk, true)
            }
            f.Close()
        }
    }

    ; detect worker end
    if (WorkerPID && !ProcessExist(WorkerPID)) {
        Log("Worker finished.")
        WorkerPID := 0
        btnStart.Enabled := true
    }
}

Log(msg, rawAppend := false) {
    global logBox
    t := FormatTime(, "yyyy-MM-dd HH:mm:ss")
    if rawAppend {
        logBox.Value .= msg
    } else {
        logBox.Value .= t "  " msg "`r`n"
    }
    try SendMessage(0x00B7, -1, -1, logBox.Hwnd) ; EM_SCROLLCARET
}


IntegerSafe(v) {
    try {
        return Integer(v)
    } catch {
        return 0
    }
}

; =========================================================
; WORKER PROCESS (Citrix keystrokes)
; =========================================================
WorkerMain() {
    global TARGET_WIN_TITLE, USERNAME_TEXT, SHORT_DELAY_MS, LONG_DELAY_MS

    ; args: --worker <day> <month> <year> <count> "<logPath>"
    if (A_Args.Length < 6)
        ExitApp

    startDay   := Integer(A_Args[2])
    startMonth := Integer(A_Args[3])
    startYear  := Integer(A_Args[4])
    credsToAdd := Integer(A_Args[5])
    logPath    := A_Args[6]

    SendMode("Event")
    SetKeyDelay(40, 40)

    WLog(logPath, "Worker started. Will add " credsToAdd " creds.")
    WLog(logPath, "Press F12 in this worker to exit instantly.")

    if !ActivateTargetWindow(logPath) {
        WLog(logPath, "ERROR: Could not activate '" TARGET_WIN_TITLE "'. Exiting.")
        ExitApp
    }

    ; Switch Search Field to Username
    Sleep(SHORT_DELAY_MS)
    Send("{F10}")
    Sleep(SHORT_DELAY_MS)
    Send("{Down 4}")
    Sleep(SHORT_DELAY_MS)
    Send("{Right}")
    Sleep(SHORT_DELAY_MS)
    Send("{Down}")
    Sleep(SHORT_DELAY_MS)
    Send("{Enter}")
    Sleep(SHORT_DELAY_MS)

    ; Open Credential Box
    Sleep(SHORT_DELAY_MS)
    Send("{Space}{Backspace}")
    PasteText(USERNAME_TEXT, false, 80, 350)
    Send("{Enter}")
    WLog(logPath, "Credential Box opened.")

    ; Select Credential Button
    Sleep(LONG_DELAY_MS)
    Send("{F10}")
    Sleep(SHORT_DELAY_MS)
    Send("{Down 2}")
    Sleep(SHORT_DELAY_MS)
    Send("{Right}")
    Sleep(SHORT_DELAY_MS)
    SendText("c")
    Sleep(LONG_DELAY_MS)

    day := startDay, month := startMonth, year := startYear

    Loop credsToAdd {
        idx := A_Index - 1
        WLog(logPath, "Creds Created: " idx)

        Sleep(SHORT_DELAY_MS)
        if (idx = 0) {
            PressTab(4)
        } else {
            PressTab(2)
        }
        Sleep(SHORT_DELAY_MS)
        Send("{Down}")
        Sleep(SHORT_DELAY_MS)
        Send("{Tab}")
        Sleep(SHORT_DELAY_MS)

        ; Choose Credential
        SendText("a")
        Sleep(SHORT_DELAY_MS)

        ; Go to type of licence
        Send("{Tab}")
        Sleep(400)

        ; Choose Licence
        SendText("l")
        Sleep(SHORT_DELAY_MS)

        PressTab(4)
        Sleep(SHORT_DELAY_MS)

        ; Enter date: DDMMYYYY
        dateText := Format("{:02}{:02}{}", day, month, year)
        PasteText(dateText, false, 80, 500)

        ; next date
        day += 1
        if (day > 25) {
            day := 1
            month += 1
        }
        if (month > 12) {
            day := 1
            month := 1
            year += 1
        }

        ; Hit Apply
        Sleep(SHORT_DELAY_MS)
        PressTab(7)
        Sleep(SHORT_DELAY_MS)
        Send("{Enter}")
        Sleep(2000)

        ; delete credential
        PressTab(2)
        Sleep(SHORT_DELAY_MS)
        Send("{Space}")
        Sleep(SHORT_DELAY_MS)
        PressTab(2)
        Sleep(SHORT_DELAY_MS)
        Send("{Enter}")

        ; Apply deletion
        Sleep(SHORT_DELAY_MS)
        PressTab(2)
        Sleep(SHORT_DELAY_MS)
        Send("{Enter}")
        Sleep(1000)
    }

    WLog(logPath, "Done.")
}

ActivateTargetWindow(logPath) {
    global TARGET_WIN_TITLE

    Loop 3 {
        try {
            WinActivate(TARGET_WIN_TITLE)
            if WinWaitActive(TARGET_WIN_TITLE, , 1) {
                WLog(logPath, "Activated window: " TARGET_WIN_TITLE)
                return true
            }
        } catch {
            ; retry
        }
        WLog(logPath, "Attempt to activate window failed. Retrying...")
        Sleep(500)
    }
    return false
}

PressTab(n) {
    global SHORT_DELAY_MS
    Loop n {
        Send("{Tab}")
        Sleep(SHORT_DELAY_MS)
    }
}

PasteText(text, selectAll := false, preDelay := 80, postDelay := 350) {
    A_Clipboard := text
    Sleep(preDelay)
    if (selectAll) {
        Send("^a")
        Sleep(50)
    }
    Send("^v")
    Sleep(postDelay)
}

WLog(path, msg) {
    t := FormatTime(, "yyyy-MM-dd HH:mm:ss")
    try FileAppend(t "  " msg "`r`n", path, "UTF-8")
}