const awsBasicPolicies = {
    s3: {
      read: [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      write: [
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      manage: [
        "s3:CreateBucket",
        "s3:DeleteBucket",
        "s3:PutBucketPolicy"
      ]
    },
    ec2: {
      read: [
        "ec2:DescribeInstances",
        "ec2:DescribeVolumes",
        "ec2:DescribeSecurityGroups"
      ],
      write: [
        "ec2:StartInstances",
        "ec2:StopInstances",
        "ec2:RebootInstances"
      ],
      manage: [
        "ec2:RunInstances",
        "ec2:TerminateInstances",
        "ec2:CreateSecurityGroup",
        "ec2:AuthorizeSecurityGroupIngress"
      ]
    },
    dynamodb: {
      read: [
        "dynamodb:GetItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ],
      write: [
        "dynamodb:PutItem",
        "dynamodb:DeleteItem",
        "dynamodb:UpdateItem"
      ],
      manage: [
        "dynamodb:CreateTable",
        "dynamodb:DeleteTable"
      ]
    },
    lambda: {
      read: [
        "lambda:ListFunctions",
        "lambda:GetFunction"
      ],
      invoke: [
        "lambda:InvokeFunction"
      ],
      manage: [
        "lambda:CreateFunction",
        "lambda:DeleteFunction",
        "lambda:UpdateFunctionCode"
      ]
    },
    cloudwatch: {
      read: [
        "cloudwatch:GetMetricData",
        "cloudwatch:DescribeAlarms"
      ],
      write: [
        "cloudwatch:PutMetricData",
        "cloudwatch:DeleteAlarms"
      ]
    }
  };

export default awsBasicPolicies;