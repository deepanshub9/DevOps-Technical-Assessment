variable "vpc_cidr" {
  description = "CIDR block for custom VPC"
  type        = string
}

variable "cluster_name" {
  description = "Cluster name used in subnet tags"
  type        = string
}

variable "selected_azs" {
  description = "Selected AZs where subnets will be created"
  type        = list(string)
}

variable "common_tags" {
  description = "Common tags inherited from root module"
  type        = map(string)
}
