
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.20.0"
    }
  }
}

variable "region" {
  type    = string
  default = "us-west-1"
}

variable "failover" {
  type    = string
  default = "eu-west-3"
}

variable "prefix" {
  type    = string
  default = "xyz"
}

provider "aws" {
  region = var.region
}

provider "aws" {
  alias  = "failover"
  region = var.failover
}

resource "aws_s3_bucket" "destination" {
  bucket = "${var.prefix}-bucket-destination"
}

resource "aws_s3_bucket_versioning" "destination" {
  provider = aws
  bucket = aws_s3_bucket.destination.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket" "source" {
  provider = aws.failover
  bucket   = "${var.prefix}-bucket-source"
}

resource "aws_s3_bucket_acl" "source_bucket_acl" {
  bucket   = aws_s3_bucket.source.id
  acl      = "private"
  provider = aws.failover
}

resource "aws_s3_bucket_versioning" "source" {
  provider = aws.failover
  bucket   = aws_s3_bucket.source.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_replication_configuration" "src_to_dst" {
  # Must have bucket versioning enabled first
  depends_on = [aws_s3_bucket_versioning.source, aws_s3_bucket_versioning.destination]
  provider   = aws.failover
  role       = aws_iam_role.src_to_dst.arn
  bucket     = aws_s3_bucket.source.id

  rule {
    id     = "foobar"
    prefix = "foo"
    status = "Enabled"
    delete_marker_replication {
      status = "Enabled"
    }
    filter {}

    destination {
      bucket        = aws_s3_bucket.destination.arn
      storage_class = "STANDARD"
      replication_time {
        status = "Enabled"
        time {
          minutes = 15
        }
      }
      metrics {
        event_threshold {
          minutes = 15
        }
        status = "Enabled"
      }
    }
  }
}

resource "aws_s3_bucket_replication_configuration" "dst_to_src" {
  # Must have bucket versioning enabled first
  depends_on = [aws_s3_bucket_versioning.destination, aws_s3_bucket_versioning.source]

  role   = aws_iam_role.dst_to_src.arn
  bucket = aws_s3_bucket.destination.id

  rule {
    id     = "foobar"
    prefix = "foo"
    status = "Enabled"
    delete_marker_replication {
      status = "Enabled"
    }
    filter {}
    destination {
      bucket        = aws_s3_bucket.source.arn
      storage_class = "STANDARD"
      replication_time {
        status = "Enabled"
        time {
          minutes = 15
        }
      }
      metrics {
        event_threshold {
          minutes = 15
        }
        status = "Enabled"
      }
    }
  }
}
