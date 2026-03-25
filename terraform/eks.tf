# Modular EKS control-plane call. Private endpoint settings are enforced inside module.
module "eks" {
  source = "./modules/eks"

  cluster_name       = var.cluster_name
  private_subnet_ids = module.vpc.private_subnet_ids
  vpc_id             = module.vpc.vpc_id
  vpc_cidr           = module.vpc.vpc_cidr
  common_tags        = var.common_tags
}
