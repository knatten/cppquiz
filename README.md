This is the source code (but not the content) for http://cppquiz.org

Both this code and the contents of the site are licensed under a Creative Commons Attribution-ShareAlike 4.0 International License:
http://creativecommons.org/licenses/by-sa/4.0/

[![Build Status](https://knatten.visualstudio.com/CppQuiz/_apis/build/status/knatten.cppquiz?branchName=master)](https://knatten.visualstudio.com/CppQuiz/_build/latest?definitionId=1&branchName=master)

# Requirements
- Python 3.6 or 3.7
- CppQuiz is only tested on Ubuntu and MacOS, but will probably work on many other OSes as well

# Contributing

## Setting up the environment
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
- If applicable: `./bump_version.sh <version>` (e.g `./bump_version 1.11`)
- The above script prompts you to make a PR and tag the release, do this.
- `./deploy.sh beta`
- Check `http://beta.cppquiz.org/`
- `./deploy.sh prod`
