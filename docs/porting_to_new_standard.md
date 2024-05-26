### Porting to new standard

When porting the questions to a new standard, use the previous issues https://github.com/knatten/cppquiz/issues/77 and https://github.com/knatten/cppquiz/issues/293 for inspiration.

The main steps are as follows, see previous issues for details:
- Create a porting repository (previously, we've used https://github.com/knatten/cppquiz17 and https://github.com/knatten/cppquiz23)
- Copy the md files from the previous such repository to the new one
- In the main cppquiz repo, export the questions: `python manage.py export_questions_to_repo <path to porting repo>`
- Create a [personal access token](https://github.com/settings/tokens?type=beta) with permissions to create issues in the porting repo
- In the main cppquiz repo, auto-generate issues: `python manage.py create_issues <user name> <porting repo name> <access token>`
- Copy the `.github/pull_request_template.md` pull request template from a previous porting repo to the new one
- Use the porting repo to port all the questions (see previous porting issues)
- In the main cppquiz repo, import the updated questions: `python manage.py update_questions_from_repo <path to porting repo>`
