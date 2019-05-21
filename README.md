This is the source code (but not the content) for http://cppquiz.org

Both this code and the contents of the site are licensed under a Creative Commons Attribution-ShareAlike 4.0 International License:
http://creativecommons.org/licenses/by-sa/4.0/

# Contributing

## Setting up the environment
Note: CppQuiz is still running on Python 2.7
- Clone this repository
- (We recommend using Virtualenv)
- `pip install -r requirements.txt`
- `cp cppquiz/local_settings_example.py cppquiz/local_settings.py`, then edit at least `/path/to/your/code`
- `python manage.py migrate`
- `python manage.py createsuperuser`
- `python manage.py create_questions 10` (Or whatever number, just so you have some dummy questions)
- `python manage.py runserver`
- Click the link displayed to go to the site. Visit `/admin` to log in with the superuser you created above.

## Testing

### Unit tests
- `python manage.py test`

### System tests
The system tests are currently not maintained. If you want to have a go, you need at least `pip install lettuce` and `pip install splinter`. Then try to get `./run_lettuce` to work.

## Deployment
- `pip install fabric`
- Bump the version in `templates.base.html` (this should be scripted)
- `fab beta`
- Check `http://beta.cppquiz.org/`
- `fab production`
