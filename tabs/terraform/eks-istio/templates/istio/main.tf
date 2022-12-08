locals {
  istio_charts_url = "https://istio-release.storage.googleapis.com/charts"
}

resource "kubernetes_namespace" "istio_system" {
  metadata {
    name = "istio-system"
    labels = {
      istio-injection = "disabled"
    }
  }
}

resource "helm_release" "istio-base" {
  repository       = local.istio_charts_url
  chart            = "base"
  name             = "istio-base"
  namespace        = kubernetes_namespace.istio_system.metadata.0.name
  cleanup_on_fail  = true
  force_update     = false
  depends_on = [kubernetes_namespace.istio_system]
}

resource "helm_release" "istiod" {
  repository       = local.istio_charts_url
  chart            = "istiod"
  name             = "istiod"
  namespace        = kubernetes_namespace.istio_system.metadata.0.name
  cleanup_on_fail  = true
  force_update     = false

  set {
    name = "meshConfig.accessLogFile"
    value = "/dev/stdout"
  }

  depends_on       = [helm_release.istio-base]
}

resource "kubernetes_namespace" "istio_ingess" {
  metadata {
    name = "istio-ingress"
    labels = {
      istio-injection = "enabled"
    }
  }
  depends_on        = [helm_release.istiod]
}

resource "helm_release" "istio-ingress" {
  repository        = local.istio_charts_url
  chart             = "gateway"
  name              = "istio-ingressgateway"
  namespace         = kubernetes_namespace.istio_ingess.metadata.0.name
  cleanup_on_fail   = true
  force_update      = false
  depends_on        = [kubernetes_namespace.istio_ingess]
}
