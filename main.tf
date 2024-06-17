terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.46.0"
    }
  }
}

provider "aws" {
  region = var.myRegion
}

module "api" {
  source    = "./modules/api"
  accountID = var.accountID
  myRegion  = var.myRegion

  lambda_functions = {
    user = {
      runtime     = "python3.12"
      extension   = "py"
      http_method = "POST"
      layer = false
    },
    question = {
      runtime     = "python3.12"
      extension   = "py"
      http_method = "GET"
      layer = false
    },
    answer = {
      runtime     = "python3.12"
      extension   = "py"
      http_method = "POST"
      layer = true
    },
    person_data = {
      runtime     = "python3.12"
      extension   = "py"
      http_method = "POST"
      layer = false
    },
  }
}

module "table" {
  source = "./modules/table"
}
