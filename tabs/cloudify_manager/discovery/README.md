### Adding sub-manager through the discovery blueprint
First step is to deploy [manager_discovery.yaml](/submanager_discovery/manager_discovery.yaml) with proper inputs:
- ***endpoint*** - ip of sub manager 
- ***tenant*** - name of submanagar tenant
- ***protocol*** - protocol used by sub manager
- ***port*** - number of port which sub manager is exposed

#### Installation via User Interface
[Upload](https://docs.cloudify.co/latest/working_with/console/widgets/blueprintuploadbutton/) [manager_discovery.yaml](/submanager_discovery/manager_discovery.yaml) to Spire Manager.

Next, click ***Deploy*** under the blueprint tile. Instead of this, you can also click on the blueprint name and next ***[Create deployment](https://docs.cloudify.co/latest/working_with/console/widgets/blueprintactionbuttons/)***

After that, the following window will appear:
![This is an image](/images/submanager_exposition.png)

Fill all necessary information and click ***Install*** button at the bottom of the dialog to start the ***Install*** workflow.
To make sure if *Environment* is installed successfully, check the ***Verification of Installation*** chapter in the following part.