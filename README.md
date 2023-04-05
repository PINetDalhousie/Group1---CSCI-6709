## SDN-based Federated Learning System for Detecting DDoS on IoT
### CSCI 6709 - Software Defined Networking, Dalhousie University.
#### Han Yang, Nathanael Bowley, Hongwei Zhang, Raham Moghaddam, Ehssan Mousavipour

> System Architecture:  
> <img src="Document/arch.png"  width="50%">

> Abstract:  
Our system has three main components: the controller, switch, and security gateway. The controller takes responsibility for network management and acts as the model parameter aggregation server on the FL. The switch is responsible for communication and will maintain a flow table for routing. The security gateway is the network's access point, which will store the traffic data for IoT devices connected to it and train localized ML models based on saved data. Lastly, the gateway will retrieve an updated global model from the controller and then use it to monitor the communication traffic of the connected device. The controller will inject flow rules on the switch when traffic arrives, and will pass them to the security gateway for attack detection.

> Dataset:
[N-BaIoT Dataset to Detect IoT Botnet Attacks](https://www.kaggle.com/datasets/mkashifn/nbaiot-dataset)


> [Proposal](Document/Proposal.pdf)  
> [Report](Document/)