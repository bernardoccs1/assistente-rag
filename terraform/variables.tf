variable "aws_region" {
  description = "Região da AWS onde a infra será criada"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "Tamanho da máquina EC2"
  type        = string
  default     = "t3.medium" # 2 vCPUs, 4GB RAM - ideal para o RAG rodar liso
}

variable "instance_name" {
  description = "Nome da tag da instância"
  type        = string
  default     = "projeto-assistente-rag"
}