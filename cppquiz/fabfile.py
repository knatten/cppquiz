from fabric.api import cd, run, env, local

env.hosts = ['cppquiz.org']
env.user = 'riktigbil'

directory = '/home/riktigbil/webapps/cppquiz/cppquiz/cppquiz'

def pull():
    sshagent_run('git pull')

def deploy():
    pull()
    sshagent_run('python2.7 manage.py migrate')
    sshagent_run('python2.7 manage.py collectstatic --noinput')
    sshagent_run('../../apache2/bin/restart')


def sshagent_run(cmd):
    """
    Stolen from http://lincolnloop.com/blog/2009/sep/22/easy-fabric-deployment-part-1-gitmercurial-and-ssh/ 
    Helper function.
    Runs a command with SSH agent forwarding enabled.
    
    Note:: Fabric (and paramiko) can't forward your SSH agent. 
    This helper uses your system's ssh to do so.
    """

    for h in env.hosts:
        try:
            # catch the port number to pass to ssh
            host, port = h.split(':')
            local('ssh -p %s -A %s@%s "cd %s; %s"' % (port, env.user, host, directory, cmd))
        except ValueError:
            local('ssh -A %s@%s "cd %s; %s"' % (env.user, h, directory, cmd))
