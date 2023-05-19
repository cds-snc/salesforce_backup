module "cds_salesforce_backups_bucket" {
  source = "github.com/cds-snc/terraform-modules?ref=v5.1.8//S3"

  bucket_name       = "cds-salesforce-backups"
  billing_tag_value = var.billing_code
  critical_tag_value = "true"
  versioning = {
    "enabled" = true
  }
}

module "cds_salesforce_backups_logs_bucket" {
  source = "github.com/cds-snc/terraform-modules?ref=v5.1.8//S3"

  bucket_name       = "cds-salesforce-backups-access-logs"
  billing_tag_value = var.billing_code

}