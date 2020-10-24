from paramiko import SSHClient, AutoAddPolicy, \
                    AuthenticationException, SSHException, BadHostKeyException
import os
from logzero import logger

__author__ = 'talamo_a'
# class secret:
#     def __init__(self, name, age):
#         self.passwordAuth = passwordAuth
#         self.


def init_con(host: str,  username: str, password: str,
             port: int = 22, keyAuth: bool = False):
    """ initiates a connection """
    #  secrets: secret):
    logger.info('Asked connection to ' + username + '@' + host + ':'
                + str(port))
    c = SSHClient()
    c.load_system_host_keys()
    c.set_missing_host_key_policy(AutoAddPolicy())
    # c.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    if keyAuth:
        logger.info('Enabled SSH Key support.')
        # c.set_missing_host_key_policy(AutoAddPolicy())
    logger.info('Attempting connection...')
    try:
        c.connect(host, port, username, password, allow_agent=keyAuth)
        return c
    except AuthenticationException as authException:
        e = 'Password authentication failed : %s' % authException
        logger.exception(e)
        raise AuthenticationException(e)
    except SSHException as sshException:
        e = 'Unable to establish SSH connection: %s' % sshException
        logger.exception(e)
        raise SSHException(e)
    except BadHostKeyException as badHostKeyException:
        e = 'Unable to verify server\'s host key: %s' % badHostKeyException
        logger.exception(e)
        raise BadHostKeyException(e)


def cmd(con, cmd):
    """ run a command over a connection """
    logger.debug('Running command ' + cmd + ' at host '
                 + con.get_transport().sock.getpeername()[0])
    return con.exec_command(cmd)


def close_con(con):
    """ closes a connection """
    logger.debug('Attempting to close connection...')
    try:
        con.close()
    except e:
        logger.exception('Unable to close connection:', e)
        raise('Unable to close connection.')
    logger.info('Connection closed!')


def sftp_exists(sftp, path):
    """ tests if a remote path exists """
    try:
        sftp.stat(path)
        return True
    except FileNotFoundError:
        return False
