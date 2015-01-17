from fabric.api import env, run, settings, cd, execute, sudo, parallel, task, execute
import os

key_file_name_prefix = 'jarvis-ec2-'
env.shell = '/bin/bash -l -i -c'
env.user = 'ubuntu'

@parallel
def nbserver():
	run('tmux new -s itorch -d "cd $HOME/demos && nohup itorch notebook --ip=* --no-browser"')

@task
def start_nbserver(region):
  key_file_name = key_file_name_prefix+region+'.pem'
  key = os.path.join(os.environ['HOME'],'.keys',key_file_name)
  env.key_filename = [key]
  env.hosts = [host.replace('\n','').replace('\r','') for host in open(os.path.join(os.environ['HOME'],'hosts-'+region)).readlines()]
  execute(nbserver)
  

