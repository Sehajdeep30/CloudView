import boto3
import textwrap
from datetime import datetime, timedelta,timezone
from config import TEMPLATE_URL, STACK_NAME, ACCOUNT_ID, EXTERNAL_ID
from urllib.parse import quote_plus
from aws_manager.iam import IamHandler
from repos.aws_cred_repos import get_aws_role


class AwsHandler():
    def __init__(self):
        self.user_id = 0
        self.role_arn = ''
        self.policies = ''
        self._external_id = ''
        self.__session = boto3.Session()
        self.expiry_time = None
        self._clients = {}
        self.hello = ""
        
    @staticmethod
    def get_aws_handler() -> "AwsHandler":
        return AwsHandler()
    
    def set_template_url(self,user_id,policy_arn) -> str:
        policies = ",".join(policy_arn)
        external_id = EXTERNAL_ID+str(user_id)
        launch_url = textwrap.dedent(f"""\
            https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review
            ?templateURL={quote_plus(TEMPLATE_URL)}
            &stackName={quote_plus(STACK_NAME)}
            &param_ExternalId={quote_plus(external_id)}
            &param_AppAccountId={quote_plus(ACCOUNT_ID)}
            &param_ManagedPolicyArns={quote_plus(policies)}
        """).replace("\n", "")
        
        return launch_url


    def assume_role(self, user_id: int, role_arn: str, policies: str):

        # Load from DB if first time
        if role_arn is None or policies is None:
            record = get_aws_role(user_id)
            
            if not record:
                raise ValueError("No AWS role configured for this user")
            
            role_arn, policies = record["role_arn"], record["policies"]
            
        # Save state
        self.user_id      = user_id
        self.role_arn     = role_arn
        self.policies     = policies
        self._external_id = EXTERNAL_ID + str(user_id)
        # STS call
        sts_creds = self._session.client("sts").assume_role(
            RoleArn         = self.role_arn,
            ExternalId      = self._external_id,
            RoleSessionName = f"cv-{user_id}"
        )["Credentials"]

        # Session overwrite
        self._session     = boto3.Session(
            aws_access_key_id     = sts_creds["AccessKeyId"],
            aws_secret_access_key = sts_creds["SecretAccessKey"],
            aws_session_token     = sts_creds["SessionToken"]
        )
        self._expiry_time  = sts_creds["Expiration"]
        self._clients.clear()

    def refresh_if_needed(self) -> None:
        """If within 5 minutes of expiry (or never assumed) → re-assume role."""
        if (self._expiry_time is None or
            datetime.now(timezone.utc) > self._expiry_time - timedelta(minutes=5)):
            self.assume_role(self.user_id, self.role_arn, self.policies)
                 
    @property   
    def iam(self) -> IamHandler:
        self.refresh_if_needed()
        if 'iam' not in self._clients:
            self._clients['iam'] = IamHandler(self.__session.client('iam'),self.__session.client('cloudformation'))
        return self._clients['iam']
        
        
    def remove_aws_role(self):
        self.user_id       = None
        self.role_arn      = None
        self.policies      = None
        self._external_id = None
        self.expiry_time   = None
        self._clients.clear()        
            

