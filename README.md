# AWS EC2
aws-boto code.
<br>
Let's you launch multiple instances across regions using EC2.
<br>
## Steps to Run:
* Clone the repo
* Install Fabric by running ```pip install fabric``` (use ```sudo``` in case you need to).
* To launch the instances execute ``` python ec2_instances_boto.py us-east-1 ec2-config.cfg ```. This will create 2 files, one containing the public dns of the hosts and the other containing the ids of the hosts. The dns of the hosts will be used by the ```fabfile``` to programatically start the notebook on each instance. If the keypair specified in the config file is not already created then the script will create the key pair and save it in the current working directory.
<br>
* To start itorch notbook on each server, pass the ```hosts_file``` (created in the step above) as an argument to the fabfile. Execute ```fab start_nbserver:key_file=<pem-file>.pem,hosts_file=ec2-torch-hosts``` from the directory containing the fabfile. 

