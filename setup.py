from cx_Freeze import setup, Executable

base = None    

executables = [Executable("index1.py", base=base)]

packages = ["idna","sys","os"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "<lib1>",
    options = options,
    version = "0.1",
    description = 'library managment system',
    executables = executables
)