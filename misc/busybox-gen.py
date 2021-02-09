import os

directory = "busybox_commands"

if not os.path.exists(directory):
    os.makedirs(directory)

with open("busybox-gen_cmds.txt", 'r') as f:
    commands = f.readlines()
commands = [x.strip() for x in commands]

for command in commands:
    filename = "busybox-" + command + ".json"
    
    with open("busybox-gen_template.json", 'r') as f:
        template = f.read().replace("_COMMAND_", command)
    
    with open(os.path.join(directory, filename), 'w') as file:
        file.write(template)

