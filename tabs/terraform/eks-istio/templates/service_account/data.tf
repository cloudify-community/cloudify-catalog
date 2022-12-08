data "kubernetes_secret" "secret" {
  metadata {
    name = "${kubernetes_service_account.service_account.default_secret_name}"
  }
}
