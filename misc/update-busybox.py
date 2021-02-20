import glob
import json
import os
import urllib.request

bucket_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'bucket')
manifest_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'bucket', 'busybox-standalone.json')
shim_template_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'busybox_shim_template.json')
upstream = "https://raw.githubusercontent.com/ScoopInstaller/Main/master/bucket/busybox.json"
additional_description = ". This is a standalone version which will not create aliases. Please install busybox-<command> to add desired aliases. "

# Read current version from existing manifest
version_existing = json.load(open(manifest_path, mode='r'))['version']

with urllib.request.urlopen(upstream) as url:
    data = json.loads(url.read().decode())
    version_current = data['version']
    busybox_bins = data['bin']

    if version_current != version_existing:
        print("New version {0} detected (current version {1}). Will update the manifest...".format(version_current, version_existing))

        data['description'] += additional_description  # Add additional description to the original description
        data['bin'] = busybox_bins[0]  # Clear busybox shims/aliases

        # Update busybox-standalone manifest
        target = open(manifest_path, 'w')
        target.write(json.dumps(data, indent=4, sort_keys=False) + "\n")
        target.close()

        # Count existing shim manifests
        existing_shims = []
        for shim in glob.glob(os.path.join(bucket_path, 'busybox-*.json')):
            shim_name = shim.replace(bucket_path, '').replace('\\busybox-', '').replace('.json', '')
            if shim_name != 'standalone':
                existing_shims.append(shim_name)

        # Generate shim-only manifests
        for shim in busybox_bins:
            if isinstance(shim, list):
                shim_name = shim[1]
                if shim_name in existing_shims:
                    existing_shims.remove(shim_name)
                else:  # Write generated template to file
                    target = open(os.path.join(bucket_path, "busybox-{0}.json".format(shim_name)), 'w')
                    target.write(open(shim_template_path, 'r').read().replace('_COMMAND_', shim_name))
                    print("New shim \"{0}\" is created. Filename: \'busybox-{0}.json\'".format(shim_name))
                    target.close()

        for outdated_shim in existing_shims:
            shim_path = os.path.join(bucket_path, "busybox-{0}.json".format(outdated_shim))
            if os.path.exists(shim_path):
                os.remove(shim_path)
                print("Old shim \"{0}\" is removed. Filename: \'busybox-{0}.json\'".format(outdated_shim))
    else:
        print("No new version detected. Will not update the manifest. ")
