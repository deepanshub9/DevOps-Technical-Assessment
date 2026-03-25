# Pull available AZs in the selected region.
data "aws_availability_zones" "available" {
  state = "available"
}

# Keep first N AZs based on az_count variable.
locals {
  selected_azs = slice(data.aws_availability_zones.available.names, 0, var.az_count)
}
