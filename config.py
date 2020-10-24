import logzero
# from logzero import logger, logfile
import logging
import config

__author__ = 'talamo_a'

logfile = 'my_deployer.log'
loglevel_logfile = logging.DEBUG
loglevel_debug = logging.DEBUG
loglevel_std = logging.INFO

d_ver_maj = '19'
d_ver_min = '03'
d_ver_latest = False
d_script_path = '/tmp/get.docker.com.sh'
d_url = "https://get.docker.com/"
d_svcs = ['checker', 'mocker', 'all']
d_remote_path = '/tmp/my_deployer'
d_image_tag = 'my_deployer/'
d_script_log = '/tmp/docker_install.log'
d_cmd_check = 'docker ps -aqf name='
d_cmd_rm = 'docker rm -f '

remote_address = ''
