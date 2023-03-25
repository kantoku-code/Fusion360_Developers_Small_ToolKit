'by kantoku
Const FUSION_PATH = "@fusionpath"
Const XML_PATH = "@xmlpath"
Const SLEEP_TIME = 10000

call main()

Sub main()

    Dim msg
    msg = canExec()
    if len(msg) > 0 Then
        msgbox msg
        exit Sub
    end if

    msg = _
        "言語を指定してFusion360を起動します。" & vbCrLf & _
        "[はい] : 日本語" & vbCrLf & _
        "[いいえ] : 英語" & vbCrLf & _
        "[キャンセル] : 中止"

    lang = ""
    Select Case MsgBox(msg, vbYesNoCancel)
        Case vbYes
            lang = "ja-JP"
        Case vbNo
            lang = "en-US"
        Case Else
            Exit Sub
    End Select

    startFusion lang

End Sub

Sub startFusion(lang)

    'バックアップ
    Dim backUpPath
    backUpPath = getUniquePath(XML_PATH)

    Dim fso
    Set fso = getFso()

    fso.copyFile XML_PATH, backUpPath

    'xml書き換え
    Set dom = get_dom(XML_PATH)
    If dom Is Nothing Then
        Exit Sub
    End If

    Set nodeRoot = dom.DocumentElement
    Set BootstrapOptionsGroup = getElementByTagName(nodeRoot, "BootstrapOptionsGroup")
    Set userLanguageOptionId = getElementByTagName(BootstrapOptionsGroup, "userLanguageOptionId")
    If userLanguageOptionId Is Nothing Then
        Set userLanguageOptionId = BootstrapOptionsGroup.appendChild(createNode(dom))
    End If

    Set langValue = getAttributeByName(userLanguageOptionId, "Value")

    langValue.Value = lang

    dom.Save XML_PATH

    '起動
    Dim ws
    Set ws = CreateObject("WScript.Shell")
    ws.Run FUSION_PATH, vbNormalFocus, False

    '削除,復旧
    WScript.Sleep SLEEP_TIME
    fso.DeleteFile XML_PATH
    renameFile backUpPath, XML_PATH

End Sub


Function canExec()

    Dim fso
    Set fso = getFso()

    Dim msg
    msg = ""

    If Not fso.FileExists(FUSION_PATH) Then
        msg = "[FusionLauncher.exe]のパスが間違っています。" & vbcrlf
    End If

    If Not fso.FileExists(XML_PATH) Then
        msg = msg & "[NMachineSpecificOptions.xml]のパスが間違っています。"
    End If

    canExec = msg

End Function


Function renameFile(target, result)

    Dim pathAry
    pathAry = splitPathName(result)

    Dim newName
    newName = pathAry(1) & "." & pathAry(2)

    Dim fso
    Set fso = getFso()

    fso.GetFile(target).name = newName

End Function


Function getUniquePath(path)

    Dim pathAry
    pathAry = splitPathName(path)

    Dim fso
    Set fso = getFso()

    Dim tmpPath
    tmpPath = joinPathName(pathAry)
    If Not fso.FileExists(tmpPath) Then
        getUniquePath = tmpPath
        Exit Function
    End If
    
    Dim baseName
    baseName = pathAry(1)

    Dim count
    count = 1
    Do
        pathAry(1) = baseName & "-" & count
        tmpPath = joinPathName(pathAry)
        If Not fso.FileExists(tmpPath) Then
            getUniquePath = tmpPath
            Exit Function
        End If
        count = count + 1
    Loop

End Function


Function joinPathName(ary)

    joinPathName = ary(0) + "\" + ary(1) + "." + ary(2)

End Function


Function splitPathName(path)

    Dim ary(2)
    With getFso
        ary(0) = .GetParentFolderName(path)
        ary(1) = .GetBaseName(path)
        ary(2) = .GetExtensionName(path)
    End With
    splitPathName = ary

End Function


Function getFso()

    Set getFso = CreateObject("Scripting.FileSystemObject")

End Function


Function createNode(dom)

    Dim node
    Set node = dom.createElement("userLanguageOptionId")
    node.appendChild dom.createTextNode("test")
    node.setAttribute "ToolTip", "ユーザ インタフェースの表示に使用する言語です。"
    node.setAttribute "UserName", "ユーザ言語"
    node.setAttribute "Value", "en-US"

    Set createNode = node

End Function

Function getAttributeByName(node, name)

    Set getAttributeByName = Nothing

    Dim attr
    For Each attr In node.Attributes
        If attr.baseName = name Then
            Set getAttributeByName = attr
            Exit Function
        End If
    Next

End Function

Function getElementByTagName(node, name)

    Set getElementByTagName = Nothing

    Dim lst
    Set lst = node.getElementsByTagName(name)
    If lst.Length < 1 Then Exit Function

    Set getElementByTagName = lst.Item(0)

End Function

Function get_dom(path)

    Dim dom
    Set dom = CreateObject("Msxml2.DOMDocument")

    Dim res
    res = dom.Load(path)

    If res Then
        Set get_dom = dom
    Else
        Set get_dom = Nothing
    End If

End Function