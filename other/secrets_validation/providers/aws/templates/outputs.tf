output "ami_id" {
  value = data.aws_ami_ids.ubuntu.id
}