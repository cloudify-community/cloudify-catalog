data "aws_availability_zones" "available" {}

data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_id
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}

data "kubernetes_secret" "admin_user" {
  metadata {
    name = kubernetes_service_account.admin_user.default_secret_name
    namespace = "kube-system"
  }
}