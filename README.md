# AWS EC2
Code to interact with AWS EC2.
Using boto and fabric for aws and remote host management.
<br>
Let's you launch multiple EC2 instances across regions.
<br>
## Steps to Run:
<br>
### Launching EC2 Instances:
* Clone the repo
* Install Fabric by running ```pip install fabric``` (use ```sudo``` in case you need to).
* To launch the instances execute ``` python ec2_instances_boto.py us-east-1 ec2-config.cfg ```. This will create 2 files, one containing the public dns of the hosts and the other containing the ids of the hosts. The dns of the hosts will be used by the ```fabfile``` to programatically start the notebook on each instance. If the keypair specified in the config file is not already created then the script will create the key pair and save it in the current working directory.
<br>

### Starting iTorch Notebook:
* To start itorch notebook on each server, pass the ```hosts_file``` (created in the step above) as an argument to the fabfile. Execute ```fab start_nbserver:key_file=<pem-file>.pem,hosts_file=ec2-torch-hosts``` from the directory containing the fabfile.

### Killing iTorch Notebook:
* To kill itorch notebook on each server, pass the ```hosts_file``` (created in the step above) as an argument to the fabfile. Execute ```fab stop_nbserver:key_file=<pem-file>.pem,hosts_file=ec2-torch-hosts``` from the directory containing the fabfile.

