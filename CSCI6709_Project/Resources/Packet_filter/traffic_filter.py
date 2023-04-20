from scapy.all import *
import sys
import csv

if len(sys.argv) < 2:
    print('Pass 1 argument: the pcap file')
    exit(1)

# Replace "input.pcap" with the name of your pcap file
packets = rdpcap(sys.argv[1])

# Define a filter function to check if the destination port is 8080
def filter_8080(packet):
    return packet.haslayer(TCP) and (packet[TCP].dport or packet[TCP].sport) == 8080

print(packets)

# Filter the packets using the filter function
filtered_packets = filter(filter_8080, packets)

print(filtered_packets)

# Write the filtered packets to a new pcap file called "output.pcap"
wrpcap("output.pcap", filtered_packets)

headers = ["Time", "Source IP", "Destination IP", "Source MAC", "Destination MAC", "PacketLength"]

import pandas as pd

df = pd.read_csv("output.csv")


first_timestamp = df['frame.time_epoch'].iloc[0]

# calculate the relative time
df['relative_time'] = df['frame.time_epoch'] - first_timestamp

print(df.head().to_string())

df.to_csv('data.csv', index=False)




