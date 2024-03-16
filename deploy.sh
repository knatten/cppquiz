function header()
{
    echo
    echo ------------------------------
    echo $1
    echo ------------------------------
}
source ../venv/bin/activate || exit $?
header "Versions"
echo -n "python: "
which python || exit $?
python --version || exit $?
echo -n "Django version: "
python -c "import django; print(django.__version__)"

header "Upgrading pip packages"
pip install -r requirements.txt || exit $?
echo "Django version is now: "
python -c "import django; print(django.__version__)" || exit $?

header "Migrating"
python manage.py migrate || exit $?

header "Collecting static"
python manage.py collectstatic --noinput || exit $?

header "Restarting"
mkdir -p ../tmp || exit $?
touch ../tmp/restart.txt || exit $?
