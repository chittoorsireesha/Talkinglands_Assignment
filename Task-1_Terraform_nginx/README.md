# Steps to Deploy

terraform init

terraform plan -var-file="terraform.tfvars"

terraform apply -var-file="terraform.tfvars"

# After Apply

Outputs:

public_ip = "public ip will be displayed"

web_url   = "web url will be displayed"
