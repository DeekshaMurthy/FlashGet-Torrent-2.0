# FlashGet-Torrent-2.0

 **Distributed Systems Project** : Designed a distributed system for fast, efficient, secure and fault-tolerant downloads of large files using socket programming from scratch.

## ABSTRACT

 File sharing is a common basic requirement when the users work on a particular domain or area of interest. We have proposed a basic design of an application for Linux systems that utilizes the concepts of distributed systems and provides the necessary functionality of remote file sharing and accessing where the files of interest that are distributed across the network, but the users have an illusion of a centralized file system and access them accordingly. The overall focus is on **fault tolerance mechanisms** and **enabling fast sharing**.


## Introduction
File sharing has become the practice of distributing or providing access to digitally stored information such as computer programs, multimedia (audio, images, and video), documents, or electronic books. Common methods of storage, transmission, and distribution used in file sharing include manual sharing using removable media, centralized server on computer networks, World Wide Web based hyperlinked documents and the use of distributed peer-to-peer networking. Users can use a system that connects into peer-to-peer networks to access shared files on the computers of other users (i.e. peers) connected to the networks. Files of interest can then be downloaded and accessed directly from other users on those networks. The most common and feasible approach is to use **`peer to peer`** file sharing for implementing a distributed files sharing system.
 
1. **Remote Information Sharing:** It will enable access to information that is being shared by a remote machine.

2. **User Mobility:** As the system will reflect all the files shared by the nodes present in the system, the user can access them from anywhere.

3. **Availability:** For better fault tolerance, the systems shared file entries are available to the users even in the temporary failure of the main directory controller.

## Related Work

 - **Centralised server- client approach:**
The central index server was meant to index all of the current users and to search their computers. When someone searches for a file, the server would find all of the available copies of that file and present them to the user. The files would be transferred between the two private computers.

 - **P2P network:**
Bit-Torrent is a well-known P2P distributed system which enables a user to share electronic data over the internet. 43% to 70% of all internet traffic is accounted for due to peer to peer network system (depending on the location). The disadvantages of a client-server file system which does not scale with respect to the number of users and exhibit a single point failure are compensated in this approach.

## Proposed Solution
We are designing a peer to peer distributed system for linux systems which resembles the **Bit - Torrent** functionality with additional features increasing the efficiency, security, scalability, robustness, better user experience without sacrificing the compulsion of contribution to the network.

1.  Encrypted data transfer.
2.  Efficient transfer by transferring compressed files.
3.  Leeching from different peers for fast transfer.
4.  Fault detection and correction.
5.  Dynamic request management.
6.  Synchronization and handshaking before process initiation.
7.  Parallel uploading and downloading for better performance.
8.  GUI and push notifications.


## General Basic Functionality

  

>**Step 1:** Node A requests the server for a list of active nodes. The server adds the Node A’s IP to the list when it pings for the first time. (Every active node pings the server periodically).

>**Step 2:** Request for the file is sent to all the nodes in the list given by the server. Autocomplete + Regex lookup in the directory of these nodes. The nodes send back the list of files’ info to node A to choose. A Display table is created merging all the received list (with the IP addresses of the nodes where the file is present hidden). Node A selects from the choices available to download.
	Eg: 	Requested file name:  ubuntu.iso
			Available similar files:
			UBUNTU1.iso : 2.4 GB
			UnixUbuntu.iso: 1.9 GB
			Node A selects from these for transfer.

  >**Step 3:**  After selecting a file, node A proceeds to request for different sections of the file from different nodes, with sections fixed to a particular node.
  
  >**Step 4:** After receiving all the packets from different nodes, node A sorts them in order and merges them and saves this in an encrypted secure folder , followed by decryption if the user asks for it. The following figure 1 describes the flow of mechanism followed, and figure 2 specifies the basic example of the system layout.


## Special cases

**Case 1:**
To increase the efficiency, when a node has finished transferring its section to node A, node A starts requesting packets of the unfinished section to that node. This is helpful for the nodes whose transfer rate is less or when a node has stopped responding or in case of node failure( the systems ping to server has stopped ).
![](https://lh5.googleusercontent.com/XPGvibaOiql44r-ItgJqiEuAJb7PyXBAtaA6ddgY862sfqwy_4X7KUoVGNRfl34OQYySXX7JxLNwYOJ7irzelt96UhNd27S_QbFik-qOB3JDKIBCIHV1vRNOu43LT8deKTYtaHWd)

Here is a visual representation of how a file is divided into n sections based on the number of nodes available initially. The dark black lines denote a section which is comprised of many packets of data. Node A requests for packets from different nodes in this manner. Clearly from the figure node ‘n’ has transferred faster than node 1 and node 2 hence after it is done sending its section, it starts sending the packets from the biggest leftover section.

  

![](https://lh4.googleusercontent.com/wjC_ZljqdpqK1dhQ4YBiC0YfVKQHCTlmjsKvGLxoyFT7LeIbu1DFNYUGCG2DRmQ207IYYLzCn476WZhNexeDytkjC4vOE_gOfIdBtZKNfjaEgHkNRmKfSAjJwsyV9zCV3-efe_pm)

Here node n starts sending from node 1’s section.

**Case 2:**
If during the process of transfer, if new nodes become active, who have the file(s) requested by node A, then node A requests for packets from those nodes too.

![](https://lh3.googleusercontent.com/iOKNud30ITr4jum-SMJOjloS_RtWlMp673YWWOEFT6CCe3gDRRLIelSSndDjrH5HkS1tJ8p4KgFd4V4atIex-PtZLbeP2RRJq-mJ_OUlgBATDc9-Qv53B9vxh-LX2HHDTHaQ4uBu)

Consider this figure. There are n nodes initially. After sometime when new nodes become active, node A creates more sections within a section and requests packets from the new nodes (node ‘n+1’ and ‘n+2’ are the new nodes that have arrived).

**Case 3:**
If a node has portions of the file requested and node A requests for a packet which it doesn’t have, then it sends a NACK message to node A along with the details of the portions of file it has access to.
Node A then analyses whether there are packets that the node can provide it with because we don’t want to turn that node away without utilizing it.

![](https://lh5.googleusercontent.com/wH3QjHi39EyJ14W9RgFfq1If3a0wNrXW7I3kSxvNxq-cU8KIksfcAduu7MCu0gqex0LkHvRiaVXGr40yliE0R68RgtLYs2Z1LkerAkhjgIApJao2QjYsCtzGQo65AOg8OHqsD0We)

Due to the unavailability of complete data from its section node 2 has resumed sending packets from node n’s section which it has access to.

## Structure
**![](https://lh3.googleusercontent.com/NSF16rOp0tw2FLG6ytBaWwx7nOTqaI_3sA_AS5XBYmGFPGPVTysehcts66SK00PTgYHJLqgzgHku9rnHJHB84eF99Ss8NJrHnzaUy9hQFSVcE-VF0o5aTau0365XfM9Vbln3V6Nx)**

## Diagrams

**![](https://lh4.googleusercontent.com/wvt9LOb1myKssgreb519lOVrwZnPgEH_yDwfYRoImgpm-GnrcclrXSbJCFzHsT2-Iq8LlBEqxTN6dd7sPgJ7uIU6-YFwN0QnX2rrZ5fHzsdEHTqDlFhtZP_xS2WGR46Ny8WEwpF5)**
