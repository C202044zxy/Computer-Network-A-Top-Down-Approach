## 5.2 Routing Algorithm

We can classify routing algorithm according to whether they are centralized or decentralized:

- A *centralized routing algorithm* computes the least-cost path using complete, global knowledge about the network. Link-state routing algorithm, also known as Dijkstra's algorithm, falls into the category.
- In a *decentralized routing algorithm*, the calculation of the least-cost path is carried out in a distributed manner by the routers. Distance-vector algorithm is an example.

In distance-vector algorithm, each node $x$ maintains a vector $D_x$ containing $x$'s estimate of its cost to all destinations $y$. The Bellman-Ford equation is applied to update its own distance vector as follows:
$$
\forall y,\ D_x(y)=\min_v\{c(x,v)+D_v(y)\}
$$

## 5.3 Intra-AS Routing in the Internet: OSPF

An *autonomous system (AS)* consists of a group of routers that are under the same administrative control. The routing algorithm running within an autonomous system is called an *intra-autonomous system routing protocol*.

*Open shortest path first (OSPF)* routing is a link-state protocol that is widely used for intra-AS routing in the Internet. With OSPF, each router constructs a complete graph of the entire AS. Each router then locally runs Dijkstra's algorithm to determine a shortest-path tree to all subnets, with itself as the root node. 

A router broadcasts routing information to all other routers in the AS. It also broadcasts a link's state periodically, even if the link's state has not changed.

## 5.4 Routing Among the ISPs: BGP

*Border Gateway Protocol (BGP)* is a protocol that glues the thousands of ISPs in the Internet together. BGP is a decentralized and asynchronous protocol in the vein of distance-vector routing. 

In BGP, packets are not routed to a specific destination address, but instead to CIDRized prefixes (e.g., 138.16.68/22). 

**Advertising BGP Route Information**

For each AS, each router is either a *gateway router* or an *internal router*. A gateway router is a router that directly connects to one or more routers in other AS. An internal router connects only to hosts and routers within its own AS.

In BGP, pairs of routers exchange routing information over semi-permanent TCP connections using port 179. Such TCP connection is called a BGP connection. 

**Determining the Best Routes**

When a router advertises a prefix across a BGP connection, it includes with the prefix several BGP attributes. Two of the attributes are:

- `AS-PATH`. To generate the AS-PATH value, when a prefix is passed to an AS, the AS adds its ASN to the existing list in the AS-PATH. Note that the ASN of the source node is not included. 
- `NEXT-HOP`. The NEXT-HOP is the IP address of the router interface that begins the AS-PATH.

<img src="\pictures\5-1.png" width = 600>

Let's look at the example in Figure 5.10. Each router in AS1 becomes aware of two BGP routes to prefix $x$:

| NEXT-HOP                                      | AS-PATH | Destination Prefix |
| --------------------------------------------- | ------- | ------------------ |
| IP address of leftmost interface of router 2a | AS2 AS3 | $x$                |
| IP address of leftmost interface of router 3d | AS3     | $x$                |

**Route Selection Algorithm**

If there are two or more routes to the same prefix, then BGP sequentially invokes the following elimination rules until one route remains:

1. A route is assigned a *local preference* value as one of its attributes. The value of the local preference attribute is a policy decision that is left entirely up to the AS's network administrator. 
2. From the remaining routes, the route with the shortest AS-PATH is selected.
3. From the remaining routes, hot potato routing is used, that is, the route with the closest NEXT-HOP router is selected.
4. If more than one route still remains, the router uses BGP identifier to select the route. 

