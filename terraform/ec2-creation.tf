
# define provider
provider "aws" {
  shared_credentials_file = "~/.aws/credentials"
  region                  = "us-east-1"
  profile                 = "default"
}

# Define security group for SSH-connections
resource "aws_security_group" "ingress-ssh-connection" {
  name = "codeassigment-ssh-connection"
  ingress {
    cidr_blocks = [
      "0.0.0.0/0"
    ]
    from_port = 22
    to_port = 22
    protocol = "tcp"
  }
  // Terraform removes the default rule
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Creation of three instances and attach previous created security group
# As we are working in default vpc, we cannot use id for security group
# we can find it by name only
resource "aws_instance" "codeassign_server_1" {
  ami           = "ami-048f6ed62451373d9"
  instance_type = "t2.micro"
  security_groups = [aws_security_group.ingress-all-test.name]
  tags = {
    Name = "codeassigment"
  }
}

resource "aws_instance" "codeassign_server_2" {
  ami           = "ami-048f6ed62451373d9"
  instance_type = "t2.micro"
  security_groups = [aws_security_group.ingress-all-test.name]
  tags = {
    Name = "codeassigment"
  }
}

resource "aws_instance" "codeassign_server_3" {
  ami           = "ami-048f6ed62451373d9"
  instance_type = "t2.micro"
  security_groups = [
    aws_security_group.ingress-all-test.name]
  tags = {
    Name = "codeassigment"
  }
}


