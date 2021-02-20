import json
import os
import urllib.request

manifest_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'bucket', 'nmap-portable.json')
upstream = "https://raw.githubusercontent.com/ScoopInstaller/Main/master/bucket/nmap-portable.json"

# Read current version from existing manifest
version_existing = json.load(open(manifest_path, mode='r'))['version']

with urllib.request.urlopen(upstream) as url:
    data = json.loads(url.read().decode())
    version_current = data['version']

    if version_current != version_existing:
        print("New version {0} detected (current version {1}). Will update the manifest...".format(version_current, version_existing))
        del data['shortcuts']  # Remove shortcuts
        target = open(manifest_path, "w")
        target.write(json.dumps(data, indent=4, sort_keys=False) + "\n")
        target.close()
    else:
        print("No new version detected. Will not update the manifest. ")
