locals {
  salesforce_backup_role_name = "salesforce-backup"
}

module "oidc" {
  source = "github.com/cds-snc/terraform-modules?ref=v5.1.8//gh_oidc_role"

  billing_tag_value = var.billing_code

  oidc_exists = true

  roles = [
    {
      name      = local.salesforce_backup_role_name
      repo_name = "salesforce_backup"
      claim     = "ref:refs/heads/main"
    }
  ]
}

data "aws_iam_policy_document" "write_to_bucket" {
  // this statement allows writing to the cds-salesforce-backups s3 bucket
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:ListBucket",
    ]
    resources = [
      module.cds_salesforce_backups_bucket.s3_bucket_arn,
      "${module.cds_salesforce_backups_bucket.s3_bucket_arn}/*",
    ]

  }
}

resource "aws_iam_role_policy" "write_to_bucket" {
  name   = "write_to_salesforce_bucket"
  role   = local.salesforce_backup_role_name
  policy = data.aws_iam_policy_document.write_to_bucket.json
}

resource "aws_iam_role_policy_attachment" "oidc" {
  role       = local.salesforce_backup_role_name
  policy_arn = aws_iam_role_policy.write_to_bucket.id

  depends_on = [
    module.oidc,
  ]
}