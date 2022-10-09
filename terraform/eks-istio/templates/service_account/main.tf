resource "kubernetes_service_account" "service_account" {
  metadata {
    name = "terraform-example"
  }
}

resource "kubernetes_cluster_role_binding" "service_account_role" {
  metadata {
    name = "${kubernetes_service_account.service_account.metadata.0.name}"
  }
  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = "cluster-admin"
  }
  subject {
    kind      = "ServiceAccount"
    name      = "${kubernetes_service_account.service_account.metadata.0.name}"
    namespace = "default"
  }
  depends_on = [ kubernetes_service_account.service_account ]
}
