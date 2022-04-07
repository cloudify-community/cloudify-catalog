
output "queue_name" {
    value = google_cloud_tasks_queue.advanced_configuration.name
}

output "queue_id" {
    value = google_cloud_tasks_queue.advanced_configuration.id
}

output "queue_location" {
    value = google_cloud_tasks_queue.advanced_configuration.location
}