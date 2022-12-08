output "cluster_name" {
  value = local.cluster_name
}

output "dashboard_hostname" {
  value = kubernetes_service.dashboard_service_loadbalancer.status.0.load_balancer.0.ingress.0.hostname
}

output "admin_token" {
  value = data.kubernetes_secret.admin_user.data.token
  sensitive =  true
}

output "kubernetes_cluster_host" {
    value = data.aws_eks_cluster.cluster.endpoint
}

output "region" {
    value = var.region
}

output "ssl_ca_cert" {
  value = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
}