## Description

CostLimiter is a solution which automatically stop different resources in AWS Account, when billing exceed specified value. This is a 1-click deployment - which simplify the whole solution. In addition to stopping resources it will also send an email message to the provided email address with information about the situation.

What exactly the solution do?
-	It stop all EC2 instances
-	It modify all auto-scaling groups and set the new desired capacity to 0.
-	It stop all RDS databases.
-	It terminates all Redshift clusters.
-	It stop all SageMaker notebooks.
-	It modify all users permissions and disable possibility of running above resources again.

It should be noted, that the solution limit the cloud spending by stopping resources such as servers and databases – but still – there might be some other costs connected with other resources which are not supported by the solution.

In addition, it should be noted, that the solution might not be automatically executed right after the billing exceed  the specified amount – but might be executed later.


## Installation

Click on the button below. It will forward you to CloudFormation service where you will deploy CloudFormation template.

<a href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=costlimiter&templateURL=https://cost-limiter.s3.amazonaws.com/CostLimiter.yaml" ><img src="https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2017/02/10/launchstack.png" width="200"></a>
