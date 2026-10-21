
group "default" {
  targets = ["api", "web"]
}

target "api" {
  context    = "./apps/api"
  dockerfile = "Dockerfile"
  tags       = ["hello-api:1.0"]
}

target "web" {
  context    = "./apps/web"
  dockerfile = "Dockerfile"
  tags       = ["hello-web:1.0"]
}
