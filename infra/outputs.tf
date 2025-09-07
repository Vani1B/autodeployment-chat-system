output "public_ip" {
  description = "Public IPv4 of the EC2 instance"
  value       = aws_instance.app.public_ip
}

output "url" {
  description = "HTTP URL of the app"
  value       = "http://${aws_instance.app.public_ip}"
}

output "instance_id" {
  description = "EC2 instance id"
  value       = aws_instance.app.id
}

output "security_group_id" {
  description = "Security Group id"
  value       = aws_security_group.web.id
}
