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


def _nestdesktop_urlparams():

    nestsrv_urlparam = None
    if _nestsrv_url:
        nestsrv_urlparam = 'nest_server_url=' + _nestsrv_url
    nestsrv_tokenparam = None
    if _nestsrv_token:
        nestsrv_tokenparam = 'nest_server_access_token=' + _nestsrv_token

    url_params = ''
    url_paramlist = [param for param in (nestsrv_urlparam, nestsrv_tokenparam) if param is not None]
    if url_paramlist:
        url_params = '?' + '&'.join(url_paramlist)

    return url_params

def _nestdesktop_mappath(path):

    # always pass the url parameter
    if path in ('/', '/index.html', ):
        url_params =  _nestdesktop_urlparams()
        path = '/index.html' + url_params 

    return path


def setup_nestdesktop():
    """ Setup commands and and return a dictionary compatible
        with jupyter-server-proxy.
    """
    from re import sub
    from tempfile import mkstemp
    from random import choice
    from string import ascii_letters, digits
    from urllib.parse import urlparse

    global _nestsrv_url, _nestsrv_token

    # check for a free port
    import socket
    s=socket.socket()
    s.bind(("", 0))
    nestsrv_port = s.getsockname()[1]
    s.close()

    # token generator
    def _get_random_alphanumeric_string(length):
        letters_and_digits = ascii_letters + digits
        return (''.join((choice(letters_and_digits) for i in range(length))))

    _nestsrv_token = _get_random_alphanumeric_string(16)
    try:
        fd_nestsrv_token, fpath_nestsrv_token = mkstemp()
        logger.info('Created secure token file for NEST Server: ' + fpath_nestsrv_token)

        with open(fd_nestsrv_token, 'w') as f:
            f.write(_nestsrv_token)

    except Exception:
        logger.error("Passwd generation in temp file FAILED")
        raise FileNotFoundError("Passwd generation in temp file FAILED")

    # generate nest-server url
    jhub_domain = os.environ.get('JUPYTERHUB_DOMAIN')
    jlab_urlprefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX')
    if jhub_domain and jlab_urlprefix:
        _nestsrv_url = (
            "https://" +
            sub(r'/+', '/', '/'.join([
                jhub_domain,
                jlab_urlprefix,
                'proxy',
                str(nestsrv_port)
            ]))
        )
    else:
        _nestsrv_url = 'http://localhost:' + str(nestsrv_port)
 
    # launchers url file including url parameters
    path_info = 'nestdesktop/index.html' + _nestdesktop_urlparams()

    # create command
    cmd = [
        get_nestdesktop_executable('nest-desktop'),
        'start',
        '-h', 'localhost',
        '-p', '{port}',
        '--srv-start',
        '--srv-auth', 'file:filename=' + fpath_nestsrv_token,
        '--srv-port', str(nestsrv_port),
        #    '--srv-log' nestsrv_logfile # default: /tmp/nest-server-$USER-$$.log
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
