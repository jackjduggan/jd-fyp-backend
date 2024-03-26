variable "gcp_project" {
    description = "The Google Cloud Project"
    type        = string
    default     = "inprov-test1"
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

variable "instance_image" {
  description = "The image path for the gcp instance"
  type        = string
  default     = "debian-cloud/debian-11" 
}

variable "instance_type" {
  description = "The type of GCP instance"
  type        = string
  default     = "e2-micro"
}

variable "hostname" {
  description = "The hostname for the machine"
  type        = string
  default     = "InProv-Test"
}

