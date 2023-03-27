disable_mlock = true
ui = false
storage "file" {
  path = "/mnt/vault/data"
}

listener "tcp" {
  address = "0.0.0.0:8200"
  tls_disable = 1
}