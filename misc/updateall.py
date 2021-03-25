updaters = [
	'busybox',
	'lessmsi',
	'nmap-portable'
]

for updater in updaters:
	print("===> {0}".format(updater))
	exec(open('update-' + updater + '.py').read())