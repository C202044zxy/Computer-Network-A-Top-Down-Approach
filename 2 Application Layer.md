## 2.1 Principles of Network Applications

In a client-server architecture, there is an always-on host, called the *server*, which services requests from many other hosts, called *clients*.

A process sends messages into, and receives messages from, the network through a software interface called a *socket*. 

<img src="\pictures\2-1.png" width = 600>

As shown in this figure, a socket is the interface between the application layer and the transport layer within a host. It is also referred to as the *Application Programming Interface (API)* between the application and the network. 

## 2.2 The Web and HTTP

The *hypertext transfer protocol (HTTP)*, the Web's application-layer protocol, is at the heart of the Web. HTTP uses TCP as its underlying transport protocol. 

Because an HTTP server maintains no information about the clients, HTTP is said to be a *stateless protocol*. 

**Cookies**

Cookies allow sites to keep track of users. Most major commercial Web sites use cookies today. 

<img src = "pictures\2-2.png" width = 600>

As shown in Figure 2.10, cookie technology has four components:

1. A cookie header line in the HTTP response message.
2. A cookie header line in the HTTP request message. 
3. A cookie file kept on the user's end system and managed by the user's browser. 
4. A back-end database at the Web site. 

During the visiting sessions, the browser passes a cookie header to the server, thereby identifying the user to the server. Cookies can thus be used to create a user session layer on top of stateless HTTP.

**Web Caching**

A *Web cache* — also called a *proxy server* — is a network entity that satisfies HTTP requests on the behalf of an origin Web server. 

<img src = "pictures\2-3.png" width = 600>

As shown in Figure 2.11, a user's browser can be configured so that all of the user's HTTP requests are first directed to the Web cache. If a browser is requesting a object, here is what happens:

1. The browser establishes a TCP connection to the Web cache and sends an HTTP request for the object to the Web cache. 
2. The Web cache checks to see if it has a copy of the object stored locally. If it does, the Web cache returns the object within an HTTP response message to the client browser.
3. If the Web cache does not have the object, the Web cache opens a TCP connection to the origin server. 
4. When the Web cache receives the object, it stores a copy in its local storage and sends a copy. 

Note that a cache is both a server and a client at the same time. When it receives requests from and sends reposes to a browser, it is a server. When it sends requests to and receives responses from an origin server, it is a client. 

## 2.4 DNS — The Internet's Directory Service

**Services Provided by DNS**

While people prefer the more mnemonic hostname identifier, routers prefer fixed-length, hierarchically structured IP addresses. The *domain name system (DNS)* is responsible for translating hostname to IP address.

In depth, the DNS is a distributed database implemented in a hierarchy of DNS servers, and an application layer protocol that allows hosts to query the distributed database. 

DNS provides a few other important services:

- *Host Aliasing*. A host with a complicated hostname (canonical hostname) can have one or more alias names.
- *Mail server aliasing*. DNS can be invoked by a mail application to obtain the canonical hostname for a supplied alias hostname as well as the IP address of the host.
- *Load distribution*. Busy sites are replicated over multiple servers. For replicated Web servers, a set of IP addresses is associated with one canonical hostname. Because a client typically sends its HTTP request message to the IP address that is listed first in the set, DNS rotation distributes the traffic among the replicated servers.

**A Distributed, Hierarchical Database**

<img src="\pictures\2-4.png" width = 600>

As shown in Figure 2.17, there are three classes of DNS servers:

- *Root DNS servers*.
- *Top-level domain (TLD) servers*. For top-level domains (com, org and gov), and all of the country top-level domains (uk, fr and jp), there is TLD server. 
- *Authoritative DNS servers*. Every organization with publicly accessible hosts on the Internet must provide publicly accessible DNS records that map the names of those hosts to IP addresses. 

<img src="\pictures\2-5.png" width = 400>

Figure 2.19 shows what is happening when host `cse.nyu.edu` desires the IP address of `gaia.cs.umass.edu`. Here is the detailed process: 

1. The requesting host sends a DNS query message to its local DNS server.
2. The local DNS server consults root DNS server. The root DNS server takes note of the `edu` suffix and returns to the local DNS server a list of IP addresses of corresponding TLD servers. 
3. The local DNS server then resends the DNS query message to one of the TLD servers. The TLD server takes note of the `umass.edu` suffix and responds the IP address of the authoritative DNS server of Massachusetts.
4. Finally, the local DNS server resends the message to `dns.umass.edu`, which responds with the IP address of `gaia.cs.umass.edu`.

The example shown above makes use of both *recursive queries* and *iterative queries*. The query sent from `cse.nyu.edu` to `dns.nyu.edu` is a recursive query, since the query asks `dns.nyu.edu` to obtain the mapping on behalf. But the subsequent three queries are iterative because all the results are directly returned to `dns.nyu.edu`.

**DNS Records**

The DNS server that together implement the DNS distributed database store *resource records (RRs)*. A resource record is a four-tuple that contains the following field:

``(Name, Value, Type, TTL)``

The meaning of `Name` and `Value` depends on `Type`:

- If `Type=A`, then `Name` is a hostname and `Value` is the corresponding IP address.
- If `Type=NS`, then `Name` is a domain and `Value` is the hostname of an authoritative DNS server that knows how to obtain the IP addresses for hosts in the domain. 
- If `Type=CNAME`, then `Value` is a canonical hostname for the alias hostname `Name`.
- If `Type=MX`, then `Value` is the canonical name of a mail server that has an alias hostname `Name`.

## 2.5 Peer-to-Peer File Distribution

**Scalability of P2P Architectures**

<img src="\pictures\2-6.png" width = 500>

As shown in Figure 2.22, the server and peers are connected to the Internet with access links. Denote the upload rate of the server's access link by $u_s$ and the upload/download rate of $i$-th peer's access link by $u_i/d_i$. 

Also denote that the size of the file to be distributed by $F$ and the number of peers that want to obtain a copy of the file by $N$. The *distribution time* is the time it takes to get a copy of the file to all $N$ peers. 

Let's go through the analysis for the P2P architecture, where each peer can assist the server in distributing the file:

- At the beginning of the distribution, only the server has the file. To get this file into the community of peers, the server must send each bit of the file at least once into its access link. Thus, the minimum distribution time is at least $F/u_s$. 
- As with the client-server architecture, the peer with the lowest download rate can not obtain all $F$ bits of the file in less than $F/d_{\min}$.
- Finally, the system must deliver $F$ bits to each of the $N$ peers, thus delivering a total of $NF$ bits. This can not be done at a rate faster than $(u_s+\sum_{i=1}^N u_i)$.

Thus, we obtain the minimum distribution time for P2P, denoted by $D_{P2P}$ :
$$
D_{P2P}\geq \max\{\frac{F}{u_s},\frac{F}{d_{\min}},\frac{NF}{u_s+\sum_{i=1}^N u_i}\}
$$
It turns out that if we imagine that each peer can redistribute a bit as soon as it receives the bit, then there is a redistribution scheme that actually achieves this lower bound. 

Applications with the P2P architecture can be self-scaling. This scalability is a direct consequence of peers being redistributors as well as consumers of bits. 

**BitTorrent**

The collection of all peers participating in the distribution of a particular file is called a *torrent*. Each torrent has an infrastructure node called a *tracker*. When a peer joins a torrent, it registers itself with the tracker and periodically informs the tracker that it is still in the torrent. In this manner, the tracker keeps track of the peers that are participating in the torrent. 

In deciding which chunks to request, Alice uses a technique called *rarest first*. In this manner, the rarest chunks get more quickly distributed. 

To determine which requests she respond to, BitTorrent uses a clever trading algorithm. Alice continually measures the rate at which she receives bits and determines the four peers that are feeding her bits at the highest rate. She then reciprocates by sending chunks to these same four peers. 

Every 10 seconds, she recalculates the rates and possibly modifies the set of four peers. Importantly, every 30 seconds, she also picks one additional neighbor at random and sends it chunks. 

In other words, every 30 seconds Alice will randomly choose a new trading partner and initiate trading with that partner. (Think about why?) 