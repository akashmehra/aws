from fabric.api import env, run, settings, cd, execute, sudo, parallel, task, execute
import os

env.shell = '/bin/bash -l -i -c'
env.user = 'ubuntu'

@parallel
def run_nbserver_parallel():
  run('tmux new -s itorch -d "([ -d $HOME/cvpr ] || mkdir $HOME/cvpr); cd $HOME/cvpr && nohup itorch notebook --ip=* --no-browser"')

@parallel
def kill_nbserver_parallel():
  run('tmux kill-session -t itorch')


def setup_environment(key_file,hosts_file):
  env.key_filename = [key_file]
  env.hosts = [host.replace('\n','').replace('\r','') for host in open(hosts_file).readlines()]

@task
def start_nbserver(key_file,hosts_file):
  setup_environment(key_file,hosts_file)
  execute(run_nbserver_parallel)

@task
def stop_nbserver(key_file,hosts_file):
  setup_environment(key_file,hosts_file)
  execute(kill_nbserver_parallel)
  

