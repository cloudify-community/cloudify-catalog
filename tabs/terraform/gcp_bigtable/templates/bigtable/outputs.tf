output "instance_name" {
    value = google_bigtable_instance.instance.display_name
}

output "instance_id" {
    value = google_bigtable_instance.instance.id
}