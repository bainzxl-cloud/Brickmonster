Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class Win32 {
  [DllImport("user32.dll")]
  public static extern void keybd_event(byte bVk, byte bScan, int dwFlags, int dwExtraInfo);
}
'@

# VK_MEDIA_PLAY_PAUSE = 0xB3, KEYEVENTF_KEYUP=0x2
[Win32]::keybd_event(0xB3, 0, 0, 0)
Start-Sleep -Milliseconds 50
[Win32]::keybd_event(0xB3, 0, 2, 0)
