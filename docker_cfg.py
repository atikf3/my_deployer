import urllib.request
import io
import config
from logzero import logger

__author__ = 'talamo_a'


def command_exist(con, cmd):
    """ checks if a command exists """
    try:
        logger.debug('Checking if ' + cmd + ' is installed.')
        (stdin, stdout, stderr) = con.exec_command('command -v ' + cmd)
        return not stdout.channel.recv_exit_status()
    except Exception:
        logger.exception('Failed to run command_exists')


def check_docker_install(con):
    """ checks if docker is installed """
    logger.debug('lookign for docker installation.')
    return command_exist(con, 'docker')


def check_version(con):
    """ checks docker version """
    """ example : Docker version 19.03.13, build 4484c46d9d """
    logger.debug('fetching docker version..')
    (stdin, stdout, stderr) = con.exec_command('docker -v')
    ver = stdout.read().decode('ascii').strip("\n")
    return ver.split(" ")[2].split('.')[0:2]


def need_upgrade(con):
    """ determines if we need a major and/or minor upgrade """
    ver = check_version(con)
    logger.debug('checking if we need to upgrade...')
    return int(ver[0]) < config.d_ver_maj or \
        (int(ver[0]) == int(config.d_ver_maj) and
         int(ver[1]) < int(config.d_ver_min))


def install_docker(con, username):
    """ installs docker """
    logger.info('Installing docker from get.docker.com')
    try:
        r = urllib.request.urlopen(config.d_url).read()
        script = r.decode("utf-8")
        # script.replace('$user', '$USER')
    # con.exec_command('cat <<EOF > /tmp/get.docker.sh\n' + script + '\nEOF')
        ftp = con.open_sftp()
        ftp.putfo(io.BytesIO(script.encode()), config.d_script_path)
        ftp.close()
        logger.debug('Sent script to server, path: ' + config.d_script_path)
        cmd = config.d_script_path + ' &> ' + config.d_script_log
        con.exec_command('chmod +x ' + cmd)
        if config.d_ver_latest:
            logger.debug('Installing latest version...')
        else:
            ver_str = config.d_ver_maj + '.' + config.d_ver_min
            logger.info('Installing version ' + ver_str)
            cmd = 'VERSION=' + ver_str + ' ' + cmd
        (stdin, stdout, stderr) = con.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            logger.info('Installation ended.')
            if not username == 'root':
                con.exec_command('sudo usermod -aG docker ' + username)
            return True
        else:
            if not check_docker_install(con):
                logger.error('Installation failed, return code: %d' %
                             exit_status)
                res = stderr.read().decode('ascii')
                logger.error('Install log:\n%s' % res)
                return False
            else:
                return True
    except urllib.error.URLError as e:
        logger.exception(e)
        raise SystemExit(e)


def init(con, user, installCount=1):
    """ init docker configuration """
    logger.info('Initializing docker configuration..')
    logger.debug('Checking for docker installation...')
    if not check_docker_install(con):
        logger.info('Docker is not installed!')
        if not install_docker(con, root):
            logger.warning(
                'Install docker did not ended successfully...')
            if installCount < 4:
                logger.warning(
                    'retrying install (' + str(installCount) + '/3) ...')
                init(con, user, installCount + 1)
            else:
                logger.error(
                    'Tried to install docker 3 times without succcess.')
                raise SystemExit()
        logger.info('Finished docker installation.')
    elif need_upgrade(con):
        logger.info('Upgrade needed for version' + '.'.join(check_version())
                    + ', running installer...')
        install_docker(con)
        logger.info('Upgrade finished! Current version: '
                    + '.'.join(check_version()))
