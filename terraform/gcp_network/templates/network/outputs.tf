output "network_name" {
    value = google_compute_network.network.name
}

output "network_gateway" {
    value = google_compute_network.network.gateway_ipv4
}

output "network_id" {
  value = google_compute_network.network.id
}