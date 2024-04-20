variable "aws_region" {
  description = "The AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "instance_ami" {
  description = "The AMI ID for the AWS instance"
  type        = string
  default     = "ami-0c7217cdde317cfec"
}

variable "instance_type" {
  description = "The type of AWS instance"
  type        = string
  default     = "t2.micro"
}


variable "instance_tags" {
  description = "Tags for the AWS instance"
  type        = map(string)
  default = {
    Name = "fyp-puppet-server"
  }
}

variable "hostname" {
  description = "The hostname for the machine"
  type        = string
  default     = "fyp-puppet-server"
}

