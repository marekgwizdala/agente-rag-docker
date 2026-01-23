# Configuración del Proveedor (AWS)
provider "aws" {
  region = "us-east-1"
}

# 1. Red Privada (VPC)
resource "aws_vpc" "ai_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "AI-RAG-Network"
  }
}

# 2. Firewall (Security Group)
resource "aws_security_group" "allow_ai_traffic" {
  name        = "allow_streamlit"
  description = "Permitir trafico al Frontend de IA"
  vpc_id      = aws_vpc.ai_vpc.id

  # Permitir entrada al puerto 8501 (Streamlit)
  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Abierto al mundo
  }

  # Permitir SSH para administración
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Permitir salida a internet
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 3. Servidor (EC2 Instance)
resource "aws_instance" "ai_server" {
  ami           = "ami-0c55b159cbfafe1f0" # Ubuntu 22.04 LTS
  instance_type = "t3.medium" # 2 vCPU, 4GB RAM
  
  security_groups = [aws_security_group.allow_ai_traffic.name]

  tags = {
    Name = "AI-Agent-Server"
  }

  # Bootstrapping: Script que se ejecuta al iniciar la máquina
  user_data = <<-EOF
              #!/bin/bash
              echo "Iniciando despliegue automático..."
              apt-get update
              apt-get install -y docker.io docker-compose git
              git clone https://github.com/KorbenDallas007/agente-rag-docker.git
              cd agente-rag-docker
              docker-compose up -d
              EOF
}
