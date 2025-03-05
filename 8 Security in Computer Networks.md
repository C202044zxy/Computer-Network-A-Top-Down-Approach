## 8.1 What is Network Security

We can identify the following desirable properties of secure communication:

- *Confidence*. Only the sender and intended receiver should be able to understand the contents of the transmitted message. 
- *Message Integrity*. Alice and Bob want to ensure that the content of their communication is not altered.
- *End-point authentication*. Both the sender the receiver should be able to confirm the identity of the other party involved in the communication. 
- *Operational security.* Operational devices such as firewalls and intrusion detection systems are used to counter attack against an organization's network.

## 8.2 Principles of Cryptography

Suppose now that Alice wants to send a message to Bob. Alice's message in original form is known as *plaintext*, or *cleartext*. Alice encrypts her plaintext message using an encryption algorithm so that the encrypted message, known as *ciphertext*, looks unintelligible to any intruder. 

<img src="\pictures\8-1.png" width = 600>

As shown in Figure 8.2, Alice provides a key $K_A$ as input to encryption algorithm. The notation $K_A(m)$ refers to the ciphertext form of the plaintext message $m$. Similarly, Bob will provide a key $K_B$ to the decryption algorithm. Therefore:
$$
K_B(K_A(m)) = m
$$
In symmetric key systems, Alice's and Bob's keys are identical and are secret. In public key systems, a pair of keys is used. One of the keys is publicly accessed, while the other is known only by either Alice or Bob. 

**Block Ciphers**

One class of symmetric key encryption is *block ciphers*. To encode a block, the cipher uses a one-to-one mapping to map the $k$-bit block of plaintext to a $k$-bit block of ciphertext. One possible mapping for $k=3$ is shown as follows:

<img src="\pictures\8-2.png" width = 600>

However, full-table block ciphers can't scale to large $k$ (e.g. 64). To this end, block ciphers use functions that simulate randomly permuted tables. 

<img src="pictures\8-3.png" width = 600>

An example of such a function for $k=64$ bits is shown in Figure 8.5. The function first breaks a 64-bit block into $8$ chunks, with each chunk consisting of $8$ bits. Each $8$-bit chunk is processed by an $8$-bit full table, which is of manageable size.

Next, the positions of the $64$ bits in the block are then scrambled (permuted) to produce a $64$-bit output. After $n$ such cycles, the function provides a $64$-bit block of ciphertext. The purpose of the rounds is to make each input bit affect most (if not all) of the final input bits. 

Today there are a number of popular block ciphers, including DES (Data Encryption Standard), 3DES, and AES (Advanced Encryption Standard). Each of these standards uses functions, rather than predetermined tables. 

**Cipher-Block Chaining**

For identical blocks, a block cipher would produce the same ciphertext. An attacker could potentially guess the cleartext when it sees identical ciphertext blocks.

To address this problem, we can mix some randomness into the ciphertext. Let $m(i)$ denote the $i$-th plaintext block, $c(i)$ denote the $i$-th ciphertext block. *Cipher Block Chaining (CBC)* operates as follows:

1. The sender generates a random $k$-bit string, called the *Initialization Vector (IV)*. 
2. For the $i$-th block, the sender generates the ciphertext block from $c(i)=K_S(m(i)\oplus c(i-1))$.

**Public Key Encryption**

<img src="\pictures\8-4.png" width = 600>

Let go back to the case where Alice wants to send message to Bob. In Figure 8.6, Bob has two keys — a *public key* $K_B^+$ that is available to everyone in the world, and a *private key* $K_B^-$ that is known only to Bob. 

In order to communicate to Bob, Alice first fetches Bob's public key and computes $K_B^+(m)$. After receiving Alice's ciphertext, Bob compute $K^-_B(K^+_B(m))$, which gives back $m$.

This is a remarkable result! In this manner, Alice can use Bob's publicly available key to send a secret message to Bob without either of them having to distribute any secret keys. 

**RSA**

Over the years, the *RSA algorithm* (named after its founders) has become synonymous with public key cryptography. 

To generate the public and private RSA keys, Bob performs the following steps:

1. Choose two large prime numbers $p$ and $q$. The product of $p$ and $q$ is recommended to be on the order of $1024$ bits. 
2. Compute $n=pq$ and $z=\phi(n)=(p-1)(q-1)$.
3. Choose a number $e <n$ that has no common factors (other than $1$) with $z$. 
4. Find a number $d$ such that $ed=1\bmod z$.
5. The public key that Bob makes available to the world $K_B^+$ is the pair of numbers $(n,e)$. The private key $K_B^-$ is the pair of numbers $(n,d)$.

The encrypted value $c$ of Alice's plaintext $m (m<n)$ is:
$$
c=m^e\mod n
$$
To decrypt the received ciphertext message $c$, Bob computes:
$$
m=c^d\mod n
$$
Why does RSA work? According to Euler Theorem, we have:
$$
m^{\phi(n)}=1\mod n
$$
Therefore:
$$
m^{ed}=m^{ed\bmod \phi(n)}=m^{ed\bmod z}=m\mod n
$$
So the number after decryption is exactly the plaintext. 

Even more wonderful is the fact that if we first exponentiate to the power of $d$ and then exponentiate to the power of $e$ — that is, we reverse the order of encryption and decryption — we also obtain the original value. 

The security of RSA relies on the fact that there are no known algorithm for quickly factoring a number, in this case the public value $n$, into the primes $p$ and $q$.

**Session Keys**

We note that the exponentiation required by RSA is a rather time-consuming process. As a result, RSA is often used in practice in combination with symmetric key cryptography.

First Alice chooses a key that will be used to encode the data itself. This key is referred to as a *session key* and is denoted by $K_S$. Alice must inform Bob of the session key, since this is the shared symmetric key they will use with a symmetric key cipher. 

Alice encrypts the session key using Bob's public key. When Bob receives the RSA-encrypted session key, he decrypts it to obtain the session key. 

## 8.3 Message Integrity and Digital Signatures 

**Message Authentication Code**

To perform message integrity, Alice and Bob will need a shared secret $s$, also known as the *authentication key*. Using the sharing secret, message integrity can be performed as follows:

1. Alice creates message $m$, concatenates $s$ with $m$ to create $m+s$, and calculates the hash $H(m+s)$, which is called the *message authentication code (MAC)*. 
2. Alice then appends the MAC to the message $m$, creating an extended message $(m,H(m+s))$, and sends the extended message to Bob.
3. Bob receives an extended message $(m,h)$ and knowing $s$, calculates the MAC $H(m+s)$. If $H(m+s)=h$, Bob concluded that the message is not altered.

**Digital Signatures**

In a digital world, one often wants to indicate the owner or creator of a document, or to signify one's agreement with a document's content. A *digital signature* is a cryptographic technique for achieving these goals in a digital world.

Imagining Bob is sending a message to Alice. To create a digital signature, Bob first take the hash of the message $H(m)$ and then encrypt the message with his private key. So the digital signature is $K_B^-(H(m))$. 

In the decryption stage, Alice finds that:
$$
K_B^+(K_B^-(H(m))) = H(m)
$$
Alice then argues that only Bob could have signed the document. Because the only one who could have known the private key $K_B^-$ is Bob.

But Alice should verify that the public key that is supposed to be Bob's is indeed Bob's. She can consult a *Certification Authority (CA)*, whose responsibility is binding a public key to a particular entity. 

## 8.6 Securing TCP connections: SSL

A enhanced version of TCP is commonly known as *Secure Sockets Layer (SSL)*. A sightly modified version of SSL version 3, called *Transport Layer Security (TLS)*. 

**The Big Picture**

Almost-SSL has three phases: *handshake*, *key derivation*, and *data transfer*. 

During the handshake phase, Bob needs to:

1. establish a TCP connection with Alice.
2. verify that Alice is really Alice.
3. send Alice a *master secret (MS)* key.

<img src = "\pictures\8-5.png" width = 600>

In key derivation phase, both Alice and Bob use the MS to generate four keys:

- $E_B$ — session encryption key for data sent from Bob to Alice.
- $M_B$ — session MAC key for data sent from Bob to Alice.
- $E_A$ — session encryption key for data sent from Alice to Bob.
- $M_A$ — session MAC key for data sent from Bob to Alice. 

Alice and Bob each generate the four keys from the MS. This could be done by simply slicing the MS into four keys.

As for data transfer, SSL uses sequence number to defend reordering or replaying attack. Bob maintains a sequence number counter, which begins at zero and is incremented for each SSL record he sends. 

Bob doesn't include a sequence number in the record itself, but he includes the sequence number in the MAC calculation. Thus, the MAC is $H(m+s+seqno)$. Alice tracks Bob's sequence numbers, allowing her to verify the data integrity of a record by including the appropriate sequence number in the MAC calculation. 

