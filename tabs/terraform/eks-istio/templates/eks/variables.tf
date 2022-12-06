variable "region" {
  type        = string
  description = "Name of the AWS region to deploy EKS into"
  default     = "us-east-1"
}

variable "vpc_id" {
  type        = string
  description = "ID of the VPC to deploy EKS cluster into"
}

variable "cluster_name" {
  type        = string
  description = "Name of the VPC cluster to deploy"
  default     = "example-cluster"
}

variable "kubernetes_version" {
  type        = string
  description = "Version of Kubernetes to deploy"
  default     = ""
}

variable "instance_type" {
  type        = string
  description = "Managed node group instance size to use"
  default     = "t3.medium"
}

variable "node_group_name" {
  type        = string
  description = "Name of the EKS managed node group"
  default     = "example-nodes"
}

variable "minimum_nodes" {
  type        = number
  description = "Minimum number of nodes in the node group"
  default     = 1
}

variable "maximum_nodes" {
  type        = number
  description = "Maximum number of nodes in the node group"
  default     = 3
}

variable "desired_nodes" {
  type        = number
  description = "Desired number of nodes in the node group"
  default     = 1
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnet IDs to deploy EKS nodes into"
}
