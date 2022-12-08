data "kubernetes_service" "istio-ingress-gateway" {
  metadata {
    name = "${helm_release.istio-ingress.name}"
    namespace = "${helm_release.istio-ingress.namespace}"
  }
  depends_on = [ helm_release.istio-ingress ]
}
