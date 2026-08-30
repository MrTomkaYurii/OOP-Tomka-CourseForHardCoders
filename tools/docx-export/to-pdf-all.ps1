param([string]$Dir = "$PSScriptRoot\..\..\output\labs")
$ErrorActionPreference = 'Stop'
$dir = (Resolve-Path $Dir).Path
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
  Get-ChildItem $dir -Filter *.docx | Sort-Object Name | ForEach-Object {
    $out = [System.IO.Path]::ChangeExtension($_.FullName, '.pdf')
    $doc = $word.Documents.Open($_.FullName, $false, $true)
    $doc.SaveAs([ref]$out, [ref]17)
    $doc.Close($false)
    Write-Output ("  {0} -> pdf" -f $_.Name)
  }
} finally {
  $word.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
