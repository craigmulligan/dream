terraform {
  backend "local" {}
}

resource "aws_sns_topic" "audit_log" {
  name = "audit-log"
}
