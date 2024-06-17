resource "aws_dynamodb_table" "workshop" {
  name           = "workshop"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "login"

  attribute {
    name = "login"
    type = "S"
  }

}

resource "aws_dynamodb_table" "data_workshop" {
  name           = "data_workshop"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "id"

  attribute {
    name = "id"
    type = "N"
  }

}
