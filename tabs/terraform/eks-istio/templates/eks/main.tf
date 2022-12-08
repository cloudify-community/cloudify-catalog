module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.cluster_name
  cluster_version = var.kubernetes_version

  vpc_id     = var.vpc_id
  subnet_ids = var.subnet_ids

  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = true
  create_cloudwatch_log_group     = false

  cluster_addons = {
    coredns = {
      resolve_conflicts = "OVERWRITE"
    }
    kube-proxy = {}
    vpc-cni = {
      resolve_conflicts = "OVERWRITE"
    }
  }

  eks_managed_node_group_defaults = {
    ami_type       = "AL2_x86_64"
    disk_size      = 20
    instance_types = [var.instance_type]
  }

  eks_managed_node_groups = {
    group = {
      name         = var.node_group_name
      min_size     = var.minimum_nodes
      max_size     = var.maximum_nodes
      desired_size = var.desired_nodes

      capacity_type = "ON_DEMAND"
    }
  }

  cluster_security_group_additional_rules = {
    egress_source_cluster_all = {
      description                = "All Ports/protocols"
      protocol                   = "-1"
      from_port                  = -1
      to_port                    = -1
      type                       = "egress"
      source_node_security_group = true
    }
  }


  node_security_group_ntp_ipv4_cidr_block = ["169.254.169.123/32"]
  node_security_group_additional_rules = {
    ingress_self_nodes_all = {
      description = "Node to node all ports/protocols"
      protocol    = "-1"
      from_port   = 0
      to_port     = 0
      type        = "ingress"
      self        = true
    }
  }
}

resource "aws_security_group_rule" "allow_ingress_all_traffic" {
  description = "Node to node all ports/protocols"
  protocol    = "-1"
  from_port   = 0
  to_port     = 0
  type        = "ingress"
  cidr_blocks      = ["0.0.0.0/0"]
  ipv6_cidr_blocks = ["::/0"]
  prefix_list_ids = []
  self = null
  source_security_group_id = null

  security_group_id        = module.eks.node_security_group_id
}

resource "aws_security_group_rule" "allow_egress_all_traffic" {
  description = "Node to node all ports/protocols"
  protocol    = "-1"
  from_port   = 0
  to_port     = 0
  type        = "egress"
  cidr_blocks      = ["0.0.0.0/0"]
  ipv6_cidr_blocks = ["::/0"]
  prefix_list_ids = []
  self = null
  source_security_group_id = null

  security_group_id        = module.eks.node_security_group_id
}
