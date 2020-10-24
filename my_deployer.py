#!/usr/bin/env python3
import argparse
import ssh
import docker_cfg
import docker_build
import config
from logzero import logger, logfile, loglevel

__author__ = 'talamo_a'


def init_logging():
    """ initializes the logging """
    logfile(config.logfile, loglevel=config.loglevel_logfile)
    # my_formatter = logging.Formatter(
    #     '%(filename)s - %(asctime)s - %(levelname)s: %(message)s')
    # logzero.formatter(my_formatter)


def hello(e):
    print('hello')


def parsearg():
    """ parse cli args """
    parser = argparse.ArgumentParser(prog="my_deployer.py")
    subparsers = parser.add_subparsers(help='Commands',
                                       required=True, dest='command')

    """ commands """
    cmd_configure = subparsers.add_parser('config', help='configure a host '
                                          'with docker')
    cmd_configure.add_argument('remote_ip', type=str, help='the target host')
    cmd_configure.set_defaults(func=configure)

    cmd_build = subparsers.add_parser('build',
                                      # choices=['checker', 'mocker', 'all'],
                                      help='builds the local services'
                                      'on the remote host')
    cmd_build.add_argument('remote_ip', type=str, help='the target host ')
    cmd_build.add_argument('service',
                           choices=['checker', 'mocker', 'all'],
                           type=str, help='the services you want to build')
    cmd_build.set_defaults(func=build)

    cmd_build = subparsers.add_parser('deploy',
                                      # choices=['checker', 'mocker', 'all'],
                                      help='builds the local services'
                                      'on the remote host')
    cmd_build.add_argument('remote_ip', type=str, help='the target host ')
    cmd_build.add_argument('service',
                           nargs='+',
                           choices=['checker', 'mocker', 'all'],
                           type=str, help='the services you want to deploy')
    cmd_build.set_defaults(func=deploy)

    """ args """
    parser.add_argument("-v", "--version", action="version",
                        version="Version 1.0")
    parser.add_argument("-d", "--debug", help="debug flag")
    parser.add_argument("-p", "--port", type=int,
                        default=22, help="Remote port")
    parser.add_argument("-u", "--username", type=str,
                        default="root", help="Remote username")
    parser.add_argument("--password", type=str,
                        default="password", help="Remote password")

    options = parser.parse_args()
    loglevel(config.loglevel_std
             if not options.debug else config.loglevel_debug)
    options.func(options)


def configure(opts):
    """ handles config command. """
    con = ssh.init_con(opts.remote_ip, opts.username,
                       opts.password, opts.port)
    docker_cfg.init(con, ops.username)
    ssh.close_con(con)


def build(opts):
    """ handles build command """
    con = ssh.init_con(opts.remote_ip, opts.username,
                       opts.password, opts.port)
    docker_build.handle_build(con, opts)
    ssh.close_con(con)


def deploy(opts):
    """ handles deploy command """
    con = ssh.init_con(opts.remote_ip, opts.username,
                       opts.password, opts.port)
    docker_build.handle_deploy(con, opts)
    ssh.close_con(con)


if __name__ == '__main__':
    """ my_deployer """
    init_logging()
    parsearg()
