
class AwsHandler():
    user_id = 0
    role_arn = ''
    policies = ''
    
    def set_aws_role(self,user_id,role_arn,policy_arn):
        self.user_id = user_id
        self.role_arn = role_arn
        policies = ",".join(policy_arn)
        self.policies = policies
        
    def remove_aws_role(self):
        self.user_id = 0
        self.role_arn = ''
        self.policies = ''