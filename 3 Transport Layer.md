## 3.3 Connectionless Transport: UDP

Some applications are better suited for UDP for the following reasons:

- *Finer application-level control over what data is sent, and when*. Real-time applications often require a minimum sending rate, do not want to overly delay segment transmission, and can tolerate some data loss. UDP's service is well matched to these application's needs.
- *No connection establishment*.
- *No connection state*.
- *Small packet header overhead*.

<img src="pictures\3-1.png" width = 600>

The UDP checksum provides for error detection. UDP at the sender side performs the 1s complement of the sum of all the 16-bit words in the segment. If no errors are introduced into the packet, then clearly the sum at the receiver will be all ones.

## 3.5 Connection-Oriented Transport: TCP

**The TCP Connection**

TCP is said to be *connection-oriented* because before one application process can begin to send data to another, the two processes must first *handshake* with each other. 

A TCP connection is also always *point-to-point*, that is, between a single sender and a single receiver. 

<img src="\pictures\3-2.png" width = 500>

As shown in Figure 3.28, TCP directs this data to the connection's send buffer. The maximum amount of data that can be grabbed and placed in a segment is limited by the *maximum segment size (MSS)*. TCP pairs each chunk of client data with a TCP header, thereby forming *TCP segments*. 

**TCP Segment Structure**

<img src="\pictures\3-3.png" width = 550>

Figure 3.29 shows the structure of the TCP segment. As with UDP, the header includes source and destination port numbers, which are used for multiplexing/demultiplexing data from/to upper-layer applications.

A TCP segment header also contains the following field:

- The 32-bit *sequence number field* and the 32-bit *acknowledgment number field* are used by TCP sender and receiver in implementing a reliable data transfer service. 
- The 16-bit *receive window field* is used for flow control. 
- The 4-bit *header length field* specifies the length of the TCP header in 32-bit words.
- The *flag field* contains 6-bits. The ACK bit is used to indicate that the value carried in the acknowledgment field is valid. The RST, SYN and FIN bits are used for connection setup and teardown. The CWE and ECE bits are used in explicit congestion notification. 

The acknowledgment number that Host A puts in its segment is the sequence number of the next byte Host A is expecting from Host B. Because TCP only acknowledges bytes up to the first missing byte in the stream, TCP is said to provide *cumulative acknowledgment*. 

**Round-Trip Time Estimation and Timeout**

The sample RTT, denoted `SampleRTT`, for a segment is the amount of time between when the segment is sent and when an acknowledgment for the segment is received. 

Obviously the `SampleRTT` values will fluctuate from segment to segment due to congestion in the routers and to the varying load on the end systems. 

Upon obtaining net `SampleRTT`, TCP updates `EstimatedRTT`:
$$
EstimatedRTT = (1-\alpha)\cdot EstimatedRTT+\alpha\cdot SampleRTT
$$
The recommended value of $\alpha$ is $0.125$.

In addition to having an estimate of the RTT, it is also valuable to have a measure of the variability of RTT. `DevRTT` is given by:
$$
DevRTT=(1-\beta)\cdot DevRTT+\beta\cdot|SampleRTT-EstimatedRTT|
$$
The recommended value of $\beta$ is $0.25$.

All of these considerations are taken into account in TCP's method for determining the retransmission timeout interval:
$$
TimeoutInterval=EstimatedRTT+4\cdot DevRTT
$$
An initial `TimeoutInterval` value of $1$ second is recommended. Also, when a timeout occurs, the value of `TimeoutInterval` is doubled to avoid a premature timeout occurring for a subsequent segment that will soon be acknowledged.

**Flow Control**

TCP provides flow control by maintaining a variable called the *receive window*. The receive window is used to give the sender an idea of how much free buffer space is available at the receiver. 

Because TCP is not permitted to overflow the allocated buffer, we must ensure the following property at the receiver:
$$
LastByteRcvd-LastByteRead\leq RcvBuffer
$$
The receive window, denoted `rwnd` is set to the amount of spare room in the buffer:
$$
rwnd=RcvBuffer-[LastByteRcvd-LastByteRead]
$$
The meaning of `rwnd` is illustrated in Figure 3.38:

<img src="\pictures\3-4.png" width = 600>

The sender in turn keeps track of two variables, `LastByteSent` and `LastByteAcked`. Note that `LastByteSent-LastByteAcked` is the amount of unacknowledged data that $A$ hash sent into the connection. 

By keeping the amount of unacknowledged data less than the value of `rwnd`, the sender is assured that it is not overflowing the receive buffer at the receiver:
$$
LastByteSent-LastByteAcked\leq rwnd
$$
If `rwnd=0`, the TCP specification requires sender to continue to send segments with one data byte when receive window is zero (in order to get acknowledgment).

**TCP connection Management**

The TCP in the client then proceeds to establish a TCP connection with the TCP in the server in the following manner:

1. The client first sends *TCP SYN segment*, with the SYN bit is set to $1$. In addition, the client randomly chooses an initial sequence number `client_isn` and puts this number in the sequence number field.
2. The server extracts the TCP SYN segment from the datagram, allocates the TCP buffers and variables to the connection, and sends a connection-granted segment to the client TCP. First, the SYN bit is set to $1$. Second, the acknowledgment field of the TCP segment header is set to `client_isn+1`. Finally, the server chooses its own initial sequence number `server_isn`. This connection-granted segment is referred to as a *SYN ACK segment*.
3. Upon receiving the SYN ACK segment, the client also allocates buffers and variables to the connection. The client puts the `server_isn+1` into the acknowledgment field and set SYN to $0$. This third stage may carry data in the segment payload. 

This connection-establishment procedure is referred to as a *three-way handshake*. 

## 3.7 TCP Congestion Control

The TCP congestion-control mechanism operating at the sender keeps track of an additional variable, called *congestion window*. The congestion window `cwnd` imposes a constraint on the rate at which a TCP sender can send traffic into the network:
$$
LastByteSent-LastByteAcked\leq \min\{cwnd,rwnd\}
$$
The sender's sending rate is roughly `cwnd/RTT`. By adjusting the value of `cwnd`, the sender can therefore adjust the rate at which it sends data into its connection. 

The following guiding principles is applied when adjusting TCP's sending rate:

- A lost segment implies congestion. So the TCP sender's rate should be decreased when a segment is lost.
- An acknowledged segment indicates that the network is delivering the sender's segments to the receiver. So the sender's rate can be increased when an ACK arrives for a previously unacknowledged segment.
- *Bandwidth probing*. TCP increases its transmission rate in response to arriving ACKs until a loss event occurs. 

*TCP congestion-control algorithm* has three components: (1) slow start, (2) congestion avoidance, and (3) fast recovery. 

**Slow Start**

In the *slow-start* state, the value of `cwnd` begins at $1$ MSS and increases by $1$ MSS every time a transmitted segment is first acknowledged. 

The following two events will end the exponential growth of slow-start stage:

- If there is a loss event indicated by a timeout, the TCP sender sets the value of `cwnd` to $1$ MSS and begins the slow start process again. It also sets the value of slow start threshold `ssthresh` to `cwnd/2`.
- If the value of `cwnd` equals `ssthresh`, slow start ends and TCP transitions into congestion avoidance mode. 

**Congestion Avoidance**

In congestion avoidance stage, each arriving ACK increases the congestion window linearly (of $1$ MSS per RTT).

If there is a timeout event, it goes back to slow-start state. If a triple duplicate ACKs were received, the fast-recovery state is the entered. 

**Fast Recovery**

In the case that three duplicate ACKs are received, the TCP sender performs a *fast retransmit*, retransmitting the missing segment before that segment's timer expires. 

In fast recovery, the value of `cwnd` is increased by $1$ MSS for every duplicate ACK received for the missing segment that caused TCP to enter the fast-recovery state.

Eventually, when an ACK arrives for the missing segment, TCP enters the congestion-avoidance state. If a timeout event occurs, fast recovery transitions to the slow-start state.

<img src="\pictures\3-5.png" width = 700>

Figure 3.51 presents the complete description of TCP's congestion-control algorithms. 

