data "aws_availability_zones" "available" {
  state = "available"
}


data "aws_eks_cluster_auth" "default" {
  name = module.eks.cluster_id
}
