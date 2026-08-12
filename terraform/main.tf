terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# -------------------------------------------------------------------------
# SECURITY GROUP (O Firewall da Instância)
# -------------------------------------------------------------------------
resource "aws_security_group" "rag_sg" {
  name        = "rag-assistant-sg"
  description = "Permite acesso ao Streamlit, FastAPI e SSH"

  # Porta do Streamlit (Frontend)
  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Aberto para a internet
  }

  # Porta do FastAPI (Backend - Opcional se tudo rodar interno, mas bom para testar)
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Porta SSH para você se conectar na máquina remotamente
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Em producao, o ideal e colocar o seu IP aqui
  }

  # Liberar toda a saída de rede (install do Python, Docker, HuggingFace, etc)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# INSTÂNCIA EC2 (A Máquina Virtual)

resource "aws_instance" "rag_server" {
  ami           = "ami-0c7217cdde317cfec" # ID da AMI do Ubuntu 22.04 LTS em us-east-1 (verificar se mudar de regiao)
  instance_type = var.instance_type

  security_groups = [aws_security_group.rag_sg.name]

  # Script de automação: Instala o Docker e o Docker Compose assim que a máquina liga
  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update -y
              sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
              curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
              echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/yaml/sources.list.dist/docker.list > /dev/null
              sudo apt-get update -y
              sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
              sudo systemctl start docker
              sudo systemctl enable docker
              sudo usermod -aG docker ubuntu
              EOF

  tags = {
    Name = var.instance_name
  }
}