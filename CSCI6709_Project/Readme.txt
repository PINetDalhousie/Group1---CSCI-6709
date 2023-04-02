There are following instructions might need take to run the Demo:

1. Downloading the "processedDataset" and make it under folder named "dataset"

2. Open two terminal, one for controller, another for mininet

3. Terminal1 Go to the path /Desktop/ryu/bin, run command python3.8 ryu-manager --observe-links <Path of controller>/controller.py

4. Terminal2 go to the path ./src, run command sudo -E mn --custom myTopo.py --topo create_topo --switch ovs --controller=remote --arp --mac

5. In mininet, call xterm h1, xterm h2, xterm h3 to access three hosts

6. Under host1 go to folder client, run: python3 server1.py (To enbale the aggregrator).

7. Under host2, go to folder server, run: python3 client1.py (To enbale the worker1).

8. Under host3 go to folder client, run: python3 client2.py (To enbale the worker2).

9. repeat for other clients.
