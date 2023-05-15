# Juniper Notebook With TensorFlow ResNet-50 Image Inference

## General

The blueprint shows how Cloudify automates endpoint deployment and endpoint monitoring of Machine Learning system, by orchestrating an Intel-optimized TensorFlow workload running inference with a pre-trained ResNet-50 model from the Intel Model Zoo.

## Requirements

In order to run successfully the blueprint you'll need to provide the Kubernetes target cluster, with appropriate credentials in kube_config within Cloudify VM (or modify as per Kubernetes samples for your cluster, https://docs.cloudify.co/latest/trial_getting_started/examples_k8s/ ) .

## Usage

The blueprint creates Junyper Notebook TensorFlow app with set web UI password the to access it using web browser. Before accessing the application, from bastion VM forward ports with

```
kubectl port-forward -n tensorflow-demo service/tensorflow-demo --address 0.0.0.0 8888:8888
```

or appropriate enable LoadBalancer as exposed Kubernetes service type in tensorflow-demo.yaml .

Connect browser to bastion VM public IP port 8888 Jupyter Notebook web UI ( like http://publicip:8888/ or http://cfy-tensorflow-demo:8888/ if you add it to hosts file), enter web UI password.

Available Jupyter Notebooks are for two different types of analysis:

1. Notebook benchmark_data_types_perf_comparison.ipynb: Comparison of data types FP32 and int8 when running on Intel Optimization for TensorFlow:
On Notebook benchmark_data_types_perf_comparison.ipynb web UI in menues click Cells \ Run All. While it runs it will show that kernel is busy, so wait until it is idle again. In Cell 3.2 Pick a Data Type change data_type_index = 0 to data_type_index = 1. Cells \ Run All Cells Below. Wait for test to stop, and in Step 7 see result.

2. Notebook benchmark_perf_comparison.ipynb: Comparing Intel Optimizations for TensorFlow with "Stock TensorFlow" (note that TensorFlow from v2.5 also includes oneDNN optimizations that can be enabled by setting an environment variable):
On Notebook benchmark_perf_comparison.ipynb UI \ Cells \ Run All, wait for it to finish (kernel idle), Kernel \ Change Kernel \ stock-tensorflow. Again run all cells, wait for it to finish, and in Step 5 see result.

## Secrets

The blueprint uses below secret.

| Name                       | Description                           |
| -------------------------- | ------------------------------------- |
| jupyter_notebook_password  | Password for Jupyter Notebook web UI  |

## Plugins

cloudify-kubernetes-plugin

## Inputs

| Display Label                        | Name             | Type    | Default Value  |
| ------------------------------------ | ---------------- | ------- | -------------- |
| Validate Status after k8s deployment | validate_status  | boolean | false          |
