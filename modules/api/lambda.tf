data "archive_file" "lambda" {
  for_each    = var.lambda_functions
  type        = "zip"
  source_file = "${path.module}/src/${each.key}.${each.value.extension}"
  output_path = "${path.module}/src/${each.key}.zip"
}

resource "aws_lambda_function" "lambda" {
  for_each         = var.lambda_functions
  filename         = "${path.module}/src/${each.key}.zip"
  function_name    = each.key
  role             = aws_iam_role.lambda.arn
  handler          = "${each.key}.handler"
  source_code_hash = data.archive_file.lambda[each.key].output_base64sha256
  runtime          = each.value.runtime
  timeout          = 60
  architectures = ["x86_64"]
  layers = each.value.layer ? [aws_lambda_layer_version.langchain.arn ] : []

}


data "archive_file" "layer_zip" {
  type        = "zip"
  source_dir = "${path.module}/src/langchain_layer/layer"
  output_path = "${path.module}/src/langchain_layer/langchain_layer.zip"
}

resource "aws_lambda_layer_version" "langchain" {
  filename                 = data.archive_file.layer_zip.output_path
  source_code_hash         = filebase64sha256(data.archive_file.layer_zip.output_path)
  layer_name               = "langchain"
  compatible_architectures = ["x86_64"]

  compatible_runtimes = ["python3.8", "python3.9", "python3.10", "python3.11", "python3.12"]
}


data "aws_iam_policy_document" "lambda_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "dynamodb_access_doc" {
  statement {
    actions = [
      "dynamodb:PutItem",
      "dynamodb:GetItem",
      "dynamodb:Scan",
      "dynamodb:BatchWriteItem"
    ]
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "logs_policy_doc" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "secretsmanager:GetSecretValue",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "logs_policy" {
  policy = data.aws_iam_policy_document.logs_policy_doc.json
}
resource "aws_iam_policy" "dynamodb_access_policy" {
  policy = data.aws_iam_policy_document.dynamodb_access_doc.json
}



resource "aws_iam_role" "lambda" {
  name                = "lambda"
  assume_role_policy  = data.aws_iam_policy_document.lambda_role.json
  managed_policy_arns = [
    aws_iam_policy.logs_policy.arn,
    aws_iam_policy.dynamodb_access_policy.arn,
  ]
}
