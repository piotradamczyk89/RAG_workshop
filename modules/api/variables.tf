variable "lambda_functions" {
  type = map(object({ extension = string, runtime = string, http_method= string, layer = bool }))
}

variable "accountID" {
  type = string
}
variable "myRegion" {
  type = string
}

