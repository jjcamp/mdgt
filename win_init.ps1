# Sets up a virtual environment and runs pip for all dependencies.

# Get dependencies from requirements.txt
$depsFile = Get-Content "requirements.txt"
$deps = @{}
$depsFile | % {
    # As of this time, all dependencies are treated as '=='
    if ($_ -match '^(?<pkg>\w*)[\s=<>]*(?<ver>.*)$') {
        $deps.add($matches['pkg'], $matches['ver'])
    }
}

Write-Host 'Checking for virtual environment...'
if (!(Test-Path 'venv')) {
	'Virtual environment not found, creating...'
	python -m venv venv
}
else {
	'Virtual environment found.'
}

Write-Host 'Loading virtual environment...'
.\venv\Scripts\Activate.ps1

Write-Host 'Checking for dependencies...'
$instDepsOut = pip list --disable-pip-version-check
$instDeps = @{}
$needMdgtDev = $false
$instDepsOut | % {
	$_ -match '(?<pkg>.*?)\s*?\((?<ver>.*?)\)' | Out-Null
	if (($matches.containsKey('pkg')) -and ($matches.containsKey('ver'))) {
		$instDeps.add($matches['pkg'], $matches['ver'])
	}
}
ForEach ($d in $deps.KEYS.GetEnumerator()) {
	if (!($instDeps.containsKey($d)) -and ($instDeps[$d] -ne $deps[$d])) {
		# If the package is lxml, do not update yet, but set a flag for later
		if ($d -eq 'lxml') {
			Write-Host 'Installing lxml from included .whl file...'
            $whl = 'lxml-3.5.0-cp35-none-win_amd64.whl'
	        &python -m pip install $($whl) --disable-pip-version-check
		}
        elseif ($d -eq 'setuptools') {
            Write-Host 'Installing setuptools...'
            (Invoke-WebRequest https://bootstrap.pypa.io/ez_setup.py).Content | python -
        }
        elseif ($d -eq 'pip') {
            &python -m pip install --upgrade pip
        }
		else {
			Write-Host "Installing dependency $($d) ($($deps[$d]))."
			&python -m pip install $d==$($deps[$d]) --disable-pip-version-check
		}
	}
    # Install mdgt in development mode if not already done
    elseif (!$instDeps.containsKey('mdgt')) {
        $needMdgtDev = $true
    }
}
if ($needMdgtDev) {
    Write-Host "Installing mdgt as a development package..."
    &python setup.py develop
}
Write-Host 'Initialization complete, use "deactivate" to leave the virtual environment.'
