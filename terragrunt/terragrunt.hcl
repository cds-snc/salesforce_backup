terraform { 
  source = "."
}

inputs = {
  product_name              = "gc-design-system"
  account_id                = "563894450011"
  region                    = "ca-central-1"
  billing_code              = "platform-core-services"
}


remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    encrypt             = true
    bucket              = "${inputs.billing_code}-salesforce-backup-tf"
    dynamodb_table      = "terraform-state-lock-dynamo"
    region              = "ca-central-1"
    key                 = "${path_relative_to_include()}/terraform.tfstate"
    s3_bucket_tags      = { CostCentre : inputs.billing_code }
    dynamodb_table_tags = { CostCentre : inputs.billing_code }
  }
}
