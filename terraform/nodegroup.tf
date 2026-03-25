# Modular managed-node-group call.
module "nodegroup" {
  source = "./modules/nodegroup"

  cluster_name       = module.eks.cluster_name
  node_group_name    = var.node_group_name
  private_subnet_ids = module.vpc.private_subnet_ids
  vpc_id             = module.vpc.vpc_id
  vpc_cidr           = module.vpc.vpc_cidr

  desired_nodes      = var.desired_nodes
  min_nodes          = var.min_nodes
  max_nodes          = var.max_nodes
  node_instance_type = var.node_instance_type
  common_tags        = var.common_tags
}
