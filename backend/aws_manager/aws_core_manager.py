import boto3
import textwrap
from datetime import datetime, timedelta,timezone
from config import TEMPLATE_URL, STACK_NAME, ACCOUNT_ID
from urllib.parse import quote_plus
from backend.aws_manager.iam import IamHandler


class AwsHandler():
    def __init__(self, session: boto3.Session = None):
        self.user_id = 0
        self.role_arn = ''
        self.policies = ''
        self.__external_id = ''
        self.__session = session or boto3.Session(``)
        self.expiry_time = None
        self.aws_handler = None
        self._clients = {}
        
    
    def set_aws_role(self,user_id,role_arn,policy_arn):
        self.user_id = user_id
        self.role_arn = role_arn
        policies = ",".join(policy_arn)
        self.policies = policies
        self.__external_id = f"safe-id-is-{user_id}"
        self._clients.clear()
        self.set_aws_session()
        
        
    def remove_aws_role(self):
        self.__init__()  
    
    def set_template_url(self,user_id,policy_arn):
        policies = ",".join(policy_arn)
        launch_url = textwrap.dedent(f"""\
            https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review
            ?templateURL={quote_plus(TEMPLATE_URL)}
            &stackName={quote_plus(STACK_NAME)}
            &param_ExternalId={quote_plus(self.__external_id)}
            &param_AppAccountId={quote_plus(ACCOUNT_ID)}
            &param_ManagedPolicyArns={quote_plus(policies)}
        """).replace("\n", "")
        
        return launch_url

    def set_aws_session(self):
        sts = self.__session.client('sts')
        
        response = sts.assume_role(
        RoleArn=self.role_arn,
        ExternalId=self.__external_id,
        )["Credentials"]
        
        user_session = boto3.Session(
            aws_access_key_id=response['AccessKeyId'],
            aws_secret_access_key=response['SecretAccessKey'],
            aws_session_token=response['SessionToken']
        )
        
        self.expiry_time = response['Expiration']
        self.aws_handler = AwsHandler(session=user_session)
        
    def get_handler(self):
        if not self.expiry_time or datetime.now(timezone.utc) > self.expiry_time - timedelta(minutes=5):
            self._clients.clear()
            self.set_aws_role()
        return self.aws_handler
     
    @property   
    def iam(self) -> IamHandler:
        if 'iam' not in self._clients:
            self._clients['iam'] = IamHandler(self.__session.client('iam'))
        return self._clients['iam']
