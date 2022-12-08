output "primary" {
    value = aws_s3_bucket.source.bucket_domain_name
    sensitive = false
}

output "failover" {
    value = aws_s3_bucket.destination.bucket_domain_name
    sensitive = false
}