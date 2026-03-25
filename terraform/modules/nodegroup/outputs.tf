output "node_group_name" {
  description = "Managed node group name"
  value       = aws_eks_node_group.main.node_group_name
}

output "node_group_arn" {
  description = "Managed node group ARN"
  value       = aws_eks_node_group.main.arn
}
