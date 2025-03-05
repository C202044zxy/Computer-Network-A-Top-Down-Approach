## 6.2 Error-Detection and Techniques

Error-detection techniques allow the receiver to sometimes, *but not always*, detect that bit errors have occurred.

**Checksumming Methods**

In the TCP and UDP protocols, the Internet checksum is computed over all fields. In IP the checksum is computed over the IP header. 

Because transport-layer error detection is implemented in software, it is important to have a simple and fast error-detection scheme such as checksumming. On the other hand, error detection at the link layer is implemented in dedicated hardware in adapters, which can rapidly perform the more complex CRC operations.

**Cyclic Redundancy Check (CRC)**

An error-detection technique widely in today's computer networks is based on *cyclic redundancy check (CRC) codes*. CRC codes are also known as *polynomial codes*.  

CRC codes operate as follows. Consider the $d$-bit piece of data $D$. The sender and receiver must first agree on an $r+1$ bit pattern, known as a *generator*, which we will denote as $G$. We will require that the most significant bit of $G$ be 1.

For a given piece of data $D$, the sender will choose $r$ additional bits $R$, and append them to $D$ such that the resulting $d+r$ bit is exactly divisible by $G$ using modulo-2 arithmetic.

In modulo-2 arithmetic, addition and subtraction are identical, and both are equivalent to the bitwise XOR. Multiplication and division are the same as in base-2 arithmetic, except that any required addition or subtraction is done without carries or borrows.

Let's now turn to the crucial question of how the sender computes $R$. Recall that we want to find $R$ such that there is an $n$ such that:
$$
D\cdot 2^r\oplus R = nG
$$
Moving $R$ to the right side:
$$
D\cdot 2^r = nG\oplus R
$$
This equation tells us if we divide $D\cdot 2^r$ by $G$, the value of the remainder is precisely $R$. Therefore, we can calculate $R$ as:
$$
R = D\cdot 2^r \bmod G
$$
Figure 6.7 illustrates this calculation for the case of $D=101110,d=6,G=1001$ and $r=3$. The 9 bits transmitted in this case are $101110011$.

<img src="\pictures\6-1.png" width = 500>

Each of the CRC standards can detect burst errors of fewer than $r+1$ bits. Furthermore, under appropriate assumptions, a burst of length greater than $r+1$ bits is detected with probability $1-0.5^r$.

## 6.3 Multiple Access Links and Protocols

A *point-to-point link* consists of a single sender at one end of the link and a single receiver at the other end of the link. The second type of link, a *broadcast link*, can have multiple sending and receiving nodes all connected to the shared broadcast channel.

How to coordinate the access of multiple sending and receiving nodes to a shared broadcast channel is so-called *multiple access problem*.

To this end, various multiple access protocols are proposed. We can divide any multiple access protocol into one of three categories: *channel partitioning protocols*, *random access protocols*, and *taking-turns protocols*.

A multiple access protocol for a broadcast channel of rate $R$ bps should have the following characteristics:

1. When only one node has data to send, that node has a throughput of $R$ bps.
2. When $M$ nodes have data to send, each node should have an average transmission rate of $R/M$ over some suitably defined interval of time. 
3. The protocol is decentralized. That is, there is no master node.
4. The protocol is simple and inexpensive to implement.  

**Channel Partitioning Protocols**

*Time-division multiplexing (TDM)* divides time into *time frames* and further divides each time frame into $N$ *time slots*. *Frequency-division multiplexing (FDM)* divides the $R$ bps channel into different frequencies and assigns each frequency to one of the $N$ nodes.

A third channel partitioning protocol is *code division multiple access (CDMA)*, which is used in wireless LANs (Chapter 7).

**Slotted ALOHA**

The slotted ALOHA is one of the simplest random access protocol. In our description of slotted ALOHA, we assume the following:

- All frames consist of exactly $L$ bits. 
- Time is divided into slots of size $L/R$ seconds (one slot one frame).
- The nodes are synchronized so that each node knows when the slot begins. 
- If two or more frames collide in a slot, all the nodes detect the collision event before the slot ends. 

The operation of slotted ALOHA in each node is simple:

- When the node has a fresh frame to send, it waits until the beginning of the next slot and transmits the entire frame in the slot. 
- If there isn't a collision, the node has successfully transmitted its frame.
- Otherwise, the node aborts the transmission and retransmits its frame in each subsequent slot with probability $p$ until the frame is transmitted without a collision.

Slotted ALOHA is highly decentralized, because each node detects collisions and independently decides when to retransmit. 

Suppose there are $N$ nodes. The probability that any one of the $N$ nodes has a success is $Np(1-p)^{N-1}$. When $p=\frac{1}{N}$, the maximum efficiency of the protocol is given by $\frac{1}{e} = 0.37$.

**ALOHA**

In pure ALOHA, the nodes are asynchronized. That is, when a frame first arrives, the node immediately transmits the frame into the broadcast channel. Each node thus has asynchronous time frame to retransmit data. 

The probability of ALOHA is given by $Np(1-p)^{2(N-1)}$. We find that the maximum efficiency of the pure ALOHA is only $\frac{1}{2e}$. 

**Carrier Sense Multiple Access (CSMA)**

There are two rules for polite human conversation:

- Listen before speaking. This is called *carrier sensing* — a node listens to the channel before retransmitting. 
- If someone else begins talking at the same time, stop talking. This is called *collision detection* — a transmitting node listens to the channel while it is transmitting. 

There two rules are embodied in the family of *carrier sense multiple access (CSMA)* and *CSMA with collision detection (CSMA/CD)*.

Before analyzing the CSMA/CD protocol, let's summarize its operation from the perspective of an adapter (in a node) attached to a broadcast channel: 

1. The adapter obtains a datagram from the network layer, prepares a link-layer frame, and puts the frame adapter buffer.
2. If the adapter senses the channel is idle, it starts to transmit the frame. Otherwise, it waits until no signal energy is detected. 
3. When transmitting, the adapter monitors for the presence of signal energy coming from other adapters using broadcast channel. 
4. If the adapter detects signal energy, it aborts the transmission. 
5. After aborting, the adapter waits a random amount of time and then back to step 2.

The random amount of time is determined by the *binary exponential backoff* algorithm. When transmitting a frame that has already experienced $n$ collisions, a node chooses the value of $K$ at random from $\{0,1,2,...,2^{n}-1\}$. 

For Ethernet, the actual amount of time a node waits is $K\cdot 512$ bit times (i.e., $K$ times the amount of time needed to send 512 bit into the Ethernet) and the maximum value that $n$ can take is capped at 10.

**Taking-Turns Protocols**

The first taking-turns protocol is the *polling protocol*. The polling protocol requires one of the nodes to be designated as a master node. The master node polls each of the nodes in a round-robin fashion.

The second taking-turns protocol is the *token-passing protocol*. In this protocol there is no master node. A small frame known as a token is exchanged among the node in some fixed order. 

For example, node 1 sends token to node 2 (similarly, 2 to 3,..., N to 1). When a node receives a token, it holds onto the token only if it has some frame to transmit. Otherwise, it immediately forwards the token to the next node. 

