# AWS region where infrastructure will be created.
variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "ap-south-1"
}

# Base CIDR for custom VPC.
variable "vpc_cidr" {
  description = "CIDR block for custom VPC"
  type        = string
  default     = "10.0.0.0/16"
}

# Use at least 2 Availability Zones as required by the assignment.
variable "az_count" {
  description = "Number of AZs to use for private subnets"
  type        = number
  default     = 2
}

# EKS cluster name output requirement.
variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "private-eks-assignment"
}

# Managed node group name output requirement.
variable "node_group_name" {
  description = "EKS node group name"
  type        = string
  default     = "private-workers"
}

# Node instance type (t3.small chosen for lower cost in learning labs).
variable "node_instance_type" {
  description = "EC2 instance type for EKS workers"
  type        = string
  default     = "t3.small"
}

# Assignment requires 3 worker nodes.
variable "desired_nodes" {
  description = "Desired number of worker nodes"
  type        = number
  default     = 3
}

# Keep min=3 and max=3 to strictly satisfy fixed 3-node requirement.
variable "min_nodes" {
  description = "Minimum number of worker nodes"
  type        = number
  default     = 3
}

variable "max_nodes" {
  description = "Maximum number of worker nodes"
  type        = number
  default     = 3
}

# Common tags used across resources.
variable "common_tags" {
  description = "Default resource tags"
  type        = map(string)
  default = {
    Project     = "aws-assignment-1"
    Environment = "learning"
    ManagedBy   = "terraform"
    Owner       = "deepanshu"
  }
}
