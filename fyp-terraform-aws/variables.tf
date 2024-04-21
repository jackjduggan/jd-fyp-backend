variable "aws_region" {
  description = "The AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "operating_system" { # formerly "instance_ami"
  description = "The AMI ID for the AWS instance"
  type        = string
}

variable "cpu_cores" { # formerly "instance_type"
  description = "The type of AWS instance"
  type        = string
}

# Mapping definition to map os to ami and cpu_cores to type
locals {
  os_to_ami = {
    "ubuntu" = "ami-0c7217cdde317cfec", # Ubuntu 22.04
    "al2" = "ami-0c101f26f147fa7fd" # Amazon Linux
  }

  num_cores_to_instance_type = {
    "1" = "t2.nano",
    "2" = "t2.micro"
  }
}

variable "instance_tags" {
  description = "Tags for the AWS instance"
  type        = map(string)
  default = {
    Name = "FYP-VM"
  }
}

variable "hostname" {
  description = "The hostname for the machine"
  type        = string
}

