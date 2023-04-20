#!/bin/bash

# iterate through all pcap files called output.pcap in the current directory
for file in $(find . -name "output.pcap")
do
  # use tshark to extract fields from pcap and convert to CSV
	tshark -r "$file" -T fields -E separator=, -E quote=d -E header=y \
	-e ip.src -e ip.dst -e eth.src -e eth.dst -e frame.len -e frame.time_epoch \
	> "${file%.pcap}.csv"
done
