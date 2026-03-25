# Modular VPC call. The actual resources are implemented inside modules/vpc.
module "vpc" {
  source = "./modules/vpc"

  vpc_cidr     = var.vpc_cidr
  cluster_name = var.cluster_name
  selected_azs = local.selected_azs
  common_tags  = var.common_tags
}
