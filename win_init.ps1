# Sets up a virtual environment and runs pip for all dependencies.

# Dependencies
$deps = @{
	'lxml' = '3.5.0'
	'requests' = '2.9.1'
	'wheel' = '0.29.0'
	'pip' = '8.0.2'
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
$lxmlNeedsUpdate = $false
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
			$lxmlNeedsUpdate = $true
		}
		else {
			Write-Host "Installing dependency $($d) ($($deps[$d]))."
			&python -m pip install $d==$($deps[$d]) --disable-pip-version-check
		}
	}
	else {
		Write-Host "Dependency $($d) ($($deps[$d])) already installed."
	}
}
if ($lxmlNeedsUpdate) {
	# Had to ensure wheel was installed first, now install the wheel file
	Write-Host 'Installing lxml...'
	$whl = 'lxml-3.5.0-cp35-none-win_amd64.whl'
	&python -m pip install $($whl) --disable-pip-version-check
}
Write-Host 'Initialization complete, use "deactivate" to leave the virtual environment.'
