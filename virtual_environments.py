# source: https://fastapi.tiangolo.com/virtual-environments/#create-a-project

# Create a virtual environment
'''
`python -m venv .venv`

# python: use the program called python
# -m: call a module as a script, we'll tell it which module next
# venv: use the module called venv that normally comes installed with Python
# .venv: create the virtual environment in the new directory .venv
'''

# Activate the virtiual environment
# on Linux and macOS
'''
source ./venv/bin/activate
'''

# Check the virtual environment is active
# on Linux and macOS
'''
which python

If it shows the python binary at .venv/bin/python, inside of your project (in this case awesome-project), then it worked. 🎉
'''

# Upgrade pip 
'''
python -m pip install --upgrade pip

note: Many exotic errors will while installing a packages are solved bu just upgradong `pip` first
'''

# Add `.gitignore`
'''
if you are using git, add a .gitignore file to exclude everything in your `.env` from Git.


echo "*" > .venv/.gitignore

# echo "*": will "print" the text * in the terminal (the next part changes that a bit)
# >: anything printed to the terminal by the command to the left of > should not be printed but instead written to the file that goes to the right of >
# .gitignore: the name of the file where the text should be written
# And * for Git means "everything". So, it will ignore everything in the .venv directory.

That command will create a file .gitignore with the content: `*`
'''

# Install packages

# install packages directly
'''
pip install <module>
'''

# install packages from `requirements.txt`
# if we have a `requirements.txt`, we can use the following command to install its packages.
'''
pip install -r requirements.txt

requirements.txt file could look like:
fastapi[standard]==0.113.0
pydantic==2.8.0
'''

# Run the program
'''
After you activated the virtual environment, you can run your 
program, and it will use the Python inside of your virtual
environment with the packages you installed there.

python <filename.py>
'''

# Configure the editor
'''
 source: https://fastapi.tiangolo.com/virtual-environments/#configure-your-editor
# VS Code
# PyCharm
'''

# Deactivate the virtual environment
# to deactivate our virtual environment
'''
deactivate
'''


# Why virtual environments
'''
source: https://fastapi.tiangolo.com/virtual-environments/#why-virtual-environments
'''

## the problem:
'''
source: https://fastapi.tiangolo.com/virtual-environments/#the-problem
'''

