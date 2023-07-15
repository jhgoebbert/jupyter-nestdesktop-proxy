import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel('INFO')

HERE = os.path.dirname(os.path.abspath(__file__))


def get_nestdesktop_executable(prog):
    from shutil import which

    # Find prog in known locations
    other_paths = [
        os.path.join('/opt/nestdesktop/bin', prog),
    ]

    wp = os.path.join(HERE, 'bin', prog)
    if os.path.exists(wp):
        return wp

    if which(prog):
        return prog

    for op in other_paths:
        if os.path.exists(op):
            return op

    if os.getenv("NESTDESKTOP_BIN") is not None:
        return os.getenv("NESTDESKTOP_BIN")

    raise FileNotFoundError(f'Could not find {prog} in PATH')


def _nestdesktop_mappath(path):

    # always pass the url parameter
    if path in ('/', '/index.html', ):
        path = '/index.html' 

    return path


def setup_nestdesktop():
    """ Setup commands and and return a dictionary compatible
        with jupyter-server-proxy.
    """

    # launchers url file including url parameters
    path_info = 'nestdesktop/index.html' + _nestdesktop_urlparams()

    # create command
    cmd = [
        get_nestdesktop_executable('nest-desktop'),
        '-h localhost',
        '-p {port}',
    ]
    logger.info('NEST Desktop command: ' + ' '.join(cmd))

    return {
        'command': cmd,
        'mappath': _nestdesktop_mappath,
        'absolute_url': False,
        'timeout': 90,
        'new_browser_tab': True,
        'launcher_entry': {
            'enabled': True,
            'icon_path': os.path.join(HERE, 'icons/nestdesktop-logo.svg'),
            'title': 'NEST Desktop',
            'path_info': path_info,
        },
    }
