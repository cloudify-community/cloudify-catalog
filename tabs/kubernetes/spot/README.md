# Provisioning Spot Ocean EKS Cluster Examples

See [Cloudify Manager Blueprints guide](https://docs.cloudify.co/latest/) for a blueprint authoring guide.

Note about `spot.yaml` blueprint:
`SPOT_ACCOUNT_ID` and `SPOT_TOKEN` needs to be set as secrets prior to running the deployment. 
You have to register with Spot.io for account and generate a token. 
`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are taken from secrets.
`AWS_DEFAULT_REGION` is taken from Inputs.
