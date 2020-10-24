import urllib.request
import io
import config
import tarfile
import os
import ssh
from logzero import logger

__author__ = 'talamo_a'


def look_for_services():
    """ automatically search for all local services """
    pass


def handle_build(connection, options):
    # jobs = []
    services = options.service
    logger.info('Building %s service(s)' % services)
    if 'all' in services:
        services = config.d_svcs
        services.remove('all')
    elif type(services) is str:
        services = services.split()

    print(services)
    logger.debug('starting sftp')
    ftp = connection.open_sftp()
    for service in services:
        logger.debug('working on service ' + service)
        with tarfile.open('./' + service + '.tar.gz', "w:gz") as tar:
            logger.debug('creating tar file ./%s.tar.gz' % service)
            tar.add('./' + service, arcname=os.path.basename('./'))

        logger.debug('remote chdir to %s' % config.d_remote_path)
        try:
            ftp.chdir(config.d_remote_path)
        except IOError:
            logger.debug('Remote path not found, creating...')
            ftp.mkdir(config.d_remote_path)
        src = './' + service
        f_src = src + '.tar.gz'
        dst = config.d_remote_path + '/' + service
        f_dst = dst + '.tar.gz'
        logger.debug("copying %s to remote path: %s" % (f_src, f_dst))
        ftp.put(f_src, f_dst)
        logger.debug('uncompressing remote file at %s' % dst)
        ssh.cmd(connection,
                'mkdir -p ' + dst + '&& tar xzf ' + f_dst + ' -C $_')
        if not (ssh.sftp_exists(ftp, dst)):
            logger.error('Failed to untar remote file.')
            raise SystemExit()
        logger.info('Building %s ...' % service)
        (stdin, stdout, stderr) = ssh.cmd(connection,
                                          'docker build ' + dst + ' -t ' +
                                          config.d_image_tag + service +
                                          ' --build-arg https_proxy')
        if options.debug:
            while True:
                line = stdout.readline()
                if not line:
                    break
                print(line, end="")
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            logger.info('Service %s has been successfully built.' % service)
        else:
            logger.error('Service build failed with code %d' %
                         exit_status)
            res = stderr.read().decode('ascii')
            logger.error('log:\n%s' % res)
    ftp.close()


def handle_deploy(connection, options):
    services = options.service
    if 'all' in services:
        services = config.d_svcs
        services.remove('all')
    logger.info('%d services to build' % len(services))
    for service in services:
        logger.info('Deploying %s service' % service)
        cmd = config.d_cmd_check + service
        (stdin, stdout, stderr) = connection.exec_command(cmd)
        res = stdout.read().decode('ascii')
        if len(res) == 0:
            logger.debug('Service is not deployed with name %s' % service)
            start_service(connection, service)
        else:
            res = res.split('\n', -1)
            for item in res:
                if item == '':
                    res.remove(item)
            cmd = config.d_cmd_rm + service
            (stdin, stdout, stderr) = connection.exec_command(cmd)
            res = stdout.read().decode('ascii')


def start_service(connection, service):
    """ starts a given service over a connection """
    cmd = 'cat ' + config.d_remote_path + '/' + service + '/run.txt'
    (stdin, stdout, stderr) = ssh.cmd(connection, cmd)
    res = stdout.read().decode('ascii')
    if len(res) == 0:
        logger.error('Failure to fetch remote command for %s, '
                     'we\'re not deploying this one.' % service)
    else:
        (stdin, stdout, stderr) = ssh.cmd(connection, res)
        if options.debug:
            while True:
                line = stdout.readline()
                if not line:
                    break
                print(line, end="")
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            logger.info('Service %s has been successfully built.'
                        % service)
        else:
            logger.error('Service build failed with code %d' %
                         exit_status)
            res = stderr.read().decode('ascii')
            logger.error('log:\n%s' % res)
