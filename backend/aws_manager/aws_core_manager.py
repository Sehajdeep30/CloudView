from config import *

class AwsHandler():
    user_id = 0
    role_arn = ''
    policies = ''
    __external_id = ''
    
    def set_aws_role(self,user_id,role_arn,policy_arn):
        self.user_id = user_id
        self.role_arn = role_arn
        policies = ",".join(policy_arn)
        self.policies = policies
        
    def remove_aws_role(self):
        self.user_id = 0
        self.role_arn = ''
        self.policies = ''
    
    def set_template_url(self,user_id,policy_arn):
        policies = ",".join(policy_arn)
        self.__external_id = f"safe-id-is-{user_id}"
        launch_url = f"https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review\
?templateURL={TEMPLATE_URL}\
&stackName={STACK_NAME}\
&param_ExternalId={self.__external_id}\
&param_AppAccountId={ACCOUNT_ID}\
&param_ManagedPolicyArns = {policies}"

        return launch_url

        
