# types and validation
# https://fastapi.tiangolo.com/environment-variables/#types-and-validation

###### any value read in Python from an environment variable will be a str, and any conversion to a different type or any validation has to be done in code.

# PATH environment variables
# The value of the variable `PATH` is a long string that is made of directories separated by a color `:`
# on LinuX and macOS and by `;` a semicolon on windows.

'''
for instance 
, the PATH environment variable could look like this:


Linux, macOS
Windows

/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
This means that the system should look for programs in the directories:

/usr/local/bin
/usr/bin
/bin
/usr/sbin
/sbin

When you type a command in the terminal, the operating system looks for the program in each of those directories listed in the PATH environment variable.

For example, when you type python in the terminal, the operating system looks for a program called python in the first directory in that list.

If it finds it, then it will use it. Otherwise it keeps looking in the other directories.
'''

