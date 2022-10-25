output "region" {
  value       = var.region
  description = "GCloud Region"
}

output "project_id" {
  value       = var.project_id
  description = "GCloud Project ID"
}

output "kubernetes_cluster_name" {
  value       = google_container_cluster.primary.name
  description = "GKE Cluster Name"
}

output "kubernetes_cluster_host" {
  value       = google_container_cluster.primary.endpoint
  description = "GKE Cluster Host"
}

output "dashboard_ip" {
  value = kubernetes_service.dashboard_service_loadbalancer.status.0.load_balancer.0.ingress.0.ip
}

output "admin_token" {
  value = data.kubernetes_secret.admin_user.data.token
  sensitive =  true
}

output "ssl_ca_cert" {
  value = base64decode(google_container_cluster.primary.master_auth[0].cluster_ca_certificate)
  sensitive = true
}