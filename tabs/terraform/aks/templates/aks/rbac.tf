resource "kubernetes_service_account" "admin_user" {
  metadata {
    name      = "admin-user"
    namespace = "kube-system"
  }
  automount_service_account_token = false
}

resource "kubernetes_cluster_role_binding" "admin_user" {
  metadata {
    name = "admin-user"
  }

  subject {
    kind      = "ServiceAccount"
    name      = "admin-user"
    namespace = "kube-system"
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = "cluster-admin"
  }
}

resource "kubernetes_secret" "service_account" {
  metadata {
    name = "service-account-token"
    namespace = "kube-system"
    annotations = {
      "kubernetes.io/service-account.name" = "admin-user"
      "kubernetes.io/service-account.namespace" = "kube-system"
    }
    
  }
  type = "kubernetes.io/service-account-token"
}
