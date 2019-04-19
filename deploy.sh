#!/bin/bash
# This shell file deploys a new version to our server.

# since the server setup is not complete, let's just exit with success:
exit 0

eval "$(ssh-agent -s)" # Start ssh-agent cache
chmod 600 ~/.ssh/emu_rsa # Allow read access to the private key
ssh-add ~/.ssh/emu_rsa # Add the private key to SSH

echo "SSHing to PythonAnywhere."
ssh gcallah@ssh.pythonanywhere.com << EOF
    cd /home/gcallah/Emu86
    /home/gcallah/Emu86/myutils/rebuild.sh
EOF

