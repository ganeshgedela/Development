**VoLTE: End to end QoS control**

The end to end QoS control is an important factor to be considered to
provide a qualified service to users. It would become more so when the
service is required to be provided in real time such as voice call or
multimedia streaming.  If the voice call service is provided through the
best-effort network where the QoS is not guaranteed, the users will
experience frequent call attempt failure, call setup delay, call drop,
voice cracking, etc. 

In the following are introduced several different level of QoS control
methodologies for VoLTE service.

**I. Separated APN for VoLTE**

The UE can attach multiple PDNs at the same time and each PDN connection
can have multiple EPS bearers. Each PDN connectivity has one default EPS
bearer and can have multiple dedicated EPS bearers up to 11 in total.
The UE is assigned with a different IP address for each APN by the P-GW
during PDN connectivity procedure for each APN.

![](media/image1.png){width="5.208333333333333in"
height="1.3958333333333333in"}

In general, the operator uses an IMS APN separately from the Internet
APN. This dedicated APN for VoLTE service may have the intention to
provide the quality of VoLTE service not to be affected by other
non-real time service such as the internet service. The default APN is
provided by the network based on subscriber profile fetched from the HSS
during the initial attach procedure. 

The following diagram shows a call flow of initial attach procedure.
During the initial attach procedure, the MME obtains the APN list from
the HSS in the Location Update Answer message as a part of subscriber\'s
profile. The MME determines the default APN based on the received APN
list and parameters, creates the GTP-C session with the corresponding
S-GW/P-GW. Once the GTP-C session is created successfully, the default
APN information is delivered to the UE in the Attach Accept message. If
the default APN is pre-configured in the UE, the same should also be the
part of the subscriber profile stored in HSS in order to avoid the
conflict which leads to the attach failure. If the default APN is not an
IMS APN, the UE has to trigger additional PDN Connectivity with its APN
parameter set to \"IMS\".

NOTE the EPS bearer creation procedure is not shown in this diagram. 

![](media/image2.png){width="6.268055555555556in"
height="3.388888888888889in"}

The following shows an example of the Location Update Answer message
from the HSS which contains the APN list for the subscriber. Each
APN-Configuration AVP under the APN-Configuration-Profile AVP contains
the APN information. The Context-Identifier AVP which is one of sub AVPs
of the APN-Configuration-Profile AVP is used to determine the defalut
APN. Whereas, the same AVP under the Configuration-Profile AVP indicates
the context identifier for respective APNs. Given this, the APN whose
own Context-Identifier is matched with the upper level
Context-Identifier will become the defualt APN. 

In this example, there are three APNs in total and the \"IMS\" APN will
be selected as a default APN of which Context-Identifier(=10) has the
same value as upper level Context-Identifier.

![](media/image3.png){width="6.268055555555556in" height="4.68125in"}

**II. PCC(Policy and Charging Control) rules**

When the PDN connection is established with the IMS APN, the EPC and the
PCRF creates the EPS bearer of QCI=5 for IMS signaling. Since then, all
the SIP signaling in VoLTE goes through this EPS bearer of QCI=5.
Subsequently, when the user requests a VoLTE call setup and the media
information is exchanged end to end, the EPC and the UE creates
dedicated EPS bearer(e.g., QCI=1 for Voice, QCI=2 for Video, etc) to
transfer media traffic. 

The PCC architecture consists of P-CSCF(i.e., AF), PCRF, P-GW(i.e.,
PCEF) and S-GW(i.e., BBERRF). All of these components are involved in
delivering the service data flow to the right EPS bearer with the right
QoS conditions. The PCC rules generated or assigned by the PCRF define
the mapping relations between the QoS paramemters and the service data
flows. Upon receiving a VoLTE request(i.e., SIP INVITE with SDP offer),
the P-CSCF extracts the 5-tuples of media information(i.e., source ip
address, destination ip address, source port, destination port,
protocol), codec profile, etc. The P-CSCF interworks these service data
flow information to the PCRF and the PCRF either dynamically generates
the corresponding PCC rules or assigns the predefined PCC rule. The PCC
rules are provisioned to the P-GW. As its logical name suggests(i.e.,
PCEF), the P-GW performs gating control for the uplink/downlink traffic
based on the given PCC rules. After successful PCC provisioning, the
P-GW initiates the dedicated EPS bearer creation via the S-GW towards
the eNB. \
\
![](media/image4.png){width="6.268055555555556in"
height="2.5069444444444446in"}\
\
The following example shows the PCC rule information in the
RAR(Re-Authenticate Request) over Gx. In this case, there are two
Charging-Rule-Definition AVPs defined each for RTP and RTCP
respectively. The Charging-Rule-Definition AVP contains various
information that is required for service data control such as PCC rule
name(i.e., Charging-Rule-Name AVP), 5-tuple for each direction(i.e.,
Flow-Information AVP), QoS parameters(i.e., QoS-Information AVP), etc.
The QOS parameters includes the QCI, GBR(UL/DL), AMBR(UL/DL), ARP, etc.

![](media/image5.png){width="5.208333333333333in" height="3.75in"}

-   QCI(CoS Class Index): A level of QoS classified based on the
    required quality per service usages.

-   GBR(Guaranteed Bit Rate) : The minimum bit rate to be guaranteed for
    the given bearer. A certain amount of bandwidth will be reserved for
    this bearer. The GBR bearer always takes up resources over the radio
    link, even if no traffic is sent.

-   AMBR(Aggregated Maximum Bit Rate) : The total bit rate that is
    allowed to be used for all non-GBR bearers associated with a
    specific APN/UE.

-   ARP(Allocation and Retention Priority) : Being used to indicate a
    priority for the allocation and retention of bearers. It's typically
    used to decide whether a bearer establishment or modification can be
    accepted or needs to be rejected due to resource limitations..

**III. DSCP(Differentiated Services Code Point) marking**

The DSCP marking is an IP level QoS control for each IP packet to flow
through the backhaul with a certain priority and the appropriate
latency. As the IP packets from different PDN with different QCI values
will be mixed inside the backhaul(e.g., VoLTE, internet), the DSCP
marking at IP layer would be an important factor to be considered by
switches and routers to guarantee the quality service for VoLTE. Without
DSCP marking, IP packets can be delayed or dropped significantly when
there is a burst of IP traffic at the same time within the IP network.

The DSCP marking shall be done by both end points of the backhaul for
both uplink and downlink IP packets based on the QCI of the service
traffic. The following shows a recommended DSCP mapping relations
between the QCI and the DSCP values as specified in GSMA IR.34
\"Inter-Service Provider IP backbone guidelines\". For instance, the IP
packets with QCI=1 and 2 for voice and video respectively is marked with
the 2E, whereas the IP packets with QCI=5 for IMS signaling will be
marked as 1A.

NOTE the DSCP-QCI mapping relation is a part of operator\'s policy. All
the switches and routers aware of DSCP values needs to adjust itself to
the correct behavior according to the agreed DSCP values as to handling
the IP packets.

![](media/image6.png){width="4.166666666666667in" height="3.75in"}

![](media/image7.png){width="4.166666666666667in"
height="2.5520833333333335in"}

The following shows an example of DSCP marking in the IP packet. In this
example, the IP packet has been used to deliver the SIP INVITE and the
IPv4 packet is wrapped by the IPv6 header at P-GW/S-GW. The 6-bit DS
field in this IPv6 header is set to \"2e\"(i.e.,the Expedited
Forwarding). This is a different value from the one specified in the
above case 

![](media/image8.png){width="6.268055555555556in"
height="3.329861111111111in"}

**VoLTE: QCI=1 setup failure when S1 handover is in progress**

In a mobile environment, by its nature, the handover may occur while the
user is engaged in a VoLTE call session. The UE periodically reports
measurements of various parameters to the eNB and the eNB determines
whether the handover is required. Once it is determined by the eNB to
trigger the handover, the eNB will decide whether to perform X2 handover
or the S1 handover. When there is an existing X2AP connection towards
the target eNB, the source eNB performs X2 handover. If there is no X2AP
connection or the X2 handover attempt has failed for some reasons, the
source eNB may trigger the S1 handover.

As to the PGW initiated bearer related requests(e.g.,
Create/Update/Delete Bearer request) there is no cause-id defined in the
3GPP TS29.274(r8),  Therefore, in this case, the MME may reject the
request with the cause-id of reason unspecified. This cause-id will lead
to the ripple effect towards the upstream forcing each node on the path
to release the corresponding resources. This is shown in the following
flow diagram.

![](media/image9.png){width="6.268055555555556in"
height="4.250694444444444in"}

Even though the handover is successful in this flow, the error cause of
RESOURCE ALLOCATION FAILURE in the CCR over Gx will lead to the PCRF to
send RAR(Re-Authentication Request) or ASR(Abort-Session-Request) over
Rx with a cause-id of RESOURCE NOT AVAILABLE, and the process will end
up with sending the 503 Service Unavailable by the P-CSCF. Upon
receiving the 503 Service Unavailable, the UE releases all the resources
for the call.\
\
In a circumstance where the eNB is not optimized, the handover might
occur relatively often. If this racing condition is not handled
properly, the result will lead to bad user experiences for VoLTE as the
rejection of the bearer related request may often lead to the VoLTE
setup failure for QCI=1 bearer for voice.

In the 3GPP TS29.274(r9), the 3GPP has specified the proper cause value
of \"Temporarily rejected due to handover in progress\" and in the 3GPP
TS29.274(r11), \"Temporarily rejected due to handover/TAU/RAU procedure
in progress\". This cause-id value is used by the MME rejecting the
bearer related request when the handover results in the relocation of
the Serving GW and/or MME. The PDN GW which initiated the bearer related
request will be able to consider this error cause value to handle the
rejection. 

The following flow shows one example of how to handle the rejected
bearer related request. In this flow, the Create Bearer Request is
rejected by the MME. The PDN GW may retry the Create Bearer Request
based on the operator\'s policy. 

![](media/image10.png){width="6.268055555555556in"
height="4.642361111111111in"}

If there is no need of relocation of MME and/or Serving GW, the MME does
not need to respond with the cause-id, rather it can perform
store-and-forward way of message handling. In this case, the MME will
temporarily store the message and wait for the handover to be completed
and if it\'s done soon enough, the Create Bearer Request can be sent to
the UE via the target eNB. How \'soon\' is the \'soon enough\' time is
usually up to the operator\'s policy.

**VoLTE: Understanding of GTP TEID to use in LTE trouble shooting**

The GTP(GPRS Tunneling Protocol) is a communication protocol used by the
LTE to deliver IP packets within the EPC. The GTP-C is used to deliver
the controlling signals over S11 and S5, whereas the GTP-U is used to
deliver application payload over S1 and S5. 

![](media/image11.png){width="5.208333333333333in"
height="1.8541666666666667in"}

**I. TEID exchanges**

The TEID(Tunnel Endpoint IDentifier) is generated by each node during
the initial attach procedure. The Create Session Request includes the
S11 MME DL TEID and the S5 SGW DL TEID, which are generated and included
by MME and Serving GW respectively. The Create Session Response includes
the S5 PGW UL TEID and the S11 SGW UL TEID, which are generated and
included by PGW and Serving GW respectively.\
\
The following diagram shows the actual call flow and depicts how the
TEID is exchanged between NEs. Upon receiving the Create Session
Request, the Serving GW establishes the downlink GTP-C tunnel towards
the MME using the received S11 MME DL TEID. In the same way the MME
establishes the uplink GTP-C tunnel towards the Serving GW using the
received S11 SGW UL TEID. The TEID for GTP-U is included in the body of
bearer related messages (e.g., Create Bearer Request/Response, Modify
Bearer Request/Response). 

![](media/image12.png){width="6.268055555555556in"
height="6.268055555555556in"}

The newly generated TEID is included in the body of each sending message
and delivered to the peer node. The peer node perceives the end point of
the GTP based on the received TEID. When the message goes through the
existing GTP tunnel, the TEID of the peer node will be included in the
GTP header of the sending message. The following example shows the TEID
included in the Create Session Request being sent from the MME towards
the Serving GW. 

![](media/image13.png){width="6.268055555555556in"
height="2.370138888888889in"}

In the mean time, the following example shows the TEID included in
Create Session Response, where the TEID received from the MME is used in
the header and the newly generated TEID of Serving GW is included in the
body.

![](media/image14.png){width="6.268055555555556in"
height="1.9784722222222222in"}

**II. TEID lifetime**\
\
The life time of the GTP-C session lasts along with the life time of the
UE\'s IP-CAN connection. It starts when the UE attaches to network and
ends when the UE detaches from the network. In case there are multiple
PDNs , there is only one GTP-C session per UE. The following example
shows the lifetime of the same GTP-C session, which is defined by same
TEIDs. In this example, there are two Create Session Requests, each for
different PDNs. Each Create Session Response is followed by the Modify
Bearer Request for establishing default EPS bearers. Lastly, the Create
Bearer Request is to establish dedicated EPS bearers.

![](media/image15.png){width="2.53125in" height="4.166666666666667in"}

The lifetime of the GTP-U depends on the attributes of the EPS bearer.
The GTP-U connection associated with the default EPS bearer has the same
lifetime of that of GTP-C connection, whereas the GTP-U connection
associated with the dedicated EPS bearer will be dynamically created and
deleted within the lifetime of IP-CAN connection.

**III. TEID usage**\
\
When there are multiple EPS bearers established for the same APN and
there needs to verify if  specific service data flow goes through the
right EPS bearer, the TEID can be a useful tool to figure it out. The
following example shows the GTP-U packet of the SIP REGISTER being sent
from the UE towards the IMS Core. The TEID in the GTP header indicates
\"0x005b8422\".

![](media/image16.png){width="6.268055555555556in"
height="1.9979166666666666in"}

The following shows the same TEID appears in the body of a Modify Bearer
Request. This Modify Bearer Request is for the EPS bearer of QCI=5.

![](media/image17.png){width="6.268055555555556in"
height="2.527083333333333in"}

**VoLTE: E-RAB management vs Handover**

The 3GPP TS36.413 addresses the racing condition between UE handover and
the E-RAB management procedures. The UE handover occurs based on the
measurement parameters sent by the UE whereas the EPS bearer creation as
a part of VoLTE call setup procedure in general. When these two
independent events occur at the same time, there can be a collision at
eNB, as the eNB is involved in both procedures. In this collision state,
the eNB has two options to take as follows:\
\
\
**I. Terminating the E-RAB Setup and continues the UE S1 handover**

The following flow shows the eNB rejecting the E-RAB setup request and
continues the handover procedure. Upon receiving the rejection to the
E-RAB setup request with its cause id, e.g., \"S1 intra system Handover
Triggered\", the MME continues the S1 handover procedure. In the
meantime, the Create Bearer Request can be postponed temporarily until
the handover is completed. If the Serving GW or MME is to be changed,
the Create Bearer Request will be rejected with its cause id set to
\"Temporarily rejected due to handover\" and the P-GW may retry the EPS
bearer creation procedure after the S1 handover is completed(refer
to [[http://bit.ly/1H4Z7yr]{.underline}](http://bit.ly/1H4Z7yr) for the
detail).

![](media/image18.png){width="6.268055555555556in"
height="3.1930555555555555in"}

**II. Cancelling the UE handover and continues E-RAB Setup**

The following shows the eNB cancels the S1 handover towards the MME and
continues the EPS bearer creation procedure. Upon receiving the Handover
Cancel, the MME terminates ongoing Handover Preparation procedure and
release any resources associated with the handover preparation. If the
eNB does not receive the Handover Cancel Ack, it is assumed that the
handover is terminated successfully.

![](media/image19.png){width="6.268055555555556in"
height="2.957638888888889in"}

The following shows the eNB cancels the X2 handover to continue the EPS
bearer creation procedure according to 3GPP TS36.423. Upon receiving the
Handover Cancel, the target eNB releases any resources reserved for the
concerned UE context.

![](media/image20.png){width="6.268055555555556in"
height="2.957638888888889in"}

**III. Service impact**\
The eNB shall be able to handle the racing condition between two
independent events(i.e., E-RAB setup request and handover) either by
cancelling the handover or by rejecting the E-RAB setup request. The MME
also needs to be able to handle the racing condition either by rejecting
the bearer related requests with a corresponding reason (e.g.,
Temporarily rejected due to handover) or by possibly providing
pause-and-resume mechanism itself for bearer related requests in case
the handover is in progress. If the bearer related request is rejected,
the PGW may realize the retry mechanism(refer
to [[http://bit.ly/1H4Z7yr]{.underline}](http://bit.ly/1H4Z7yr) for the
detail). If this type of racing condition is not handled appropriately,
there could be frequent call drops or call setup failures based on eNB
optimization status resulting in bad user experiences of VoLTE user.

**VoLTE: Using TCP parameters in packet analysis**

The TCP is used to transfer a continuous stream of octets in each
direction between users by packaging some number of octets into segments
for transmission through the internet system\[RFC793\]. In SIP realm,
the TCP is one of the most commonly used protocol along with UDP to
transfer user data.

![](media/image21.png){width="5.208333333333333in"
height="2.1458333333333335in"}

The above diagram shows an example of the protocol map for LTE user
plane. The backhaul is placed between eNB and the EPC in the operator\'s
network in general. The IPv4 packet sent by the UE over the air is
wrapped by the eNB using GTP and IPv6 headers. The eNB sends the IPv6
packet through the GTP tunnel and the PGW at the end of GTP tunnel
unwraps the IPv6 and GTP headers. The retrieved IPv4 packet at PGW is
forwarded to the P-CSCF over SGi interface.\
\
**I. TCP header**\
\
The following shows the TCP headers and parameter descriptions as
specified in RFC793

![](media/image22.png){width="5.208333333333333in"
height="3.1354166666666665in"}

-   Sequence Number(32bits): The sequence number of the first data octet
    in this segment(except when SYN is present). If SYN is present, the
    sequence number is the initial sequence number(ISN) and the first
    data octet is ISN+1.

-   Acknowledgment Number(32bits): If the ACK controls bit is set this
    field contains the value of the next sequence number the sender of
    the segment is expecting to receive. Once a connection is
    established this is always sent.

-   Control bits(6bits)

    -   URG: Urgent Pointer field significant

    -   ACK: Acknowledgement field significant

    -   PSH: Push Function

    -   RST: Reset the connection

    -   SYN: Synchronize sequence number

    -   FIN: No more data from sender

-   Checksum(16bits): The 16bit one\'s complement of the one\'s
    complement sum of all 16 bit words in the header and text. This is
    used to detect the corruption of data over TCP

**II. Usage of TCP headers in packet analysis**\
\
After successful initial attachment to the LTE network, the VoLTE
UE(i.e., IMS UE) establishes a TCP connection with the P-CSCF in order
to process the IMS registration. Once the TCP connection is established,
the UE starts sending SIP messages(i.e., SIP REGISTER).\
\
TCP parameters can be useful when they are used to identify the
identical packets between sending and the receiving node respectively.
It is true in particular when the network(e.g., backhaul) is unstable
where there can be a lot of packet delay, packet loss and packet
re-transmissions, as it becomes far more difficult to analyze the packet
flows.\
\
NOTE In the following snapshot, the yellow box depicts a UE side ip
address and the green box a Core side ip address. All the detailed ip
address is hidden for security purpose.\
\
The following snapshot shows the UE side trace log that was captured at
UE. This example shows the normal SIP procedure that can occur when the
call is requested by the user.

![](media/image23.png){width="6.268055555555556in"
height="3.4277777777777776in"}

The following snapshot shows the Core side trace log that was captured
between backhaul and the  Serving GW. The procedure in this example is
correlated with the above figure.

![](media/image24.png){width="6.268055555555556in"
height="3.3493055555555555in"}

In order to find the matched transaction between the two nodes, the TCP
checksum data can be used to identify the same packet. In this example,
the same TCP packet for SIP INVITE can be found with its checksum value
= 0x8bef. Note that it would be more usual to find the matched SIP
transaction based on Call-Id in normal situation. However, when there
are many packet re-transmissions and delays, the Call-Id wouldn\'t be
enough to pinpoint the matched ones.\
\
On the other hand, taking a look at the SIP PRACK, the UE has sent two
packets. As they are re-transmitted by the SIP layer, they will have
different checksum value. (i.e., ox28e2, 0x2781)

![](media/image25.png){width="6.268055555555556in"
height="2.7618055555555556in"}

In the meantime, there are three SIP PRACKs appears in the core side and
all of them has the same checksum value(0x2781). This checksum value
indicates that they are matched only with second SIP PRACK sent by the
UE. Therefore it can be reasoned that the first SIP PRACK sent by the UE
has been lost somewhere between UE and the Serving GW.

![](media/image26.png){width="6.268055555555556in"
height="2.3895833333333334in"}

In the following core trace, it is observed that the TCP Ack for the SIP
PRACK(TCP Syn) is sent only after 40 ms from the received SIP PRACK. The
corresponding TCP Ack can be identified by mapping the TCP Acknowledge
Seqnum of the TCP Syn with the Seqnum of the TCP Ack.

![](media/image27.png){width="6.268055555555556in" height="2.78125in"}

The same TCP Ack can also be found based on the checksum value. In this
example, the UE received the TCP Ack for the SIP PRACK after 700 ms.

![](media/image28.png){width="6.268055555555556in"
height="0.4701388888888889in"}

Given the relative time gap between the SIP PRACK(TCP Syn) and the
corresponding TCP Ack at both ends, it can be reasoned that there has
been a packet delay somewhere in a downlink between  Serving GW and the
UE.

\*\*\*

The TCP packet analysis can be used to correlate the packets between
sending node and the receiving node. Measuring the relative time gap of
sending and receiving packets also makes it easier to identify the
problematic NEs or interfaces. As such, the TCP headers give useful
information to engineers in analyzing the technical problems in VoLTE
service. As the TCP packet delays and losses can more often than not
lead to the IMS registration delay, IMS registration failure, call setup
delay and call setup failure, it is directly related to the quality of
user experiences. The TCP packet analysis becomes very useful way to
realize the quality of VoLTE Service as it might also be in other
services.

**VoLTE: Bearer binding and Session binding**

The LTE supports the PCC(Policy and Charging Control) architecture for
QoS control applied to service data flow. In the PCC architecture, the
PCRF(Policy and Charging Rules Function) takes the role of a central
network component interacting with P-CSCF, SPR(Subscription Profile
Repository) and the EPC. The PCRF is always involved in the activities
of EPS bearer creation by generating the PCC(Policy and Charging
Control) rules and provisioning them to PDN GW(i.e., PCEF). In order to
generate PCC rules, the PCRF needs to gather service data flow
information from the P-CSCF and possibly the subscription information
from the SPR. As the PCC rule shall be applied from the access network
to the EPC core with consistency, the PCRF needs to be able to maintain
the relations of different sessions over different interfaces across the
IP-CAN, EPS bearer and applications, in which the binding mechanism
becomes a basic concept.\
\
NOTE In this article, it is assumed that the S5 between the SGW(Serving
GW) and PGW(PDN GW) is using GTP, where the PGW becomes the end point of
the GTP tunnel.\
\
\
**I. Session binding**\
\
The session binding is an association of the AF session information to
one and only one IP-CAN session \[TS23.203\]. Th AF(Application Focus)
session is defined as a service level session such as IMS service
session that is established by the application level signaling protocol
offered by the AF that requires a session-setup with explicit session
description before the use of the service\[TS29.214\].

![](media/image29.png){width="5.208333333333333in" height="1.65625in"}

The IP-CAN session information is obtained by the PCRF during the UE
initial attach procedure.\
When the UE performs the initial attach to the LTE network, the PGW
triggers the *CCR-I* towards the PCRF. The *CCR-I* contains the IP-CAN
related AVPs such as Framed-IP-Address, IP-CAN-Type, RAT-Type,
Called-Station-Id, AN-GW-Address. The following is an example
of *CCR-I* captured over Gx.

![](media/image30.png){width="6.268055555555556in"
height="3.6631944444444446in"}

-   Framed-IP-Address: The valid routable IPv4 address that is
    applicable for the IP Flows towards the UE at the PCEF. The PCRF
    shall use this address to identify the correct IP-CAN session
    binding\[TS29.214\].

-   Freamed-IPv6-Prefix: A valid full IPv6 address that is applicable to
    an IP flow or IP flows towards the UE at the PCEF. The PCRF shall
    use this address to identify the correct IP-CAN session
    binding\[RFC4005,RFC3162\].

-   IP-CAN-Type: Type of Connectivity Access Network in which the user
    is connected\[TS29.212\]. 

-   RAT-Type: The Radio Access Technology that is currently serving the
    UE\[TS29.212\].

-   Called-Station-Id: APN \[TS29.212\].

The service data flow information is obtained while the service session
is set up. Upon UE request for VoLTE call setup, the *SIP INVITE* is
delivered to the P-CSCF(i.e., AF) with an SDP offer. The SDP offer
includes media session information such as 5-tuples(source ip address,
destination ip address, source port, destination port and protocol),
codec information, etc. Upon receiving the *SIP INVITE*, the P-CSCF
interprets the received SDP contents into diameter AVPs and triggers the
AAR towards the PCRF. The following shows an example of SDP contents
included in the *SIP INVITE*.\
\
NOTE It would be possible for the P-CSCF to trigger *AAR *once when
the *183 Session In Progress* is received(SDP answer) in order to reduce
diameter traffic.

![](media/image31.png){width="6.268055555555556in"
height="3.1729166666666666in"}

The following is an example of diameter *AAR *over Rx which includes the
service data flow information.

![](media/image32.png){width="6.268055555555556in"
height="5.014583333333333in"}

-   Media-Sub-Component: contains the requested bitrate and filters for
    the set of IP flows identified by their common
    Flow-Identifier\[TS29.212\].

-   Flow-Description: defines a packet filter for an IP flow with the
    following information\[TS29.212\].

-   Flow-Status: describes whether the IP flow(s) are enabled or
    disabled\[TS29.214\].

-   Max-Requested-Bandwidth-UL/DL: Indicates the maximum requested
    bandwidth in bits per second for an uplink/downlink IP
    flow\[TS29.214\].

-   RS-Bandwidth: indicates the maximum required bandwidth in bits per
    second for RTCP sender reports within the session
    component\[TS29.214\].

-   Codec-Data: contain codec related information known at the
    AF\[TS29.214\].

Upon receiving the *AAR*, the PCRF binds the service data flow
information received from the P-CSCF to a specific IP-CAN session
received from the PGW.\
\
\
**II. Bearer Binding**\
\
The bearer binding is the association of the PCC rule and the QoS rule
(if applicable) to an IP-CAN bearer within that IP-CAN\[TS23.203\]. Upon
user\'s request for voice call, the SIP signals will flow through the
EPS bearer of QCI=5 and there will be additional EPS bearer newly
established to transfer voice traffic. In the same way as described in
the previous section, the PCC rules are generated and provisioned to the
PGW by the PCRF. The PGW enforces PCC rules accordingly by performing
gating control over service data flow.

![](media/image33.png){width="5.208333333333333in"
height="2.2708333333333335in"}

The PCC rule contains various parameters that can be used to control
service data flow such as Flow-Information, Flow-Status, QoS, etc. The
following snapshot shows an example of PCC rule contained in the
diameter RAR over Gx for voice traffic.

![](media/image34.png){width="6.268055555555556in"
height="4.309027777777778in"}

Upon receiving the *RAR*, the PGW triggers the EPS bearer creation
procedure by sending the *Create Bearer Request* to the MME. The *Create
Bearer Request* contains the TEID for GTP-U created by the PGW and QoS
parameters(QCI, MBR, GMBR) as well. In return, the corresponding
response from the MME, *Create Bearer Response*, contains the allocated
EBI(EPS Bearer ID) and the TEID for GTP-U created by the eNB. As an end
point of the GTP Tunnel, the PGW shall maintain the relations between
EPS bearers and PCC rules. The following is an example of *Create Bearer
Response* captured over GTPv2.

![](media/image35.png){width="6.268055555555556in"
height="2.2333333333333334in"}

\*\*\*

The session binding and the bearer binding are basic concepts to
understand how different type of sessions are related with each other
over different interfaces within the PCC architecture. The IP-CAN
session to which the UE is attached is bound with the AF session by the
PCRF and the service data flow for that AF session is used to generate
the PCC rules. These PCC rules are used to map the specific service data
flow to a certain EPS bearer which belongs to that IP-CAN session.\
\
Thanks to this binding relations, one event at one place makes a ripple
effect to the other, thereby the LTE core can maintain the consistent
status for the same UE. If the UE releases an AF session, the
corresponding PCC rules for the service data flow belonging to that AF
session are removed and in turn, the EPS bearer for that PCC rules will
also be released. If the UE detaches from the network, the IP-CAN
session will be released and in turn, all the AF session and EPS bearers
belonging to the same IP-CAN will also be released.

**VoLTE: PDN connectivity request vs handover**

The PDN connectivity procedure is to request the setup of a default EPS
bearer  to a PDN\[TS24.301\]. The PDN can either be the default PDN or
an additional PDN. When it is the default PDN, the UE establishes the
default EPS bearer as a part of the process of initial attach. If it is
a subsequent PDN, this procedure will establish additional default EPS
bearer with that PDN. As such the UE supports multiple default EPS
bearers in multiple PDNs.\
\
When the PDN connectivity procedure does collide with the handover
procedure, the EPS shall be able to handle the situation based on the
principle of best effort. The MME may pause the bearer creation
procedure and resume when the handover is completed or the MME shall
reattempt the *E-RAB setup request* after the handover is
completed\[TS23.401\].\
\
The following is the case where the PDN connectivity procedure collides
with the X2 handover.

![](media/image36.png){width="6.25in" height="5.875in"}

The above is the case the *PDN connectivity request* is sent for the
second PDN. In this example, the MME proceeds the activation of the
default EPS bearer by sending the *Activate default EPS bearer Context
request* over S1AP while the X2 handover is in progress at the eNB. The
eNB rejects the *E-RAB Setup request* with its cause value set to
\"X2-handover-triggered\". Upon receiving the rejection to the *E-RAB
Setup request*, the MME shall wait until the X2 handover is completed.
Once it is completed, the MME re-attempts the activation of the default
EPS bearer request. The following shows the S1AP procedure where
the *E-RAB setup request* is rejected while subsequent PDN connectivity
procedure.

![](media/image37.png){width="6.268055555555556in"
height="2.1347222222222224in"}

The same mechanism is also applied to the S1 handover case as shown
below.

![](media/image38.png){width="6.25in" height="5.6875in"}

In this case, the MME requests activation of the default EPS bearer as a
normal procedure before receiving the *Handover Required* while the eNB
already sent the *Handover Required* and subsequently receives
the *Activate default EPS bearer Context request*. If the handover is
only in preparation stage, the eNB may be able to cancel the handover
and continues the E-RAB setup procedure. Instead, in this example, the
eNB rejects the *E-RAB setup request* with its cause value set to \"S1
intra system handover triggered\". Upon rejection, the MME hold the
state until the S1 handover is completed and resumes by reattempting the
activation of the default EPS bearer.\
\
NOTE the MME may pause between the step #b and the setp #6  as it is
already aware of the S1 handover in progress. However, from
implementation point of view, it looks better to pause after the setp #6
as it is a common place both for S1 and X2 handover.\
\
If the timer at MME expires and the PDN connectivity couldn\'t be
completed, it is expected that the UE reattempts the PDN connectivity
procedure. In order to request connectivity to an additional PDN, the UE
shall start timer T3482 after sending *PDN connectivity request* and
enter the state of PROCEDURE TRANSACTION PENDING\[TS24.301\]. The T3482
stops when the UE receives the *Activate default EPS bearer Context
request* or if expires, the UE reattempts the PDN connectivity
procedure.

**VoLTE: Traffic Flow Templates**

The service data flow template is a set of packet filters applied to IP
packets to identify the service data flow belonging to a specific
application. The packet filters typically consist of IP 5-tuples, i.e.,
source IP address, destination IP address, source port, destination
port, protocol type. The service data flow template is delivered to the
PGW contained in the PCC rules. The PGW identifies the service data flow
based on the service data flow template applied in the order of
filtering priorities. Once the service data flow is identified, the
corresponding QoS parameters are applied to relate the service data flow
to a certain EPS bearer.\
\
**I. TFT filter**\
Once the bearer binding is completed, that is, the PGW builds mapping
relations between EPS bearers and the corresponding PCC rules, the PGW
requests the creation of the EPS bearer (i.e., *Create Bearer Request*)
towards the MME in which the set of IP 5-tuples are interpreted as a
bearer level Traffic Flow Template (TFT). The TFT can be defined either
separately for uplink and downlink or for both uplink and downlink. The
TFT for the downlink is used by the network element whereas the TFT for
the uplink is used by the UE. The following diagram shows the TFT
structure when the TFT operation is add, create or replace \[TS24.008\].

![](media/image39.png){width="4.010416666666667in"
height="4.166666666666667in"}

-   TFT operation code : the action to be taken to the TFT and/or packet
    filter list e.g., create, delete, add, replace, etc. 

-   Number of packet filters : the number of packet filters. In case the
    operation code is \"Delete existing TFT\" or \"no operation code\",
    the number of filters will be 0. Otherwise, the maximum number of
    packet filters is 15.

-   Packet filter direction: the direction of the traffic, i.e., uplink
    only, downlink only, bidirectional

-   Packet filter identifier: the unique number to identify the packet
    filter

-   Packet filter evaluation precedence: the precedence for the packet
    filter among all the packet filters in all TFTs associated with the
    PDP address.

-   Packet filter contents: variable components with variable size such
    as remote/local IPv4/IPv6 address, protocol identifier, remote/local
    port, etc.

The following snapshot shows the TFT included in the *Create Bearer
Request *(PGW/SGW-\>MME) captured over S11. The TFT operation code is to
\"Create a new TFT\" and the direction of the IP flow to which this TFT
is applied is an \"uplink only\" as this TFT is supposed to be used by
the UE. The precedence value indicates the priority for this filter
among other filters to be applied to the IP flow. Therefore this
priority value must be locally unique in the UE. In this example, the
IPv4 remote address indicates the P-CSCF address.

![](media/image40.png){width="6.268055555555556in"
height="4.034722222222222in"}

The following snapshot shows the TFT included in the *Activate dedicated
EPS bearer* (MME -\>eNB) captured over S1AP. As the TFT is included in
the NAS message, it is delivered to the UE transparently so it can be
used by the UE.

![](media/image41.png){width="6.268055555555556in"
height="3.682638888888889in"}

In a nutshell, the uplink-only TFT is created by the PGW based on the
received PCC rules and sent to the UE so the UE can utilize it to filter
and map the outgoing IP packets with the corresponding uplink EPS
bearer.\
\
\
**II. TFT errors**\
The TFT is delivered from the MME to UE or vice versa contained in a NAS
message over S1AP and the RRC interfaces. The TFT errors indicate
operational inconsistencies from semantics or syntax perspectives
between TFT operations, packet filters and NAS messages and once
detected, it leads to the failure of EPS bearer level operations. The
3GPP TS24.301 has specified four types of TFT related errors as below:\
\
(1) [Semantic error in the TFT operation]{.underline} is more likely the
case when there is a contextual inconsistency in the TFT operation. The
following shows example cases:\
   - The TFT operation of other than \"Create a new TFT\" in
the *Activate dedicated EPS bearer context request*.\
   - The TFT operation of \"Delete packet filters from existing TFT\"
when the deletion will result in the empty TFT.\
(2) [Syntactical error in TFT operations]{.underline} is more likely the
case when there is a logical inconsistency between TFT operation and the
packet filters. The following shows example cases:\
   - The TFT operation of \"Create a new TFT\" and the empty packet
filter list in the TFT IE.\
   - The TFT operation of \"Add packet filters in existing TFT\" and the
empty packet filter list in the TFT IE.\
   - The TFT operation of \"Delete packet filters from existing TFT\"
when there is no corresponding packet filter in the existing TFT.\
(3) [Semantic error(s) in packet filter(s)]{.underline} is more likely
the case when a packet filter consists of conflicting packet filter
component which would render the packet filter ineffective.\
(4) [Syntactical error(s) in packet filters(s)]{.underline} is more
likely the case when two or more packet filters in the resultant TFT
would have component(s) with identical values such as the same packet
filter identifiers, the same packet filter precedence values, etc.\
\
Each of the above error cause can appear in the following NAS messages
as an ESM cause:\
\
(1) The *Activate dedicated EPS bearer context reject* (UE\--\>MME) as a
failure to create the dedicated EPS bearer.\
(2) The *Modify EPS bearer context reject* (UE\--\>MME) as a failure to
modify the dedicated EPS bearer.\
(3) The *Bearer Resource Allocation reject* (MME\--\>UE) as a failure to
initiate the activation of the dedicated EPS bearer.\
(4) The *Bearer Resource Modification reject* (MME\--\>UE) as a failure
to initiate the update of the dedicated EPS bearer.\
\
\
**III. Case study**\
The following snapshot has been captured while testing the conference
call scenario. Having been sorted out based on the MME-UE-S1AP-ID, it
shows the lifetime of the EPS bearer from when it is created until it is
released due to the \"semantic error in the TFT operation\". In the
meantime, there are five times of EPS bearer modifications occurred.\
\
NOTE The MME-UE-S1AP-ID is assigned by the MME to identify the UE over
S1AP. In the same way, the eNB also identifies the UE by assigning the
ENB-UE-S1AP-ID.

![](media/image42.png){width="6.268055555555556in"
height="2.7618055555555556in"}

The following snapshot shows the TFT in the *Activate dedicated EPS
bearer context request*. Please note that there are two packet filters,
one for the RTP and the other one for the RTCP. The TFT operation has to
be \"Create a new TFT\". The packet filter identifiers are 1 and 2 and
the precedence values are 223 and 191, respectively.\
\
NOTE the detail of the second packet filter is not shown in this
snapshot.

![](media/image43.png){width="6.268055555555556in"
height="3.761111111111111in"}

The following snapshot shows the TFT in the first *Modify EPS bearer
context request*. The TFT operation is \"Add packet filters to existing
TFT\". The packet filter identifiers are 3 and 4 and the packet
precedence values are 247 and 239, respectively.\
\
NOTE the detail of the second packet filter is not shown in this
snapshot.

![](media/image44.png){width="6.268055555555556in"
height="4.1722222222222225in"}

All the history of packet filters for the rest of operations can also be
analyzed following the same way. The following table shows the resulting
analysis of the details for all the packet filters during the lifetime
of the EPS bearer.

![](media/image45.png){width="6.268055555555556in"
height="2.272222222222222in"}

In this example, the last TFT \"Add packet filters to existing TFT\"
operation which is sent in the *Modify EPS bearer context request *has
the same packet precedence value with the existing packet filter #5.
Therefore, the UE responds with the ESM cause = \"semantic error in the
TFT operation\" in the *Modify EPS bearer context reject*.\
\
NOTE The UE seems to have a glitch sending the wrong ESM cause in this
test case. The duplicated packet precedence value will lead to the ESM
cause of \"Syntactical errors in packet filter(s)\" according to the
3GPP TS24.301.

**VoLTE: Tracking Area Update and combined attach**

A telecommunication network provides the way of identifying and tracking
the location of the UE to maintain the UE mobility. The UE registers its
location first time when it attaches the LTE network. Once the UE
location is registered in the network, the UE may either periodically or
per event initiate the tracking area update procedure. In case the
tracking area update procedure has failed, the UE retries the same
procedure based on the retry scheme. If the UE loses the connection
and/or falls into the idle state, the UE needs to re-register its
location as soon as it comes back to connected state. Without location
report, the network may assume that the UE stays at the last visited
tracking area and if not, the network will have a strategy to get to
know the UE location based on the paging scheme.\
\
NOTE Refer to the section 5.3.3 \"*Tracking Area Update procedures*\" of
3GPP TS23.401 for the detailed cases where the UE triggers the Tracking
Area Update (TAU) procedure.

**I. Identifying UE location **

The location of the UE is identified by the combination of several
identifiers and it is subject to the configuration of the physical and
logical network topology. The following shows the conceptual diagram of
the radio network.

  -----------------------------------------------------------------------
  ![](media/image46.png){width="6.0625in" height="2.8645833333333335in"}
  -----------------------------------------------------------------------
                   Fig 1. UE location and Tracking Area

  -----------------------------------------------------------------------

-   Cell-ID : locally unique identifier of a cell with the eNB

-   eNB-ID : locally unique identifier of an eNB within the PLMN

-   E-UTRAN Cell ID(ECI): locally unique identifier of a cell within a
    PLMN \[eNB ID + Cell ID\]

-   E-UTRAN CGI (ECGI): globally unique identifier of a cell \[PLMN ID +
    ECI\]

-   Tracking Area Code (TAC): locally unique identifier of the tracking
    area within a PLMN

-   Tracking Area Id (TAI): globally unique identifier of a tracking
    area \[PLMN ID + TAC\]

-   PLMN ID: globally unique identifier of a PLMN \[MCC + MNC\]

**II. Tracking Area Update procedure and combined attach**

The tracking area update procedure is initiated by the UE to register
its own location to the network and it can occur when the UE is either
in an idle state (i.e., ECM-IDLE) or in an active state (i.e.,
ECM-CONNECT bearer before release it sends *TAU* request. The UE uses
the LAI and the ECGI to represent its own location. The UE may request
the combined attach for both EPS services and non-EPS services. In this
case, the EPS will need to interwork with the legacy network. The
failure of such interworking will lead to retrials of tracking area
update procedure. The following flow shows a normal procedure of the UE
registering its location and updating its tracking area.

  -----------------------------------------------------------------------
            ![](media/image47.jpeg){width="6.083333333333333in"
                       height="5.416666666666667in"}
  -----------------------------------------------------------------------
         Fig 2. Initial attach and Tracking Area Update procedure

  -----------------------------------------------------------------------

\[1\] After RRC connection has been completed, the UE attaches to LTE
network by sending *Attach Request* to MME*.* The
S1AP *InitialUEMessage *that delivers the *Attach Request *contains TAI
and ECGI to inform the network of its location. Upon receiving
the *Attach Request*, the MME performs the LTE authentication and
Security measurement with the UE.

![](media/image48.png){width="6.268055555555556in"
height="6.398611111111111in"}

In this example, the UE requested the combined attach with its EPS
attach type set to \"Combined EPS/IMSI attach\", which indicates that
the UE wants to attach for both EPS and non-EPS services. The voice
domain preference and UE usage has been set to \"IMS PS voice preferred,
CS voice as secondary\". Given these, the UE may be able to attempt the
VoLTE and if it is not available it will perform CS fallback (CSFB)
procedure.

![](media/image49.jpeg){width="6.268055555555556in" height="3.36875in"}

\[2-3\] The MME update the location of the UE to the HSS by
sending *Update Location Request* that contains the visited PLMN
identifier (i.e., MCC and MNC).\
\
\[4-7\] The MME creates a GTP-C session with the SGW/PGW by sending
the *Create Session Request *and the PGW triggers
the *Credit-Control-Request (CCR)* to the PCRF. The *Create Session
Request* contains the Serving-Network IE for the PLMN ID and the User
Location Info IE for TAI and ECGI. The *CCR* contains the
3GPP-User-Location-Info AVP to accommodate the TAI and ECGI.\
\
\[8\] Upon receiving the Create Session Response from the SGW/PGW, the
MME responds with the *Attach Accept* towards the UE. The Attach Request
contains the Tracking Area List (TAL), which is the list of TAIs to
which UE is implicitly registered by the network. Henceforth, the UE
does not need to update its location when it moves within the given TAL,
thereby the intention is to reduce the traffic regarding the TAU.

![](media/image50.jpeg){width="5.96875in" height="4.989583333333333in"}

In this example, the combined attach has been accepted with its attach
result set to \"EPS only\" and supports the IMS Voice over PS session in
S1 mode. The \"EPS only\" indicates that the EPS service has been
successful but attach for non-EPS has failed\[3\].\
\
\[9-11\] The UE establishes the E-RAB with the eNB and sends the *Accept
Complete* to the MME. The MME requests the SGW/PGW to establish the S1
bearer by sending *Modify EPS bearer request*.\
\
\[12-13\] The UE may trigger the TAU procedure by sending the *TAU
request* following the criteria as defined in TS23.401.
The *TAU *contains the UE\'s current TAI and the ECGI. The voice domain
preference has been set to \"IMS PS voice preferred, CS voice as
secondary\" indicating that the VoLTE is preferred but if it\'s not
available, the UE will perform CS fallback. The EPS update type has been
set to \"Combined TA/LA updating with IMSI attach\" indicating that the
UE wants to perform an attach for non-EPS services while it is attached
for EPS services. The last visited TAI is included if the UE has a valid
TAI of the last visited tracking area and used by the MME to make a good
list of TAI (i.e., TAL) for the UE. The TAL is contained in the *TAU
Accept*.

![](media/image51.jpeg){width="6.268055555555556in"
height="4.485416666666667in"}

**III. Periodic TAU and retrying scheme**\
\
The timer, T3402 and T3411, specifies the time interval after which the
tracking area update procedure takes place. Upon expiry of T3402 or
T3411, the UE sends *TAU *with its EPS update type set to \"Combined
TA/LA updating with IMSI attach\". The timer value is set by the network
and sent to the UE being contained in the *Attach Accept *and
every *TAU* response.\
\
When the UE receives the \"Network Failure\" in the *TAU* response for
combined attach, the UE starts the T3411 and retries the *TAU* procedure
up to 5 times. If it has already retried 5 times, the UE starts the
T3420 for the next retry cycle. The T3411 is recommended to be set to 10
seconds and the T3420 to 12 minutes according to 3GPP TS24.301.\
\
The following shows the *TAU* retries history when the UE receives the
Network Failure error for combined update. There are only 4-times of
retrial in the first cycle as the first request in the *Attach
Request* has not been counted.

![](media/image52.jpeg){width="6.268055555555556in"
height="1.9590277777777778in"}

NOTE The TAU procedure can also take place when the UE receives the RRC
connection release with its reason set to \"load balancing TAU
required\" for MME offloading or when the UE moves into the LTE from 3G
network. This will be discussed later under the different subject.

**\*\*\***

In summary, the UE triggers the TAU procedure periodically and whenever
it looks the UE location has changed or needs to be updated at MME. The
detailed cases have been specified in 3GPP TS24.301 though, the
operators may need to optimize the TAU traffic in a way not to cause a
traffic overload. The traffic can be possibly controlled by finding out
appropriate timer values or by optimizing the list of TAIs in a TAL.

***Red Mouse*** 

REFERENCES\
\
\[1\] 3GPP TS23.003, \"Numbering, Addressing and Identification\",
v11.0.0, Dec 2011\
\[2\] 3GPP TS23.401, \"General Packet Radio Service(GPRS) enhancements
for Evolved Universal Traversal Radio Access Network(E-UTRAN) access\",
v12.4.0, Mar 2014

\[3\] 3GPP TS24.301, \"Non-Access-Stratum(NAS) protocol for Evolved
Packet System(EPS); stage3\", v12.4.0, Mar 2014

\[4\] 3GPP TS36.300, \"Evolved Universal Traversal Radio Access (E-UTRA)
and Evolved Universal Traversal Radio Access Network(E-UTRAN); Overall
description; stage2\", v10.0.0, Jun 2010\
\[5\] 3GPP TS36.331, \"Evolved Universal Traversal Radio Access
(E-UTRA); Radio Resource Control(RRC); Protocol specification\",
v12.6.0, Jun 2015\
\[6\] Netmanias, \"LTE Identification

**E2E VoLTE call setup(1/4) : Initial attach and default EPS
bearercreation**

  -----------------------------------------------------------------------
  When the UE is turned on, it establishes a PDN connection with a
  default APN. In this test for VoLTE call setup, the operator provides
  two APNs, i.e., "Internet" APN and the "IMS" APN. The default APN is an
  "Internet" APN that is used for internet data traffic and its default
  EPS bearer has a QCI value of '9'. After the PDN connection is
  established with the internet APN, the UE attempts additional PDN
  connection with the IMS well known APN, i.e., "IMS APN". The IMS APN is
  preconfigured in the UE and its default EPS bearer has a QCI value of
  '5' being used for SIP signaling. Once the PDN connection with the IMS
  APN is completed and the default EPS bearer is successfully created,
  the UE is able to communicate with the IMS Core for VoLTE call service.
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

**Introduction**

The UE\'s initial attach procedure consists of two routines. One is to
establish a signaling path on RRC, S1AP and GTP-C interfaces and the
other one is to establish the bearer path including Data Radio Bearer
(DRB) and GTP-U (i.e., S1 and S5 bearer). The following diagram show
overall LTE architecture and different signaling and media paths with
multiple PDNs.

NOTE In this diagram, the S5 interface between the SGW and the PGW has
been omitted for simplicity.

  -----------------------------------------------------------------------
            ![](media/image53.png){width="6.208333333333333in"
                      height="3.3958333333333335in"}\
                                     \
                        Figure 1. PDN Connectivity

  -----------------------------------------------------------------------

The signaling connection procedure involves LTE authentication, NAS
security procedure and the UE\'s location update procedure. Therefore,
when the signaling connection is completed, the UE comes to have a
secured connection to communicate with the network and the network
becomes aware of the UE\'s context as to its location, subscriber\'s
information, QoS requirements, etc. Along with the signaling connection,
there comes a default EPS bearer established from the UE to the PGW,
which covers the DRB, S1 bearer and S5 bearer.

**I. Initial attachment **

A UE establishes an RRC connection with an eNB and the eNB creates an
S1AP session with an MME for signaling. The NAS messages are exchanged
between UE and the MME once the RRC and S1AP connection is established
and it is composed of two layers, i.e., EPS Session Management (ESM)
layer and EPS Mobility Management (EMM) layer. The ESM message is used
to control PDN connectivity, bearer resource allocation/modification,
activation/deactivation of a default/dedicated EPS bearer. The EMM
message is used to maintain the mobility of the UE using e.g., Attach,
Detach, Tracking Area Update (TAU). The NAS message transparently goes
through the eNB contained in RRC and S1AP messages.

  -----------------------------------------------------------------------
            ![](media/image54.jpeg){width="6.268055555555556in"
                       height="6.438888888888889in"}
  -----------------------------------------------------------------------
                       Figure 2. Initial Attach flow

  -----------------------------------------------------------------------

\[1-2\] The UE in idle mode requests the eNB to establish a signaling
connection by sending *RRC Connection request*. The eNB allocates the
network resource based on the received radio configuration and initiates
an RRC connection towards the UE by sending *RRC Connection Setup*.

\[3\] The UE configures a radio bearer and transport channel based on
predefined parameters identified by a received predefined configuration
identity and confirms RRC connection by sending the *RRC Connection
Setup Complete* to the eNB. Meanwhile, the NAS messages (i.e., *Attach
Request *at EMM layer and* the PDN Connectivity Request *at ESM layer)
is transparently delivered to the MME via eNB being contained in the RRC
and S1AP messages (i.e., *RRC Connection Setup
Complete* and *InitialUEMessage*, respectively).

The following snapshot shows the NAS part of *InitialUEMessage* captured
on S1AP interface.

  -----------------------------------------------------------------------
            ![](media/image55.jpeg){width="6.268055555555556in"
                       height="4.427083333333333in"}
  -----------------------------------------------------------------------
                        Figure 3. InitialUEMessage

  -----------------------------------------------------------------------

In case the UE wants to use both LTE and non-LTE, the *EPS Attach
type* will be set to \"Combined EPS/IMSI attach\" and the *Voice domain
preference* set to \"IMS PS voice preferred, CS voice as secondary\".

-   EPS Attach Type : EPS attach/combined EPS/IMSI attach/EPS emergency
    attach

-   Voice domain preference : a preferred network for voice call

The Protocol Configuration Option (PCO) is used by the UE to request a
certain information like UE IP address, DNS IP address, etc. 

The following snapshot shows an example of *PCO* configuration included
in the *initialUEMessage*.

  -----------------------------------------------------------------------
   ![](media/image56.png){width="6.268055555555556in" height="3.075in"}
  -----------------------------------------------------------------------
                   Figure 4. PCO for initial attachment

  -----------------------------------------------------------------------

The following snapshot shows other parameters of *initialUEMessage*,
which contains the UE\'s location information (i.e., Tracking Area
Identifier, E-UTRAN Cell Global Identity) and RRC establishment cause.

  -----------------------------------------------------------------------
            ![](media/image57.png){width="6.239583333333333in"
                       height="5.833333333333333in"}
  -----------------------------------------------------------------------
                 Figure 5. Parameters in initialUEMessage

  -----------------------------------------------------------------------

\[4-5\] Upon receiving the *Attach Request*, the MME requests the
authentication vector to HSS by sending *Authentication Information
Request* (AIR) to authenticate the subscriber. 

![](media/image58.jpeg){width="6.268055555555556in" height="2.625in"}

Figure 6. Authentication Information Request

The HSS responds with the Authentication Vector in the *Authentication
Information Response* (AIA) as shown in the following snapshot.

![](media/image59.jpeg){width="6.125in" height="2.8645833333333335in"}

Figure 7. Authentication Information in AIA

The following diagram shows a conceptual data flow of LTE-AKA
authentication. The MME delivers the AUTN and RAND to the UE among the
received parameters. (2) The UE authenticates the network by running the
authentication algorithm which uses the received RAND and local
parameters as input and then (3) verifies if the output of the
calculation is matched with the received AUTN. The UE sends the RES
which is another output of the authentication algorithm to the MME so
that (4) MME can verify the RES by comparing it with the XRES received
from the HSS in (1).

![](media/image60.png){width="5.0in" height="2.8645833333333335in"}

  -----------------------------------------------------------------------
  Figure 8. LTE authentication
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

As such the UE and LTE network performs the mutual authentication. After
successful authentication, there comes the NAS security establishment
procedure between the UE and the LTE network in order to provide a
secured data transfer and data integrity.

**II. Location update and GTP-C session creation**

In this part of the flow, the MME updates the UE\'s location information
stored in the HSS and creates GTP-C session with the SGW. The GTP-C
session is used to control GTP-U (i.e., S1 and S5 bearers) media session
belonging to the same APN.

![](media/image61.jpeg){width="5.791666666666667in"
height="5.895833333333333in"}

  -----------------------------------------------------------------------
         Figure 9. Location update and GTP-C session creation flow
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

\[6-7\] The MME registers the UE\'s location to the network by
sending *Update Location Request* to the HSS. The following lists some
of parameters as shown in the snapshot.

-   User-Name AVP: IMSI

-   Terminal Information AVP: IMEI, Software version

-   Visited PLMN-Id AVP: MCC and MNC of a visited network

-   RAT-Type AVP: EUTRAN

![](media/image62.jpeg){width="6.268055555555556in"
height="2.702777777777778in"}

Figure 10. Update Location Request

In return, the MME receives the *Update Location Answer *from the HSS
and it contains* *the APN list as shown in the snapshot below.

![](media/image63.jpeg){width="6.268055555555556in"
height="3.535416666666667in"}

Figure 11. Update Location Answer

Upon receiving the list of APN in the *Update Location Answer (ULA)*,
MME determines the default APN. In this example, there are two APNs
received as shown in the following snapshot.

![](media/image64.png){width="6.268055555555556in"
height="2.095833333333333in"}

Figure 12. APN list

The following snapshot shows the detailed APN configuration. One of APNs
(bottom one) is an \"Internet\" APN as indicated by Service-Selection
AVP. The other APN (upper one) is an "IMS" APN. The default APN is
determined by comparing the Context-Identifier AVP under the
APN-Configuration-Profile AVP with another Context-Identifier AVP in the
APN-Configuration AVP. In this case, the context identifier value of
\"10\" in the APN-Configuration AVP for "Internet" is matched with the
context identifier value in the upper layer. Given this, the MME will
select the "Internet" APN as a default APN.

![](media/image65.jpeg){width="6.268055555555556in"
height="4.877083333333333in"}

Figure 13. APN Configuration Profile

\[8\] The MME requests S11 (GTP-C) session creation by sending
the *Create Session Request* to the SGW. The *Create Session
Request* contains the following parameters along with subscriber\'s
information like MSISDN, IMEI and IMSI.

-   APN : the access point name to which the GTP-C session is to be
    established.

-   PDN Address Allocation (PAA) : UE IP address. It is empty at this
    moment in time as no IP address has been allocated for the UE.

-   Serving Network : the MCC and MNC of the serving network which the
    UE is attached to.

-   User Location Info: TAI, ECGI

-   MME GTP-C TEID : Identifier of the MME as an end point of the GTP-C
    tunnel

-   EPS Bearer ID (EBI) of the default EPS bearer 

-   QoS Class Identifier (QCI) : '9'

In this case the QCI value of "9" for the default EPS bearer has been
allocated as this is a PDN connection with the "internet" APN.

NOTE The UE can have up to 11 EPS bearers in total and assign the same
amount of EPS Bearer Id (EBI) from 5 to 15.

NOTE The SGW will also establish the GTP-C session with the PGW on S5
interface which is not shown in this flow.

![](media/image66.png){width="6.268055555555556in"
height="3.859027777777778in"}

Figure 14. Create Session Request

\[9\] Upon receiving the *Create Session Request*, the PGW assigns an IP
address for the UE from an IP pool. The PGW sends
the *Credit-Control-Request *(CCR) to the PCRF indicating that this is
an initial request and requests the PCC rule for the default EPS bearer.
The *Credit-Control-Request *(*CCR)* contains the following parameters
in this example.

-   CC-Request-Type AVP: "INITIAL REQUEST"

-   Subscription-Id AVP: IMSI, MSISDN

-   Framed-IP-address AVP: the allocated UE IP address

-   QoS-Information AVP: APN-AMBR (UL/DL)

-   3GPP-User-Location-Info AVP: TAI, ECGI

-   Call-Station-Id AVP: APN (Internet)

-   Default-EPS-Bearer-QoS AVP: QCI, ARP

The following snapshot shows the *CCR* captured on Gx interface.

![](media/image67.png){width="6.268055555555556in"
height="3.379166666666667in"}

Figure 15. Credit Control Request

\[10\] Upon receiving the *CCR*, the PCRF determines the PCC rule based
on the received subscriber\'s information and responds
with *Credit-Control-Answer (CCA) *including a PCC rule(s). When it
comes to a default bearer, the PCRF may include only a PCC rule name
which indicates the predefined PCC rule locally stored in the PGW.
Henceforth, the PCC rule is applied to all the traffic by the PGW.

![](media/image68.png){width="6.268055555555556in"
height="2.076388888888889in"}

Figure 16. Credit Control Answer

\[11\] The SGW/PGW completes the GTP-C session creation procedure by
sending the *Create Session Response*. The *Create Session
Response* contains the following parameters:

-   AMBR : Aggregated maximum bit rate that is allowed for this APN

-   EPS Bearer ID : 5

-   Protocol Configuration Options (PCO) : P-CSCF IP address, DNS IP
    address, etc, based on the requested configuration information by
    the UE in the *Attach Request*

-   PDN Address Allocation (PAA): UE's IP address

-   SGW GTP-C TEID : Identifier of the SGW as the end point of the GTP-C
    tunnel

-   Bearer Context: the information of the S1-U default EPS bearer to be
    created, which contains EBI, SGW GTP-U TEID, QCI, etc

![](media/image69.png){width="6.268055555555556in"
height="2.732638888888889in"}

Figure 17. Create Session Response

**III. Default EPS bearer creation**

Once the signaling path is successfully set up, the MME requests the eNB
to activate the default EPS bearer with the SGW and the UE. The eNB
establishes S1 bearer towards SGW and the Data Radio Bearer (DRB)
towards the UE. The SGW will also establish the S5 bearer with the PGW,
which is not shown in this flow.

![](media/image70.png){width="5.78125in" height="6.645833333333333in"}

Figure 18. Default EPS bearer creation flow

\[12\] The MME accepts the initial attach request by sending the *Attach
Accept* and requests to activate the default EPS bearer to the UE which
contains *Activate default EPS bearer context request* in the ESM
message container. The NAS message (i.e., *Attach Accept *in EMM
layer*, Activate default EPS bearer context request* in ESM layer)
contains the following parameters.

-   TAI list : the list of Tracking Area Identity within which the UE
    doesn\'t need to send *Tracking Area Update* (TAU) 

-   EPS QoS : QCI (9)

-   Access Point Name (APN) : Internet APN

-   PDN address: the allocated UE IP address

-   APN-AMBR: the maximum aggregated bit rate allowed for this APN

-   Protocol Configuration Options (PCO) : DNS IP address, etc, based on
    the requested configuration information by the UE in the *Attach
    Request*

![](media/image71.png){width="6.268055555555556in"
height="4.348611111111111in"}

Figure 19. Attach Accept (Activate default EPS bearer context request)

The above NAS message is contained in the *Initial Context Setup
Request* message on S1AP interface. Other than the NAS message, it also
contains the following parameters.

-   UE-AMBR : Aggregated maximum bit rates for the UE (UL/DL)

-   E-RAB ID : identifier of the radio access bearer towards the eNB

-   SGW GTP-U TEID : identifier of SGW as an end point of the GTP-U
    tunnel which was delivered in *Create Session Response* (step#11).

![](media/image72.png){width="6.268055555555556in"
height="4.504861111111111in"}

Figure 20. Initial UE Context Request

Upon receiving the *Attach Accept *and *RRC Connection Reconfiguration*,
the UE establishes a DRB with the eNB and responds with *RRC Connection
Reconfiguration Complete* to the eNB.

The eNB establishes the uplink S1-U bearer with the SGW. After
successful GTP-U establishment, the eNB responds with the *initial UE
Context Response* to the MME. In this response, the eNB contains the eNB
GTP-U TEID, which will be routed to the SGW via the MME and used to
identify the eNB as an end point of the GTP-U by the SGW.

NOTE The SGW GTP-U TEID is generated by the SGW and transparently routed
to the eNB via the MME contained in *Create Session
Response* and *Initial Context Setup Request* on S11 and S1AP,
respectively. In the same way, the eNB GTP-U TEID is generated by the
eNB and transparently routed to the SGW via the MME contained in
the *Initial Context Setup Response* and *Modify Bearer Request *at
step#14.

![](media/image73.png){width="6.268055555555556in"
height="3.0458333333333334in"}

Figure 21. Initial UE Context Response

\[13\] The UE confirms the *Attach Accept* and informs the MME of the
fact that the default EPS bearer has been activated by sending
the *Attach Complete,* which contains the *Activate Default EPS Bearer
Context Accept* as a response to a corresponding request.

![](media/image74.png){width="6.268055555555556in"
height="3.134027777777778in"}

Figure 22. Attach Complete (Activate default EPS bearer context accept)

\[14\] The MME sends the *Modify EPS Bearer Request* requesting the SGW
to establish the downlink S1 bearer towards the eNB. The *Modify EPS
Bearer Request* contains the following parameters:

-   EPS Bearer ID : identifier of a default EPS bearer (5)

-   eNB GTP-U TEID : identifier of the eNB as an end point of the GTP-U
    tunnel

![](media/image75.png){width="6.268055555555556in"
height="4.7555555555555555in"}

Figure 23. Modify EPS bearer request

Upon receiving the *Modify EPS Bearer Request*, the SGW establishes the
S1 bearer towards the eNB.

\[15\] The SGW responds with the *Modify EPS Bearer Response*.

![](media/image76.png){width="6.268055555555556in"
height="2.3506944444444446in"}

Figure 24. Modify EPS bearer response

**IV. PDN Connection to IMS APN**

So far, the UE has performed the initial attachment procedure with the
LTE network and as a result, the PDN connection has been established
between the UE and the default APN, i.e., internet APN. After successful
PDN connection with the default APN, if the default APN is not an IMS
APN, the VoLTE UE initiates an additional PDN connection procedure with
the "IMS" APN.

![](media/image77.png){width="5.770833333333333in"
height="8.520833333333334in"}

Figure 25. PDN connection with IMS APN flow

\[16\] The UE requests to establish an additional PDN connection with
the IMS APN, which is typically used for VoLTE. There is no need of
establishing RRC connection at this stage as it was already established
at step#3. In this message, the Access Point Name (APN) is set to "IMS"
and the UE may request the P-CSCF address and it is indicated by the
Protocol Configuration Option (PCO) parameter. The following snapshot
shows an example of *PDN Connectivity Request* which is contained by
the *uplinkNASTransport* S1AP message.

![](media/image78.png){width="6.268055555555556in"
height="4.338888888888889in"}

Figure 26. PDN connectivity request for IMS APN

\[17\] Upon receiving the *PDN Connectivity Request*, the MME
sends *Create Session Request* to the SGW. Refer to step #8 for overall
description.

-   APN : "IMS"

-   MME GTP-C TEID: the same TEID that was allocated at step #8. The MME
    and the SGW use the same TEID for different PDNs.

-   EPS Bearer ID (EBI): '6' in this case as the EBI '5' was already
    used in step#8. The EBI will be incremented along with a new EPS
    bearer.

-   QoS Class Identifier (QCI): '5' for IMS signaling.

![](media/image79.png){width="6.268055555555556in"
height="4.338888888888889in"}

Figure 27. Create Session Request

\[18\] Upon receiving the *Create Session Request*, the MME
sends *CCR* to the PCRF. Refer to step #9 for overall description.

![](media/image80.png){width="6.268055555555556in"
height="3.467361111111111in"}

Figure 28. Credit-Control-Request

-   CC-Request-Type AVP: "INITIAL REQUEST"

-   Framed-IP-address AVP: The UE IP address is different from what was
    allocated at step #9. The UE is allocated with different IP address
    per PDN.

-   Call-Station-Id AVP: IMS APN

-   Default-EPS-Bearer-QoS AVP: In case of IMS APN, the default EPS
    bearer has a QCI=5.

\[19\] Upon receiving the *CCR*, the PCRF responds with *CCA* containing
the PCC rule of the default EPS bearer for IMS APN. Refer to step #10
for overall description.

![](media/image81.png){width="6.268055555555556in"
height="4.1722222222222225in"}

Figure 29. Credit-Control-Answer

\[20\] Upon receiving the *CCA*, the MME responds with *Create Session
Response* containing the PCC rule of the default EPS bearer for IMS APN.
Refer to step #11 for overall description.

-   EPS Bearer ID: '6'

-   Protocol Configuration Options (PCO) contains P-CSCF IP address and
    will be delivered to the UE.

-   PDN Address Allocation (PAA): UE's IP address and will be delivered
    to the UE.

-   SGW GTP-C TEID: The same TEID that was allocated at step #11. The
    MME and the SGW use the same TEID for different PDNs.

-   Bearer Context contains the SGW GTP-U TEID for the default EPS
    bearer which is different from what was used in step #11.

![](media/image82.png){width="6.268055555555556in"
height="4.908333333333333in"}

Figure 30. Create Session Response

\[21\] Upon receiving the *Create Session Response*, the MME requests to
activate the default EPS bearer by sending *Activate default EPS bearer
context request* towards the UE, which is contained in *E-RAB Setup
Request* on S1AP interface. The *E-RAB Setup Request* is used to assign
resources on Uu (i.e., air interface between UE and the eNB) and S1 for
one or several E-RABs. The following shows parameters contained in
the *E-RAB Setup Request*.

-   UE-AMBR (UL/DL): The aggregated maximum bit rate of the UE
    associated with the same PDN.

-   E-RAB to be setup parameters contains E-RAB ID=6 and SGW GTP-U TEID
    which was delivered at step #20.

The following shows parameters contained in the *Activate default EPS
bearer context request*:

-   EPS QoS QCI = 5

-   Access Point Name (APN): "IMS"

-   PDN address: The newly allocated UE IP address

-   Protocol Configuration Options (PCO) contains the P-CSCF address
    which was delivered in step #20.

-   APN-AMBR: aggregated maximum bit rate for the same APN.

![](media/image83.png){width="6.268055555555556in"
height="3.8291666666666666in"}

Figure 31. E-RAB Setup Request (Activate default EPS bearer context
request)

The eNB delivers the *Activate default EPS bearer context
request* transparently to the UE, which is contained in *RRC Connection
Reconfiguration*. Refer to step #12 for UE behavior after receiving *RRC
Connection Reconfiguration*.

\[22\] \] The UE informs the MME of the fact that the default EPS bearer
has been activated by sending the *Activate Default EPS Bearer Context
Accept* as a response to a corresponding request.

![](media/image84.png){width="6.268055555555556in"
height="2.8208333333333333in"}

Figure 32. Activate default EPS bearer context request

![](media/image85.png){width="5.78125in" height="3.40625in"}

Figure 33. EPS bearer creation flow

\[23\] The MME sends the *Modify Bearer Request* requesting the SGW to
establish the downlink S1 bearer towards the eNB. Refer to step #14 for
overall description. The message contains eNB GTP-U TEID that shall be
used by the SGW to identity the end point of the GTP-U of default EPS
bearer.

![](media/image86.png){width="6.268055555555556in"
height="2.4583333333333335in"}

Figure 34. Modify Bearer Request

\[24\] Upon receiving the *Modify Bearer Request*, the SGW establishes a
downlink S1 bearer and responds with *Modify Bearer Response*.

![](media/image87.png){width="6.268055555555556in"
height="3.251388888888889in"}

Figure 35. Modify Bearer Response

Consequently, the default EPS bearer with QCI value of '5' between the
UE and the IMS APN is established. Hereafter all the SIP traffic goes
through the default EPS bearer.

***Red Mouse*** 

**REFERENCES**

\[1\] 3GPP TS25.331, \"Radio Resource Control (RRC); protocol
specification\", v12.3.0, Sep 2014

\[2\] 3GPP TS24.301, \"Non-Access-Stratum (NAS) protocol for Evolved
Packet System (EPS); stage3\", v12.4.0, Mar 2014

\[3\] 3GPP TS36.413, \"Non-Access-Stratum (NAS) protocol for Evolved
Packet System (EPS); stage3\", v12.4.0, Mar 2014

\[4\] Red Mouse, \"[[Tracking Area Update and Combined
Attach]{.underline}](http://bit.ly/1MNWcsl)\", Jul, 2015

\[5\] Red Mouse, \"[[Understanding of GTP TEID to use it in LTE
troubleshooting]{.underline}](http://bit.ly/1HPM3dv)\", Jun, 2015

\[6\] Netmanias, \"LTE Security II: NAS and AS security\", Aug 5th 2013

\[7\] Netmanias, \"LTE IP Address Allocation Schemes I: Basic\", Feb
13th 2015

**E2E VoLTE call setup(2/4) : IMS registration**

  -----------------------------------------------------------------------
  Once the UE attaches to the LTE network and the default EPS bearer is
  created successfully with the IMS APN, the UE registers to the IP
  Multimedia Subsystem (IMS) network before accessing the VoLTE service.
  The IMS registration procedure includes the IMS authentication, e.g.,
  IMS-AKA, and security negotiation between UE and IMS network. After
  successful IMS registration, the IMS network becomes aware of UE
  context such as subscription profile, registration status, etc. After
  the initial IMS registration, the UE shall refresh the IMS registration
  status by periodically sending re-Registration.
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

**Introduction**

It is assumed that the UE has established a PDN connection to the IMS
APN with the QCI value of its default EPS bearer set to '5'. The IMS
registration signal goes through the default EPS bearer and gets inside
the IMS core via the P-CSCF. The P-CSCF, I-CSCF and the S-CSCF consists
the IMS core and they controls SIP signaling for VoLTE. The I-CSCF and
the S-CSCF interworks with the HSS via Diameter Routing Agent (DRA) to
retrieve subscriber's profile, authentication vector, etc. At the front
of the P-CSCF lies the Session Border Controller (SBC). The SBC provides
a security function like IPSec, topology hiding, media controlling, etc.
It can either be co-deployed with the P-CSCF or separated from the IMS
Core.

NOTE the DRA between Diameter clients and Diameter servers (i.e., PCRF,
HSS) is omitted in the diagram to clarify the reference points.

![](media/image88.png){width="6.268055555555556in" height="1.60625in"}

Figure 1. Overall architecture

**I. IMS Authentication and Key Agreement (AKA) during IMS
registration**

The IMS AKA is a mutual authentication methodology used by the IMS
network to authenticate a UE. In this authentication procedure, both
server and client runs the same authentication algorithm using the same
secret key and several public parameters. The secret key is known to
both UE and the IMS network. It can be stored in IP Multimedia Services
Identity Module (ISIM) and at the same time, be provisioned to the Home
Subscriber Server (HSS) in advance. After running the authentication
algorithm, the server and the client exchanges their outcome with each
other and authenticate the peer by comparing the received authentication
parameter with the outcome of their own. The following is the conceptual
diagram of the IMS AKA mechanism.

![](media/image89.png){width="6.268055555555556in" height="5.26875in"}

Figure 2. IMS AKA

(1)   The secret-key K and the sequence number SQN are commonly stored
in both server and client.

(2)   The UE sends the initial registration with the user identifier
towards the IMS Core.

(3)   The S-CSCF (i.e., registrar) queries the HSS for the
authentication vector of that subscriber. The HSS generates the random
number RAND using the SQN. The HSS uses K, SQN and RAND parameters as
input to the authentication algorithm and as a result, obtains a set of
authentication parameters, i.e., the authentication vector (AV), as
listed below:

-   AUTN : Authentication token represented as a concatenation of MAC
    and SQN and used by the client to authenticate the server.

-   XRES: Expected correct result of running authentication algorithm
    and used by the server to authenticate the client.

-   CK: Cipher Key (Optional)

-   IK: Integration Key

The S-CSCF returns AV (i.e., RAND, AUTN, CK, IK) to the P-CSCF and the
P-CSCF delivers RAND and AUTN in the response to the initial
registration request (see the step#31 for the detail). XRES is stored in
the S-CSCF for later use. The CK and IK is used for integrity and
security check by the P-CSCF (or SBC).

(4)   The UE extracts MAC and SQN from the received AUTN. The UE
verifies the range of SQN and uses AUTN, K and RAND as input to the
authentication algorithm. The UE compares the resulting parameter, XMAC
with the received MAC. As such, the UE authenticates the server.

(5)   The resulting RES is sent back to the server. The S-CSCF
authenticates the client by comparing the received RES with the XRES.

**II. IMS registration procedure**

Right after the default EPS bearer is established, comes IMS
registration procedure. The IMS registration is the procedure for a
VoLTE client to register its contact information to the IMS network and
it is performed through the existing EPS bearer of QCI=5 in general. The
IMS registration procedure is composed of two transactions, that is, the
first one is for the UE to obtain the authentication challenge and the
other one is to be authenticated using the received authentication
challenge.

In case it is a re-registration, the first transaction may not be
necessary. The UE will include challenge parameters received in the
previous registration procedure so the network is able to authenticate
the UE as long as the challenge parameters are still valid. During the
registration, the VoLTE client and the IMS network authenticate each
other based on the agreed authentication algorithm and in the meantime,
negotiate a security algorithm for IP layer transactions. 

![](media/image90.png){width="6.268055555555556in"
height="5.690277777777778in"}

  -----------------------------------------------------------------------
                       Fig 3. IMS registration flow

  -----------------------------------------------------------------------

\[25\] The UE initiates the IMS registration by sending the
SIP *REGISTER *towards the P-CSCF.

-   Authorization: Authentication information e.g., authentication
    scheme, nonce, realm, authentication algorithm, etc. The nonce value
    is empty as this is the first registration.

-   Expires[:]{.underline} The validity time of this registration. The
    UE is supposed to perform re-registration before the timer is
    expired. It is usual for the UE to re-register after 1/2\*(timer
    value) seconds. When the UE is connected to the LTE network, the
    value of this header would be 3600 seconds and when it is connected
    to the Wi-Fi, it would be 60 seconds typically.

-   Security-Client: A list of supported security algorithm by the UE.

-   Contact: UE IP address, device capabilities and various feature
    tags.

The following snapshot shows an example of SIP *REGISTER*.

![](media/image91.png){width="6.268055555555556in"
height="4.026388888888889in"}

  -----------------------------------------------------------------------
  Fig 4. SIP REGISTER
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

The P-CSCF routes the SIP *REGISTER* to the I-CSCF as the P-CSCF does
not know at this moment as to which S-CSCF is going to serve this UE
yet.

\[26\] Upon receiving the SIP *REGISTER*, the I-CSCF performs user
registration status query by sending *User-Authorization-Request* (UAR)
to the HSS.

-   User-Name AVP: IMS Private User Identity (IMPI) of the user and used
    to authenticate the user based on the username part of the value.

-   Public-Identity AVP: IMS Public User Identity, which is either SIP
    URI or TEL URI of the user.

-   Visited-Network-Identifier AVP: The domain of the visited PLMN

The following snapshot shows an example of *UAR*.

![](media/image92.png){width="6.268055555555556in" height="4.23125in"}

  -----------------------------------------------------------------------
  Fig 5. User Authorization Request (UAR)
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

\[27\] The HSS authorizes the user for IMS service (i.e., verifying the
user's IMPI and IMPU) and if successful, returns with the S-CSCF address
for this user in the response, *User-Authorization-Answer* (UAA).

-   Server-Name AVP: The S-CSCF address assigned for the IMS subscriber.

-   Experimental-Result: DIAMETER_FIRST_REGISTRATION if it is the first
    time IMS access for the user and there is no S-CSCF assigned yet. If
    there is already assigned S-CSCF for the user, it will be set to
    DIAMETER_SUBSEQUENT_REGISTRATION and the Server-Name AVP will be
    provided.

The following snapshot shows the case where there is already assigned
S-CSCF for the user, in which case the I-CSCF does not have to assign a
new S-CSCF. If there is no assigned S-CSCF for the subscriber, the HSS
returns a set of S-CSCF capabilities and the I-CSCF shall assign a new
one based on the received capabilities.

![](media/image93.png){width="6.268055555555556in"
height="4.133333333333334in"}

Fig 6. User Authorization Answer (UAA)

\[28\] The I-CSCF forwards the *SIP REGISTER* towards the indicated
S-CSCF.

\[29\] The S-CSCF sends the *Multimedia-Auth-Request* (MAR) to the HSS
requesting the authentication information.

-   User-Name AVP: IMS Private User Identity (IMPI) of the user and used
    to authenticate the user based on the username part of the value.

-   Public-Identity AVP: IMS Public User Identity, which is either SIP
    URI or TEL URI of the user.

-   SIP-Auth-Data-Item AVP: The authentication algorithm set to
    "Digest-AKAv1-MD5" in this example.

-   SIP-Number-Auth-Items AVP: The number of authentication vectors.

![](media/image94.png){width="6.268055555555556in"
height="3.8881944444444443in"}

Fig 7. Multimedia Auth Request (MAR)

\[30\] The HSS responds with
the *Multimedia-Auth-Answer* (MAA) containing the authentication
information.

-   SIP-Authorization AVP: XRES, which is one of output obtained after
    running the authentication algorithm (e.g., AKAv1-MD5).

-   SIP-Authenticate AVP: The concatenation of RAND and AUTN to be used
    for authentication.

![](media/image95.png){width="6.268055555555556in"
height="4.583333333333333in"}

Fig 8. Multimedia Auth Answer (MAA)

\[31\] The S-CSCF responds with the *401 UnAuthorized* to the P-CSCF.
The WWW-Authenticate header includes nonce parameter (i.e., a
concatenation of RAND and AUTN), IK and CK. The AUTN is a concatenation
of the MAC and SQN.

-   [WWW-Authenticate:]{.underline} Authentication challenge needed for
    mutual authentication.

![](media/image96.png){width="5.729166666666667in"
height="2.8333333333333335in"}

Fig 9. 401 UnAthorized

\[32\] The P-CSCF responds with the *401 UnAuorized* towards the UE. The
WWW-Authenticate header includes nonce value. The IK and CK is stored in
the P-CSCF and removed from the WWW-Authenticate header. As the UE and
the P-CSCF negotiated the security method to use IPsec during the
initial SIP registration, the subsequent registration and the call
related signals like INVITE, 200 OK, PRACK, BYE, etc. are secured based
on IPsec.

-   [Security-Server: a list of supported security algorithm by the
    server.]{.underline}

NOTE In this field test, the SBC takes over security functions of
P-CSCF. Therefore the security negotiation and maintaining security
parameters like IK and CK are done by the SBC.

![](media/image97.png){width="6.268055555555556in"
height="2.145138888888889in"}

Fig 10. 401 UnAthorized

Upon receiving the *401 UnAuthorized*, the UE extracts the MAC and the
SQN from the AUTN, calculates its own XMAC and checks if the XMAC is the
same as the received MAC and if the SQN is in a correct range, thereby
the UE authenticates the server. The UE also obtains the RES, IK and CK
as a result of running the authentication algorithm.

\[33\] The UE sends the subsequent SIP *REGISTER *towards the P-CSCF and
the P-CSCF to the I-CSCF.

-   Authorization header: The response to the authentication challenge
    along with the private user identity, realm, nonce, URI and RES.

-   P-Access-Network-Info: The radio access technology and radio cell
    identity.

![](media/image98.png){width="6.268055555555556in"
height="4.4631944444444445in"}

Fig 11. Subsequent SIP Registration

NOTE the above snapshot has been captured between SBC and P-CSCF as the
packet on SGi/Gm interface has been secured using IPsec as a result of
security negotiation and it couldn't be decoded by the wireshark in this
test. In order to complete the security negotiation, the UE must have
included the Security-Verify header in the subsequent REGISTER
indicating IPsec, which is not shown in this snapshot as the SBC removes
the header before forwarding the message to the IMS core.

\[34\] Upon receiving the SIP *REGISTER*, the I-CSCF performs user
registration status query by sending *User-Authorization-Request* (UAR)
to the HSS.

![](media/image99.png){width="6.268055555555556in"
height="3.134027777777778in"}

Fig 12. User Auth Request (UAR)

\[35\] The HSS authorizes the user for IMS service (i.e., verifying the
user's IMPI and IMPU) and if successful, returns with the S-CSCF address
for this user in the response, *User-Authorization-Answer* (UAA).

![](media/image100.png){width="6.268055555555556in"
height="3.3006944444444444in"}

Fig 13. User Auth Answer (UAA)

\[36\] The I-CSCF forwards the SIP *REGISTER *towards the indicated
S-CSCF. Upon receiving the subsequent SIP REGISTER, the S-CSCF compares
the stored XRES with the received RES (i.e., Digest Authentication
response parameter). If they are identical and successfully
authenticated, the public user identity is registered in the S-CSCF.

\[37\] The S-CSCF informs the HSS that the user has been registered by
sending *Server Assignment Request (SAR)*. Upon receiving the *SAR*, the
HSS stores the mapping relation between the S-CSCF and the corresponding
IMS subscriber.

-   User-Data-Already-Available AVP: Indicator of whether or not the
    sending S-CSCF has user profile information which is required to
    service the user. If it is set to USER_DATA_NOT_AVAILABLE, the HSS
    is expected to provide the user data in the response.

![](media/image101.png){width="6.268055555555556in"
height="2.811111111111111in"}

Fig 14. Server Assignment Request (SAR)

\[38\] The HSS responds with the* Server Assignment Answer* (SAA) to the
S-CSCF. As it was indicated in the *SAR* that the S-CSCF does not have
user profile, the HSS includes the User-Data AVP in the response. 

![](media/image102.png){width="6.268055555555556in"
height="4.122916666666667in"}

Fig 15. Server Assignment Request (SAA)

The User-Data AVP may contain the following items as is shown below:

-   Private Id

-   Service Profile

-   Public Identity

-   a list of initial Filter Criteria (iFC)

![](media/image103.png){width="5.5in" height="5.552083333333333in"}

Fig 16. User Data in SAA

\[39\] The 200 OK for the SIP *REGISTER *is sent back towards the UE
following the reverse signaling path.

![](media/image104.png){width="6.268055555555556in"
height="2.2430555555555554in"}

Fig 17. 200 OK to SIP EGISTER

NOTE the above message has been captured on the interface between SBC
and P-CSCF as the 200 OK on SGi/Gm interface has been secured using
IPsec.

After successful IMS registration, the UE subscribes to the reg event
package for the public user identity registered at the S-CSCF. The UE
will get notified of a registration status of public identities
belonging to the same user.

![](media/image105.png){width="6.268055555555556in"
height="3.4868055555555557in"}

Fig 18. Subscription for reg event package

\[40\] The UE subscribes to the reg event package by sending *SIP
SUBSCRIBE* towards the S-CSCF.

-   Event: "reg" indicating this is the subscription to the reg event
    package

-   Expires: Validity time period during which this subscription session
    is valid..

![](media/image106.png){width="6.268055555555556in"
height="3.2708333333333335in"}

Fig 19. SIP SUBSCRIBE

\[41\] The P-CSCF forwards the SIP SUBSRIBE to the S-CSCF which is known
to P-CSCF during the registration procedure.

![](media/image107.png){width="6.268055555555556in"
height="3.692361111111111in"}

Fig 20. SIP SUBSCRIBE

\[42-43\] The S-CSCF returns with the 200 OK response and it is
forwarded to the UE following the signaling path.

![](media/image108.png){width="6.268055555555556in"
height="2.017361111111111in"}

Fig 21. 200 OK response to SIP SUBSCRIBE

\[44-45\] The S-CSCF notifies the UE of its current registration status
by sending SIP NOTIFY, which is forwarded to the UE

![](media/image109.png){width="6.268055555555556in"
height="5.053472222222222in"}

Fig 22. SIP NOTIFY

\[46-47\] The UE responds with 200 OK response towards the S-CSCF.

![](media/image110.png){width="6.268055555555556in"
height="1.9388888888888889in"}

Fig 23. 200 OK response to SIP NOTIFY

**REFERENCE**

\[1\] IETF RFC4740, \"Diameter Session Initiation Protocol (SIP)
Application\", Nov 2006

\[2\] IETF RFC3310, \"Hypertext Transfer Protocol (HTTP) Digest
Authentication Using Authentication and Key Agreement (AKA)\", Sep 2002

\[3\] IETF RFC7315, \"Private Header (P-Header) Extension to the Session
Initiation Protocol (SIP) for the 3GPP\", July 2014

\[4\] IETF RFC3329, \"Security Mechanism Agreement for the Session
Initiation Protocol (SIP)\", Jan 2003

\[5\] 3GPP TS 29.228, \"IP Multimedia (IM) Subsystem Cx and Dx
interfaces; Signaling flows and message contents\", v12.3.0, Sep 2014

\[6\] 3GPP TS 29.229, \"Cx and Dx interfaces based on the Diameter
protocol; Protocol details\", v12.6.0, Jun 2015

\[7\] 3GPP TS 24.228, \"Signaling flow for the IP multimedia call
control based on Session Initiation Protocol (SIP) and Session
Description Protocol (SDP)\", v5.15.0, Sep 2006

\[8\] 3GPP TS 33.203, \"3G Security; Access security for IP-based
services\", v12.5.0, Mar 2014

**E2E VoLTE call setup(3/4) - Voice call setup**

  -----------------------------------------------------------------------
  Once the IMS registration is successfully done between the UE and the
  IMS network, the user can make a VoLTE call. Upon request for voice
  call from the user, the VoLTE UE starts SIP signaling with the IMS
  core. The SIP messages are routed based on initial Filter Criteria
  (iFC) in the IMS Core and delivers SDP offer and answer to establish
  media session along with various SIP headers. As a consequence of the
  SIP signaling, a new dedicated EPS bearer is established between the UE
  and the SGW/PGW which is used to transfer voice media. The QoS of this
  new dedicated EPS bearer is defined by the PCC rules generated by the
  PCRF.
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

**Introduction**

While the SIP messages go through the default EPS bearer (QCI=5) towards
the IMS core, the voice media path is established at the front-end NEs
taking the role of IMS Application Level Gateway (IMS-ALG) and IM Access
Gateway based on SDP negotiation. The following diagram shows the
conceptual diagram of IMS-ALG and IMS Access Gateway model specified in
3GPP TS23.228. The IMS-ALG controls media resources and gating functions
of the IM Access Gateway over Iq interface. It acts as a B2BUA and can
modify the SDP and SIP headers of SIP messages if necessary. The IM
Access Gateway executes the allocation and release of transport
addresses, IP versioning and the media gating function under the control
of the IMS-ALG.

+:---------------------------------------------------------------------:+
| ![](media/image111.png){width="4.90625in"                             |
| height="3.5416666666666665in"}                                        |
|                                                                       |
| Fig 1. IMS-ALG and IMS Access Gateway model                           |
+-----------------------------------------------------------------------+

The following diagram shows how the media path is established. Upon
request from the user for voice call setup, the UE sends VoLTE call
setup request (i.e., SIP INVITE) to the IMS core with an SDP offer,
which contains the allocated media information of the originating UE
\[A\]. The IMS-ALG allocates media resource in the IM Access Gateway to
which the originating VoLTE UE can access. The allocated media
information at IM Access Gateway is sent back to the UE in the response
as an SDP answer \[a\]. The IMS-ALG allocates additional media resource
for the upstream, includes it in the SDP offer and sends it towards the
remote IMS-ALG \[B\]. The IMS-ALG in the remote IMS network responds
with the SDP answer containing the media access point of IM Access
Gateway in the same network \[b\]. The IMS-ALG in the remote network
also allocates another media resources and sends it to the UE as an SDP
offer \[C\]. In turn, the UE will also send back the response including
SDP answer of its own \[c\].

NOTE the gray arrow indicates the signaling path and the rest indicate
the media path and its direction.

![](media/image112.png){width="5.177083333333333in"
height="4.052083333333333in"}

  -----------------------------------------------------------------------
  Fig 2. Media path establishment
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

NOTE The IM Access Gateway functionality is typically provided by
Service Border Controller (SBC).

**II. VoLTE call setup procedure**

Upon request from the user for VoLTE call setup, the UE initiates SIP
signaling with the IMS core. The P-CSCF address is informed to the UE
when the UE attaches to the network. The signaling path beyond the
P-CSCF is determined based on a routing mechanism of IMS core. The SDP
negotiation is performed along with the SIP signaling and determines the
media path for voice call setup.

Upon receiving call setup request (i.e., *SIP INVITE*), the P-CSCF
informs the PCRF of the service data flow information. The PCRF triggers
the Evolved Packet Core (EPC) to create a dedicated EPS bearer of QCI=1
for voice media by generating and provisioning PCC rules to the SGW/PGW.
The PCC rules include QoS parameters and rules to be applied to service
data flows based on which the SGW/PGW establishes mapping relations
between service data flows and the EPS bearers.

NOTE Based on GSMA IR.92, the UE is strongly recommended to support the
precondition framework for VoLTE. Please note that, in the following
practice, the precondition procedure has been disabled before testing.
Please refer
to [[FCM.01]{.underline}](http://www.gsma.com/network2020/wp-content/uploads/2014/10/FCM.01-VoLTE-Service-Description-and-Implementation-Guidelines-Version-2.0.pdf), [[IR.92]{.underline}](http://www.gsma.com/newsroom/wp-content/uploads/IR.92-v9.0.pdf) and
3GPP [[TS
24.229]{.underline}](http://www.3gpp.org/DynaReport/24229.htm) for the
detail.

NOTE While the following procedure shows the only originating side, the
same procedure and principles can also be applied to the terminating
side. The signaling procedure handled within the IMS core has not been
described to avoid complexities as it can vary based on the deployment
architecture as per IMS vendor.

![](media/image113.png){width="6.268055555555556in"
height="5.905555555555556in"}

  -----------------------------------------------------------------------
                       Fig 3. VoLTE setup call flow

  -----------------------------------------------------------------------

\[48\] Upon request from the user to make a voice call, the originating
UE sends the SIP *INVITE *towards the P-CSCF.

-   Supported header: a list of option tags indicating supporting
    features. In this example, the \"timer\" and \"100rel\" indicate
    support of session timer and a reliable delivery of the provisional
    response (i.e., 183 Session In Progress), respectively.

-   P-Early-Media header: indicator of whether the UE supports the early
    media mode.

-   Allow header: a list of SIP methods that is supported by the UE.

-   P-Preferred-Identity header: the originating user\'s identity that
    is preferred by the originating user to be used. This header is
    replaced with the P-Asserted-Identity header by the P-CSCF in the
    IMS network. If the SIP message is sent towards untrusted IMS core,
    the P-Asserted-Identity header shall be removed.

-   User-Agent header: VoLTE client information

-   Privacy header: preference of sending UE indicating that any
    sensitive information shall be hidden from any parties that do not
    need to know it.

-   Accept-Contact header: a list of features of target UE preferred by
    the sending UE

-   P-Access-Network-Info header: the radio access technology and cell
    identity.

-   Session-Expires header: a valid period of time of this SIP INVITE
    session. The parameter "uac" indicates that the sending UE will
    refresh the session before the timer is expired.

-   P-Preferred-Service header: service identification user wishes to be
    used. This header is replaced with the P-Asserted-Service header by
    the P-CSCF.

-   Content-Type: media type of the message-body sent to the recipient.

-   Route header: a list of IP addresses of intermediary nodes which the
    SIP request will go through. This would a copy of Service-Route
    header returned in 200 OK response to SIP REGISTER, which is
    inserted by the S-CSCF. The Service-Route header indicates the
    intermediary node associated with that S-CSCF.

-   From header: sending user's SIP URI or TEL URI

-   To header: recipient's SIP URI or TEL URI

-   Call-ID header: a globally unique identifier of the SIP session. All
    the SIP messages of the same session must have the same Call-ID
    value.

-   CSeq header: sequence of the same SIP method. The sequence number is
    incremented as the same SIP method is being sent.

-   Max-Forwards header: maximum number of hops that the message can go
    through.

-   Contact header: the contact address, device capabilities,
    feature-tags, etc. of the sending UE.

-   Via header: a list of SIP addresses of intermediary nodes. The entry
    is inserted by each node that wants to stay in the signaling path
    for the SIP response. The response message for this request
    (e.g., *183 session in progress, 100 Trying, 200 OK,* etc) will be
    transferred to the originating UE following the reverse path listed
    in this header.

-   Content-Length: body length in bytes.

![](media/image114.png){width="6.268055555555556in"
height="3.4472222222222224in"}

  -----------------------------------------------------------------------
  Fig 4. headers in SIP INVITE
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

The SIP *INVITE *contains an SDP offer. The SDP defines media
information of the sending node which contains the contact ip address,
port number and a list of supporting codec information. The following
shows descriptions of each parameters used in SDP.

-   'o' (originator and session identifier):
    \<username\>\<session-id\>\<network type\>\<address type\>\<ip
    address\>

-   's' (session name): any textual session name

-   'c' (connection data): \<network type\>\<address type\>\<connection
    address\>

-   't' (timing): \<start time\>\<stop time\>

-   'm' (media description): \<media type\>\<port\>\<protocol\>\<fmt:
    media format description\>

-   'b' (bandwidth): AS (application specific) -- maximum RTP session
    bandwidth (kbytes), RS -- sending RTCP bandwidth (bytes), RR --
    receiving RTCP bandwidth (bytes)

-   'a=rtpmap' (attributes): \<payload type\>\<encoding name\>\<clock
    rate\>\<encoding parameters\>

-   'a=fmtp'(attributes): format specific parameters related with the
    corresponding media

-   'a=ptime'(attributes): length of time represented by the media in a
    packet (ms)

-   'a=maxptime'(attributes): maximum amount of media that can be
    encapsulated in each packet(ms)

The following is an SDP example included in the SIP *INVITE* captured on
the Gm interface. The UE's IP address is "100.64.63.41" and port number
for audio is "1234", which is depicted as \[A\] in Fig2.

![](media/image115.png){width="6.268055555555556in"
height="3.692361111111111in"}

Fig 5. Attributes in Session Description Protocol (SDP) offer

NOTE Upon receiving the SIP *INVITE* with an SDP offer, the P-CSCF may
send service data information to the PCRF of which flow-status AVP set
to 'DISABLED'. In this case, the P-CSCF will send additional service
data information when it receives the *183 Session In Progress* with SDP
answer. In the following example, the service data information is sent
only once when the P-CSCF obtains SDP offer and answer all together at
step #48.

The P-CSCF responds with a *100 Trying* provisional response. The
provisional response is a one-way response sent back to the originating
side used as informative. It is not necessarily guaranteed for its safe
arrival.

![](media/image116.png){width="6.268055555555556in"
height="1.4736111111111112in"}

Fig 6. Parameters in 100 Trying

\[49\] The terminating UE locally allocates resources, generates
the *183 Session In Progress* along with SDP answer and sends it back
towards the originating UE. The *183 Session In Progress* arrives the
originating S-CSCF following the reverse path of the SIP messages. The
S-CSCF forwards it to the P-CSCF.

-   Record-Route header: a list of IP addresses that is copied from the
    Route header by the terminating UE in the received SIP *INVITE*. The
    value of this header will be reused by the originating UE when it
    composes Route header upon sending subsequent SIP request.

-   Require header: a list of option tags indicating features that needs
    to be supported by the recipient (i.e., the originating UE) of this
    message. In this case, the \"100rel\" indicates the originating UE
    shall support the reliable delivery of provisional response. 

NOTE the provisional response, 1xx, is an informative response therefore
it does not usually require the reliable delivery. However, *183 Session
In Progress* would be an exception as it contains the SDP answer.

-   RSeq header: the sequence number of this response. The value of this
    header is copied to the CSeq header in the following *SIP
    PRACK* sent by the originating UE.

-   P-Asserted-Identity header : the authorized user\'s identity of the
    sending user of this message (i.e., the terminating user)

-   P-Charging-Vector header: a collection of charging information,
    which consists of IMS Charging Identity (ICID) value, the address of
    the SIP proxy that creates the ICID value and the Inter Operator
    Identifiers (IOI). The ICID indicates a globally unique charging
    value that identifies a dialog, the IOI identifies both the
    originating and terminating networks involved in a SIP dialog. In
    the following example, the full text for the header is as follow:

  ---------------------------------------------------------------------------------------------------------------------------------
  icid-value=0.274.195-1418282284.647;term-ioi=32345;term-ioi=22345;icid-generated-at=10.75.0.5;term-ioi=Type3Term;orig-ioi=32345
  ---------------------------------------------------------------------------------------------------------------------------------

  ---------------------------------------------------------------------------------------------------------------------------------

![](media/image117.png){width="6.268055555555556in" height="2.91875in"}

Fig 7. Headers in *183 Session In Progress*

\[50\] Upon receiving the* 183 Session In Progress*, the P-CSCF triggers
the *Authentication and Authorization Request *(AAR) towards the PCRF to
inform the fact that there is a new Application Focus (AF) session being
created. The PCRF performs [[session
binding]{.underline}](http://hongjoo71-e.blogspot.in/2015/06/volte-bearer-binding-and-session-binding.html) between
the AF session and the corresponding IP-CAN session.

NOTE AF indicates an element offering applications that require the
Policy and Charging control of the user plane resources. In this
context, it indicates the P-CSCF.

-   Session-Id AVP: identifier of Rx session for this application. It
    lasts until this application (i.e., VoLTE session) does exist.

-   AF-Application-Identifier AVP: identifier of the VoLTE call session
    assigned by the P-CSCF.

-   Media-Component-Description AVP: media information of the service
    data flow

-   Service-Info-Status AVP: the status of the service information that
    the P-CSCF is providing to the PCRF.

    -   FINAL SERVICE INFORMATION (0): the service has been fully
        negotiated between the two nodes and the provided service
        information is the result of the negotiation.

    -   PRELIMINARY SERVICE INFORMATION (1): the provided service
        information is a preliminary and further negotiation is to be
        needed between two nodes.

NOTE In this example, the value is set to be "FINAL SERVICE INFORMATION"
as the P-CSCF has both SDP offer and answer.

-   AF-Charging-Identifier AVP: identifier for charging correlation with
    bearer layer.

-   Specific-Action AVP: a list of events that P-CSCF wants to be
    informed from the PCRF. The PCRF shall report to the P-CSCF when any
    of these events occurs.

-   Subscription-Id AVP: identifier of the end user's subscription. It
    holds subscription type and data. Multiple instances of the
    subscription-id indicates multiple type of identifiers of the same
    subscriber such as E164, SIP URI, IMSI, etc.

-   Framed-IP-Address AVP: UE's IP address which is allocated by the PGW
    during initial attach procedure.

-   Required-Access-Info AVP: indicator of query by the P-CSCF for
    access network information.

![](media/image118.png){width="6.268055555555556in"
height="5.063194444444444in"}

Fig 8. AVPs in *AAR*

The Media-Component-Description AVP reflects the SDP offer and answer
which includes the media type, direction and codec information.

-   Media-Sub-Component AVP: descriptions for media flows. There are two
    sub components appears in this snapshot, one for RTP and the other
    one for RTCP.

-   Flow-Description AVP: description for IP flow in each direction, of
    which IP addresses and port numbers are copied from the SDP offer
    and answer by the P-CSCF.

    -   Uplink IP flow: UE ("100.64.63,41", "1234") 🡪 SBC
        ("10.75.23.197", "10570")

    -   Downlink IP flow: SBC ("10.75.23.197", "10570") 🡪 UE
        ("100.64.63,41", "1234")

-   Flow-Status AVP: permission status of each media flow.

    -   ENABLED-UPLINK (0): enable associated uplink IP flow(s) only.

    -   ENABLED-DOWNLINK (1): enable associated downlink IP flow(s)
        only.

    -   ENABLED (2): enable all associated IP flow(s)

    -   DISABLED (3): disable all associated IP flow(s)

    -   REMOVED (4): remove all associated IP flow(s)

-   Media-Type AVP: the type of media stream e.g., audio, video, data,
    text, message.

-   Max-Requested-Bandwidth-UL/DL AVP: the Maximum Bit Rate (MBR) of the
    IP flow in each direction. The bandwidth contains all the overhead
    coming from IP layer and the layer above e.g., IP, UDP, RTP, RTP
    payload.

-   RS-Bandwidth AVP: maximum required bandwidth for RTCP sender
    reports.

-   RR-Bandwidth AVP: maximum required bandwidth for RTCP receive
    reports.

-   Codec-Data AVP: codec related information known at the P-CSCF.

![](media/image119.png){width="6.268055555555556in"
height="3.692361111111111in"}

Fig 9. Sub-AVPs of Media-Component-Description AVP

\[51\] Upon receiving the *AAR*, the PCRF generates PCC rules. PCC rules
includes IP flow description for uplink and downlink (i.e., 5-tuple),
QoS information, the flow status, etc. The SGW/PGW performs [[bearer
binding]{.underline}](http://hongjoo71-e.blogspot.in/2015/06/volte-bearer-binding-and-session-binding.html) between
the received PCC rules and the corresponding IP-CAN bearer. The IP flow
shall be mapped to a specific IP-CAN bearer based on these PCC rules by
the SGW/PGW

-   Charging-Rule-Definition AVP: A PCC rule. There are two PCC rules
    showing up for voice call, one for RTP and the other one for RTCP.

-   Charging-Rule-Name AVP: A PCC rule name. It is uniquely defined
    within the same IP-CAN. If the PCC rule is pre-defined in PGW as is
    the case for default EPS bearer, it is uniquely defined within the
    PGW.

-   Flow-Information AVP: a single IP flow packet filter. It includes
    the ip address and port number and the direction of the IP flow.

-   Flow-Status AVP: permission status of each media flow. Refer to
    step#49 for the detail.

-   QoS-Information AVP: QoS information to be applied to the IP flow,
    which includes QoS Class Identifier (QCI), GBR (Guaranteed Bit
    Rate), MBR (Maximum Bit Rate) and ARP (Allocation Retention
    Precedence).

-   QoS-Class-Identifier AVP: QoS Class Identifier

-   Guaranteed-Bitrate-UL/DL AVP: guaranteed for service data flow. The
    bandwidth contains all the overhead coming from the IP-layer and the
    layers above e.g., IP, UDP, RTP and RTP payload.

-   Max-Requested-Bandwidth-UL/DL AVP: the Maximum Bit Rate (MBR) of the
    IP flow in each direction. The bandwidth contains all the overhead
    coming from IP layer and the layer above e.g., IP, UDP, RTP, RTP
    payload.

-   Allocation-Retention-Priority AVP: The priority of allocation and
    retention. When a new media resource is required to be allocated and
    all the resources are already occupied, the PGW can release the
    allocated media resource and re-allocate it for the new IP flow
    based on this value.

-   Precedence AVP: the order of applying the service data flow template
    consisting of service data flow filters to the service data flow at
    PGW.

-   Flows AVP: Indicator of the IP flow to which this PCC rule is to be
    applied.

![](media/image120.png){width="6.268055555555556in"
height="4.886805555555555in"}

Fig 10. AVPs of RAR

\[52\] The SGW/PGW initiates the EPS bearer creation procedure and
responds with the *Re-Auth-Answer* (RAA) to the PCRF.

-   Access-Network-Charging-Address AVP: IP address of the network
    entity within the access network performing charging.

-   3GPP-SGSN-MCC-MNC AVP: MCC and MNC of the access network.

-   3GPP-User-Location-Info AVP: UE's current location. It is composed
    of Tracking Area Identity (TAI) and E-UTRAN Cell Global Identifier
    (ECGI).

![](media/image121.png){width="6.268055555555556in"
height="4.211111111111111in"}

Fig 11. AVPs of RAA

\[53\] The PCRF responds with the *AAA* to the P-CSCF.

![](media/image122.png){width="5.895833333333333in"
height="3.0833333333333335in"}

Fig 12. AVPs of AAA

\[54\] Upon receiving the successful *AAA *from the PCRF, the P-CSCF
continues the SIP signaling by forwarding the *183 Session In
Progress* towards the UE. The following snapshot shows headers of *183
Session In Progress* captured on Gm interface.

-   P-Early-Media header: indicator of whether the UE supports the early
    media mode. The early media option has been disabled in the
    practice.

Refer to step#47 and step#48 for the detailed description for SIP
headers.

![](media/image123.png){width="6.268055555555556in"
height="2.527083333333333in"}

Fig 13. Headers of 183 Session In Progress

The following snapshot shows the SDP answer included in the *183 Session
In Progress*. The SBC is going to be a peer node from UE's perspective.
Given that, the IP address and port number represents the SBC to which
the originating UE shall connect for media. The codec information
represents the one supported by the SBC. Refer to step#47 for the
detailed description for SDP attributes.

![](media/image124.png){width="6.268055555555556in"
height="2.9381944444444446in"}

Fig 14. SDP answer in 183 Session In Progress

The SDP answer delivered to the originating UE shows the IP address is
10.75.23.197 and port number is 10570, which is depicted as \[a\] in
Fig2.

\[55\] The UE confirms that the *183 Session In Progress *with SDP
answer has been received safely by sending SIP *PRACK*.

-   RACK header: the sequence number the corresponding *183 Session In
    Progress* and the SIP *INVITE*.

Refer to step#47 for the detailed description for other headers.

![](media/image125.png){width="6.268055555555556in"
height="1.9388888888888889in"}

Fig 15. Headers in SIP PRACK

\[56\] The *200 OK* response to the SIP *PRACK* is received by the UE.

![](media/image126.png){width="6.268055555555556in"
height="1.4590277777777778in"}

Fig 16. Headers in 200 OK for PRACK

\[57\] The *180 Ringing* provisional response is received by the UE. It
indicates the voice call setup request is being notified to the
recipient. Refer to step#47 and step#48 for the detailed description for
headers.

NOTE If the option tag '100rel' appears in the Require header, the UE
shall acknowledge the provisional response by sending *PRACK*. If it
appears in Supported header, it is just informative.

![](media/image127.png){width="6.268055555555556in" height="2.19375in"}

Fig 17. Headers in 180 Ringing

\[58\] The 200 OK response for the SIP *INVITE* is received by the UE.
It indicates that the terminating user answered the phone. Upon
receiving the response, the UE allocates the media resource. Refer to
step#47 and step#48 for the detailed description for headers.

![](media/image128.png){width="6.268055555555556in"
height="2.5854166666666667in"}

Fig 18. Headers in 200 OK for SIP INVITE

\[59\] The UE sends SIP *ACK* towards the terminating user. Refer to
step#47 for the detailed description for headers.

![](media/image129.png){width="6.268055555555556in"
height="1.6652777777777779in"}

Fig 19. Headers in SIP ACK

***Red Mouse***

REFERENCES

\[1\] 3GPP TS 23.228, \"IP Multimedia System (IMS); Stage 2\", v11.4.0,
Mar 2012

\[2\] 3GPP TS 24.229, \"IP multimedia call control protocol based on
Session Initiation Protocol (SIP) and Session Description Protocol
(SDP); stage3\", v11.3.0, Mar 2012

\[3\] 3GPP TS 24.628, \"  \", v11.3.0, Mar 2012

\[4\] 3GPP TS 29.212, \"Policy and Charging Control (PCC); Reference
points\", v12.6.0, Sep 2014

\[5\] 3GPP TS 29.214, \"Policy and Charging Control over Rx reference
point\", v12.5.0, Sep 2014

\[6\] IETF RFC7315, \"Private Header (P-Header) Extension to the Session
Initiation Protocol (SIP) for 3GPP\", July 2014

\[7\] IETF RFC4028, \"Session Timer in the Session Initiation Protocol
(SIP)\", Apr 2005

\[8\] IETF RFC3264, \"A offer and answer model with the Session
Description Protocol (SDP)\", Jun 2002

\[9\] IETF RFC3262, \"Reliability of the Provisional Responses in
Session Initiation Protocol (SIP)\", Jun 2002

\[10\] IETF RFC3608, "Session Initiation Protocol (SIP) Extension Header
Field for Service Route Discovery During Registration", Oct, 2003

**E2E VoLTE call setup(4/4) - dedicated EPS bearer creation**

  -----------------------------------------------------------------------
  While SIP signaling is in progress in VoLTE call setup, a dedicated EPS
  bearer is created for voice media transfer. The dedicated EPS bearer
  for voice is temporary one as it lasts only during the voice media
  session which is different from the default EPS bearer in that the
  default EPS bearer is persistent until the UE is detached from the LTE.
  The creation of dedicated EPS bearer is triggered by the P-CSCF sending
  service data information (i.e., *AAR*) to the PCRF. Once the dedicated
  EPS bearer is created for voice, there comes two EPS bearer created
  between the UE and the IMS APN, i.e., a default EPS bearer for SIP
  signaling and a dedicated EPS bearer for voice media. On top of this,
  there can be more dedicated EPS bearers created with different PCC
  rules and QoS according to service types.
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

**I. Introduction**

The P-CSCF converts the media information in the SDP into the service
data information and sends it to the PCRF. The PCRF performs session
binding between IP-CAN session and the Application Session, generates
PCC rules and provisions them to the SGW/PGW. The SGW/PGW requests to
the MME the creation of dedicated EPS bearer using the received PCC
rules. The SGW/PGW also performs bearer binding between PCC rules and
the to-be-created IP-CAN bearer. The creation of dedicated EPS bearer
procedure is composed of sequential procedures of creating uplink S1
bearer, DRB (Data Radio Bearer) and downlink S1 bearer across UE, eNB
and SGW/PGW.

NOTE the S5 interface between SGW and PGW is not depicted in the
following practice for simplicity.

**II. Creation of a dedicated EPS bearer for voice traffic**

The following scenario shows the procedure of creating a dedicated EPS
bearer during VoLTE call setup.

![](media/image130.png){width="5.802083333333333in"
height="7.104166666666667in"}

  -----------------------------------------------------------------------
                   Fig 1. dedicated EPS bearer creation

  -----------------------------------------------------------------------

\[59\] The SGW/PGW generates its own GTP-U TEID and initiates the
procedure to create a dedicated EPS bearer by sending *Create Bearer
Request* (CBR) to the MME. The *CBR* contains Bearer Context information
of the dedicated EPS bearer to be created.

-   (Linked) EPS Bearer ID: Indicate the default bearer associated with
    the PDN connection.

-   Bearer Context: a set of information for dedicated EPS bearer to be
    created which contains EPS Bearer ID, Bearer TFT, GTP-U TEID and
    Bearer QoS.

-   EPS Bearer ID : a requested EPS bearer ID to be created and shall be
    set to \'0\' at this stage.

-   Bearer TFT : the uplink packet filters to be sent all the way down
    to the UE and applied by the UE when the UE sends out RTP and RTCP
    packet.

-   SGW GTP-U TEID : the identifier of the SGW as an end point of the
    GTP-U tunnel.

-   Bearer QoS : QoS for this dedicated EPS bearer which includes UL/DL
    MBR, UL/DL GBR and QCI.

![](media/image131.png){width="6.268055555555556in"
height="4.358333333333333in"}

  -----------------------------------------------------------------------
  Fig 2. IEs in Create Bearer Request
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

\[60\] Upon receiving the *CBR*, the MME allocates the EPS bearer ID and
requests the UE to activate the dedicated EPS bearer by
sending *Activate dedicated EPS bearer context request *towards the
UE*. *The message is delivered to the UE being contained in the *E-RAB
Setup request* and the *RRC Downlink Direct Transfer* over S1AP and RRC
interfaces respectively. The *E-RAB Setup request* contains SGW GTP-U
TEID and the E-RAB level QoS parameters e.g., ARP, UL/DL MBR, UL/DL GBR,
etc.

-   e-RAB ID: unique identifier of the E-RAB for the UE. Please note
    that the E-RAB ID='5' was for the default EPS Beaer with the
    Internet APN, '6' was for default EPS bearer with the IMS APN and
    now, it is set to be '7'.

-   e-RAB level QoS Parameters: QoS to be applied to an E-RAB, which
    contains QCI, ARP, MBR and GBR of the E-RAB. This is a copy of the
    received Bearer level QoS at step #59.

-   SGW GTP-TEID: the identifier of the SGW at the end of GTP-U tunnel.

![](media/image132.png){width="6.268055555555556in"
height="4.6715277777777775in"}

Fig 3. IEs in E-RAB Setup Request

  

The following snapshot shows the *Active dedicated EPS bearer context
request* contained in the Non-Access-Stratum (NAS) PDU container.

-   EPS QoS: QoS of an EPS bearer context which includes QCI, MBR and
    GBR of the EPS bearer

-   Traffic Flow Template (TFT): the uplink packet filters to be sent
    all the way down to the UE and applied by the UE when it sends RTP
    and RTCP packet.

-   Linked Transaction Identifier (TI): the identifier of the active PDP
    context from which PDP address for the new PDP context could be
    derived.

-   Negotiatiated QoS: QoS of a PDP context

  

![](media/image133.png){width="6.268055555555556in"
height="2.517361111111111in"}

Fig 4. IEs in Activate dedicated EPS bearer context request

Upon receiving the *E-RAB Setup request*, the eNB allocates the required
resources and establishes uplink S1 bearer with the SGW as part of the
E-RAB establishment.

\[61-62\] The eNB sends the *RRC Connection Reconfiguration request* to
the UE. The UE modifies the radio bearer accordingly and responds with
the *RRC Conenction Reconfiguration Complete*.

\[63\] The eNB responds with the the *E-RAB Setup response* to the MME
and it contains eNB GTP-U TEID which is allocated by the eNB.

-   E-RAB ID: unique identifier of the E-RAB for one UE. This value is
    originally assigned by the MME and if this is already occupied, the
    UE can change it.

-   eNB GTP-U TEID: the identifier of the eNB at the end of GTP-U
    tunnel. The eNB newly assigns the GTP-U TEID for this dedicated EPS
    bearer and it is delivered to the SGW via MME.

  

![](media/image134.png){width="6.268055555555556in"
height="5.182638888888889in"}

Fig 5. IEs in E-RAB Setup Response

\[64\] The UE responds with the *Activate dedicated EPS bearer context
response* to the MME which is wrapped in the RRC* Uplink Direct
Transfer* and S1AP *Uplink NAS Transport *on RRC and S1AP interfaces
respectively.

-   E-UTRAN Cell Group Identifier (CGI): globally unique identifier of a
    cell (PLMN ID + ECI)

-   Tracking Area Identifier (TAI): globally unique identifier of a
    tracking area \[PLMN ID + TAC\]

![](media/image135.png){width="6.268055555555556in"
height="3.995833333333333in"}

Fig 6. IEs in Activate dedicated EPS bearer context response

  

\[65\] The MME responds to the SGW/PGW by sending *Create Bearer
Response*. The *Create Bearer Response* contains the eNB GTP-U TEID
which was received at step #63. Upon receiving the *Create Bearer
Response*, the SGW establishes downlink S1 bearer towards the eNB.

![](media/image136.png){width="6.268055555555556in" height="3.54375in"}

Fig 7. IEs in Create Bearer Response

**II. PDN connectivity and EBI allocation**

The following shows the summary of all the procedures shown in the VoLTE
call setup procedures, in which steps (1) to (4) are performed at the
background automatically.

(1)    UE turend on.

(2)    PDN connection with the Internet APN: the QCI of the default EPS
bearer = '9', EBI = '5'.

(3)    PDN connection with the IMS APN: the QCI of the default EPS
bearer = '5', EBI = '6'.

(4)    IMS registration through the default EPS bearer with IMS APN.

(5)    The dedicated EPS bearer creation for voice upon request for
VoLTE service: the QCI of the default EPS bearer = '1', EBI = '7'.

+:---------------------------------------------------------------------:+
| ![](media/image137.png){width="5.208333333333333in"                   |
| height="2.9583333333333335in"}                                        |
|                                                                       |
| Fig 8. PDN connection and EBI allocation                              |
+-----------------------------------------------------------------------+

***Red Mouse***

**REFERENCES**

\[1\] 3GPP TS25.331, \"Radio Resource Network (RRC); Protocol
specification\", v12.3.0, Sep 2014

\[2\] 3GPP TS24.301, \"Non-Access-Stratum (NAS) protocol for Evolved
Packet System (EPS); Stage3\", v12.4.0, Mar 2014

\[3\] 3GPP TS24.008, \"Mobile radio interface Layer 3 specification;
Core network protocols; Stage3\", v13.4.0, Dec 2015

\[4\] 3GPP TS29.274, \"3GPP Evolved Packet System (EPS); Evolved General
Packet Radio Service (GPRS); Tunneling Protocol for Control Plane
(GTPv2-C); Stage3\", v13.0.0, Dec 2014

\[5\] 3GPP TS36.331, \"Evolved Universal Terrestrial Radio Access
(E-UTRA); Radio Resource Control (RRC); Protocol specification\",
v12.3.0, Sep 2009

\[6\] 3GPP TS36.413, \"Evolved Universal Terrestrial Radio Access
Network (E-UTRAN); S1 Application Protocol (S1AP)\", v12.3.0, Sep 2014

**VoLTE : UE initiated voice call release**

When the VoLTE call session does exist, either one of users engaged in
the call can release the call session by sending SIP *BYE *towards the
IMS network in a normal case. The user\'s request comes to the IMS
network and it makes a chain reaction from the IMS network to EPC and to
the UE. The P-CSCF informs the release of the AF session (i.e., SIP
session) to the PGW via the PCRF and the PGW initiates the release of
allocated resources for that application. The following scenario shows
the case where the user requested to end the voice call session.

![](media/image138.png){width="6.268055555555556in"
height="6.501388888888889in"}

\[1-2\] Upon request from the user, the UE sends SIP *BYE *towards the
IMS network to release the existing SIP session.

-   [Call-ID header]{.underline} is a globally unique identifier of this
    SIP session. In this context, it will identify the SIP session to be
    released.

-   [Route header]{.underline} is a list of IP addresses of intermediary
    nodes which stays in the signaling path.

-   [P-Preferred-Identity header]{.underline} indicates the originating
    user\'s identity that is preferred by the user to be used.

-   [P-Access-Network-Info header]{.underline} includes the radio access
    technologies and cell id.

\[3\] The P-CSCF sends *Session-Terminating-Request *(STR) to inform the
PCRF that the established session shall be terminated over Rx, which
combines the AF session and the IP-CAN session. As a result of this
procedure, the session binding between the AF session and the IP-CAN
session is terminated.\
\
\[4\] The PCRF requests to remove the corresponding PCC rule by sending
the *Re-Auth-Request* (RAR) containing the Charging-Rule-Remove AVP to
the PGW. In this example, there are two charging rules to be removed for
RTP and RTCP as the voice media session is to be released.

![](media/image139.png){width="6.268055555555556in"
height="3.2493055555555554in"}

\[5-6\] The PGW unbinds the PCC rules from the corresponding EPS bearer
and responds with the *Re-Auth-Answer *(RAA) to the PCRF. The PCRF
unbinds the AF session from the corresponding IP-CAN and responds with
the *Session-Termination-Answer* (STA) to the P-CSCF.\
\
\[7\] The PGW sends the *Delete Bearer Request* containing the EPS
Bearer Id (EBI) towards the MME.\
\
\[8\] The MME requests the eNB to deactivate the EPS bearer context by
sending *Deactivate EPS bearer context request*, which is wrapped by
the *E-RAB Release Command* and *RRC Downlink Direct Transfer* over S1AP
and RRC respectively.

![](media/image140.png){width="6.268055555555556in"
height="4.358333333333333in"}

Upon receiving the *E-RAB Release Command, *the eNB releases allocated
resources on Uu and S1 for the corresponding E-RAB(s).\
\
\[9-10\] The eNB sends the *RRC Connection Reconfiguration request* to
release the radio bearer. The UE releases allocated resources on Uu.\
\
\[11-12\] The UE responds with the* Deactivate EPS bearer Context
accept* to the MME and the eNB responds with the *E-RAB Release
Response* to the MME.\
\
\[13\] Upon receiving the *E-RAB Release Response*, the MME updates the
ECM and EMM state of the UE and sends *Delete Bearer Response* to the
SGW/PGW. The SGW/PGW releases allocated resources on S1 and S5.

**VoLTE: Service Request scenario in IDLE mode**

The IDLE state is defined as the state when both RRC state (i.e., eNB
and UE signaling connection state) and ECM state (i.e., NAS signaling
connection state) are IDLE while the EMM state maintained by the MME is
still REGISTERED. This indicates that the UE is logically attached to
the LTE network but the physical connection and the corresponding
resources have been released from the UE up to the SGW (i.e., DRB and S1
bearer). The UE may fall into the IDLE mode when there hasn\'t been any
activities for a while between the UE and the LTE network or when it is
regarded the UE connection is lost.\
\
In order to transfer any data to the UE in the IDLE mode, the MME has to
wake up the UE in the first place so the UE can reconnect to the
network. While reconnecting to the network, the UE and the network shall
recover required resources and connections over RRC, S1AP and S1
interfaces. Once the EPS bearer is recovered, the data buffered in the
SGW can be transferred to the UE. The following shows the conceptual
sequence of the data transfer to the UE in the IDLE mode.

  -----------------------------------------------------------------------
  ![](media/image141.png){width="5.0625in" height="2.2916666666666665in"}
  -----------------------------------------------------------------------
      Fig 1. Conceptual diagram of network initiated service request

  -----------------------------------------------------------------------

**\
I. Network Initiated Service Request**

The following flow shows the detailed procedure of how the application
payload is delivered to the UE in the IDLE mode. As a precondition, the
UE stays in the IDLE mode and the payload (i.e., SIP Message) has
arrived at SGW.

  -----------------------------------------------------------------------
            ![](media/image142.png){width="4.967361111111111in"
                       height="9.693055555555556in"}
  -----------------------------------------------------------------------
        Fig 2. VoLTE call flow - network initiated service request 

  -----------------------------------------------------------------------

\[1\] Upon receiving the data when there is no available S1 bearer at
the moment as the UE is in IDLE mode, the SGW sends the *Downlink Data
Notification* (DDN) to the MME to request for paging the UE. The DDN
includes the EPS Bearer ID (EBI) stored in the EPS bearer context of the
bearer on which the downlink data packet was received over S5
interface.\
\
\[2\] The MME acknowledges the request by sending *Downlink Data
Notification Acknowledge.*\
\
\[3\] The MME initiates the paging procedures by sending PAGING message
to each eNB that serves cells belonging to the tracking area in which UE
is registered.\
\
The following shows paging messages distributed across multiple eNBs
that belong to the target TA List.

![](media/image143.png){width="6.268055555555556in" height="3.36875in"}

NOTE As the paging procedure itself can cause heavy traffic in the air,
the MME may need to have an optimized paging scheme to minimize the
side-effect. After having been awaken, the UE performs RRC connection
establishment procedure with the eNB from which the paging was sent.\
\
\[4\] Once the RRC connection is established, the UE requests the
network to establish NAS Signaling connection, radio connection and S1
bearers by sending *Service Request *towards the MME. The *Service
Request* is delivered wrapped in *RRC Connection Complete* and *Initial
UE Message* on RRC and S1AP interfaces. The RRC state transits from the
RRC-Idle to RRC-Connected.

![](media/image144.png){width="6.268055555555556in"
height="2.752083333333333in"}

\[5\] The MME requests to establish the E-RAB connection by sending
the *Initial Context Setup Request* to the eNB.

-   [UE-AMBR]{.underline} indicates the maximum aggregated bit rate for
    non-GBR bearers for the concerned UE.

-   [E-RAB To Be Setup Item]{.underline} includes the E-RAB information
    for each EPS bearers to be setup. 

In this example, there are three E-RABs to be setup which is the list of
non-GBR bearers. Each E-RAB information contains the E-RAB ID, ARP and
the SGW GTP-U TEID.

![](media/image145.png){width="6.268055555555556in"
height="4.122916666666667in"}

Upon receiving the *Initial Context Setup Request*, the eNB executes the
E-RAB configuration and creates UE context based on the received
parameters. In the meantime, the MME may perform the security setup
procedure with the UE for integrity protection and ciphering of
signaling data.\
\
\[6-7\] The eNB requests the UE to establish the DRB by sending *RRC
Connection Reconfiguration*. Once the DRB is established successfully,
the UE responds with the *RRC Connection Reconfiguration Complete *to
the eNB.\
\
\[8\] After the DRB is successfully established, the eNB responds with
the *Initial Context Setup Response* to the MME. The ECM state transits
from ECM-Idle to ECM-Connected.

-   [E-RAB Setup List ]{.underline}is a list of E-RABs that has been
    successfully established, which contains each E-RAB ID and eNB GTP-U
    TEID.

-   [E-RAB Failed Setup List]{.underline} is a list of E-RABs that has
    failed to establish.

![](media/image146.png){width="5.104166666666667in"
height="3.6979166666666665in"}

\[9\] The MME requests the SGW to resume the suspended S1 bearer by
sending the *Modify Bearer Request*. If there were multiple APNs to
which the UE was connected before falling into IDLE state, there can be
multiple *Modify Bearer Request* sent, one for each APN.\
\
The Bearer Context IE contains the EBI and the eNB GTP-U TEID with which
the SGW will establish the S1 bearer towards the eNB. In this example,
there are two EBIs one for the default EPS bearer and the other one for
dedicated EPS bearer.

![](media/image147.png){width="5.697916666666667in"
height="4.541666666666667in"}

\[10\] The SGW responds with the *Modify EPS bearer response* containing
the resulting cause value for each requested EBI. The Bearer Context IE
contains the EBIs and the SGW GTP-U TEID which is the same value that
was contained in the *Initial Context Setup Request* at step #5. 

![](media/image148.png){width="5.697916666666667in"
height="4.302083333333333in"}

Once the S1 bearer is recovered, the SGW starts sending buffered data
towards the UE. This procedure happens seamlessly without necessarily
user interaction.\
\
\
**II. UE Initiated Service Request**\
In the same way, the UE may initiate the service request procedure in
the IDLE to perform the VoLTE call initiation or location update
procedures in the IDLE mode.

![](media/image149.png){width="5.78125in" height="4.020833333333333in"}

\[1-10\] Same as \[4-10\] in the figure 2. During this procedure, the
RRC connection and NAS signaling connection is re-established. The UE
context is recovered in MME. The EPS bearer including DRB and the S1
bearer is also re-established.\
\
\[11-12\] The UE may trigger the TAU procedure by sending *Tracking Area
Update* (TAU) request following the criteria as defined in TS23.401.
The *TAU* contains the UE\'s current *Tracking Area Identifier* (TAI)
and the ECGI. The last visited TAI is included if the UE has a valid TAI
of the last visited tracking area and used by the MME to make a good
list of TAI(i.e., TAL) for the UE. The TAL is contained in the TAU
Accept.

![](media/image150.png){width="6.268055555555556in"
height="4.642361111111111in"}

Please refer to \"[*[VoLTE: Tracking Area Update and Combined
Attach]{.underline}*](http://hongjoo71-e.blogspot.kr/2015/07/volte-tracking-area-update-and-combined.html)\"
for the detail.\
\
\
Once the EPS bearer is recovered, the UE is able to initiate a voice
call setup procedure by sending SIP INVITE. If there is no service data
flow for a while, the UE and the network may again fall into the IDLE
state.

\*\*\*

In order to optimize the transactions between the UE and the network,
the eNB shall be optimized as to criteria based on which the UE state
falls into the IDLE mode. Furthermore the MME shall also provide the
optimized scheme for paging schedules considering user experiences. If
the paging scheme (i.e., timer values) is too loose, it will aggravate
user experiences. If it is too frequent, it will cause heavy traffic in
the air.

***Red Mouse***

REFERENCES\
\
\[1\] 3GPP TS29.274, \"3GPP Evolved Packet System (EPS); Evolved General
Packet Radio Services (GPRS) Tunneling Protocol for Control Plane
(GTPv2-C); stage 3\", v13.0.0\
\[2\] 3GPP TS36.413, \"Evolved Universal Terrestrial Radio Access
Network (E-UTRAN); S1 Application Protocol (S1AP)\", v12.3.0\
\[3\] Netmanias, \"LTE EMM and ECM States\", Sep 2013

**E2E VoLTE call flow : detach (UE-initiated)**

The UE initiated detach procedure may occur when the UE is turned off or
the UE needs to fall back from EPS services to non-EPS services or vice
versa. Along with the detach procedure all the allocated resources are
released and connections for signaling and bearer are disconnected.

![](media/image151.png){width="4.822916666666667in"
height="3.1458333333333335in"}

The above figure shows the overall sequence of how the UE and the
network releases related resources when the UE detaches. Upon receiving
the detach request from the UE(1), the MME releases the EPS bearer
context towards the S/PGW(2) and in turn, the bearer binding and the
session binding is released over Gx and Rx(3,4). Apart from this
procedure, the MME also releases the UE context towards the eNB(5) and
the eNB releases RRC connection with the UE(6). Meanwhile, the IMS
network is informed of bearer release from the PCRF and proceeds the
release procedure of the SIP session(7).

**I. EPS bearer release**

  -----------------------------------------------------------------------
            ![](media/image152.png){width="5.291666666666667in"
                       height="5.135416666666667in"}
  -----------------------------------------------------------------------
               Fig 1. Detach procedure - EPS bearer release

  -----------------------------------------------------------------------

\[1\] The UE triggers the detach procedure from the LTE network by
sending *Detach Request* towards the MME.

-   [Detach Type IE]{.underline} indicates the reason of detach
    procedure and where the UE is being detached from (i.e., EPS
    services only, non-EPS services only, both). In this example, the UE
    is being detached from the LTE network due to switch-off.

-   [EPS mobile identity IE]{.underline} is set to be GUTI when the UE
    has a valid GUTI. If the UE does not have the valid GUTI, the EPS
    mobile identity will be the IMSI.

The GUTI is a globally unique identifier of the UE. It is composed of
the M-TMSI, PLMN-ID (MCC+MNC) and MMEI (MMEGI+MMEC). The M-TMSI is
assigned by the MME when the UE attaches to the network and remain
unchanged until the UE detaches from the network. The following shows
the GUTI format and the sample message of *Detach Request*.

![](media/image153.png){width="5.03125in" height="0.6875in"}

![](media/image154.png){width="6.268055555555556in"
height="4.632638888888889in"}

If it is the detach for EPS only or combined EPS/IMSI detach, the MME
deactivates the EPS bearer context(s) for this UE locally and enter the
state EMM-DEREGISTERED for this UE.

\[2-3\] The MME requests the S/PGW to delete the corresponding session
by sending *Delete Session Request*. If there are multiple APNs that the
UE was attached to, there will be multiple *Delete Session
Request, *one* *for each APN. The message contains the list of EBIs to
be deleted for each APN. In case of detach, all the EBIs belong to that
APN shall be included.\
\
Upon receiving the *Delete Session Request*, the SGW/PGW deactivates the
EPS bearer context corresponding to the received EBIs of this UE. The
bearer binding relation between EPS bearer and PCC rule is also
released. The SGW/PGW responds with the *Delete Session Response*.\
\
\[4\] The MME sends *Detach Accept* only if the Switch off parameter is
not \"Switch off\". Otherwise, this transaction will be spared.\
\
\[5\] The MME performs MME-initiated UE context release by sending *UE
Context Release Command* to the eNB, which is to release the
UE-associated logical connection. In this case, the message contains the
cause value of \"Detach\". Upon receiving the *UE Context Release
Command*, the eNB releases all related signaling and user data transport
resources for the indicated UE by the UE S1AP ID.

![](media/image155.png){width="4.041666666666667in" height="2.5625in"}

\[6-7\] The eNB sends the *RRC Connection Release* to the UE. In case
the RRC connection has not been released already, the *RRC Connection
Release* will be sent as an Acknowledge Mode(AM). After releasing the
RRC connection, the UE responds with the *RRC Connection Release
Complete*.\
\
NOTE Whether to use Acknowledge Mode (AM) or UnAcknowledge Mode(UM) is
dependent on the requirements for the radio bearer such as packet loss,
packet delay, etc. The basic difference between the UM and AM is that
the UM would be compared with the UDP where re-transmission control is
not provided, whereas the AM is more likely TCP. The detail for this
technology may need to be referred to the radio expert.\
\
\[8\] The eNB responds with the* UE Context Release Complete* to the MME
and releases the S1 signaling connection. This step would be performed
without necessarily waiting for the *RRC Connection Release
Complete* from the UE. Upon receiving the *UE Context Release Complete*,
the MME deletes any eNB related information.\
\
\
**II. IMS de-Registration**\
\
Once the GTP-C, S1-MME connection and the corresponding S1 bearers have
been released, the network starts to release remaining resources and
connections towards upstream.

  -----------------------------------------------------------------------
            ![](media/image156.png){width="6.268055555555556in"
                       height="5.435416666666667in"}
  -----------------------------------------------------------------------
            Fig 2. Detach procedure - application level release

  -----------------------------------------------------------------------

\[9-10\]  The PGW reports the event to the PCRF by
sending *Credit-Control-Request*(CCR*)*. The *CCR *contains the cause
value set to be \"TERMINATION-REQ\". The \"TERMINATION-REQ\" is sent
only when the IP-CAN session is terminated, i.e., detach. If there are
multiple APNs to which the UE attaches, there will be
multiple *CCRs *sent to the PCRF, one for each APN. The PCRF
acknowledges with the *Credit-Control-Answer*(CCA*)*.

![](media/image157.png){width="6.268055555555556in" height="3.4375in"}

\[11-12\] Upon receiving the *CCR *from the PGW containing the IP-CAN
session termination event, the PCRF releases session binding relation
between IP-CAN session and the corresponding AF-session and requests to
release the Rx session by sending *Abort Session Termination* (ASR) to
the P-CSCF. The message contains the Abort-cause value of
\"BEARER_RELEASED\". The PCRF acknowledges with the *Abort Session
Answer* (ASA).

![](media/image158.png){width="6.268055555555556in"
height="2.154861111111111in"}

\[13\] Upon receiving the *CCR *containing the cause value of \"BEARER
RELEASED\", the P-CSCF performs de-registration procedure by sending
the *SIP REGISTER* to the I-CSCF in the UE\'s home network with its
Expires header set to zero. The P-CSCF performs a name-address
resolution mechanism for P-Visited-Network-ID header to determine the
address of the home network.

![](media/image159.png){width="6.268055555555556in"
height="3.261111111111111in"}

\[14\] The I-CSCF requests the registration state of the received Public
User Identity to the HSS by sending
the *User-Authentication-Request*(UAR*)* with its
User-Authorization-Type set to \"DE_REGISTRATION\". The *UAR* contains
the Public User Identity, Private User Identity, Visited Network Id,
etc.

![](media/image160.png){width="6.268055555555556in"
height="2.9381944444444446in"}

\[15\] The HSS determines if the user is currently registered and
responds with the *User-Authentication-Answer*(UAA) with the
corresponding S-CSCF name (i.e., Server-Name AVP). 

\[16\] The I-CSCF determines the address of the S-CSCF through the
name-address resolution mechanism and sends the *SIP REGISTER* to that
S-CSCF.

\[17-18\] Upon receiving the* SIP REGISTER*, the S-CSCF may trigger the
3rd-party de-Registration procedure towards the application server based
on the iFC mechanism. On the other hand, the S-CSCF sends
the *Server-Assignment-Request*(SAR*)* towards the HSS. In this example,
the Server-Assignment-Type AVP is set to
\"USER_DEREGISTRATION_STORE_SERVER_NAME\", which indicates that the give
Public User Identity is no longer considered as registered and the HSS
needs to keep the S-CSCF name after this action. 

![](media/image161.png){width="6.268055555555556in"
height="2.595138888888889in"}

\[19-20\] The 200 OK for the *SIP REGISTER* is sent towards the P-CSCF.\
\
\[21\] The S-CSCF may send the *SIP NOTIFY *towards the UE to inform
that the subscription has terminated. The body of the *SIP
NOTIFY* includes the fact that the registration state has also been
terminated. This *SIP NOTIFY* transaction is correlated with the
subscription procedure that was done when the UE registered to this IMS
network.

![](media/image162.png){width="6.268055555555556in"
height="3.8881944444444443in"}

\*\*\*

When it comes to IMS de-registration, it is supposed to happen before
LTE attach in a normal situation and it would be a quite natural
sequence considering the protocol stack. The UE shall release all the
resources relating to applications before it detaches from the network.
However, in this example, the UE performs LTE detach first and then the
IMS Core initiates the IMS de-registration based on the bearer loss
event reported from the PGW. This type of exceptional situation happens
more often than not in reality. It can come from incomplete
implementation of the VoLTE client in a UE or the UE might not be able
to perform IMS de-registration for some reasons.

***Red Mouse***

REFERENCES\
\
\[1\] 3GPP TS24.301, \"Non-Access Stratum (NAS) protocol for Evolved
Packet System (EPS); Stage 3\", v12.4.0, Mar 2014\
\[2\] 3GPP TS29.274, \"3GPP Evolved Packet System (EPS); General Radio
Packet Service (GPRS) Tunneling Protocol for Control Plane (GTPv2-C);
Stage 3\", v9.3.0, Jun 2014\
\[3\] 3GPP TS23.401, \"General Radio Packet Service (GPRS) enhancements
for Evolved Universal Terrestrial Radio Access Network (E-UTRAN)
access\", v12.4.0, Mar 2014\
\[4\] 3GPP TS23.228, \"IP Multimedia System (IMS); stage2\", v11.4.0,
Mar 2012\
\[5\] 3GPP TS29.229, \"Cx and Dx interfaces based on the Diameter
Protocol; Protocol details\", v12.6.0, Jun 2015\
\[6\] 3GPP TS36.413, \"Evolved Universal Terrestrial Radio Access
Network (E-UTRAN); S1 Application Protocol (S1AP)\", v13.0.0, Jun 2015

\[7\] Netmanias, \"EMM Procedure 2. Detach\", Jan 2014

**Bearer level event and VoLTE call setup failure**

The application layer needs to be aware of bearer level status as the
EPS bearer is tightly coupled with the application session and some
events in an EPS bearer can affect the application session handling and
resource management. For instance, when the VoLTE call session is about
to be established, the IMS core establishes the logical connection with
the UE. Meanwhile, the EPS will prepare for the EPS bearer through which
signaling and payload will flow. If the EPS bearer is disconnected
somehow (e.g., due to connection loss, user inactivity), the IMS core
needs to be informed of it so the corresponding application session
shall be handled accordingly. The PCC architecture handles the binding
relations between the application session, PCC rules and the EPS bearers
as is described in \"[[Bearer binding and Session
binding]{.underline}](http://hongjoo71-e.blogspot.kr/2015/06/volte-bearer-binding-and-session-binding.html)\".\
\
The following diagram shows the Policy and Charging Control (PCC)
architecture that controls the EPS bearer related QoS policies and is
used to request the bearer level event reporting and deliver the bearer
events to application layer.

  -----------------------------------------------------------------------
            ![](media/image163.png){width="6.268055555555556in"
                      height="2.5854166666666667in"}
  -----------------------------------------------------------------------
                          Fig 1. PCC architecture

  -----------------------------------------------------------------------

\[1\] Upon receiving the request for voice call (i.e., SIP INVITE), the
P-CSCF triggers the *Authentication-and-Authorization Request* (AAR)
towards the PCRF containing the service information like
source/destination ip addresses and ports, codec information, etc.
The *AAR* also accommodates the list of events that the P-CSCF wants to
be informed of.\
\
\[2-3\] The PCRF generates the PCC rule for this application session and
sends *Re-Authorization Request* (RAR) which contains the PCC rules.\
\
\[4\] The EPC binds the received PCC rules and the EPS bearers so it can
map the IP flow to the corresponding EPS bearer.\
\
\[5\] When there is an event occurred that corresponds one of events
listed in the received parameters, the P-GW reports the event to the
PCRF by sending the *Credit-Control Request* (CCR) towards the PCRF.\
\
\[6\] The PCRF unbinds the AF session from the IP-CAN and sends
the *Re-Authentication Request* (RAR) or the* Abort-Session
Request* (ASR) to the P-CSCF reporting the occurred event. Upon
receiving the *RAR* or *ASR*, the P-CSCF may release or update the
application session by sending appropriate error response to end
points.\
\
NOTE Refer to procedures described in \"*[[Voice Call
Setup]{.underline}](http://hongjoo71-e.blogspot.kr/2015/08/e2e-volte-call-flow-34-voice-call-setup.html)\"* and
\"[*[dedicated EPS bearer
creation]{.underline}*](http://hongjoo71-e.blogspot.kr/2015/08/e2e-volte-call-flow-44-dedicated-eps.html)\"
for the detail.\
\
The following flow shows the voice call setup procedure where the voice
session is about to establish but fails due to the error event occurred
in the EPS bearer.

![](media/image164.png){width="5.78125in" height="8.020833333333334in"}

NOTE The step #1 to step #8 follows the normal procedure for VoLTE call
setup as described in \"[*[dedicated EPS bearer
creation]{.underline}*](http://hongjoo71-e.blogspot.kr/2015/08/e2e-volte-call-flow-44-dedicated-eps.html)\".

\[1-2\] While VoLTE call setup procedure, the P-CSCF receives the
SIP *INVITE* and *183 Session In Progress* with SDP offer and SDP
answer, respectively.\
\
\[3\] The P-CSCF triggers the binding procedure by sending *AAR *towards
the PCRF. The *AAR *includes the list of events that it wants to be
informed of.

![](media/image165.png){width="6.268055555555556in"
height="2.076388888888889in"}

\[4-6\] The PCRF sends the PCC rule to the SGW/PGW so it can enforce the
rule for the incoming IP flow. The SGW/PGW binds the received PCC rules
with an EPS bearer and responds with the *RAA* towards the PCRF and in
turn, the PCRF responds with the *AAA* towards the P-CSCF.\
\
\[7-8\] The SGW/PGW initiates the EPS bearer creation procedure by
sending the *Create Bearer Request* towards the MME. The MME request to
activate the EPS bearer by sending *Activate EPS bearer context
request *towards the eNB. The *E-RAB Setup request* over S1AP interface
which delivers the NAS message to the eNB includes the list of E-RAB to
be setup.\
\
\[9\] Upon receiving the *AAA* from the PCRF, the P-CSCF proceeds the
call setup procedure by sending the *183 Session In Progress* which
contains the SDP answer.\
\
\[10\] In this example, the eNB responds with the error response with
its cause value set to \"multiple-E-RAB-ID-instances\" which is the case
when the eNB receives the same E-RAB ID as the one that already does
exist.

![](media/image166.png){width="6.268055555555556in"
height="3.8291666666666666in"}

Skimming over the trace history on S1AP interface, there was an attempt
to delete the E-RAB but failed due to a problem in a radio interface,
which is followed by X2 handover several times. It is suspected that the
MME might have deleted the E-RAB ID anyway without considering the
failure response and later on, re-assigned the same value for E-RAB in
the *E-RAB Setup Request* while the eNB is still maintaining the value
as the E-RAB release procedure has failed.

![](media/image167.png){width="6.268055555555556in"
height="3.2708333333333335in"}

\[11\] The MME rejects the request for bearer creation by sending
the *Create Bearer Response* to the SGW/PGW with its cause value set to
\"No resource available\".

![](media/image168.png){width="6.268055555555556in"
height="2.477777777777778in"}

\[12\] The MME also initiates the E-RAB release procedure for the
concerned E-RAB ID.

![](media/image169.png){width="4.65625in" height="3.3645833333333335in"}

\[13\] Meanwhile, the SGW/PGW may internally revoke the bearer binding
and informs the bearer event to the PCRF by sending *CCR* with its
Charging-Rule-Report AVP set to RESOURCE_ALLOCATION_FAILURE.

![](media/image170.png){width="6.268055555555556in"
height="3.467361111111111in"}

\[14\] The PCRF informs the P_CSCF of the received bearer event by
sending *ASR* with its Abort-cause AVP set to BEARER_RELEASED in this
example. The *ASR* is sent when all the service data flows regarding the
AF session are deleted. Otherwise, the PCRF would send RAR.

![](media/image171.png){width="6.268055555555556in"
height="2.3409722222222222in"}

\[15-16\] The P-CSCF responds with the *ASA* and the PCRF with *CCA*.\
\
\[17, 21\] Upon receiving the event report indicating the bearer
release, the P-CSCF abort the call processing by sending the *503
Service Unavailable*. The UE responds with the SIP *ACK* and releases
all the resources regarding this application session.\
\
\[18-19\] The P-CSCF sends the Session-Termination-Request towards the
PCRF indicating that the application session has been terminated.\
\
\[20\] The eNB responds to the *E-RAB Release Command* by sending
the *E-RAB Release Response* towards the MME.

***Red Mouse***

REFERENCES\
\
\[1\] 3GPP TS 29.213, \"Policy and Charging Control signalling flows and
Quality of Services (QoS) parameter mapping\", v12.3.0, Mar 2014\
\[2\] 3GPP TS 29.214, \"Policy and Charging Control over Rx reference
point\", v13.2.0, June 2015\
\[3\] TS 36.413, \"Evolved Universal Terrestrial Radio Access Network
(E-UTRAN); S1 Application Protocol (S1AP)\", v13.0.0, June 2015

**X2 handover**

Handover is a process for a UE to transfer its sessions from the current
network to another one while it is moving towards a neighbor cell. So,
the handover procedure ends up with a new connection between the UE and
the new eNB. The intra E-UTRAN handover indicates the case where the SGW
and/or MME is not relocated whereas the inter E-UTRAN handover is the
case where the SGW and/or MME shall be relocated. In this post, the
intra E-UTRAN will be described.\
\
It is a serving eNB that determines whether to initiate the handover
procedure or not based on measurement reports received from the UE
periodically. When handover is to happen, the serving eNB also chooses
the target eNB from the list of neighbor eNBs and the type of handover,
i.e., X2 handover or S1 handover. If there is an established X2
connection with the target eNB and it is available at the moment, the
source eNB performs X2 handover. Otherwise the eNB will perform the S1
handover.

**I. Overall scenario**

The X2 handover procedure involves signaling transactions among two eNBs
and the MME. The following diagram shows the conceptual flow of X2
handover procedure.

  -----------------------------------------------------------------------
  ![](media/image172.png){width="5.520833333333333in" height="2.78125in"}
  -----------------------------------------------------------------------
                   Fig 1. overall scenario - X2 handover

  -----------------------------------------------------------------------

\(1\) UE periodically sends measurement reports to the source eNB.\
(2) The source eNB determines X2 handover and requests X2 handover to
the target eNB. The target eNB establishes uplink S1 bearer with the
same SGW with which the source eNB has been connected. The source eNB
establishes a direct tunnel with the target eNB.\
(3) UE handover is successfully performed. Hencefortjh, the buffered
media is transferred to the UE from the target eNB.\
(4) The target eNB informs the SGW of the fact that the handover has
been completed successfully. The SGW establishes downlink S1 bearer with
the target eNB.\
(6) The SGW switches the media path from the source eNB to the target
eNB and releases the old S1 bearer.

**II. X2 handover flow**

  -----------------------------------------------------------------------
            ![](media/image173.png){width="4.655555555555556in"
                       height="9.693055555555556in"}
  -----------------------------------------------------------------------
                       Fig 2. X2 handover call flow

  -----------------------------------------------------------------------

\[1\] The UE periodically sends a measurement report to the serving eNB.
This reporting mechanism is intended for the UE to find out the best
cell to communicate with the network. The measurement report may contain
the list of neighbor cells, their signal strength and its current
condition.\
\
\[2\] Based on the received report, the serving eNB determines whether
the handover is required and if it is required, the serving eNB selects
a target eNB among the list of neighbor eNBs with which X2 connection is
established. The source eNB requests the target eNB to prepare for
handover by sending *Handover Request*. The message contains the target
Cell ID and the UE Context. The following shows some of parameters
included in the UE Context.

-   *UE-AMBR* indicates aggregated maximum bit rate for all the bearers
    of the UE.

-   *E-RABsToBeSetupList* indicates a list of radio access bearer. Each
    E-RAB is defined by E-RAB ID and corresponding QoS parameters like
    ARP, QCI, GBR, etc.

-   *UL GTP TEID* indicates the SGW endpoint of the S1 bearer for
    delivery of uplink packets. It is delivered to the target eNB so the
    target eNB can establish the UL S1 bearer with the same SGW as like
    the source eNB. 

Upon receiving the *Handover Request*, the target eNB allocates required
resources to proivde the same quality of service to the UE as the source
eNB. The required resources will include resources for RRC to
communicate with the UE and resources for S1 bearer to communicate with
the SGW. Additionally, the target eNB also allocates a new DL GTP TEID
that will be delivered to the source eNB in step#3 and used for direct
GTP Tunnel between two eNBs.

\[3\] The target eNB informs the source eNB about the prepared resources
by sending *Handover Request Acknowledge*.

-   *E-RABs Admitted List* contains the list of E-RABs for which the
    resources have been allocated. It also contains the DL GTP TEID that
    identifies the X2 transport bearer that shall be used by the source
    eNB to forward the downlink packets towards the target eNB.

-   *E-RABs Not Admitted List* contains the list of E-RABs for which
    resources won\'t be allocated.

-   *Target eNB to source eNB transparent container* is used by the
    target eNB to deliver the message to the UE through the source eNB
    transparently. In this case, it contains the *Handover
    Command *which is a command to the UE for handover execution.

Upon receiving the acknowledgement, the source eNB establishes the X2
direct tunnel with the target eNB. Henceforth, the traffic received by
the eNB is forwarded to the target eNB and will be buffered until the UE
handover is completed.\
\
\[4\] The source eNB requests the UE to reconfigure the RRC connection
by sending *RRC Connection Reconfiguration, *which also
contains *Handover Command* that was received from the target eNB.

-   *C-RNTI (Cell Radio Network Temporary Identifier)* is a temporary UE
    identifier assigned by the serving eNB. It is persistent while the
    UE is connected to that eNB and re-assigned whenever the serving eNB
    changes.

-   *DRB-ID (Data Radio Bearer Identifier)* is an identifier of the data
    bearer between UE and the eNB to be established with the target
    eNB. 

Upon receiving the *Handover Command*, the UE executes handover from the
current eNB to the target eNB.\
\
\[5\] The source eNB informs the target eNB of the current status of
packet transmitter and receiver by sending *SN Status Transfer*. The
message includes the uplink/downlink PDCP SN and HFN.

-   *PDCP(Packet Data Convergence Protocol) SN* indicates the sequence
    number assigned for each packet data unit.

-   *HFN (Hyper Frame Number)* is used to limit the actual number of
    sequence number bits that\'s needed to be sent over the radio. When
    the PDCP SN reaches the maximum value, the PDCP SN is restarted from
    zero and HFN is incremented by one. This value shall be synchronized
    between the UE and the eNB.

\[6\] After the UE has successfully synchronized to the target cell, it
sends a target eNB a *Handover Confirm* informing that the handover has
been completed. The buffered data at the target eNB is forwarded to the
UE through the DRB. The uplink data from the UE can also be sent
hereafter.\
\
\[7\] The target eNB creates the S1 eNB GTP TEID and sends the MME
the *Path Switch Request* to inform that the UE has changed the cell.

-   *ECGI (E-UTRAN Cell Global Identifier)* is a globally unique cell
    identifier to which the UE is camping on.

-   *TAI (Tracking Area Identity)* is a globally unique tracking area
    identifier.

-   *E-RAB to be switched *indicates the list of EPS bearers to be
    switched.

-   *S1 eNB GTP TEID* indicates the end point of the GTP Tunnel that
    will be used by the SGW to identify the target eNB.

![](media/image174.png){width="5.947916666666667in"
height="4.333333333333333in"}

\[8\] Upon receiving the *Path Switch Request*, the MME requests the SGW
to modify EPS bearers by sending *Modify Bearer Request *per PDN
connection. The *Modify Bearer Request* contains the list of EPS bearers
to be modified.

![](media/image175.png){width="6.268055555555556in"
height="2.154861111111111in"}

The PGW may need to inform the PCRF of the fact that the UE\'s location
has been updated based on the request from the PCRF when the Gx session
was established. Refer to \"[[Bearer level event and VoLTE call setup
failure]{.underline}](http://hongjoo71-e.blogspot.kr/2015/09/bearer-level-event-and-volte-call-setup.html)\"
for basic understanding as to how the bearer level event reporting
mechanism is realized within the PCC architecture.\
\
\[9\] The SGW establishes the downlink S1 bearer with the target eNB and
responds with the *Modify Bearer Response*, which includes the list of
successfully modified EPS bearers.

![](media/image176.png){width="6.268055555555556in"
height="2.3722222222222222in"}

\[10\] The SGW acknowledges the target eNB by sending Path Switch by
sending Path Switch Acknowledge.

\[11\] The target eNB informs the source eNB that the handover has been
completed successfully by sending *UE Context Release*. Upon receiving
the *UE Context Release*, the source eNB releases all the resources
associated with the received UE context.

\*\*\*

As a result of X2 handover, the UE context that was maintained by the
source eNB is moved to the target eNB. The UE\'s location will be
updated (e.g., ECGI, TAI) and the UE\'s C-RNTI will be re-assigned by
the target eNB. The target eNB shall also assign a new eNB S1AP UE ID
which will be updated at MME. The S1 bearer between the SGW and the
source eNB will be replaced by another S1 bearer between the same SGW
and the target eNB, which requires updates of eNB S1 GTP-U TEID. The
PCRF may need to update UE\'s location.\
\
Please note that all these changes does not affect the existing VoLTE
session. All the EPS bearers being used to transfer VoLTE signaling and
data moves to the target eNB. In case there is an existing voice media
session, the voice data arriving at the source eNB while the UE handover
is in progress will be transferred to the target eNB through the direct
tunnel between two eNBs and buffered at the target eNB. The buffered
data is eventually transferred to the UE when the handover is completed.
Assuming that the handover takes less than a few milliseconds, the user
won\'t notice a voice cracking.

***Red Mouse***

REFERENCES\
\
\[1\] GPP TS23.401, \"General Packet Radio Service (GPRS) enhancement
for Evolved Universal Terrestrial Radio Access Network (E-UTRAN)
access\", v12.4.0, Mar 2014\
\[2\] 3GPP TS36.423, \"Evolved Universal Terrestrial Radio Access
Network (E-UTRAN); X2 application protocol (X2AP)\", v13.1.0, Sep 2015\
\[3\] 3GPP TS25.331, \"Radio Resource Control (RRC) Protocol
specification\", v10.0.0, Jun 2010\
\[4\] 3GPP TS36.331, \"Evolved Universal Terrestrial Radio Access
Network (E-UTRAN); Radio Resource Control (RRC) Protocol
specification\", v12.7.0, Sep 2015\
\[5\] 3GPP TS25.323, \"Packet Data Convergence Protocol (PDCP)
specification (release 9)\", v9.0.0, Dec 2012\
\[6\] 3GPP TS36.300, \"Evolved Universal Terrestrial Radio Access
(E-UTRA) and Evolved Universal Terrestrial Radio Access Network
(E-UTRAN); Overall description; Stage 2\", v10.0.0, Jun 2010\
\[7\] EventHelix.com, \"[[LTE X2 handover sequence
diagram]{.underline}](https://www.eventhelix.com/lte/handover/x2/lte-x2-handover-sequence-diagram.htm#.VhERzfntmko)\",
20th Apr 2013\
\[8\] Netmannias, \"[[EMM Procedure 6. Handover over without TAU -
Part2. X2
handover]{.underline}](http://www.netmanias.com/en/post/techdocs/6257/emm-handover-lte/emm-procedure-6-handover-without-tau-part-2-x2-handover)\",
Mar 21th 2014

**VoLTE S1 Handover preparation (1/3)**

While UE crosses the border towards the neighborhood cell, the source
eNB determines whether there needs a handover based on the received
measurement report from the UE. When there is no established X2
connection with the target eNB, the source eNB determines to perform S1
handover. In this post, the handover preparation phase will be
addressed. The handover preparation procedure includes the determination
of handover by the eNB, handover request by the MME, the allocation of
required resources and establishing the indirect data forwarding tunnels
among NEs.

**I. Indirect Data Forwarding Tunnel**

S1 handover is different from the X2 handover in that the media is
anchored by the SGW under the control of MME rather than by eNB. During
the S1 handover, a temporary indirect data forwarding tunnel is
established between two eNBs via the common SGW. All the media arriving
at the source eNB while S1 handover is in progress, which can be uplink
data from UE side or the downlink data from the network side, will be
re-directed to the target eNB through this indirect data forwarding
tunnel and buffered at the target eNB. When the S1 handover is
completed, the buffered media at the target eNB is transferred to the
UE. The following diagram shows Indirect Data Forwarding Tunnel
established between the source eNB and target eNB anchored by the common
SGW during S1 handover procedure.

![](media/image177.png){width="4.958333333333333in"
height="3.6041666666666665in"}

Figure 1. Indirect Data Forwarding Tunnel in S1 handover

**II. S1 handover preparation**

As a precondition of this practice, the UE has PDN connections with the
internet APN and IMS APN and there are three EPS bearers established in
total with EPS bearer ID of '5', '6' and '7' and the relocation of
SGW/PGW does not occur. The S1 handover procedure is triggered by the
source eNB. The MME controls establishing the Indirect Data Forwarding
Tunnel by intermediating required data between two eNBs like Bearer
Context. The Bearer Context contains EPS bearer ID and their GTP-U TEIDs
corresponding to each EPS bearers. The SGW anchors the media transfer
between source eNB and the target eNB. As the SGW and two eNBs are
involved in the media control, they allocate the required media
resources, generate their own GTP-U TEIDs and establishes S1 bearer and
indirect data forwarding tunnels based on the GTP-U TEID of the peer
node delivered via MME.

![](media/image178.png){width="5.5in" height="7.354166666666667in"}

Figure 2. S1 handover procedure - preparation

\[1\] The UE periodically sends a measurement report to the serving eNB.
This reporting mechanism is intended for the UE to find out the best
cell to communicate with the network. The measurement report may contain
the list of neighbor cells, signal strength, current condition, etc.

\[2\] Based on the received report, the serving eNB determines whether
the handover is required and if it is required, the serving eNB selects
a target eNB among the list of neighbor eNBs. If there is no X2
connection with the target eNB, the source eNB performs S1 handover and
sends *Handover Required* to the serving MME requesting to prepare for
resources at the target. 

-    MME UE S1AP ID: Unique identifier of the UE association over the S1
    within the MME

-   eNB UE S1AP ID: Unique identifier of the UE association over the S1
    within the eNB

-   Handover Type: The type of triggered handover in the source side
    (i.e., intraLTE, LTEtoUTRAN, LTEtoGERAN, UTRANtoLTE, GERANtoLTE)

-   Cause: A reason for a particular event for the S1AP. In this
    practice, the value "Handover Desirable for Radio Reasons" indicates
    that the cause is related with radio. Refer to section
    9.2.1.3 *Cause* of \[TS36.413\] for the detail.

-   Target ID: The target eNB for the handover. It is composed of
    "Global eNB ID" and "selected TAI". The Global eNB ID is composed of
    PLMN ID (MCC+MNC) and macro eNB-ID identifying the specific eNB of a
    certain operator in a certain country. The selected TAI uniquely
    identifies the target Tracking Area i.e., PLMN ID + TAC, identifying
    a specific tracking area that is served by that eNB.

-   Source to Target Transparent Container: Information elements created
    by the source eNB and transmitted to the target eNB, which contains
    the RRC related information, E-RAB information, Target Cell-ID and
    UE History Information as shown in the following bullets.

-   RRC Container: RRC Information used by the target eNB during
    handover preparation including UE capability information. Refer to
    "HandoverPreparationInformation" in section 10.2.2 "Message
    definitions" of TS36.331 for the detail.

-   e-RABInformationList: The list of eRAB to be handed over. The E-RAB
    ID identifies a radio access bearer for a particular UE, which makes
    the E-RAB ID unique over one S1 connection. The
    "dL-Forwarding-proposed" indicates that the source eNB proposes the
    list of E-RABs for forwarding of data. In this practice, there are
    three E-RABs (i.e., E-RAB ID='5','6' and '7') proposed and they
    actually represent existing E-RABs of the source eNB. If the target
    eNB accepts it in the *Handover Request Acknowledge*, the downlink
    data received by the source eNB during the handover will be
    forwarded to the target eNB through the indirect data forwarding
    tunnel.

-   Target Cell ID: Globally unique cell identifier. It is composed of
    PLMN ID and Cell ID.

-   UE-HistoryInformation: The list of cells that a UE has been served
    by in the active state prior to the target cell.

![](media/image179.png){width="3.7263888888888888in"
height="9.693055555555556in"}

Figure 3. Handover Required

\[3\] the MME initiates the procedure by sending the *Handover
Request* to the target eNB requesting to prepare for resources for
handover.

-    MME UE S1AP ID: refer to step#2.

-   Handover Type: refer to step#2.

-   Cause: refer to step#2.

-   UE-AMBR: Aggregated maximum bit rates per UE being applicable for
    Non-GBR bearers.

-   E-RAB to be SetupList: A list of E-RAB to be setup where each item
    contains E-RAB ID, Transport Layer Address, GTP-TEID and E-RAB level
    QoS parameters as addressed in the following bullets.

-   E-RAB ID: Refer to step#2

-   The Transport Layer Address : IP address of the source eNB.

-   The GTP-TEID : The GTP Tunnel Endpoint Identifier of the SGW towards
    the source eNB. This has been known to the MME during the initial
    attach of the UE and used by the source eNB to maintain the S1
    bearer with the SGW. Now, the MME intends to take this to the target
    eNB to replace the existing S1 bearer in the end.

-   E-RAB Level QoS Parameters indicates the QoS to be applied to the
    corresponding E-RAB. It is composed of QCI and ARP. Refer to the
    section 9.2.1.60 "Allocation of Retention Priority" in TS36.413 for
    the detail.

-   Source to Target Transparent Container: Information elements created
    by the source eNB and transmitted to the target eNB. Refer to
    step#2.

-   UESecurityCapabilities: Supported algorithms for encryption and
    integrity protection in the UE.

-   HandoverRestrictionList: Roaming or access restrictions for
    subsequent mobility action for which the eNB provides information
    about the target of the mobility action towards the UE.

-   SecurityContext: Security related parameters to the eNB which are
    used to derive security keys for user plane traffic and RRC
    signaling messages and to generate security parameters for the
    current S1 handover. 

![](media/image180.png){width="2.9381944444444446in"
height="9.693055555555556in"}

Figure 4. Handover Request

\[4\] The target eNB allocates all the necessary resources for the
admitted E-RABs and establishes uplink S1 bearer with the SGW. The
target eNB creates its own GTP TEID for S1 bearers which will be
delivered to the SGW later and used by the SGW to establish the downlink
S1 bearer (SGW🡪target eNB), thereby replaces that the source eNB. The
uplink and downlink GTP-TEID for each admitted E-RABs are also included.
These DL/UL GTP-TEIDs are used for indirect media transfer. The target
eNB responds with the *Handover Request Acknowledge* to the MME.

-   MME UE S1AP ID: refer to step#2.

-   eNB UE S1AP ID: refer to step#2.

-   E-RAB Admitted List: The list of E-RAB for which the target eNB
    admitted to establish. This is composed of E-RAB ID, GTP-TEID, UL/DL
    GTP-TEIDs and the Transport Layer for each Admitted Item as
    addressed in the following bullets.

-   E-RAB ID : Refer to step#2.

-   GTP-TEID indicates GTP Tunneling Endpoint Identifier of the target
    eNB which will replace the corresponding GTP-TEID of the source eNB
    in the end (i.e., downlink S1 bearer).

-   The DL/UL GTP-TEIDs indicate the Tunneling Endpoint Identifiers of
    the target eNB for Indirect Data Forwarding Tunnels. The following
    diagram shows the GTP TEID for indirect data forwarding dedicated
    for one E-RAB.

-    Target to Source Transparent Container: Information element that is
    used to transparently pass radio related information from the
    handover target to the handover source through the MME.
    The *Handover Command* is transparently delivered to the source eNB.

  

![](media/image181.png){width="4.158333333333333in"
height="9.693055555555556in"}

Figure 5. Handover Request Acknowledge

\[5\] Upon receiving the *Handover Request Acknowledge*, the MME sends
the *Create Indirect Data Forwarding Tunnel Request* to the SGW, which
contains the Bearer Context for each bearer which was received at step
#4 from the target eNB. The Bearer Context represents the attributes of
each bearer including bearer identifier and TEIDs as below:

-   EPS Bearer ID : Identifier of EPS bearer to be established.

-   eNB F-TEID for DL data forwarding: GTP Tunneling Endpoint Identifier
    created by the target eNB for downlink data forwarding. Refer to
    step#4 

-   eNB F-TEID for UL data forwarding: GTP Tunneling Endpoint Identifier
    created by the target eNB for uplink data forwarding. Refer to
    step#4 

  

![](media/image182.png){width="3.9180555555555556in"
height="9.693055555555556in"}

Figure 6. Create Indirect Data Forwarding Tunnel Request

\[6\] Upon receiving the *Create Indirect Data Forwarding Tunnel
Request*, the SGW establishes the Indirect Data Forwarding Tunnel
towards the target eNB using the received DL/UL eNB F-TEIDs. The SGW
allocates its own UL/DL F-TEID for indirect data forwarding tunnel,
which is delivered to the source eNB via MME at step #7. The SGW
responds to the MME with the *Create Indirect Data Forwarding Tunnel
Response* which contains the Bearer Context of the SGW.

-   Cause : Indicates if the Indirect Data Forwarding Tunnel has been
    created in the SGW. Refer to section 7.2.19 "Create Indirect Data
    Forwarding Tunnel Response" of TS29.274 for the detail.

-   EPS Bearer ID : refer to step #5.

-   SGW F-TEID for DL data forwarding: GTP Tunneling Endpoint Identifier
    created by the SGW for downlink data forwarding.

-   SGW F-TEID for UL data forwarding: GTP Tunneling Endpoint Identifier
    created by the SGW for uplink data forwarding.

  

![](media/image183.png){width="3.7395833333333335in"
height="9.693055555555556in"}

Figure 7. Create Indirect Data Forwarding Tunnel Response

\[7\] The MME sends the *Handover Command* to the source eNB informing
that resources for handover has been prepared at the target eNB. Upon
receiving the *Handover Command*, the source eNB establishes Indirect
Data Forwarding Tunnel towards the SGW using the received E-RAB Subject
to Data Forwarding List, i.e., DL/UL GTP-TEIDs for each E-RAB.

-   MME UE S1AP ID: refer to step#2.

-   eNB UE S1AP ID: refer to step#2.

-   Handover Type: refer to step#2.

-   E-RAB Subject to Data Forwarding List : The list of E-RAB items to
    be used for indirect data forwarding. Each E-RAB Data Forwarding
    Item identifies the E-RAB context of each E-RAB and it consists of
    E-RAB ID, DL/UL GTP-TEIDs as addressed below.

-   E-RAB ID: Refer to step #2.

-   DL/UL GTP-TEIDs : Tunneling End Point Identifier of the SGW created
    and delivered at step #6 for the Indirect Data Forwarding Tunnel.

-   Target To Source Transparent Container: Radio related information
    transparently delivered to the source eNB through the MME. It was
    created by the target eNB and sent to the MME at step #4.

![](media/image184.png){width="4.495138888888889in"
height="9.693055555555556in"}

Figure 8. Handover Command

***Red Mouse***

**REFERENCES**

\[1\] 3GPP TS25.331, \"Radio Resource Network (RRC); Protocol
specification\", v12.3.0, Sep 2014

\[2\] 3GPP TS24.301, \"Non-Access-Stratum (NAS) protocol for Evolved
Packet System (EPS); Stage3\", v12.4.0, Mar 2014

\[3\] 3GPP TS24.008, \"Mobile radio interface Layer 3 specification;
Core network protocols; Stage3\", v13.4.0, Dec 2015

\[4\] 3GPP TS29.274, \"3GPP Evolved Packet System (EPS); Evolved General
Packet Radio Service (GPRS); Tunneling Protocol for Control Plane
(GTPv2-C); Stage3\", v13.0.0, Dec 2014

\[5\] 3GPP TS36.331, \"Evolved Universal Terrestrial Radio Access
(E-UTRA); Radio Resource Control (RRC); Protocol specification\",
v12.3.0, Sep 2009

\[6\] 3GPP TS36.413, \"Evolved Universal Terrestrial Radio Access
Network (E-UTRAN); S1 Application Protocol (S1AP)\", v12.3.0, Sep 2014

**VoLTE S1 handover execution (2/3)**

S1 handover preparation procedure includes the decision of S1 handover
by the source eNB, allocation of network resources to establish Indirect
Data Forwarding Tunnel among two eNBs and common S-GW and establishment
of uplink S1 bearer from the target eNB to the S-GW. Once the S1
handover preparation procedure is completed, the MME initiates the S1
handover by sending *Handover Command* to the UE via the source eNB. The
UE executes the handover by detaching from the source eNB and attaching
to the target eNB. Meanwhile, the downlink data is forwarded to the
target eNB and buffered while the UE handover is in progress. Lastly,
the UE informs the target eNB of the fact that the handover has been
successfully completed and thereafter, the buffered data and downlink
data is forwarded the UE through the target eNB. 

![](media/image185.png){width="5.34375in" height="5.541666666666667in"}

Figure 1. S1 handover procedure - execution

\[8\] The *Handover Command* received from the MME is wrapped by the
source eNB within the *RRC Connection Reconfiguration *and sent to the
UE. The *RRC Connection Reconfiguration *is the message to perform
logical, transport and physical channel configurations. In this case, it
is used to send NAS signaling to the UE to reduce the latency. Upon
receiving the *Handover Command*, the UE detaches from the source eNB
and performs handover to the target eNB.

\[9\] The source eNB stops assigning PDCP-SNs to downlink packets and
sends the *eNB Status Transfer* to the target eNB via MME that contains
uplink and downlink PDCP-SN and HFN (Hyper Frame Number) for each
respective E-RAB. This procedure is initiated by the source eNB at the
moment when it considers the transmitter/receiver status to be frozen.
The use of PDCP-SN and HFN is part of overflow control mechanism for
radio. The PDCP-SN is the serial number of PDCP packets increasing up to
MAX-PDCN-SN. If the number reaches the MAX-PDCP-SN, the HFN is
incremented by one. 

-   Subject to Transfer Items: contains uplink/downlink PDCP-SN and HFN
    for each respective E-RAB.

-   E-RAB ID: Identifies a radio access bearer for a particular UE. This
    value remains the same after S1-handover.

-   uL-/dL-Count value: contains the PDCP-SN and HFN values

-   Received Status of UL PDCP SDUs: indicates the missing and the
    received uplink SDUs (Service Data Units) for each bearer for which
    the source eNB has accepted the request from the target eNB for
    uplink forwarding.

  

![](media/image186.png){width="5.717361111111111in"
height="9.693055555555556in"}

Figure 2. eNB Status Transfer

\[10\] The MME forwards the received PDCP-SN and HFN information to the
target eNB by sending *MME Status Transfer*. Upon receiving the *MME
Status Transfer*, the target eNB does not deliver any uplink packet
whose PDCP-SN is lower than the value received in the PDCP-SN in the
uL-COUNT value. The target eNB uses the received PDCP-SN in the dL-COUNT
value for the first downlink packet for which no PDCP-SN is assigned
yet. The downlink traffic received by the source eNB is routed to the
target eNB following the *Indirect Data Forwarding Tunnel*.

\[11\] After the UE successfully synchronized with the target cell, it
sends a *Handover Confirm *to the target eNB. The *Handover Confirm* is
contained in the *RRC Connection Reconfiguration Complete* message on
RRC. Please note that, at this moment, there is no direct S1 bearer
established yet between S-GW and the target eNB. Therefore, the downlink
data is sent to the source eNB and forwarded to the target eNB following
the Indirect Data Forwarding Tunnel. The uplink data from the UE will be
forwarded to the S-GW following the direct S1 interface.

***Red Mouse***

**REFERENCES**

\[1\] 3GPP TS25.331, \"Radio Resource Network (RRC); Protocol
specification\", v12.3.0, Sep 2014

\[2\] 3GPP TS23.401, "General Packet Radio Service (GPRS) enhancements
for Evolved Universal Terrestrial Radio Access Network (E-UTRAN)
access", v12.4.0, Mar 2014

\[3\] 3GPP TS36.331, \"Evolved Universal Terrestrial Radio Access
(E-UTRA); Radio Resource Control (RRC); Protocol specification\",
v12.3.0, Sep 2009

\[4\] Blog, "[[How LTE Stuff Works?: RRC Connection
Reconfiguration]{.underline}](http://howltestuffworks.blogspot.kr/2011/10/rrc-connection-reconfiguration.html)",
Oct 2011

**VoLTE S1 handover completion (3/3)**

After the UE confirms the completion of the S1 handover in a new cell,
the target eNB initiates the completion procedure by sending towards the
network. The completion procedure involves the SGW and PGW replacing the
downlink S1 bearer from the source eNB to the source eNB releasing the
UE associated resources and lastly, the release of Indirect Forwarding
Tunnels by the SGW.

![](media/image187.png){width="5.614583333333333in"
height="4.541666666666667in"}

Figure 1. S1 handover procedure - complete

\[12\] The target eNB sends the *Handover Notify* to the MME notifying
that the UE has been identified in the target cell and S1 handover has
been completed.

-   E-UTRAN CGI: globally identifies a cell and composed of PLMN
    identity and Cell identity.

-   TAI: uniquely identify a Tracking Area and composed of PLMN identity
    and TAC (Tracking Area Code). 

![](media/image188.png){width="6.125in" height="5.34375in"}

Figure 2. Handover Notify

\[13\] The MME sends the *Modify Bearer Request* to the SGW requesting
to switch the media path from the source eNB to the target eNB. The
switch of media path from the SGW is done by updating the S1 bearer
tunneling end point.

-   Indication: includes various application flags. Refer to section
    7.2.7 "Modify Bearer Request" in \[TS 29.274\].

-   Bearer Context: identifies the bearer to be modified. It is composed
    of EPS Bearer ID and S1 eNB F-TEID sub elements.

In this practice, there are three bearers, i.e., bearer id = 5,6,7. The
bearer 5 and 6 belongs to the internet APN, meanwhile the bearer 7
belongs to the IMS APN. The MME sends multiple Modify Bearer Request for
each APN.

Note that in the following message, the value of F-TEID is set to
0x018088ed. This value is the one that was sent by the target eNB in
step \[4\] *Handover Request Acknowledge* where it represents the
tunneling end point of the target eNB for the downlink S1 bearer. Now,
the MME deliver this value to the S-GW so the S-GW can use this value as
a new target end point for the media path. As such, the downlink media
path on S1 bearer is switched from the source eNB to the target eNB.

![](media/image189.png){width="5.804166666666666in"
height="9.693055555555556in"}

Figure 3. Modify Bearer Request for bearer 7

The following message shows the *Modify Bearer Request* for the bearer 5
and 6. In the same as described in the above, the value of F-TEID is set
to 0x018008ed and 0x018048ed for bearer 5 and 6, respective. They are
the same values as were sent by the target eNB in step \[4\] *Handover
Request Acknowledge* where they represent tunneling end points of the
target eNB for the downlink S1 bearer.

![](media/image190.png){width="4.238888888888889in"
height="9.693055555555556in"}

Figure 4. Modify Bearer Request for bearer 5 and 6

Note that the *Modify Bearer Request* is also sent by the SGW to the PGW
which is not depicted here. The SGW and PGW are logically separated but
in many cases, they are deployed on the same platform.

\[14\] The *Modify Bearer Response* sent from the PGW to the SGW and
from the SGW to the MME.

-   Cause: indicates the result of modifying the requested bearer.

-   Bearer Context: identifies the bearer that has been modified. It is
    composed of EPS Bearer ID, Cause and S1 eNB F-TEID sub elements.

Note that in the following message, the value of F-TEID is set to
0x005b8422. This value is the one that was sent by the MME to the target
eNB in step \[3\] *Handover Request *where it represents the tunneling
end point of the SGW for the uplink S1 bearer. The tunneling end point
values of SGW is created when the UE attaches the network at the very
beginning. Upon S1 handover, the MME sends this value to the target eNB
and the target eNB establishes uplink S1 bearer to the SGW using this
value. At this moment, the source eNB also has uplink S1 bearer
connection with the SGW with the same tunneling end points. As both
source eNB and target eNB can send traffic to the SGW, there is no
change that the data sent by the UE gets lost during handover procedure.

Now, the SGW sends this TEID to the MME for the downlink S1 bearer
informing the tunneling end point for the downlink S1 bearer.

![](media/image191.png){width="6.177083333333333in" height="8.65625in"}

Figure 5. Modify Bearer Response for bearer 7

The same principal is applied to the following message which is for
bearer 5 and 6.

![](media/image192.png){width="4.252083333333333in"
height="9.693055555555556in"}

Figure 6. Modify Bearer Response for bearer 5 and 6

\[15\] The MME requests the release of UE-associated S1 logical
connections over S1 interface by sending *UE Context Release Command*.
The source eNB releases its resources related to the given UE.

-   UE S1AP ID Pair: contains the UE S1AP identifiers. It is composed of
    MME UE S1AP ID and eNB UE S1AP ID

-   Cause: indicates the reason for this command. Refer to section
    9.2.1.3 "*Cause*" in TS36.413 for the detail.

![](media/image193.png){width="6.166666666666667in" height="4.28125in"}

Figure 7. UE Context Release Command

\[16\] The source eNB confirms the release of UE-associated S1 logical
connections over S1 interface by sending *UE Context Release Complete*.

-   MME UE S1AP ID: uniquely identifies the UE association with the S1
    interface within the MME.

-   eNB UE S1AP ID: uniquely identifies the UE association with the S1
    interface within the eNB.

![](media/image194.png){width="6.135416666666667in"
height="3.5416666666666665in"}

Figure 8. UE Context Release Complete

\[17\] The MME requests the SGW to delete the Indirect Forwarding
Tunnels by sending *Delete Indirect Data Forwarding Tunnel Request*.

![](media/image195.png){width="6.1875in" height="1.28125in"}

Figure 9. Delete Indirect Data Forwarding Tunnel Request

\[18\] The SGW responds with *Delete Indirect Data Forwarding Tunnel
Response* to the MME.

![](media/image196.png){width="6.1875in" height="3.0416666666666665in"}

Figure 10. Delete Indirect Data Forwarding Tunnel Response

***Red Mouse***

**REFERENCES**

\[1\] 3GPP TS23.401, "General Packet Radio Service (GPRS) enhancements
for Evolved Universal Terrestrial Radio Access Network (E-UTRAN)
access", v12.4.0, Mar 2014

\[2\] 3GPP TS29.274, "Evolved General Packet Radion Service (GPRS)
Tunneling Protocol for Control Plane (GTPv2-C); Stage3", v13.2.0, Jun
2015

\[3\] 3GPP TS36.411, \"Evolved Universal Terrestrial Radio Access
(E-UTRA); S1 Application Protocol (S1AP)\", v13.0.0, Jun 2015
