resource "kubernetes_service" "dashboard_service_loadbalancer" {
  metadata {
    name      = "dashboard-service-loadbalancer"
    namespace = kubernetes_namespace.kubernetes_dashboard.metadata[0].name
  }

  spec {
    port {
      protocol    = "TCP"
      port        = 443
      target_port = "8443"
    }

    selector = {
      k8s-app = "kubernetes-dashboard"
    }

    type = "LoadBalancer"
  }
}