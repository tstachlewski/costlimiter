import json
import os
import boto3

def handler(event, context):
    
    ec2 = boto3.client('ec2');
    regions = ec2.describe_regions()['Regions']
    
    for region in regions:
        
        regionName = region['RegionName']

        stopRDS(regionName);
        stopAutoscaling(regionName);
        stopInstances(regionName);
        stopRedshift(regionName);
        stopSageMaker(regionName);
        modifyPermissions();
        
    return {
        'statusCode': 200,
        'body': json.dumps('DONE')
    }

def modifyPermissions():
    iam = boto3.client('iam');
    
    users = iam.list_users()["Users"];
    for user in users:
        iam.attach_user_policy( UserName=user["UserName"], PolicyArn=os.environ['STOPPER_POLICY'] )
    
    
def stopSageMaker(region):
    sagemakerClient = boto3.client('sagemaker', region_name=region);
    notebooks = sagemakerClient.list_notebook_instances()["NotebookInstances"];
    for notebook in notebooks:
        notebookName = notebook["NotebookInstanceName"];
        print("Stopping SageMaker Notebook (" + notebookName + ")");
        try:
            sagemakerClient.stop_notebook_instance( NotebookInstanceName=notebookName );
        except: 
            print("Error");
        

def stopRedshift(region):
    redshiftClient = boto3.client('redshift', region_name=region);
    clusters = redshiftClient.describe_clusters()["Clusters"];
    for cluster in clusters:
        clusterId = cluster["ClusterIdentifier"];
        try:
            print("Stopping Redshift Cluster ("+ clusterId + ")");
            redshiftClient.delete_cluster( ClusterIdentifier=clusterId, SkipFinalClusterSnapshot=True);
        except: 
            print("Error");
    

def stopRDS(region):
    
    #Stopping RDS Instances/Clusters
    rdsclient = boto3.client('rds', region_name=region);
    rdsClusters = rdsclient.describe_db_clusters()["DBClusters"];
    for rdsCluster in rdsClusters:
        clusterId = rdsCluster["DBClusterIdentifier"];
        print("Stopping RDS Cluster (" + clusterId + ")");
        try:
            rdsclient.stop_db_cluster( DBClusterIdentifier=clusterId );
        except: 
            print("Error");         
    dbsInstances = rdsclient.describe_db_instances()["DBInstances"];
    for dbsInstance in dbsInstances:
        instanceId = dbsInstance["DBInstanceIdentifier"];
        print("Stopping RDS Instance ("+instanceId+")");
        try:
            rdsclient.stop_db_instance( DBInstanceIdentifier=instanceId );
        except: 
            print("Error");   
def stopAutoscaling(region):
    autoscalingclient = boto3.client('autoscaling', region_name=region);
    groups = autoscalingclient.describe_auto_scaling_groups()["AutoScalingGroups"]
    for group in groups:
        groupName = group["AutoScalingGroupName"];
        print("Reducing AutoScaling Group (" + groupName + ")");
        try:
            autoscalingclient.update_auto_scaling_group( AutoScalingGroupName=groupName, DesiredCapacity=0, MinSize=0, MaxSize=0 );
        except: 
            print("Error");  
def stopInstances(region):
    #Stopping all EC2 Instance
    ec2client = boto3.client('ec2', region_name=region);
    reservations = ec2client.describe_instances()['Reservations']
    for reservation in reservations:
        instances = reservation['Instances']
        for instance in instances:
            instanceId = instance['InstanceId']
            state = instance['State']['Name']
            if (state == "running"):
                print ('Stopping instance ' + instanceId + " (" + region + ")");
                try:
                    ec2client.stop_instances( InstanceIds=[ instanceId ] )
                except: 
                    print("Error");  
