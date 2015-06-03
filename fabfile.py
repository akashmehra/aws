from fabric.api import env, run, settings, cd, execute, sudo, parallel, task, execute
import os

env.shell = '/bin/bash -l -i -c'
env.user = 'ubuntu'

@parallel
def nbserver():
	run('tmux new -s itorch -d "cd $HOME/cvpr && nohup itorch notebook --ip=* --no-browser"')

@task
def start_nbserver(key_file,hosts_file):
  env.key_filename = [key_file]
  env.hosts = [host.replace('\n','').replace('\r','') for host in open(hosts_file).readlines()]
  execute(nbserver)
  

