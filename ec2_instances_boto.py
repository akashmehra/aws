 
import boto
import boto.ec2 as ec2
import time,os,sys,json
 
 
# amis are located here: http://cloud-images.ubuntu.com/releases/14.04/release/
# ami_id = 'ami-4ae27e22' Trusy in us-east-1, supports hvm, root volume is SSD.
# to directly launch using console: https://console.aws.amazon.com/ec2/home?region=us-east-1#LaunchInstanceWizard:ami=ami-4ae27e22
 
# the ami that we created can be launched using the following code:
 
# only execute if needed.
'''block_device = ec2.blockdevicemapping.BlockDeviceType(delete_on_termination=True,size=200)
block_device_mapping = ec2.blockdevicemapping.BlockDeviceMapping()
block_device_mapping['/dev/sda2'] = block_device'''
 
def instance_state(instance):
    print 'Updating the instance: {0}'.format(instance.id)
    instance.update()
    print 'Instance State: {0}'.format(instance.state)
    return instance.state
 
def poll_aws_for_instance_state(instances, finalState, sleepTime):
    conditionSatisfied = False
    while not conditionSatisfied:
        instanceStatesPred = [instance_state(instance) == finalState for instance in instances]
        conditionSatisfied = instanceStatesPred[0]
        for idx,pred in enumerate(instanceStatesPred):
            conditionSatisfied = conditionSatisfied and pred
            if conditionSatisfied:
                print '{0}:{1}:{2}'.format(instances[idx].id,instances[idx].public_dns_name, finalState)
        if not conditionSatisfied:
            print 'Will sleep for {0} seconds before polling AWS again.'.format(sleepTime)
            time.sleep(10)
 
def save_instance_dns(instances,region):
    f = open(os.path.join(os.environ['HOME'],'hosts-'+region),'w')
    f.writelines([instance.public_dns_name+'\n' for instance in instances])
    f.close()
 
def save_instance_ids(instances,region):
    f = open(os.path.join(os.environ['HOME'],'instance-ids-'+region),'w')
    f.writelines([instance.id+'\n' for instance in instances])
    f.close()
 
def tag_instance(instances,key,value):
    for instance in instances:
        instance.add_tag(key,value)
 
def create_instances(conn,region,ami_id,instance_type,key_pair_name,min_count,max_count,nameTag, security_group_ids):
    new_reservation = conn.run_instances(ami_id,instance_type=instance_type, 
                                     min_count=min_count,max_count=max_count,
                                     key_name=key_pair_name, security_group_ids=security_group_ids)
                                     #,block_device_map=block_device_mapping)
    instances = new_reservation.instances
    state = 'running'
    sleepTime = 10
    poll_aws_for_instance_state(instances,state,sleepTime)
    print 'Instance details: \n'
    for instance in instances:
        print '{0}:{1}'.format(instance.id, instance.public_dns_name)
    save_instance_dns(instances,region)
    save_instance_ids(instances,region)
    print 'Tagging the instances...'
    time.sleep(sleepTime)
    tag_instance(instances,'Name',nameTag)
    print 'Done Tagging!'
    return instances
 
def terminate_instances(instances):
    conn.terminate_instances([instance.id for instance in instances])
 
def authorize_rule(sg,ip_protocol,from_port,to_port,source):
    try:
        sg.authorize(ip_protocol,from_port,to_port,source)
    except Exception as e:
        pass

def main(region,config_file):
    config = json.loads(open(config_file).read())
    aws_access_key = config['AWS_ACCESS_KEY']
    aws_secret_key = config['AWS_SECRET_KEY']
    group_name = config['security_group']['name']
    group_description = config['security_group']['description']
    conn = ec2.connect_to_region(region,aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    security_groups = filter(lambda group: True if group.name == group_name else False, conn.get_all_security_groups())
    security_group = None
    if not security_groups:
        security_group = conn.create_security_group(group_name,group_description)
    else:
        security_group = security_groups[0]
    for rule in config['security_group']['rules']:
        authorize_rule(security_group,rule['ip_protocol'],rule['from_port'],rule['to_port'],rule['source'])
    
    instance_type = 'g2.2xlarge'
    region_info = config[region]

    min_count = region_info['count']
    max_count = region_info['count']
    instances = create_instances(conn,region,region_info['ami_id'],instance_type,region_info['key_pair_name'],min_count,max_count,config['tag'],[security_group.id])

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1],sys.argv[2])
    else:
        print 'Usage: {0} <region> <config_file>'.format(sys.argv[0])
 
