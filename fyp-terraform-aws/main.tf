terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.aws_region
}

resource "aws_security_group" "puppet-sg" {
  name = "puppet-sg"
}

resource "aws_security_group" "puppet-test-sg" {
  name = "puppet-test-sg"

  # Ingress rule for port 80
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Egress rule allowing all traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Ingress rule for puppet-sg on ports 0-65535
  ingress {
    from_port       = 0
    to_port         = 65535
    protocol        = "tcp"
    security_groups = [aws_security_group.puppet-sg.id]
  }

  # Ingress rule for SSH on port 22
  ingress {
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    cidr_blocks     = ["0.0.0.0/0"]
    security_groups = [aws_security_group.puppet-sg.id]
  }
}

data "template_file" "user_data" {
  template = file("cloud-config.cfg")
}

resource "aws_instance" "app_server" {
  ami                    = lookup(local.os_to_ami, var.operating_system, "ami-0c7217cdde317cfec") # defaults to ubuntu if issue
  instance_type          = lookup(local.num_cores_to_instance_type, var.cpu_cores, "t2.micro")
  user_data              = data.template_file.user_data.rendered
  vpc_security_group_ids = [aws_security_group.puppet-test-sg.id]

  tags = merge(var.instance_tags, {
    Name = var.hostname
  })
}
