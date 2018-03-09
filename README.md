This is the source code (but not the content) for http://cppquiz.org

Both this code and the contents of the site are licensed under a Creative Commons Attribution-ShareAlike 4.0 International License:
http://creativecommons.org/licenses/by-sa/4.0/

# Contributing

## Setting up the environment
Note: CppQuiz is still running on Python 2.7
- Clone this repository
- Install Django 1.11 (Using Virtualenv is recommended)
- `cp cppquiz/local_settings_example.py cppquiz/local_settings.py`, then edit at least `/path/to/your/code`
- Read the Django docs
- `python manage.py migrate`
- `python manage.py createsuperuser`
- `python manage.py runserver`
- `python manage.py create_questions 10` (Or whatever number, just so you have some dummy questions)

## Testing
### Setting up
- `pip install mock`
- `pip install markdown`
- `pip install six` If you're on OS X and get an error about importing `wraps`, see http://stackoverflow.com/questions/31417964/importerror-cannot-import-name-wraps

### Unit tests
- `./manage.py test`

### System tests
The system tests are currently not maintained. If you want to have a go, you need at least `pip install lettuce` and `pip install splinter`. Then try to get `./run_lettuce` to work.

## Deployment
- `pip install fabric`
- Bump the version in `templates.base.html` (this should be scripted)
- `fab beta`
- Check `http://beta.cppquiz.org/`
- `fab production`
