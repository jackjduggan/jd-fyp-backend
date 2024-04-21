terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }

  required_version = ">= 1.2.0"
}

provider "google" {
  credentials = file("/home/jackd/.keys/inprov-fyp1-0bd45adbf84b.json")
  project = var.gcp_project
  region  = var.gcp_region
  zone    = var.gcp_zone
}

# Firewall (Same as Security Group)
resource "google_compute_firewall" "inprov-sg" {
  name = "inprov-sg"
  network = "default"

  allow {
    protocol = "tcp"
    ports = ["80"]
  }

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  allow {
    protocol = "icmp"
  }

  source_ranges = ["0.0.0.0/0"]
}

data "cloudinit_config" "conf" {
  gzip = false
  base64_encode = false

  part {
    content_type = "text/cloud-config"
    content = file("cloud-config.cfg")
    filename = "cloud-config.cfg"
  }
}

# Instance
resource "google_compute_instance" "vm_instance" {
  name         = var.hostname
  machine_type = lookup(local.num_cores_to_instance_type, var.cpu_cores, "e2-micro")

  boot_disk {
    initialize_params {
      image = lookup(local.os_to_image, var.operating_system, "projects/ubuntu-os-cloud/global/images/family/ubuntu-2204-lts")
    }
  }

  network_interface {
    # A default network is created for all GCP projects
    network = "default"
    access_config {
    }
  }

  metadata = {
    user-data = "${data.cloudinit_config.conf.rendered}"
    ssh-keys = "${var.instance_username}:${file("/home/jackd/.ssh/gcp-key.pub")}"
  }
  #tags = var.instance_tags
}

resource "google_compute_network" "vpc_network" {
  name                    = "terraform-network"
  auto_create_subnetworks = "true"
}

output "instance_ip" {
  value = google_compute_instance.vm_instance.network_interface.0.access_config.0.nat_ip
}