variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
}

variable "node_group_name" {
  description = "Node group name"
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for worker nodes"
  type        = list(string)
}

variable "vpc_id" {
  description = "VPC ID for security group creation"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR used to restrict inbound rules"
  type        = string
}

variable "desired_nodes" {
  description = "Desired number of nodes"
  type        = number
}

variable "min_nodes" {
  description = "Minimum number of nodes"
  type        = number
}

variable "max_nodes" {
  description = "Maximum number of nodes"
  type        = number
}

variable "node_instance_type" {
  description = "Worker node instance type"
  type        = string
}

variable "common_tags" {
  description = "Common tags inherited from root module"
  type        = map(string)
}
