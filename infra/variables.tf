variable "region" {
  description = "AWS region"
  type        = string
  default     = "ca-central-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Existing EC2 key pair name (optional)"
  type        = string
  default     = ""
}

variable "allowed_cidrs_http" {
  description = "CIDRs allowed to access HTTP"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "app_name" {
  description = "Tag/name prefix"
  type        = string
  default     = "autodeploy-hello-world"
}

variable "repo_url" {
  description = "App repository to clone in user_data"
  type        = string
  default     = "https://github.com/Arvo-AI/hello_world"
}

variable "branch" {
  description = "Branch to checkout"
  type        = string
  default     = "main"
}
