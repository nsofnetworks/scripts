# ##########################################
#this script will provide the option to enable ipv6 on windows client, UAC will pop up if the script isn't runing with admin permissions
# Determine if we have Administrator rights
Write-Host 'Checking user permissions... '
$windowsID = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$windowsSecurityPrincipal = New-Object System.Security.Principal.WindowsPrincipal($windowsID)
$adminRole = [System.Security.Principal.WindowsBuiltInRole]::Administrator

If (!($windowsSecurityPrincipal.IsInRole($adminRole))) {
    Write-Warning 'Current user does not have Administrator rights'
    Write-Host 'Attempting to copy files to temporary location and restarting script'

    # Get random file name
    Do {
        $temp = [System.IO.Path]::GetTempPath() + [System.IO.Path]::GetRandomFileName()
    } Until (!(Test-Path -LiteralPath "$temp"))

    # Create directory
    Write-Host 'Creating temp directory... ' -NoNewLine
    New-Item -Path "$temp" -ItemType 'Directory' | Out-Null
    Write-Host 'done.'

    # Copy script to directory
    Write-Host 'Copying script to temp directory... ' -NoNewLine
    Copy-Item -LiteralPath "$($myInvocation.MyCommand.Path)" "$temp" | Out-Null
    Write-Host 'done.'
    $newScript = "$($temp)\$($myInvocation.MyCommand.Name)"

    # Start new script elevated
    Write-Host 'Starting script as administrator... ' -NoNewLine
    $adminProcess = New-Object System.Diagnostics.ProcessStartInfo
    $adminProcess.Filename = ([System.Diagnostics.Process]::GetCurrentProcess()).Path
    $adminProcess.Arguments = " -File `"$newScript`""
    $adminProcess.Verb = 'runas'

    Try {
        [System.Diagnostics.Process]::Start($adminProcess) | Out-Null
    }
    Catch {
        Write-Error 'Could not start process'
        Exit 1
    }
    Write-Host 'done.'
    Exit 0
}
Add-Type -AssemblyName PresentationCore,PresentationFramework
$registryPath = "HKCU:\Software\ScriptingGuys\Scripts"
$registryPath = "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters"
$Name = "DisabledComponents"
$value = 0
Set-ItemProperty -Path $registryPath -Name $name -Value $value -Force 
$msgBoxInput =  [System.Windows.MessageBox]::Show('IPV6 enabled! Would you like to reboot now?','Meta','YesNoCancel','Question')
    switch  ($msgBoxInput) {
        'Yes' {
        Restart-Computer
        }
        'No' {
        }
        'Cancel' {
        }
    }
 
