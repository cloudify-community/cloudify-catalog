output "istio_ingress_gateway" {
  description = "Istio Ingress Gatway"
  value = data.kubernetes_service.istio-ingress-gateway.status.0.load_balancer.0.ingress.0.hostname
}
