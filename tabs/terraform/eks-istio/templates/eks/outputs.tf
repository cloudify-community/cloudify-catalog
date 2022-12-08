output "cluster_endpoint" {
  description = "API endpoint for the cluster"
  value = module.eks.cluster_endpoint
}

output "cluster_certificate_authority" {
  description = "certitifcate authority for the cluster"
  value = base64decode(module.eks.cluster_certificate_authority_data)
}

output "cluster_token" {
  description = "Token for the cluster"
  value = nonsensitive(data.aws_eks_cluster_auth.default.token)
}
