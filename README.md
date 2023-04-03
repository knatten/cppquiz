This is the source code (but not the content) for https://cppquiz.org

Both this code and the contents of the site are licensed under a Creative Commons Attribution-ShareAlike 4.0 International License:
http://creativecommons.org/licenses/by-sa/4.0/

![Build Status](https://github.com/knatten/cppquiz/actions/workflows/ci.yml/badge.svg)

# Requirements
- Python 3.8 or higher
- CppQuiz is only tested on Ubuntu and MacOS, but will probably work on many other OSes as well

# Contributing

Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

# Running the code locally

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

- `python manage.py test`

## Formatting
All code is formatted with `autopep8` and checked in CI. To format your code, run `./ci/format.sh --fix`

## Adding / upgrading dependencies
- Add any new dependencies to `requirements.in`
- Run `pip-compile --upgrade requirements.in`

## Deployment
- Check out the branch you want to deploy
- Run ./deploy.sh
