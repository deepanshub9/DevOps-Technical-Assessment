# Required output: EKS cluster name.
output "eks_cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name
}

# Required output: VPC ID.
output "vpc_id" {
  description = "Custom VPC ID"
  value       = module.vpc.vpc_id
}

# Required output: Node group name.
output "node_group_name" {
  description = "EKS managed node group name"
  value       = module.nodegroup.node_group_name
}

# Helpful output: private subnet IDs (for debugging and verification).
output "private_subnet_ids" {
  description = "Private subnet IDs used by worker nodes"
  value       = module.vpc.private_subnet_ids
}
