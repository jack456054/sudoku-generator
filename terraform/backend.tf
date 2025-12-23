terraform {
  backend "gcs" {
    # Bucket and prefix will be passed via -backend-config in deploy.sh
    # prefix = "sudoku-generator"
  }
}
