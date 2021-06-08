terraform {
  backend "local" {}
}

provider "aws" {
    region = "us-east-1"
    skip_credentials_validation = true
    skip_requesting_account_id = true
    skip_metadata_api_check = true
    s3_force_path_style = true

    access_key                  = "mock_access_key"
    secret_key                  = "mock_secret_key"
    endpoints {
        sqs  = "http://localstack:4566"
        s3   = "http://localstack:4566"
        lambda = "http://localstack:4566"
        iam   = "http://localstack:4566"
        apigateway = "http://localstack:4566"
        sns = "http://localstack:4566"
    }
}

resource "aws_sns_topic" "audit_log" {
  name = "audit-log"
}
