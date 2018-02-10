

Set-Location -Path $PSScriptRoot;

if (![IO.File]::Exists('7za.exe')){
  Invoke-WebRequest -Uri 'https://chocolatey.org/7za.exe' -OutFile '7za.exe'
}

if (![IO.File]::Exists('mod_spatialite-4.3.0a-win-amd64.7z')){
  Invoke-WebRequest -Uri 'http://www.gaia-gis.it/gaia-sins/windows-bin-amd64/mod_spatialite-4.3.0a-win-amd64.7z' -OutFile 'mod_spatialite-4.3.0a-win-amd64.7z'
}

if (![IO.Directory]::Exists('mod_spatialite-4.3.0a-win-amd64')){
  Start-Process -FilePath 7za.exe -ArgumentList 'e mod_spatialite-4.3.0a-win-amd64.7z -o"mod_spatialite-4.3.0a-win-amd64"' -Wait -NoNewWindow
}
