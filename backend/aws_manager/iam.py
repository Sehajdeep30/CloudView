from botocore.exceptions import ClientError
from config import STACK_NAME, EXTERNAL_ID

class IamHandler:
    def __init__(self, iam_client, cloudform_client):
        self.client = iam_client
        self.cloudformation = cloudform_client

    def delete_user_stack(self):
        try:
            self.cloudformation.describe_stacks(StackName=STACK_NAME)
            self.cloudformation.delete_stack(StackName=STACK_NAME)
            return True
        except ClientError as e:
            if "does not exist" in str(e):
                return False
            raise

    def update_iam_policy(self, user_id, new_policies, old_policies):
        # Ensure both policies are strings (comma-separated) or lists
        if isinstance(new_policies, str):
            new_policy_list = new_policies.split(",")
        else:
            new_policy_list = new_policies


        if isinstance(old_policies, str):
            old_policy_list = old_policies.split(",")
        else:
            old_policy_list = old_policies

        external_id = EXTERNAL_ID + str(user_id)

        # Strip any whitespace
        new_policy_list = [p.strip() for p in new_policy_list]
        old_policy_list = [p.strip() for p in old_policy_list]

        added_policies = [p for p in new_policy_list if p and p not in old_policy_list]
        removed_policies = [p for p in old_policy_list if p and p not in new_policy_list]

        for policy in added_policies:
            try:
                self.client.attach_role_policy(
                    PolicyArn=policy,
                    RoleName=f"CloudViewAccessRole-{external_id}"
                )
            except ClientError as e:
                raise e

        for policy in removed_policies:
            try:
                self.client.detach_role_policy(
                    PolicyArn=policy,
                    RoleName=f"CloudViewAccessRole-{external_id}"
                )
            except ClientError as e:
                raise e

        if isinstance(new_policies, list):
            new_policy_str = ",".join(new_policy_list)
            
        return new_policy_str
