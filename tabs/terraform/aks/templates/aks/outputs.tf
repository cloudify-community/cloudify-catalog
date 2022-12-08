output "cluster_name" {
    value = azurerm_kubernetes_cluster.aks.name
}

output "kubernetes_cluster_host" {
    value = azurerm_kubernetes_cluster.aks.kube_config.0.host
}

output "admin_token" {
    value = data.kubernetes_secret.admin_user.data.token
    sensitive =  true
}

output "ssl_ca_cert" {
    value = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.cluster_ca_certificate)
}