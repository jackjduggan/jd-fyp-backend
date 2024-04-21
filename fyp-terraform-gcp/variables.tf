variable "gcp_project" {
    description = "The Google Cloud Project"
    type        = string
    default     = "inprov-fyp1"
}

variable "gcp_region" {
  description = "The Google Cloud region for resources"
  type        = string
  default     = "europe-west2"
}

variable "gcp_zone" {
  description = "The Google Cloud zone for resources"
  type        = string
  default     = "europe-west2-a"
}

variable "operating_system" {
  description = "The image path for the gcp instance"
  type        = string
}

variable "cpu_cores" {
  description = "The type of GCP instance"
  type        = string
}

locals {
  os_to_image = {
    "ubuntu" = "projects/ubuntu-os-cloud/global/images/family/ubuntu-2204-lts",
    "al2"    = "projects/gce-uefi-images/global/images/family/rhel-8"
  }

  num_cores_to_instance_type = {
    "1" = "e2-micro",
    "2" = "e2-small"
  }
}

variable "instance_tags" {
  description = "Tags for the GCP instance"
  type        = map(string)
  default = {
    Name = "FYP-VM"
  }
}

variable "instance_username" {
  description = "Username for the SSH key in the instance metadata"
  type        = string
  default     = "jack"
}

variable "hostname" {
  description = "The hostname for the machine"
  type        = string
  default     = "InProv-Test"
}

