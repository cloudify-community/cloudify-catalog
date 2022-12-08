terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "3.22.0"
    }
  }
}

variable "vm_id" {
  type = string
  description = ""
}

variable "disk_size" {
  type = string
  description = "Disk size"
}

variable "region" {

}

provider "aws" {
  region = var.region
}

resource "aws_volume_attachment" "ebs_att" {
  device_name = "/dev/sdh"
  volume_id   = aws_ebs_volume.disk.id
  instance_id = var.vm_id
}

resource "aws_ebs_volume" "disk" {
  availability_zone = "${var.region}b"
  size              = var.disk_size
}