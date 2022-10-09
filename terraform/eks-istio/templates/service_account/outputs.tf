output "cluster_service_account_token" {
  description = "Cluster Service Account Token"
  sensitive = true
  value = lookup(data.kubernetes_secret.secret.data, "token")
}
