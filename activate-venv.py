#To activate a virtual environment from within a Python script, you can use the venv module

import subprocess
import sys
import os
import venv

# Define the path to the virtual environment
venv_path = "/root/rcx-devops/infrastructure/jenkins/dcf/venv"

# Activate the virtual environment
activate_script = os.path.join(venv_path, "bin", "activate_this.py")
exec(open(activate_script).read(), {"__file__": activate_script})

# Run the desired command within the virtual environment
command = f"flask --version"
subprocess.run(command, shell=True)
