import os.path as op

from fabric.api import local, put, run, env, cd
from fabric.contrib.files import upload_template
from fabric.contrib.project import rsync_project
import fabtools
from fabtools import require

import deploy_settings as settings


THIS_DIR = op.abspath(op.dirname(__file__))
env.hosts = [settings.host]
static_root = op.join(settings.deploy_dir, 'var', 'static')
var_run_dir = op.join(settings.deploy_dir, 'var', 'run')
gunicorn_bind = 'unix:%s' % op.join(var_run_dir, 'gunicorn.sock')
venv_dir = op.join(settings.deploy_dir, 'venv')
project_dir = op.join(settings.deploy_dir, 'project')
files_dir = op.join(settings.deploy_dir, 'files')


def setup():
    """
    Prepare a host to deploy leechy.
    """
    # Create directories
    run('mkdir -p %s' % static_root)
    run('mkdir -p %s' % var_run_dir)
    run('mkdir -p %s' % project_dir)
    # Install system dependencies
    require.deb.packages(['python-dev', 'build-essential', 'memcached',
        'libevent-dev', 'libpq-dev'])
    # Setup postgres
    require.postgres.server()
    require.postgres.user(settings.db_user, settings.db_password)
    require.postgres.database(settings.db_name, settings.db_user)
    # Setup nginx
    require.nginx.server()
    require.nginx.proxied_site(settings.url, port=settings.port, 
            proxy_url='http://%s' % gunicorn_bind, docroot=static_root)
    # Setup supervisor processes
    python_bin = op.join(venv_dir, 'bin', 'python')
    gunicorn_bin = op.join(venv_dir, 'bin', 'gunicorn_django')
    gunicorn_conf = op.join(project_dir, 'gunicorn.conf.py')
    require.supervisor.process('leechy',
        command='%s -c %s -b %s' % (gunicorn_bin, gunicorn_conf,
            gunicorn_bind),
        directory=project_dir,
        user=settings.user)
    require.supervisor.process('leechy-cache',
        command='%s manage.py update_leechy_cache' % python_bin,
        directory=project_dir,
        user=settings.user)


def deploy():
    """
    Deploy leechy on a host.
    """
    # Make a source distribution and upload it
    local('python setup.py sdist')
    version = local('python setup.py --version', capture=True)
    pkg_name = 'leechy-%s.tar.gz' % version
    put('dist/%s' % pkg_name, settings.deploy_dir)
    # Upload requirements and project
    put('requirements.txt', settings.deploy_dir)
    rsync_project(project_dir, 'project/',
            exclude=['*.pyc', '*.swp'])
    # Upload project settings override
    upload_template('deploy_settings/project_settings.py', 
            op.join(project_dir, 'deploy_settings.py'), {
                'db_name': settings.db_name,
                'db_user': settings.db_user,
                'db_password': settings.db_password,
                'static_root': static_root,
                'files_dir': files_dir,
            })
    with fabtools.python.virtualenv(venv_dir):
        # Install leechy and requirements
        require.python.requirements(op.join(settings.deploy_dir,
            'requirements.txt'))
        run('pip install --ignore-installed %s' % 
                op.join(settings.deploy_dir, pkg_name))
        # Collect statics
        with cd(project_dir):
            run('python manage.py collectstatic --noinput')
    # Restart supervisor processes
    fabtools.supervisor.update_config()
    fabtools.supervisor.restart_process('leechy')
    fabtools.supervisor.restart_process('leechy-cache')
