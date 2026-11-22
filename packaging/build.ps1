param(
    [string]$Compiler = 'ISCC.exe',
    [string]$Python = '.venv-neptune\Scripts\python.exe'
)

$ErrorActionPreference = 'Stop'
Push-Location (Split-Path -Parent $PSScriptRoot)
try {
    $version = & $Python -c 'from src import __version__; print(__version__)'
    if ($LASTEXITCODE -ne 0 -or $version -notmatch '^\d+\.\d+\.\d+$') {
        throw 'Could not read the Neptune version.'
    }

    New-Item -ItemType Directory -Force dist/tools, dist/payload | Out-Null
    $archive = 'dist/tools/python-embed.zip'
    if (-not (Test-Path -LiteralPath $archive)) {
        Invoke-WebRequest -UseBasicParsing 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip' -OutFile $archive
    }
    if ((Get-FileHash -LiteralPath $archive).Hash -ne '009D6BF7E3B2DDCA3D784FA09F90FE54336D5B60F0E0F305C37F400BF83CFD3B') {
        throw 'Embedded Python ZIP checksum mismatch.'
    }

    Expand-Archive -LiteralPath $archive -DestinationPath dist/payload -Force
    & $Python -m pip download --no-deps pip==26.0.1 -d dist/tools
    if ($LASTEXITCODE -ne 0) { throw 'Could not download the pip wheel.' }
    & $Python -m pip wheel --no-deps docopt==0.6.2 -w dist/tools
    if ($LASTEXITCODE -ne 0) { throw 'Could not build the docopt wheel.' }

    $pipWheel = 'pip-26.0.1-py3-none-any.whl'
    Copy-Item -Path "dist/tools/$pipWheel", 'dist/tools/docopt-0.6.2-py2.py3-none-any.whl' -Destination dist/payload
    Copy-Item -Path packaging/install_dependencies.py, packaging/requirements-windows.txt -Destination dist/payload
    @('python311.zip', '.', 'Lib\site-packages', $pipWheel, 'import site') |
        Set-Content -Encoding ascii dist/payload/python311._pth

    & $Compiler "/DVersion=$version" packaging/neptune.iss
    if ($LASTEXITCODE -ne 0) { throw 'Inno Setup compilation failed.' }

    $file = Get-Item "dist/Neptune-$version-Windows-x64-Setup.exe"
    $sha = (Get-FileHash -LiteralPath $file.FullName).Hash.ToLowerInvariant()
    "$sha  $($file.Name)" | Set-Content -Encoding ascii "dist/$($file.BaseName).sha256"
    $file
}
finally {
    Pop-Location
}
