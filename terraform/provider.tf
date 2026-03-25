# AWS provider configuration.
# This reads credentials from your AWS CLI profile or environment variables.
provider "aws" {
  region = var.aws_region

  # Default tags are automatically added to all supported resources.
  # This is an industry best practice for cost and ownership tracking.
  default_tags {
    tags = var.common_tags
  }
}

# Optional: Remote backend for team-safe Terraform state.
# Uncomment and update values after creating S3 bucket and DynamoDB table.
# terraform {
#   backend "s3" {
#     bucket         = "replace-with-your-tf-state-bucket"
#     key            = "aws-assignment-1/terraform.tfstate"
#     region         = "ap-south-1"
#     dynamodb_table = "replace-with-your-tf-lock-table"
#     encrypt        = true
#   }
# }
