variable "account_id" {
  description = "(Required) The account ID to perform actions on."
  type        = string
}

variable "region" {
  description = "(Required) The region to perform actions in."
  type        = string
}

variable "billing_code" {
  description = "(Required) The billing code to use for resources."
  type        = string
}