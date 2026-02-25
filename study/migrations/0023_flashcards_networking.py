from django.db import migrations


def seed_flashcards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Course = apps.get_model('study', 'Course')
    Topic = apps.get_model('study', 'Topic')
    Flashcard = apps.get_model('study', 'Flashcard')

    system_user = User.objects.filter(username='system').first()
    if not system_user:
        return

    course = Course.objects.filter(
        name='Networking Fundamentals', created_by=system_user
    ).first()
    if not course:
        return

    topics = {t.name: t for t in Topic.objects.filter(course=course)}

    def add_cards(topic_name, cards):
        topic = topics.get(topic_name)
        if not topic or Flashcard.objects.filter(topic=topic).exists():
            return
        for card in cards:
            Flashcard.objects.create(topic=topic, **card)

    # -------------------------------------------------------------------------
    # 1. OSI Model & TCP/IP
    # -------------------------------------------------------------------------
    add_cards('OSI Model & TCP/IP', [
        {
            'question': 'List the 7 OSI layers from bottom to top and their primary functions.',
            'answer': '1. Physical: bits over medium (cables, signals). 2. Data Link: framing, MAC addressing, error detection. 3. Network: IP routing. 4. Transport: end-to-end delivery, TCP/UDP. 5. Session: connection management. 6. Presentation: encoding, encryption, compression. 7. Application: user-facing protocols (HTTP, DNS, FTP).',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How does the TCP/IP model compare to the OSI model?',
            'answer': 'TCP/IP has 4 layers: Network Access (≈ OSI L1+L2), Internet (≈ OSI L3), Transport (≈ OSI L4), Application (≈ OSI L5-7). TCP/IP is the practical model used in real networks. OSI is the conceptual reference model used for troubleshooting.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is encapsulation in networking?',
            'answer': 'Each layer adds its own header (and sometimes trailer) around the payload from the layer above: Application data → Transport segment (TCP/UDP header) → Network packet (IP header) → Data Link frame (Ethernet header+trailer) → Physical bits. De-encapsulation reverses this at the receiver.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Compare TCP and UDP.',
            'answer': 'TCP: connection-oriented (3-way handshake), reliable delivery (ACKs, retransmit), ordered, flow/congestion control. Used for: HTTP, SSH, FTP. UDP: connectionless, unreliable (no ACKs), lower overhead. Used for: DNS, DHCP, VoIP, video streaming, TFTP.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Describe the TCP 3-way handshake.',
            'answer': '1) Client → Server: SYN (SEQ=x). 2) Server → Client: SYN-ACK (SEQ=y, ACK=x+1). 3) Client → Server: ACK (ACK=y+1). Connection established. Data transfer begins. Teardown: FIN → FIN-ACK → FIN → ACK (4 steps).',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What are well-known port numbers for common protocols?',
            'answer': 'HTTP: 80. HTTPS: 443. SSH: 22. FTP control: 21, data: 20. SMTP: 25. DNS: 53 (UDP/TCP). DHCP: 67 (server), 68 (client). Telnet: 23. SNMP: 161 (UDP). RDP: 3389. NTP: 123. Ports 0-1023: well-known. 1024-49151: registered. 49152-65535: dynamic/ephemeral.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What does ARP do and how does it work?',
            'answer': 'ARP (Address Resolution Protocol) resolves IP addresses to MAC addresses on a local network. Process: host broadcasts ARP request ("Who has IP 192.168.1.1?"). The device with that IP replies with its MAC address. The result is cached in the ARP table (arp -a to view).',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is ICMP and how is it used?',
            'answer': 'ICMP (Internet Control Message Protocol): network layer protocol for error messages and diagnostics. Not used for data transfer. Uses: ping (ICMP Echo Request/Reply), traceroute (TTL-exceeded messages), path MTU discovery, unreachable notifications (host unreachable, port unreachable, network unreachable).',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 2. IP Addressing & Subnetting
    # -------------------------------------------------------------------------
    add_cards('IP Addressing & Subnetting', [
        {
            'question': 'What are the IPv4 address classes and their default subnet masks?',
            'answer': 'Class A: 1.0.0.0 – 126.255.255.255, /8 (255.0.0.0), 16 million hosts/network. Class B: 128.0.0.0 – 191.255.255.255, /16 (255.255.0.0). Class C: 192.0.0.0 – 223.255.255.255, /24 (255.255.255.0). D: multicast. E: experimental.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What are the private IP address ranges defined by RFC 1918?',
            'answer': '10.0.0.0 – 10.255.255.255 (/8). 172.16.0.0 – 172.31.255.255 (/12). 192.168.0.0 – 192.168.255.255 (/16). These are not routed on the public internet; used in private networks with NAT.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Subnet 192.168.10.0/24 into 4 equal subnets. What are the network addresses and usable host ranges?',
            'answer': '',
            'hint': 'Borrow 2 bits from host portion: /26 (64 addresses each)',
            'difficulty': 'hard',
            'question_type': 'step_by_step',
            'uses_latex': False,
            'steps': [
                {'move': 'Determine new prefix', 'detail': 'Need 4 subnets: 2² = 4, so borrow 2 bits. New prefix: /24+2 = /26'},
                {'move': 'Block size', 'detail': '2^(32-26) = 64 addresses per subnet'},
                {'move': 'Subnet 1', 'detail': '192.168.10.0/26, hosts: .1–.62, broadcast: .63'},
                {'move': 'Subnet 2', 'detail': '192.168.10.64/26, hosts: .65–.126, broadcast: .127'},
                {'move': 'Subnet 3', 'detail': '192.168.10.128/26, hosts: .129–.190, broadcast: .191'},
                {'move': 'Subnet 4', 'detail': '192.168.10.192/26, hosts: .193–.254, broadcast: .255'},
            ],
        },
        {
            'question': 'What is CIDR notation and how does it differ from classful addressing?',
            'answer': 'CIDR (Classless Inter-Domain Routing): specifies network prefix length explicitly: 192.168.1.0/24. No longer restricted to class boundaries — any prefix length /0 to /32 is valid. Enables efficient address allocation and route aggregation (supernetting). Replaced classful A/B/C in 1993.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is NAT (Network Address Translation) and why is it used?',
            'answer': 'NAT translates private IP addresses to a public IP (and back) at the router. Conserves IPv4 addresses (many devices share one public IP). Types: Static NAT (1:1 mapping), Dynamic NAT (pool), PAT/overload (many:1 using ports, most common). Hides internal network topology.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Describe the key differences between IPv4 and IPv6.',
            'answer': 'IPv4: 32-bit, dotted decimal, ~4.3 billion addresses. IPv6: 128-bit, hexadecimal (8 groups of 4 hex digits), 340 undecillion addresses. IPv6 features: no NAT needed, no broadcast (multicast instead), stateless address autoconfiguration (SLAAC), built-in IPsec, simplified header.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How does DHCP assign IP addresses?',
            'answer': 'DORA process: 1) Discover: client broadcasts DHCPDISCOVER. 2) Offer: server sends DHCPOFFER with available IP. 3) Request: client broadcasts DHCPREQUEST to accept. 4) Acknowledge: server sends DHCPACK confirming lease. Lease duration, gateway, DNS are included. DHCP uses UDP 67/68.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 3. Routing Protocols
    # -------------------------------------------------------------------------
    add_cards('Routing Protocols', [
        {
            'question': 'What is the difference between static and dynamic routing?',
            'answer': 'Static routes: manually configured, no overhead, no adaptation to failures. Used for small networks or specific routes. Dynamic routing: routers exchange routing information automatically, adapt to changes. Used in large networks: RIP, OSPF, EIGRP, BGP.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Compare distance-vector and link-state routing protocols.',
            'answer': 'Distance-vector: routers share routing tables with neighbours periodically (Bellman-Ford). Simple, slow convergence, routing loops possible (RIP). Link-state: routers flood link-state advertisements (LSAs), each builds a complete topology map (Dijkstra\'s SPF). Faster convergence, scalable (OSPF, IS-IS).',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is OSPF and how does it work?',
            'answer': 'OSPF (Open Shortest Path First): link-state protocol, uses Dijkstra\'s SPF algorithm, metric = cost (inversely proportional to bandwidth). Areas: area 0 (backbone) required. LSA flooding within area. DR/BDR election on multi-access networks. Fast convergence, no hop-count limit, classless.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is BGP and why is it called the routing protocol of the internet?',
            'answer': 'BGP (Border Gateway Protocol): exterior gateway protocol used between autonomous systems (AS). Path-vector protocol — tracks AS_PATH to prevent loops. Policy-based routing (prefer routes based on attributes). eBGP: between different ASes. iBGP: within an AS. TCP port 179. Slow convergence; extremely scalable.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is administrative distance (AD) in Cisco IOS routing?',
            'answer': 'AD: trustworthiness of a routing source. Lower AD = more trusted. Values: Connected=0, Static=1, eBGP=20, OSPF=110, RIP=120, iBGP=200. If multiple protocols provide a route to the same destination, the one with lowest AD is installed in the routing table.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the default route and when is it used?',
            'answer': 'Default route: 0.0.0.0/0 (IPv4) or ::/0 (IPv6). Matches any destination not in the routing table — the "last resort" gateway. Used in stub networks pointing to the ISP/upstream router. Configured with: ip route 0.0.0.0 0.0.0.0 <next-hop>.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 4. Switching & VLANs
    # -------------------------------------------------------------------------
    add_cards('Switching & VLANs', [
        {
            'question': 'How does a Layer 2 switch forward frames?',
            'answer': 'A switch learns MAC addresses by inspecting source MAC of incoming frames and associates them with the incoming port (MAC address table / CAM table). On receiving a frame: if destination MAC is known → unicast forward to that port. Unknown → flood to all ports except source. Broadcast → flood all ports.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is a VLAN and why is it used?',
            'answer': 'A VLAN (Virtual LAN) is a logical network segment that groups ports regardless of physical location, separating broadcast domains. Benefits: security (isolate sensitive data), performance (smaller broadcast domains), flexibility (move users without rewiring), easier management.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the difference between an access port and a trunk port?',
            'answer': 'Access port: carries traffic for one VLAN only; connects end devices. Frames are untagged. Trunk port: carries traffic for multiple VLANs; connects switches or routers. Frames are tagged with VLAN ID using 802.1Q (4-byte tag inserted into Ethernet frame).',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is IEEE 802.1Q VLAN tagging?',
            'answer': '802.1Q adds a 4-byte tag between source MAC and EtherType. Contains: TPID (0x8100), PCP (3-bit priority), DEI (drop eligible), VID (12-bit VLAN ID, 0-4095). The switch inserts the tag on ingress trunk ports and removes it on egress access ports.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the Spanning Tree Protocol (STP) and why is it needed?',
            'answer': 'STP (802.1D) prevents Layer 2 loops in redundant switched networks. Without STP, broadcast storms and MAC address table instability would crash the network. STP elects a root bridge, then blocks redundant ports, leaving a loop-free tree topology. RSTP (802.1w) converges much faster.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is inter-VLAN routing and how is it implemented?',
            'answer': 'Devices in different VLANs cannot communicate at Layer 2. Inter-VLAN routing uses: 1) Router with separate physical interfaces per VLAN (expensive). 2) Router-on-a-stick: one trunk link with sub-interfaces (one per VLAN). 3) Layer 3 switch with SVI (Switch Virtual Interface) per VLAN — most common in enterprise.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is EtherChannel (link aggregation) and what standard governs it?',
            'answer': 'EtherChannel bundles multiple parallel physical links into one logical link, increasing bandwidth and providing redundancy. IEEE 802.3ad LACP (Link Aggregation Control Protocol) is the open standard. Cisco\'s proprietary equivalent is PAgP. The switch treats the bundle as a single interface.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 5. Wireless Networking
    # -------------------------------------------------------------------------
    add_cards('Wireless Networking', [
        {
            'question': 'What are the IEEE 802.11 Wi-Fi standards? Compare 802.11n, 802.11ac, and 802.11ax.',
            'answer': '802.11n (Wi-Fi 4): 2.4/5 GHz, up to 600 Mbps, MIMO. 802.11ac (Wi-Fi 5): 5 GHz only, MU-MIMO, up to 3.5 Gbps, wider channels (80/160 MHz). 802.11ax (Wi-Fi 6): 2.4/5/6 GHz, OFDMA, BSS Coloring, target wake time — more efficient in dense environments, up to 9.6 Gbps.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the difference between 2.4 GHz and 5 GHz Wi-Fi bands?',
            'answer': '2.4 GHz: longer range, better penetration through walls, but more interference (microwaves, Bluetooth), fewer non-overlapping channels (3: 1, 6, 11). 5 GHz: shorter range, faster speeds, less interference, more channels (24+ non-overlapping). Choice depends on distance, obstacles, and throughput needs.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Describe the WPA2 and WPA3 security protocols.',
            'answer': 'WPA2: uses AES-CCMP encryption. Personal mode: PSK (pre-shared key). Enterprise mode: 802.1X/RADIUS authentication. Vulnerable to PMKID/dictionary attacks. WPA3: SAE (Simultaneous Authentication of Equals) replaces PSK — resistant to offline dictionary attacks. Forward secrecy. WPA3-Enterprise: 192-bit mode.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the CSMA/CA medium access method used in Wi-Fi?',
            'answer': 'Carrier Sense Multiple Access / Collision Avoidance: before transmitting, station senses channel for a random backoff period. Cannot detect collisions (unlike wired CSMA/CD) — instead avoids them. RTS/CTS (Request to Send/Clear to Send) used for hidden node problem.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is a wireless site survey and why is it performed?',
            'answer': 'A systematic assessment of wireless coverage, signal strength (RSSI), interference, and capacity across a physical area. Used to: determine optimal AP placement, identify dead zones, measure interference sources, validate coverage after installation. Tools: Ekahau, NetSpot, Wi-Fi Analyzer.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 6. Network Security
    # -------------------------------------------------------------------------
    add_cards('Network Security', [
        {
            'question': 'What is a firewall and what types exist?',
            'answer': 'A firewall controls inbound/outbound traffic based on rules. Types: 1) Packet filter: inspects header (IP, port). 2) Stateful inspection: tracks connection state. 3) Application/proxy: deep packet inspection, understands protocols. 4) NGFW (Next-Gen): IPS, app awareness, SSL inspection, user identity.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is a DMZ (Demilitarised Zone) in network security?',
            'answer': 'A DMZ is a network segment that sits between the internet and the internal network, housing public-facing servers (web, email, DNS). Protected by two firewalls: one between internet and DMZ, one between DMZ and internal network. Limits exposure of internal resources.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is VPN and compare IPsec and SSL/TLS VPNs.',
            'answer': 'VPN: encrypted tunnel over an untrusted network. IPsec VPN: operates at Layer 3, encrypts IP packets (IKEv2, AH/ESP protocols) — used for site-to-site and client VPN. SSL/TLS VPN: operates at Layer 4-7 via HTTPS — browser-based or client app. Easier through NAT/firewalls. OpenVPN, WireGuard are common implementations.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is 802.1X port-based network access control?',
            'answer': '802.1X uses RADIUS for authentication: 1) Supplicant (client) requests network access. 2) Authenticator (switch/AP) forwards credentials to RADIUS server via EAP. 3) RADIUS server authenticates (Active Directory, certificates) and responds. Switch allows/blocks port access based on result.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Explain common network attacks and mitigations.',
            'answer': 'ARP spoofing: rogue ARP replies poison cache — mitigation: dynamic ARP inspection. DHCP starvation/rogue DHCP: mitigation: DHCP snooping. VLAN hopping (double-tagging): mitigation: disable auto-trunking, change native VLAN. Man-in-the-Middle: use encryption (TLS). DoS/DDoS: rate limiting, ACLs, scrubbing centres.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is an IDS vs IPS?',
            'answer': 'IDS (Intrusion Detection System): monitors traffic and alerts on suspicious activity — passive, does not block. IPS (Intrusion Prevention System): monitors traffic and actively blocks/drops malicious packets — inline. Both use signatures (known attacks) and anomaly detection. Network-based (NIDS/NIPS) or host-based (HIDS/HIPS).',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 7. Network Troubleshooting
    # -------------------------------------------------------------------------
    add_cards('Network Troubleshooting', [
        {
            'question': 'Describe a systematic approach to network troubleshooting.',
            'answer': 'Follow the OSI model bottom-up or top-down: 1) Physical (cables, LEDs, speed/duplex). 2) Data Link (MAC, VLAN, STP state). 3) Network (IP, subnet, routing). 4) Transport (TCP/UDP, firewall rules). 5) Application (service running, DNS, firewall). Divide and conquer: test connectivity at each layer to isolate the problem.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What tools do you use to troubleshoot network connectivity at each OSI layer?',
            'answer': 'L1: cable tester, interface LEDs, show interface (errors, duplex). L2: show mac-address-table, show spanning-tree, arp -a. L3: ping, traceroute, show ip route, ip route show. L4: telnet/nc to port, netstat/ss, Wireshark. L7: curl, wget, nslookup/dig.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you use Wireshark to troubleshoot a network issue?',
            'answer': 'Capture on the relevant interface. Apply display filters: ip.addr==192.168.1.1, tcp.port==443, http, dns. Look for: retransmissions (TCP), ICMP unreachables, ARP storms, malformed packets. Follow TCP stream to see application data. Use Statistics > IO Graph and conversations for traffic analysis.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What does a duplex mismatch cause and how do you identify it?',
            'answer': 'Duplex mismatch: one side full-duplex, other half-duplex → late collisions and CRC errors on the half-duplex end, degraded performance. Identify via: show interface (look for "late collisions", CRC errors). Fix: configure both sides to the same speed/duplex, or enable auto-negotiation on both.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you troubleshoot a DNS resolution failure?',
            'answer': 'Step by step: 1) nslookup hostname — see what DNS returns. 2) nslookup hostname <alternate_dns_IP> — test against a known-good DNS server. 3) ping DNS server IP — check reachability. 4) Check /etc/resolv.conf — correct nameserver? 5) Check firewall rules for UDP/TCP port 53. 6) Check DNS server logs.',
            'difficulty': 'medium',
            'question_type': 'step_by_step',
            'uses_latex': False,
            'steps': [
                {'move': 'Test DNS resolution', 'detail': 'nslookup hostname — note error or IP returned'},
                {'move': 'Try alternate server', 'detail': 'nslookup hostname 8.8.8.8 — test with Google DNS'},
                {'move': 'Ping DNS server', 'detail': 'ping <nameserver_IP> — verify reachability'},
                {'move': 'Check configuration', 'detail': 'cat /etc/resolv.conf — verify correct nameserver IP'},
                {'move': 'Check firewall', 'detail': 'iptables -L or ufw status — ensure port 53 UDP/TCP allowed'},
                {'move': 'Check DNS server health', 'detail': 'systemctl status named/bind9/dnsmasq; check logs'},
            ],
        },
    ])

    # -------------------------------------------------------------------------
    # 8. Industrial Networking
    # -------------------------------------------------------------------------
    add_cards('Industrial Networking', [
        {
            'question': 'What is Modbus and in what variants does it appear?',
            'answer': 'Modbus: a serial communication protocol developed by Modicon (1979) for PLC communications. Variants: Modbus RTU (binary over RS-232/RS-485, most common), Modbus ASCII (readable over serial), Modbus TCP/IP (over Ethernet, TCP port 502). Master/slave architecture; still widely used in industrial automation.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Explain the Modbus register model.',
            'answer': 'Four data tables: Coils (0x, read/write, 1-bit — digital output). Discrete Inputs (1x, read-only, 1-bit — digital input). Input Registers (3x, read-only, 16-bit — analogue input). Holding Registers (4x, read/write, 16-bit — general data, most commonly used). Function codes: FC01 (read coils), FC03 (read holding registers), FC06 (write single register), FC16 (write multiple registers).',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is EtherNet/IP and how does it differ from standard Ethernet?',
            'answer': 'EtherNet/IP (Ethernet Industrial Protocol): runs CIP (Common Industrial Protocol) over standard Ethernet/TCP-UDP. Uses: TCP (port 44818) for explicit messaging (configuration, data), UDP (port 2222) for implicit/I/O messaging (real-time control). Works on standard Ethernet hardware. Developed by Rockwell/ODVA.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is PROFIBUS and where is it used?',
            'answer': 'PROFIBUS (Process Field Bus): serial field bus for manufacturing automation (PROFIBUS DP — decentralised periphery, fast I/O) and process automation (PROFIBUS PA — intrinsically safe, 2-wire, for ATEX zones). Up to 12 Mbps (DP), uses RS-485 (DP) or IEC 61158-2 (PA). Being gradually replaced by PROFINET.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is OPC UA and why is it important for Industry 4.0?',
            'answer': 'OPC UA (Open Platform Communications Unified Architecture): a platform-independent, service-oriented communication standard for industrial automation. Features: information modelling (semantic data, not just values), built-in security (encryption, authentication), publish-subscribe, runs over TCP or MQTT. Key for IIoT/Industry 4.0: enables device-to-cloud and machine-to-machine communication.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the difference between IT and OT networks, and why is their convergence challenging?',
            'answer': 'IT (Information Technology): enterprise networks, focus on data integrity and confidentiality, frequent patching/updates, standard security practices. OT (Operational Technology): industrial control systems, focus on availability and safety, long equipment lifecycles (10–30 years), often cannot be patched, proprietary protocols. Convergence challenges: OT systems were not designed with cybersecurity in mind; applying IT security tools can disrupt critical processes.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is MQTT and why is it popular in IIoT applications?',
            'answer': 'MQTT (Message Queuing Telemetry Transport): lightweight publish-subscribe messaging protocol over TCP. Broker-based: clients publish to topics, subscribers receive messages. QoS levels: 0 (fire-and-forget), 1 (at least once), 2 (exactly once). Very low overhead — suitable for constrained devices (MCUs, sensors). Used in IIoT, home automation, AWS IoT, Azure IoT Hub.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What network security zones are recommended for industrial networks (Purdue Model)?',
            'answer': 'Purdue Enterprise Reference Architecture: Level 0: Field devices (sensors, actuators). Level 1: Basic Control (PLCs, RTUs). Level 2: Area Supervisory (SCADA, DCS). Level 3: Site Operations (historian, batch management). DMZ (industrial): data diode/firewall. Level 4: Business Planning (ERP). Level 5: Enterprise. Security principle: no direct connection between levels; strict firewall rules.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])


def reverse_fn(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0022_flashcards_linux_fundamentals'),
    ]

    operations = [
        migrations.RunPython(seed_flashcards, reverse_fn),
    ]
