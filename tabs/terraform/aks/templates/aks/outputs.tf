output "cluster_name" {
    value = azurerm_kubernetes_cluster.aks.name
}

output "kubernetes_cluster_host" {
    value = azurerm_kubernetes_cluster.aks.kube_config.0.host
    sensitive = true
}

output "admin_token" {
    value = kubernetes_secret.service_account.data.token
    sensitive =  true
}

output "ssl_ca_cert" {
    value = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.cluster_ca_certificate)
    sensitive = true
}