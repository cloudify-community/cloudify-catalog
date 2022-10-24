variable "project_id" {
  description = "project id"
  default = "cloudify-cs"
}

variable "region" {
  description = "region"
  default = "us-central1"
}

variable "prefix" {
  description = "Resource prefix"
  //default = "xyz"
}

variable "dashboard_crt" {
  description = "Self signed certificate"
  default = "-----BEGIN CERTIFICATE-----\nMIICrzCCAZcCFBigTNToXhwnVMdgYTPKTjrl9G0wMA0GCSqGSIb3DQEBCwUAMBQx\nEjAQBgNVBAMMCWxvY2FsaG9zdDAeFw0yMjAyMDIyMzE3MzJaFw0yMzAyMDIyMzE3\nMzJaMBQxEjAQBgNVBAMMCWxvY2FsaG9zdDCCASIwDQYJKoZIhvcNAQEBBQADggEP\nADCCAQoCggEBAMbkhleBJR1biL8e3vxy7vX47ETk9BRQRvQ9hh+1B9/bxG7VM0p9\n7HCA0PkWbicCgOF2XTYje+FUnUWPu9l2pUMGsZtfqHFTXvjjzUwUgN0T2VWMGxyS\nzinG0bMubQAG2F6FLW4tWbLVTcssjGK47MnBMbGsqhgZSAm4dPl/mJznqceF5HBc\nWy2LLflraFKzzWUVdVgU52ImzMh6PTiXcw6GGj/fLPe9L2oi4M2V74f2445dI2Lr\nw1ayJ47qKZI7MkWfteK96TaqMp/2J/IzEf6XBkT7TJo1ZbyUnV9nQku256h4kHn9\nwhpG4LyISf9I21137VKctbDVBLzV0y79X5UCAwEAATANBgkqhkiG9w0BAQsFAAOC\nAQEAM7pFsz7V8xiF/qiILHMCLdFUnVFvR9XxRcAj9dZsLegt7GpPNyEtj/3VyoGB\nFTGYeaxoU7Y0DHMrgnbNhcq78GjK1TlfYUTjS1pCNioDiUY0Pw5FakOCcbPKiX+/\nhD5NAnwSMj0vdhx2Pbmede1vIpH9qRePUSBusfPxomAZE9ptIlgkkOfs1j6OSUs9\nmBSQ+Oh1SL68Nc95cO7LMr7A7Whw6upGhMz2V2JFn7PGR9dd0T4VYXdih5uokHIA\n2HyZ3EK207rlc7FV5elt2rfmerzwALMzLh4pa+RJRpFFz6F7pXegPSxDYvMn4HxM\nQkEQxcCbUoi3zvUIalO/G5JlYg==\n-----END CERTIFICATE-----"
}

variable "dashboard_key" {
  description = "Private key"
  default = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAxuSGV4ElHVuIvx7e/HLu9fjsROT0FFBG9D2GH7UH39vEbtUz\nSn3scIDQ+RZuJwKA4XZdNiN74VSdRY+72XalQwaxm1+ocVNe+OPNTBSA3RPZVYwb\nHJLOKcbRsy5tAAbYXoUtbi1ZstVNyyyMYrjsycExsayqGBlICbh0+X+YnOepx4Xk\ncFxbLYst+WtoUrPNZRV1WBTnYibMyHo9OJdzDoYaP98s970vaiLgzZXvh/bjjl0j\nYuvDVrInjuopkjsyRZ+14r3pNqoyn/Yn8jMR/pcGRPtMmjVlvJSdX2dCS7bnqHiQ\nef3CGkbgvIhJ/0jbXXftUpy1sNUEvNXTLv1flQIDAQABAoIBAQCZJh7MAoWxtWn2\nwK6zdUzL2oEUC7hma+o256j/gUYu+eqn7UMxeQU3G/nN05e+Mg9LjPj5VxlsyNrR\nVXwwV0up8N2R5natzKS0wbSzgJY5pa8UUG4P8nsNcCrI7lbAToUNQz9YN1N6gQUG\nDaeL3Rl3wWuihHH1XII7+e0YsUeyiNMDlh0MSJ7v1yGOxQ1PzSyDGmZVe5RJiA7J\ncskGDOLgTCURuQWvFqefTlACbZNkPsz+0NhbuPCgE95SDqylMj9AUp9XJNaW4O2N\n3yXxW6TxNLGXgdl8bGvM9CvBzlGM3T0p2kFSV6wFqJrMzfUDV8Gr75XXfHTmYBkE\nlww/ZX2BAoGBAPgGyHKhl7GVzxsafY7TsCSyxaIJ+cuqb9JN7aLlblFQg4meHj07\njiEJ88sh+uIxMqQd3rKlZ6oqLq8QsHSGT2xizEEQ8qtHyFA3KRBPXV17FM2FnsF/\nT+JbAkV7u8VV60+rr78bFkgQW7UwK8vZR+cf/2nBnJg82KO+JX3D4E/DAoGBAM1J\nYOlF5GxE1SWr7D8C22tAex7fOO2Wx5NO35+329DVT1JOfHmtbha0pf9YgM5DW0r6\nKejNqV9WX3DVVSXuDqbyzmz6WymANsMqkB3iIwZtTR/ZPHo7K8MMq93diABP+kt+\nC6SAtIMkmVoHhy1hg+6KKr9E736DoC0vy1uitDXHAoGAPig1A8VLZs3MYVZ6MNkM\nQ6YpsToex9OmwmWVMEWfJ/GthUeC/IV4UP9VgYq6fQUnU8nIjay2FgcMPANKtWkT\nbm40EfpVVmde4/tu5w98rnix9e+OoZ9uPaPhJdikbgfiOM0l9harttOip/2yfBuv\n0VRLhg1nWR+miyKT8rir9lECgYEAsMdjwP4C+ok707j9NDXNpcpdO/SWHWMecegW\nAoBdtrQ6HnKgFlgW2U6vM/iO0xCF6UcMGAIivIqwnYXYUVVzIKkuwgHFxzM19VMN\nz+4Qo1Q0ehykS83wnYKn7eL7XumAbMoaVIrQ5634sOKSsa2r4xrwPM2sP5IxuTfT\nMxIlhbkCgYEAsqjWEbwC+54lVtBU92Hr/KZ5anNgwHB1mh1KlMSFIEN1FicNOb59\nAQGwurUtGMzj1rHgiRUyN/if1SYmK+7tv7CBFoAM5H9TWhKL0CMpRBqO6f5ZyNMx\nbAOPjklEEFRHi69+lwUk0MUhAfDSwT6qjKvhFI7WOn0KTF7JuRtVPrU=\n-----END RSA PRIVATE KEY-----"
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.17.0"
    }
  }

  required_version = ">= 0.14"
}

provider "google" {
  project     = var.project_id
  region      = var.region
  zone        = "${var.region}-a"
}