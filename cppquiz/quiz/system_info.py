import os
import importlib
import cppquiz.settings

def get_system_info():
    root_dir = os.path.dirname(
        os.path.dirname(
            cppquiz.settings.__file__))
    req_file = os.path.join(root_dir, 'requirements.txt')

    info = {'packages':[]}
    with open(req_file) as f:
        contents = f.read()
        for line in contents.split():
            package, version = line.split("==")
            mod = importlib.import_module(package.lower())
            actual_version = get_version(mod)
            info['packages'].append({
                'name':package,
                'desired_version': version,
                'actual_version': actual_version,
                'path':mod.__file__})
    return info

def get_version(module):
    try:
        if module.__name__ == 'pbr':
            return "n/a"
        if module.__name__ == 'markdown':
            return module.version
        return module.__version__
    except AttributeError:
        return "n/a"
