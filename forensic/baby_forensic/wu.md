# Hackday 2024: Baby Forensic

## Challenge information

**Category**: Forensic

**Description**: This challenge is about the analysis of a pcap file. The goal is to find a flag in a file that is transmitted through a TFTP communication.

## Solution

**Step 1: Initial analysis**

We start by opening the pcap file with Wireshark.
We can see that there is a TFTP communication between a client and a server. The client is sending a file to the server.

**Step 2: Recovering the file**

We can see that the file is sent in 512 bytes blocks. We are going to use wireshark to extract the data from the packets.

We select the first data packet and right-click on the packet. We select "Follow" and then "UDP Stream".

![follow_udp_stream.png](follow_udp_stream.png)

We can now see the data in the stream. We select the communication direction (server to client) and we save the data as a raw file.

![stream_direction.png](stream_direction.png)

**Step 3: Analyzing the file**

We now have a raw file that we can analyze. We can see that the file is a Cisco configuration file.

We can rapidly eliminate the `username` line, as it is not exploitable if the password isn't in a wordlist (type 9 cisco password).

The file contains a lot of useless information, but we can see that there is a base64 encoded string in the file.
This string is encoded in the `snmp-server host` line, in the `community` parameter, which not means to be base64 encoded. 

We can decode the string to get the flag.

```bash
cat data | grep "snmp-server host" | awk '{print $6}' | base64 --decode
```

### Flag

We can now see the flag decoded: 
`HACKDAY{1N51de_7He_nEtWOrK}`

## Creator

* Name: [Louis GAMBART](https://linkedin.com/in/louis-gambart)

## References

* [Wireshark](https://www.wireshark.org/)
* [Base64](https://en.wikipedia.org/wiki/Base64)
