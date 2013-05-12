from fabric.api import cd, run, env, local

env.hosts = ['cppquiz.org']
env.user = 'riktigbil'


def production():
    deploy('/home/riktigbil/webapps/cppquiz/cppquiz/cppquiz')

def test():
    deploy('/home/riktigbil/webapps/cppquiz_beta/cppquiz/cppquiz')

def deploy(directory):
    pull(directory)
    sshagent_run('python2.7 manage.py migrate', directory)
    sshagent_run('python2.7 manage.py collectstatic --noinput', directory)
    sshagent_run('../../apache2/bin/restart', directory)

def pull(directory):
    sshagent_run('git pull', directory)

def sshagent_run(cmd, directory):
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
