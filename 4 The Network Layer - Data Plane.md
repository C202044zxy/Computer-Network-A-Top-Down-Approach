## 4.1 Overview of Network Layer

The primary role of network layer is to move packets from a sending host to a receiving host. To do so, two important network-layer functions can be identified:

- *Forwarding* refers to the router-local action of transferring a packet from an input link interface to the appropriate output link interface. 
- *Routing* refers to the network-wide process that determines the end-to-end paths that packets take from source and destination. 

A key element in every network router is its *forwarding table*. The value stored in the forwarding table entry for those values indicates the outgoing link interface at that router to which that packet is to be forwarded. 

<img src="\pictures\4-1.png" width = 600>

In figure 4.3, control-plane routing functionality is separated from the physical router — the routing device performs forwarding only, while the remote controller computes and distributes forwarding tables. 

The control-plane approach is at the heart of *software-defined networking (SDN)*. 

## 4.2 What's Inside a Router

Four router components can be identified in a generic router architecture:

- *Input ports*. Note that the term port refers to the physical input and output router interfaces.
- *Switching fabric*. The switching fabric connects the router's input ports to its output ports.
- *Output ports*. An output port stores packets received from the switching fabric and transmits these packets on the outgoing link by performing the necessary link-layer and physical-layer functions. 
- *Routing processor*. The routing processor performs control-plane functions. 

**Longest Prefix Matching**

<img src="\pictures\4-2.png" width = 600>

With this style of forwarding table, the router matches a prefix of the packet's destination address with the entries in the table. If there is a match, the router forwards the packet to a link associated with the match.

When there are multiple matches, the router uses the *longest prefix matching rule*. That is, it forwards the packet to the link interface associated with the longest prefix match.

**Weighted Fair Queuing (WFQ)**

https://web.mit.edu/pifo/pifo-sigcomm.pdf

## 4.3 IPv4

**IPv4 Datagram Format**

<img src="\pictures\4-3.png" width = 500>

As shown in Figure 4.16, the key fields are the following:

- *Type of service*. This allows different types of IP datagrams to be distinguished from each other (e.g., real-time datagrams and non-real-time traffic).
- *Identifier, flags, fragmentation offset*. These fields have to do with IP fragmentation.
- *Time-to-live*. The time-to-live (TTL) field is included to ensure that datagrams do not circulate forever in the network. 

**IPv4 Datagram Fragmentation**

The maximum amount of data that a link-layer frame can carry is called the *maximum transmission unit (MTU)*. Different link-layer protocols can have different MTUs.

What if the link has an MTU that is smaller than the length of the IP datagram. The solution is to fragment the payload in the IP datagram into two or more smaller IP datagrams. 

To allow the destination host to perform these reassembly tasks, the designer of IPv4 put *identification, flag, and fragmentation offset* fields in the IP datagram header. 

When the destination receives a series of datagrams from the same sending host, it can examine the identification numbers of the datagrams to determine which of the datagrams are actually fragments of the same larger datagram.

In order for the destination host to be absolutely sure it has received the last fragment of the original datagram, the last fragment has a flag bit set to 0, whereas all the other fragments have this flag bit set to 1​.

**IPv4 Addressing**

A host typically has only a single link into the network. The boundary between the host and the physical link is called an *interface*. Thus, an IP address is technically associated with an interface, rather than with the host or router containing the interface. 

IP addresses are written in *dotted-decimal notation*, where each byte of the address is written in its decimal form and is separated by a dot (e.g., 193.32.216.9).

<img src="pictures\4-4.png" width = 600>

As shown in Figure 4.18, three host interfaces (223.1.1.1, 223.1.1.2, 223.1.1.3) and one router interface (223.1.1.4) forms a *subnet*.

IP addressing assigns an address to this subnet: 223.1.1.0/24, where the /24 notation, sometimes known as a *subnet mask*, indicates that the leftmost 24 bits of the 32-bit quantity define the subnet address. 

**DHCP: The Dynamic Host Configuration Protocol**

A network administrator can configure DHCP so that a given host receives the same IP address each time it connects to the network, or a host may be assigned a *temporary IP address* that will be different each time the host connects to the network. 

Because of DHCP's ability to automate the network-related aspects of connecting a host into a network, it is often referred to as a *plug-and-play* or *zeroconf* protocol. 

<img src="\pictures\4-5.png" width = 500>

In Figure 4.24, `yiaddr` (your Internet address) indicates the address being allocated to the newly arriving client. The DHCP protocol is a four-step process:

- *DHCP server discovery*. This is done using a DHCP discovery message, which a client sends within a UDP packet to port 67. The DHCP client creates a broadcast message with destination IP address of 255.255.255.255 and a host source IP address of 0.0.0.0.
- *DHCP server offer(s)*. A DHCP offer message broadcasts to all nodes on the subnet, using the IP broadcast address of $255.255.255.255$. Several offers are provided, which contains the transaction ID, the IP address, and IP *address lease time* — the amount of time for which the IP address will be valid.  
- *DHCP request*. The client will choose from one or more server offers and respond with a DHCP request message. The source IP address is 0.0.0.0, since it still doesn't have an IP address.
- *DHCP ACK*.

**NAT**

*NAT (Network Address Translation)* is a technique to modify the source or destination IP address of packets as they pass through a router or firewall. NAT is commonly used to allow multiple devices on a local network (such as a home or office network) to share a single public IP address when accessing the internet.

The NAT-enabled router does not look like a router to the outside world. Instead the NAT router behaves to the outside world as a single device with a single IP address. 

But how does the router know the internal host to which it should forward a given datagram? The trick is to use a *NAT translation table* at the NAT router, and to include port numbers as well as IP addresses in the table entry. 

<img src="\pictures\4-6.png" width = 600>

## 4.4 IPv6

**IPv6 Datagram Format**

The most important changes introduced in IPv6 are:

- *Expanded addressing capabilities*. IPv6 increases the size of the IP address from 32 to 128 bits. In addition to unicast and multicast addresses, IPv6 has introduced a new type of address, called an *anycast address*, that allows a datagram to be delivered to any one of a group of hosts.
- *A streamlined 40-byte header*. The 40-byte fixed-length header allows for faster processing of the IP datagram by a router. 
- *Flow labeling*. This allows labeling of packets belonging to particular flows for which the sender requests special handling, such as a non-default quality of service or real-time service. 

<img src="\pictures\4-7.png" width = 600>

As shown in Figure 4.26, some unfamiliar fields in IPv6 are:

- *Traffic class.* The 8-bit traffic class field, like the TOS field in IPv4, can be used to give priority to certain datagrams within a flow / from certain applications. 
- *Next header*. This field identifies the upper-layer protocol (e.g., TCP or UDP). 
- *Hop limit*. The contents of this field are decremented by one by each router that forwards the datagram. If the hop limit count reaches zero, the datagram is discarded. 

Comparing the IPv6 datagram format with the IPv4 datagram format, we note that several fields are discarded in IPv6 datagram:

- *Fragmentation*. If an IPv6 datagram received by a router is too large to be forwarded over the outgoing link, the router simply drops the datagram and sends a "Packet Too Big" ICMP error message. 
- *Header checksum*. Because the transport-layer and link-layer protocols perform check-summing, the designer probably felt the checksum in IPv4 is redundant. Once again, fast processing of IP packets is a central concern. 
- *Options*. The option is no longer a part of the IP header. However, the options fields is one of the possible next headers that the IPv6 header points to (like TCP and UDP). 

**Tunneling**

The approach to IPv4-to-IPv6 transition involves *tunneling*.

<img src = "\pictures\4-8.png" width = 600>

Suppose two IPv6 nodes (in this example, B and E in Figure 4.27) want to interoperate using IPv6 datagrams but are connected to each other by intervening IPv4 routers.

We refer to the intervening set of IPv4 router between two IPv6 routers as a *tunnel*. With tunneling, the node B takes the entire IPv6 datagram and puts it in the data field of an IPv4 datagram. 

On receiving the IPv4 datagram, node E extracts the IPv6 datagram, and then routes the IPv6 datagram as it had received the IPv6 datagram from a directly connected IPv6 neighbor. 

