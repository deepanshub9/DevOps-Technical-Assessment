variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for EKS control plane"
  type        = list(string)
}

variable "vpc_id" {
  description = "VPC ID for security group creation"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR allowed to access private API endpoint"
  type        = string
}

variable "common_tags" {
  description = "Common tags inherited from root module"
  type        = map(string)
}
