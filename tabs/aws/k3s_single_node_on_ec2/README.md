# ECE with Kubernetes cluster

Blueprints installing a K3S cluster on top of VMs simulating the ECE devices.  
There are two possible scenarios:
1. _single_ece_blueprint_ - installs one ECE (Master and Worker VMs) and installs a K3S single-node cluster.
2. _three_ece_blueprint_ - installs three ECEs (6 VMs in total) and installs a K3S HA cluster.

## Requirements

### Secrets
You need to create the following secrets before deploying blueprints:
- aws_access_key_id
- aws_secret_access_key

### Plugins
You need to upload the following plugins before deploying blueprints:
- cloudify-aws-plugin
- cloudify-fabric-plugin
- cloudify-utilities-plugin

## How to install the deployment setup and deploy K3S cluster on top of it  

1. Verify if your Cloudify CLI is set to the correct Cloudify Manager instance.
   ```sh
   cfy profiles show-current 
   ```
   If not, set it using:
   ```sh
   cfy profiles use (...) 
   ```
2. Set your current directory to the main directory of the repo.
   ```sh
   cd (...)/ece-kubernetes 
   ```
3. Perform the following commands to prepare and upload necessary blueprints.
   ```sh
   cd ..
   rm -f ece-kubernetes.zip
   zip -qr ece-kubernetes.zip ece-kubernetes
   cd -
   cfy blueprint upload -b network_blueprint development/resources/network_blueprint.yaml
   cfy blueprint upload -b vm_blueprint development/resources/vm_blueprint.yaml
   cfy blueprint upload -b ece_blueprint -n ece_blueprint.yaml development_blueprints.zip
   cfy blueprint upload -b witness_blueprint -n witness_blueprint.yaml development_blueprints.zip
   ```
4. Install desired setup.
   ```sh
   cfy install -b single-ece-kubernetes -d single-ece-kubernetes -n single_ece_blueprint.yaml -i 'region_name=eu-west-1' ../ece-kubernetes.zip
   # or
   cfy install -b three-ece-kubernetes -d three-ece-kubernetes -n three_ece_blueprint.yaml -i 'region_name=eu-west-1' ../ece-kubernetes.zip
   # or
   TBD
   ```

## How to uninstall the deployment setup  

1. Verify if your Cloudify CLI is set to the correct Cloudify Manager instance.
   ```sh
   cfy profiles show-current 
   ```
   If not, set it using:
   ```sh
   cfy profiles use (...) 
   ```
2. Uninstall the main deployment and remove blueprints.
   ```sh
   cfy uninstall (...)-ece-kubernetes 
   cfy blueprint delete network_blueprint
   cfy blueprint delete vm_blueprint
   cfy blueprint delete ece_blueprint
   ```
