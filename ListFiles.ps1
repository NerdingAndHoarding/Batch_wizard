# ListFiles.ps1
param(
    [string]$Folder = ".",
    [string]$OutputFile = "file_list.txt"
)

# Get all files in the folder and subfolders, then write names to text
Get-ChildItem -Path $Folder -File -Recurse |
    Select-Object -ExpandProperty FullName |
    Out-File -FilePath $OutputFile -Encoding UTF8

Write-Host "File list saved to $OutputFile"
