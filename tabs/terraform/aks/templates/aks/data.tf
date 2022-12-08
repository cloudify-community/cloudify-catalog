data "kubernetes_secret" "admin_user" {
  metadata {
    name = kubernetes_service_account.admin_user.default_secret_name
    namespace = "kube-system"
  }
}