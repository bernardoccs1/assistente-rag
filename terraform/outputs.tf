output "instance_public_ip" {
  description = "IP Público da instância criada na AWS"
  value       = aws_instance.rag_server.public_ip
}