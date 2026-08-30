param([Parameter(Mandatory=$true)][string]$In, [string]$Out)
$ErrorActionPreference = 'Stop'
$in = (Resolve-Path $In).Path
if (-not $Out) { $Out = [System.IO.Path]::ChangeExtension($in, '.pdf') }
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
  $doc = $word.Documents.Open($in, $false, $true)
  $doc.SaveAs([ref]$Out, [ref]17)  # wdFormatPDF
  $doc.Close($false)
  Write-Output "PDF: $Out"
} finally {
  $word.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
