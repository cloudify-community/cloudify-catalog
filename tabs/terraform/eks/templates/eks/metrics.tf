resource "kubernetes_cluster_role" "system_aggregated_metrics_reader" {
  metadata {
    name = "system:aggregated-metrics-reader"

    labels = {
      "rbac.authorization.k8s.io/aggregate-to-admin" = "true"

      "rbac.authorization.k8s.io/aggregate-to-edit" = "true"

      "rbac.authorization.k8s.io/aggregate-to-view" = "true"
    }
  }

  rule {
    verbs      = ["get", "list", "watch"]
    api_groups = ["metrics.k8s.io"]
    resources  = ["pods", "nodes"]
  }
}

resource "kubernetes_api_service" "v1beta1_metrics_k8s_io" {
  metadata {
    name = "v1beta1.metrics.k8s.io"
  }

  spec {
    service {
      namespace = "kube-system"
      name      = "metrics-server"
    }

    group                    = "metrics.k8s.io"
    version                  = "v1beta1"
    insecure_skip_tls_verify = true
    group_priority_minimum   = 100
    version_priority         = 100
  }
}

resource "kubernetes_service_account" "metrics_server" {
  metadata {
    name      = "metrics-server"
    namespace = "kube-system"
  }
}

resource "kubernetes_deployment" "metrics_server" {
  metadata {
    name      = "metrics-server"
    namespace = "kube-system"

    labels = {
      k8s-app = "metrics-server"
    }
  }

  spec {
    selector {
      match_labels = {
        k8s-app = "metrics-server"
      }
    }

    template {
      metadata {
        name = "metrics-server"

        labels = {
          k8s-app = "metrics-server"
        }
      }

      spec {
        volume {
          name      = "tmp-dir"
          empty_dir  {
            medium = ""
          }
        }

        container {
          name  = "metrics-server"
          image = "k8s.gcr.io/metrics-server-amd64:v0.3.6"

          volume_mount {
            name       = "tmp-dir"
            mount_path = "/tmp"
          }

          image_pull_policy = "Always"
        }

        service_account_name = "metrics-server"
      }
    }
  }
}

resource "kubernetes_role_binding" "metrics_server_auth_reader" {
  metadata {
    name      = "metrics-server-auth-reader"
    namespace = "kube-system"
  }

  subject {
    kind      = "ServiceAccount"
    name      = "metrics-server"
    namespace = "kube-system"
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "Role"
    name      = "extension-apiserver-authentication-reader"
  }
}

resource "kubernetes_service" "metrics_server" {
  metadata {
    name      = "metrics-server"
    namespace = "kube-system"

    labels = {
      "kubernetes.io/cluster-service" = "true"

      "kubernetes.io/name" = "Metrics-server"
    }
  }

  spec {
    port {
      protocol    = "TCP"
      port        = 443
      target_port = "443"
    }

    selector = {
      k8s-app = "metrics-server"
    }
  }
}

resource "kubernetes_cluster_role" "system_metrics_server" {
  metadata {
    name = "system:metrics-server"
  }

  rule {
    verbs      = ["get", "list", "watch"]
    api_groups = [""]
    resources  = ["pods", "nodes", "nodes/stats", "namespaces"]
  }
}

resource "kubernetes_cluster_role_binding" "system_metrics_server" {
  metadata {
    name = "system:metrics-server"
  }

  subject {
    kind      = "ServiceAccount"
    name      = "metrics-server"
    namespace = "kube-system"
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = "system:metrics-server"
  }
}

resource "kubernetes_cluster_role_binding" "metrics_server_system_auth_delegator" {
  metadata {
    name = "metrics-server:system:auth-delegator"
  }

  subject {
    kind      = "ServiceAccount"
    name      = "metrics-server"
    namespace = "kube-system"
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = "system:auth-delegator"
  }
}

