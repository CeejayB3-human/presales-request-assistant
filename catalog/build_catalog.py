from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, PageBreak, KeepTogether, NextPageTemplate)

COMPANY = "Demo IT Solutions Ltd"
NAVY = colors.HexColor("#0F2A44")
TEAL = colors.HexColor("#0E7C86")
LIGHT = colors.HexColor("#EEF4F6")
GREY = colors.HexColor("#5B6770")
LINE = colors.HexColor("#C9D6DC")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=20, leading=24,
                    textColor=NAVY, spaceBefore=0, spaceAfter=8)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=16,
                    textColor=TEAL, spaceBefore=8, spaceAfter=4)
H3 = ParagraphStyle("H3", fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=NAVY,
                    spaceBefore=8, spaceAfter=3)
BODY = ParagraphStyle("Body", fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=colors.black,
                      spaceAfter=5)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=8.5, leading=11.5, spaceAfter=0)
SMALLB = ParagraphStyle("SmallB", parent=SMALL, fontName="Helvetica-Bold", textColor=colors.white)
BUL = ParagraphStyle("Bul", parent=BODY, leftIndent=12, bulletIndent=2, spaceAfter=2)
NOTE = ParagraphStyle("Note", parent=BODY, fontSize=8.5, leading=12, textColor=GREY)
TAG = ParagraphStyle("Tag", parent=BODY, fontName="Helvetica-Bold", fontSize=9, textColor=GREY, spaceAfter=2)


def P(t, s=BODY):
    return Paragraph(t, s)


def bullets(items):
    return [Paragraph(i, BUL, bulletText="\u2022") for i in items]


def table(header, rows, widths, zebra=True):
    data = [[P(h, SMALLB) for h in header]] + [[P(str(c), SMALL) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    if zebra:
        for i in range(1, len(data)):
            if i % 2 == 0:
                st.append(("BACKGROUND", (0, i), (-1, i), LIGHT))
    t.setStyle(TableStyle(st))
    return t


def callout(text):
    t = Table([[P(text, SMALL)]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("LINEBEFORE", (0, 0), (0, -1), 3, TEAL),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


W = 170 * mm

# ---------------------------------------------------------------- service data
AREAS = [
    {
        "code": "SEC", "name": "Security",
        "summary": "Protecting people, devices, data and networks from cyber threats, and helping organisations "
                   "respond quickly when something goes wrong.",
        "overview": "Our Security practice helps organisations understand their risk, put the right controls in place "
                    "and respond with confidence when an incident happens. We combine assessment, technology "
                    "deployment, user awareness and ongoing monitoring, sized to the customer's risk and budget. "
                    "Most engagements start with a short assessment so recommendations are based on evidence rather "
                    "than assumptions.",
        "signals": [
            "Staff receiving suspicious or spoofed emails, or someone has clicked a malicious link.",
            "Money lost to a fake payment request, invoice fraud or business email compromise.",
            "Devices running outdated antivirus, or no central view of which devices are protected.",
            "No firewall, or a consumer-grade router acting as the only perimeter.",
            "A customer, regulator or auditor is asking for evidence of security controls (for example NDPA, "
            "ISO 27001 or PCI DSS).",
            "Ransomware, data loss, account takeover or any other active incident.",
        ],
        "services": [
            ("SEC-01", "Security Assessment and Gap Analysis",
             "Structured review of current controls, policies, users and devices against a recognised framework.",
             "Risk register, prioritised remediation roadmap, executive summary"),
            ("SEC-02", "Next-Generation Firewall (NGFW)",
             "Design, supply and configuration of perimeter firewalls with intrusion prevention, web filtering, "
             "application control and secure remote access VPN.",
             "Firewall design, rule base, configuration backup, admin handover"),
            ("SEC-03", "Endpoint Protection and EDR/XDR",
             "Centrally managed protection for laptops, desktops and servers, with detection and response "
             "across endpoints, email and network.",
             "Deployed agents, policies, central console, coverage report"),
            ("SEC-04", "Email Security and Anti-Phishing",
             "Filtering of spam, malware and impersonation attempts, plus SPF, DKIM and DMARC setup to reduce "
             "domain spoofing.",
             "Mail filtering policy, DNS records, spoofing protection report"),
            ("SEC-05", "Identity and Access Security",
             "Multi-factor authentication, single sign-on, privileged account controls and joiner/leaver processes.",
             "MFA rollout, access policy, admin account review"),
            ("SEC-06", "Security Awareness Training",
             "Short role-based training sessions and simulated phishing campaigns that measure and improve staff "
             "behaviour.",
             "Training sessions, phishing simulation results, improvement tracking"),
            ("SEC-07", "Incident Response",
             "Rapid support to contain an active incident, preserve evidence, restore services and prevent "
             "recurrence.",
             "Containment actions, incident report, lessons learned"),
            ("SEC-08", "Managed Security Monitoring",
             "Ongoing monitoring of security alerts with triage, escalation and monthly reporting.",
             "Alert triage, monthly security report, quarterly review"),
            ("SEC-09", "Compliance Readiness",
             "Support preparing for audits and data protection obligations, including policies, evidence and "
             "control mapping.",
             "Policy set, control mapping, audit evidence pack"),
        ],
        "customers": "SMEs handling payments or customer data, financial services, healthcare, schools, "
                     "logistics and any organisation that has recently experienced phishing or fraud.",
        "questions": [
            "How many users and devices need protecting, and where do they work from?",
            "What security tools are in place today (firewall, antivirus, email filtering, MFA)?",
            "Have there been any incidents in the last 12 months? What happened and what was lost?",
            "Are there compliance or contractual requirements to meet?",
            "Who is responsible for IT and security internally?",
            "Is there an active incident right now that needs immediate containment?",
        ],
        "related": "Network Infrastructure (firewall placement, segmentation), Data Centre and Backup "
                   "(ransomware recovery), Cloud (cloud security posture).",
    },
    {
        "code": "NET", "name": "Network Infrastructure",
        "summary": "Reliable, secure connectivity across offices, warehouses and branches, wired and wireless.",
        "overview": "We design and build networks that stay up, perform well and are easy to manage. Our work covers "
                    "the full path from the internet connection to the user's device: internet links and "
                    "failover, routing, switching, Wi-Fi, structured cabling and inter-site connectivity. We "
                    "start with a site survey so the design reflects the real building, users and applications.",
        "signals": [
            "Internet or Wi-Fi keeps dropping, or is slow at busy times.",
            "Only one internet provider, so any outage stops work.",
            "Opening a new office, warehouse or branch.",
            "Untidy or undocumented cabling, unmanaged switches, or no one knows how the network is set up.",
            "Voice or video calls breaking up.",
            "Guests and staff share the same network.",
        ],
        "services": [
            ("NET-01", "Network Assessment and Site Survey",
             "Review of current topology, performance, cabling and Wi-Fi coverage, including a wireless heat map.",
             "Current-state diagram, issues list, recommended design"),
            ("NET-02", "LAN Design and Switching",
             "Managed switching with VLAN segmentation for staff, guests, voice, CCTV and servers.",
             "Network design, VLAN plan, configured switches"),
            ("NET-03", "Enterprise Wi-Fi",
             "Centrally managed access points with coverage planning, guest access and roaming.",
             "Coverage plan, installed access points, SSID and guest policy"),
            ("NET-04", "Internet Resilience and SD-WAN",
             "Dual internet links with automatic failover and load balancing; SD-WAN for multi-site organisations.",
             "Failover design, configured edge devices, failover test"),
            ("NET-05", "Structured Cabling",
             "Copper and fibre cabling, patch panels, cabinets and labelling to recognised standards.",
             "Installed cabling, test results, as-built documentation"),
            ("NET-06", "Site-to-Site and Remote Connectivity",
             "Secure links between offices, warehouses and cloud environments.",
             "VPN or private link design, configured tunnels"),
            ("NET-07", "Unified Communications",
             "IP telephony, contact centre and collaboration systems integrated with the network.",
             "Voice design, configured handsets and call flows"),
            ("NET-08", "Network Monitoring and Management",
             "Monitoring of links and devices with alerting, capacity tracking and change management.",
             "Monitoring dashboards, alerts, monthly availability report"),
        ],
        "customers": "Multi-site businesses, warehouses and logistics operators, hospitality, education, "
                     "and organisations moving into new premises.",
        "questions": [
            "How many sites, users and devices? How large is each site?",
            "Which internet providers and link speeds are in use today?",
            "Where and when do problems happen (whole site, one area, certain times)?",
            "Which applications are most sensitive (voice, video, ERP, cloud apps)?",
            "Is there existing cabling and equipment we can reuse?",
            "Are any moves, expansions or new sites planned in the next 12 months?",
        ],
        "related": "Security (firewalls, segmentation), IT Procurement (hardware supply), "
                   "Cloud (connectivity to cloud services).",
    },
    {
        "code": "CLD", "name": "Cloud",
        "summary": "Moving, building and running workloads in public cloud and Microsoft 365 / Google Workspace, "
                   "with cost and security under control.",
        "overview": "We help organisations decide what belongs in the cloud, move it safely and run it well. "
                    "Our team covers productivity suites, cloud infrastructure, modern application platforms "
                    "and cost optimisation. Every migration includes a readiness assessment, a tested rollback "
                    "plan and a handover so the customer's team understands what they own.",
        "signals": [
            "Old on-premises server nearing end of life, or no budget for new hardware.",
            "Staff need secure access to files and email from anywhere.",
            "Cloud bills are growing and nobody knows why.",
            "A new application or website needs scalable hosting.",
            "Interest in using AI on company data.",
        ],
        "services": [
            ("CLD-01", "Cloud Readiness Assessment",
             "Inventory of applications and data, suitability for cloud, cost model and migration options.",
             "Readiness report, target architecture, cost estimate"),
            ("CLD-02", "Productivity Suite Deployment",
             "Setup and migration to Microsoft 365 or Google Workspace, including email, file sharing and "
             "collaboration.",
             "Configured tenant, migrated mailboxes and files, user guides"),
            ("CLD-03", "Cloud Migration",
             "Lift-and-shift or re-platforming of servers and applications to public cloud.",
             "Migration plan, migrated workloads, cutover and rollback plan"),
            ("CLD-04", "Cloud Landing Zone and Governance",
             "Secure multi-account foundation with identity, logging, guardrails and tagging.",
             "Landing zone, policy guardrails, governance guide"),
            ("CLD-05", "Serverless and Application Modernisation",
             "Rebuilding or extending applications with managed and serverless services.",
             "Architecture design, deployed application, CI/CD pipeline"),
            ("CLD-06", "Cloud Cost Optimisation",
             "Analysis of spend with rightsizing, scheduling and commitment recommendations.",
             "Cost report, savings plan, implemented quick wins"),
            ("CLD-07", "Generative AI Solutions",
             "Proofs of concept and production builds using managed AI model services, with data kept in the "
             "customer's own cloud account.",
             "Use-case assessment, working proof of concept, production roadmap"),
            ("CLD-08", "Managed Cloud Operations",
             "Ongoing monitoring, patching, backup checks and cost reporting for cloud environments.",
             "Monitoring, monthly operations and cost report"),
        ],
        "customers": "Growing SMEs, distributed teams, software and digital businesses, and organisations "
                     "replacing ageing servers.",
        "questions": [
            "Which applications and data would move, and how much data is there?",
            "Are there data residency or regulatory constraints on where data lives?",
            "What is the current hosting cost and hardware age?",
            "Which productivity tools are used today (email, file sharing)?",
            "Who will manage the environment after go-live?",
        ],
        "related": "Data Centre and Backup (hybrid and backup to cloud), Security (identity and posture), "
                   "Business Software (cloud-hosted ERP).",
    },
    {
        "code": "DCB", "name": "Data Centre and Backup",
        "summary": "Servers, storage, power and cooling for on-premises IT, plus backup and disaster recovery "
                   "that is actually tested.",
        "overview": "We design and maintain the physical foundation of IT: server rooms, servers, storage, "
                    "virtualisation, power protection and cooling. We also make sure data can be recovered. Every "
                    "backup design is built around two agreed targets: how much data the business can afford to "
                    "lose (RPO) and how long it can afford to be down (RTO), and every design includes a "
                    "documented restore test.",
        "signals": [
            "Critical systems running on an old PC or a single ageing server.",
            "Backups exist but have never been tested, or nobody knows if they work.",
            "Frequent power cuts damaging equipment or causing downtime.",
            "Server room overheating or with no access control.",
            "Concern about ransomware wiping out data and backups together.",
        ],
        "services": [
            ("DCB-01", "Infrastructure Assessment",
             "Review of servers, storage, power, cooling and backup against business recovery needs.",
             "Asset list, risk findings, recommended design"),
            ("DCB-02", "Server and Virtualisation",
             "Supply and setup of servers and hypervisors to consolidate workloads and improve resilience.",
             "Configured hosts, virtual machines, admin handover"),
            ("DCB-03", "Storage Solutions",
             "Network attached and shared storage sized for capacity, performance and growth.",
             "Storage design, configured volumes, capacity plan"),
            ("DCB-04", "Power Protection and UPS",
             "UPS systems, power distribution and generator integration to keep equipment running through outages.",
             "Power design, installed UPS, runtime test"),
            ("DCB-05", "Server Room and Small Data Centre Build",
             "Racks, cooling, environmental monitoring, physical access control and fire suppression.",
             "Room design, installation, environmental monitoring"),
            ("DCB-06", "Backup Solutions",
             "Automated backups following the 3-2-1 rule, including immutable or off-site copies to resist "
             "ransomware.",
             "Backup policy, configured jobs, first restore test"),
            ("DCB-07", "Disaster Recovery Planning and Testing",
             "Recovery plans, standby environments (on-premises or cloud) and scheduled recovery drills.",
             "DR plan, RPO/RTO agreement, test report"),
            ("DCB-08", "Hardware Maintenance and Support",
             "Preventive maintenance and break-fix support for servers, storage and power equipment.",
             "Maintenance schedule, service reports"),
        ],
        "customers": "Organisations with on-premises systems, manufacturing and logistics sites, banks and "
                     "healthcare providers, and any business with frequent power interruptions.",
        "questions": [
            "Which systems are critical, and what happens to the business if they stop?",
            "How much data could be lost without serious harm (RPO)? How long can systems be down (RTO)?",
            "What is backed up today, where to, and when was a restore last tested?",
            "How reliable is mains power, and is there a generator or UPS?",
            "What is the age and condition of the current servers?",
        ],
        "related": "Cloud (backup and DR to cloud), Security (ransomware protection), "
                   "IT Procurement (hardware supply).",
    },
    {
        "code": "PRC", "name": "IT Procurement",
        "summary": "Sourcing, supplying and deploying hardware and software licences, with warranty and "
                   "lifecycle management.",
        "overview": "We help customers buy the right technology at the right time, through authorised channels "
                    "with genuine warranties. Beyond supply, we handle configuration, delivery, asset tagging and "
                    "end-of-life replacement planning so equipment arrives ready to use.",
        "signals": [
            "New staff joining and needing laptops, phones or desks set up.",
            "Licences expiring, or unclear which software licences the business owns.",
            "Equipment out of warranty or failing frequently.",
            "A project (network, data centre, security) requires hardware supply.",
            "Need for a single supplier with consolidated invoicing.",
        ],
        "services": [
            ("PRC-01", "End-User Devices",
             "Laptops, desktops, monitors, printers and peripherals, pre-configured and ready for users.",
             "Supplied and imaged devices, asset register"),
            ("PRC-02", "Infrastructure Hardware",
             "Servers, storage, switches, access points, firewalls and UPS units for projects.",
             "Supplied equipment, warranty registration"),
            ("PRC-03", "Software Licensing",
             "Licence sourcing, renewals and true-ups for operating systems, productivity, security and "
             "business software.",
             "Licence schedule, renewal calendar"),
            ("PRC-04", "Device Deployment and Imaging",
             "Standard builds, enrolment in device management and delivery to staff or branches.",
             "Standard image, enrolled devices, deployment report"),
            ("PRC-05", "Asset and Lifecycle Management",
             "Tracking of assets, warranties and refresh cycles, plus secure disposal of retired equipment.",
             "Asset register, refresh plan, disposal certificates"),
        ],
        "customers": "Any organisation buying IT equipment or licences, especially growing teams and project "
                     "rollouts across multiple sites.",
        "questions": [
            "What items, quantities and specifications are needed, and by when?",
            "Is there a preferred brand, standard build or existing contract?",
            "Where should equipment be delivered, and does it need configuring first?",
            "Are there existing licences or warranties to renew or consolidate?",
            "What is the procurement process on the customer side (approvals, purchase orders)?",
        ],
        "related": "All service areas, as procurement supports most project deliveries.",
    },
    {
        "code": "ERP", "name": "Business Software (ERP)",
        "summary": "Business applications for finance, invoicing, inventory, HR and customer management, "
                   "implemented and integrated.",
        "overview": "We implement business software that replaces spreadsheets and disconnected tools with a single "
                    "source of truth. Our team handles requirements, configuration, data migration, integration "
                    "and training, and we offer cloud and on-premises options depending on budget and "
                    "connectivity.",
        "signals": [
            "Invoicing, stock or accounts managed in spreadsheets or on paper.",
            "Different departments keep separate records that do not agree.",
            "Need for customer relationship management or a sales pipeline.",
            "HR and payroll handled manually.",
            "Growth makes current tools too slow or error-prone.",
        ],
        "services": [
            ("ERP-01", "Business Process Review",
             "Mapping of current processes and requirements before software selection.",
             "Process maps, requirements list, solution shortlist"),
            ("ERP-02", "Finance, Invoicing and Accounting",
             "Implementation of accounting, invoicing, tax and reporting modules.",
             "Configured modules, chart of accounts, opening balances"),
            ("ERP-03", "Inventory and Warehouse Management",
             "Stock control, purchasing, warehouse locations and barcode scanning.",
             "Configured inventory, item master, scanning workflow"),
            ("ERP-04", "CRM and Sales Management",
             "Lead, opportunity and customer management with sales reporting.",
             "Configured CRM, pipeline stages, dashboards"),
            ("ERP-05", "HR and Payroll",
             "Employee records, leave, payroll and statutory deductions.",
             "Configured HR module, payroll runs"),
            ("ERP-06", "Data Migration and Integration",
             "Moving data from spreadsheets or legacy systems and connecting applications together.",
             "Migrated data, reconciliation report, integrations"),
            ("ERP-07", "Training and Application Support",
             "User training, admin training and ongoing functional support.",
             "Training sessions, user guides, support plan"),
        ],
        "customers": "SMEs and mid-sized organisations in trading, distribution, logistics, manufacturing "
                     "and professional services.",
        "questions": [
            "Which processes are most painful today (invoicing, stock, payroll, sales)?",
            "How many users, and which departments?",
            "What tools and data are used today, and how clean is the data?",
            "Is cloud-hosted software acceptable, given internet reliability?",
            "What reporting does management need?",
        ],
        "related": "Cloud (hosting), Network Infrastructure (reliable access), "
                   "IT Procurement (licences and devices).",
    },
]

SLA = [
    ("Essential", "Business hours (8:00-17:00, Mon-Fri)", "4 business hours", "Next business day",
     "Remote helpdesk, monthly health check"),
    ("Professional", "Extended (7:00-20:00, Mon-Sat)", "2 hours", "8 hours",
     "Remote and on-site support, monitoring, quarterly review"),
    ("Premium", "24 x 7", "30 minutes (critical)", "4 hours (critical)",
     "Dedicated account engineer, proactive monitoring, monthly review"),
]

URGENCY = [
    ("High", "Active incident, financial loss, data at risk, or business stopped.",
     "Fraudulent transfer after phishing; ransomware; main site offline.",
     "Same-day response; involve security or on-call engineer."),
    ("Medium", "Recurring disruption or significant risk, but business is still operating.",
     "Frequent internet outages; untested backups; old server failing.",
     "Respond within 1 business day; schedule assessment."),
    ("Low", "Planned improvement, new project or general enquiry.",
     "Want invoicing software; planning new office next quarter.",
     "Respond within 2 business days; book discovery call."),
]

KEYWORDS = [
    ("phishing, strange emails, clicked a link, fake bank, spoofing, fraud, hacked, virus, ransomware",
     "Security", "SEC-03, SEC-04, SEC-06, SEC-07"),
    ("firewall, VPN, remote access, MFA, passwords, audit, compliance, NDPA",
     "Security", "SEC-01, SEC-02, SEC-05, SEC-09"),
    ("internet down, slow network, Wi-Fi, cabling, new office, branch, warehouse coverage",
     "Network Infrastructure", "NET-01 to NET-06"),
    ("phones, calls dropping, video conferencing", "Network Infrastructure", "NET-07"),
    ("email migration, Microsoft 365, Google Workspace, work from anywhere, file sharing",
     "Cloud", "CLD-02"),
    ("move to cloud, hosting, cloud bill, AI, chatbot", "Cloud", "CLD-01, CLD-03, CLD-06, CLD-07"),
    ("old server, PC under a desk, backup, restore, disaster recovery, power cuts, UPS",
     "Data Centre and Backup", "DCB-01, DCB-02, DCB-04, DCB-06, DCB-07"),
    ("laptops, new staff, licences, renewals, hardware purchase", "IT Procurement", "PRC-01 to PRC-04"),
    ("invoicing, accounting, stock, inventory, payroll, CRM, spreadsheets",
     "Business Software (ERP)", "ERP-01 to ERP-06"),
]

GLOSSARY = [
    ("3-2-1 backup", "Three copies of data, on two types of media, with one copy off-site."),
    ("CRM", "Customer Relationship Management: software for tracking customers, leads and sales."),
    ("DMARC, SPF, DKIM", "Email authentication records that help stop others sending email pretending to be "
                         "your domain."),
    ("EDR / XDR", "Endpoint / Extended Detection and Response: tools that detect and respond to threats on "
                  "devices, and across devices, email and network."),
    ("ERP", "Enterprise Resource Planning: integrated software for finance, inventory, HR and operations."),
    ("Immutable backup", "A backup copy that cannot be changed or deleted for a set period, protecting it from "
                         "ransomware."),
    ("MFA", "Multi-Factor Authentication: a second check, such as a code on a phone, in addition to a password."),
    ("NGFW", "Next-Generation Firewall: a firewall that also inspects applications, blocks intrusions and "
             "filters web traffic."),
    ("RPO", "Recovery Point Objective: the maximum amount of data, measured in time, the business can afford "
            "to lose."),
    ("RTO", "Recovery Time Objective: the maximum time a system can be unavailable after an incident."),
    ("SD-WAN", "Software-Defined Wide Area Network: centrally managed connectivity across multiple sites and "
               "internet links."),
    ("UPS", "Uninterruptible Power Supply: battery backup that keeps equipment running during power cuts."),
    ("VLAN", "Virtual LAN: a way of separating one physical network into isolated segments."),
]


# ---------------------------------------------------------------- page decoration
def cover_page(c, doc):
    w, h = A4
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, h * 0.42, w, 6, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 12)
    c.drawString(25 * mm, h - 40 * mm, COMPANY.upper())
    c.setFont("Helvetica-Bold", 38)
    c.drawString(25 * mm, h * 0.42 + 70, "Service Catalog")
    c.setFont("Helvetica", 15)
    c.drawString(25 * mm, h * 0.42 + 40, "Technology solutions for growing organisations")
    c.setFont("Helvetica", 11)
    y = h * 0.42 - 40
    for line in ["Security", "Network Infrastructure", "Cloud", "Data Centre and Backup",
                 "IT Procurement", "Business Software (ERP)"]:
        c.drawString(25 * mm, y, "\u2014  " + line)
        y -= 18
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.HexColor("#A9BCCB"))
    c.drawString(25 * mm, 25 * mm, "Version 1.0  |  October 2026")
    c.drawString(25 * mm, 19 * mm, "Fictional company. Created as sample reference data for a product demonstration.")
    c.restoreState()


def normal_page(c, doc):
    w, h = A4
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, h - 12 * mm, w, 12 * mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(20 * mm, h - 7.8 * mm, COMPANY)
    c.setFont("Helvetica", 8.5)
    c.drawRightString(w - 20 * mm, h - 7.8 * mm, "Service Catalog  |  v1.0")
    c.setStrokeColor(LINE)
    c.line(20 * mm, 14 * mm, w - 20 * mm, 14 * mm)
    c.setFillColor(GREY)
    c.setFont("Helvetica", 8)
    c.drawString(20 * mm, 9 * mm, "Sample catalog for demonstration purposes. Fictional company.")
    c.drawRightString(w - 20 * mm, 9 * mm, f"Page {doc.page}")
    c.restoreState()


doc = BaseDocTemplate("IT_Service_Catalog.pdf", pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=20 * mm,
                      title="IT Service Catalog", author=COMPANY,
                      subject="Sample IT services catalog for demonstration")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([
    PageTemplate(id="cover", frames=[frame], onPage=cover_page),
    PageTemplate(id="normal", frames=[frame], onPage=normal_page),
])

s = [NextPageTemplate("normal"), PageBreak()]

# ---------------------------------------------------------------- contents
s.append(P("Contents", H1))
toc = [("1", "About this catalog"), ("2", "Who we are"), ("3", "Service areas at a glance")]
for i, a in enumerate(AREAS, start=4):
    toc.append((str(i), a['name'] if a['code'] in a['name'] else f"{a['name']} ({a['code']})"))
n = 4 + len(AREAS)
toc += [(str(n), "How we engage"), (str(n + 1), "Managed support and service levels"),
        (str(n + 2), "Request urgency guide"), (str(n + 3), "What is outside our scope"),
        ("A", "Appendix A: Request keyword guide"), ("B", "Appendix B: Glossary")]
tt = Table([[P(f"<b>{a}</b>", BODY), P(b, BODY)] for a, b in toc], colWidths=[14 * mm, 150 * mm])
tt.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.3, LINE),
                        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
s.append(tt)
s.append(Spacer(1, 14))

# ---------------------------------------------------------------- 1 about
s.append(P("1. About this catalog", H2))
s.append(P(f"This catalog describes the services offered by {COMPANY}. It is written for two audiences: "
           "customers who want to understand what we can help with, and our own sales and presales teams, "
           "who use it to map a customer's request to the right services."))
s.append(P("Each service area includes an overview, the signals that suggest a customer needs it, the "
           "individual services with their deliverables, typical customers, the discovery questions we ask, "
           "and related areas. Every service has a code (for example <b>SEC-04</b>) so it can be referenced "
           "in proposals, tickets and tools."))
s.append(P("The catalog deliberately contains no prices and no specific product models. Pricing depends on "
           "scope, quantities and the vendor platform chosen, and is provided in a separate quotation after "
           "discovery."))
s.append(callout("<b>Note:</b> " + COMPANY + " is a fictional company. This document was created as sample "
                 "reference data for a product demonstration and does not describe any real organisation."))

# ---------------------------------------------------------------- 2 who we are
s.append(P("2. Who we are", H2))
s.append(P(f"{COMPANY} is an IT solutions provider serving small, medium and enterprise organisations. "
           "We design, supply, implement and support technology across six service areas, so a customer can "
           "work with one partner from first conversation to ongoing support."))
s.append(P("What we stand for", H3))
s += bullets([
    "<b>Discovery before design.</b> We understand the business problem before recommending technology.",
    "<b>Vendor-neutral advice.</b> We work with several technology vendors and recommend what fits the "
    "customer's needs and budget.",
    "<b>Phased delivery.</b> Large needs are broken into stages so customers can address the biggest risks "
    "first and spread cost.",
    "<b>Documented handover.</b> Every project ends with documentation and training so customers understand "
    "what they own.",
    "<b>Managed quality and security.</b> Our delivery processes follow documented quality and information "
    "security management practices.",
])
s.append(P("Team", H3))
s.append(P("Account managers own the customer relationship. Presales engineers run discovery, design solutions "
           "and deliver proofs of concept. Delivery engineers implement projects. The support desk and "
           "managed services team handle ongoing operations."))

# ---------------------------------------------------------------- 3 glance
s.append(PageBreak())
s.append(P("3. Service areas at a glance", H1))
s.append(P("Use this table to find the right area quickly. Detailed descriptions follow in sections 4 to 9."))
glance = []
for a in AREAS:
    glance.append((f"<b>{a['name']}</b><br/>{a['code']}", a["summary"],
                   "; ".join(x[1] for x in a["services"][:4]) + "; and more"))
s.append(table(["Service area", "What it covers", "Key services"], glance, [36 * mm, 62 * mm, 72 * mm]))
s.append(Spacer(1, 10))
s.append(P("Most customer requests touch more than one area. For example, a phishing incident usually involves "
           "Security (containment, email protection, training) and often Data Centre and Backup (confirming "
           "data can be restored)."))

# ---------------------------------------------------------------- 4-9 areas
for i, a in enumerate(AREAS, start=4):
    s.append(PageBreak())
    s.append(P(f"{i}. {a['name']}", H1))
    s.append(P(f"SERVICE AREA CODE: {a['code']}", TAG))
    s.append(callout(a["summary"]))
    s.append(P("Overview", H2))
    s.append(P(a["overview"]))
    s.append(P("When customers need this", H2))
    s += bullets(a["signals"])
    s.append(P("Services", H2))
    s.append(table(["Code", "Service", "Description", "Key deliverables"],
                   [(c, f"<b>{n}</b>", d, dl) for c, n, d, dl in a["services"]],
                   [16 * mm, 36 * mm, 70 * mm, 48 * mm]))
    s.append(P("Typical customers", H2))
    s.append(P(a["customers"]))
    s.append(KeepTogether([P("Discovery questions", H2)] + bullets(a["questions"])))
    s.append(P("Related service areas", H2))
    s.append(P(a["related"]))

# ---------------------------------------------------------------- engage
s.append(PageBreak())
s.append(P(f"{n}. How we engage", H1))
s.append(P("Every engagement follows the same five stages. Small requests move through them in days; larger "
           "projects take weeks."))
s.append(table(["Stage", "What happens", "Output"], [
    ("<b>1. Request</b>", "Customer contacts us by web form, email, phone or messaging. The request is logged "
     "and an urgency level is assigned.", "Logged request, urgency, owner"),
    ("<b>2. Discovery</b>", "A presales engineer reviews the request, asks clarifying questions and, where needed, "
     "runs a call or site visit.", "Discovery notes, confirmed requirements"),
    ("<b>3. Solution design</b>", "We design the solution, select service codes and vendor options, and "
     "agree success criteria.", "Solution outline, scope, quotation"),
    ("<b>4. Proof of concept</b> (optional)", "For larger or uncertain projects we prove the approach on a "
     "small scale before full rollout.", "Working proof of concept, results"),
    ("<b>5. Delivery and handover</b>", "Delivery engineers implement, test and document. The customer's team "
     "is trained.", "Implemented solution, documentation, training"),
], [38 * mm, 88 * mm, 44 * mm]))
s.append(Spacer(1, 8))
s.append(P("Engagement models", H2))
s += bullets([
    "<b>Fixed-scope project:</b> defined deliverables and timeline, quoted after discovery.",
    "<b>Phased programme:</b> a roadmap delivered in stages, starting with the highest-risk items.",
    "<b>Managed service:</b> ongoing monitoring and support under a service level agreement.",
    "<b>Time and materials:</b> flexible engineering support for changing or exploratory work.",
])

# ---------------------------------------------------------------- SLA
s.append(P(f"{n + 1}. Managed support and service levels", H1.clone("H1b", spaceBefore=14)))
s.append(P("Managed services are available across all service areas. Response time is when an engineer "
           "starts working on the issue; resolution target applies to critical issues where a workaround or fix "
           "is reasonably possible."))
s.append(table(["Tier", "Coverage", "Response (critical)", "Resolution target", "Includes"],
               [(f"<b>{a}</b>", b, c, d, e) for a, b, c, d, e in SLA],
               [26 * mm, 38 * mm, 30 * mm, 30 * mm, 46 * mm]))

# ---------------------------------------------------------------- urgency
s.append(PageBreak())
s.append(P(f"{n + 2}. Request urgency guide", H1))
s.append(P("Every incoming request is given one urgency level so the right people respond in the right time. "
           "When in doubt, choose the higher level."))
s.append(table(["Urgency", "Definition", "Examples", "Expected first response"],
               [(f"<b>{a}</b>", b, c, d) for a, b, c, d in URGENCY],
               [20 * mm, 52 * mm, 52 * mm, 46 * mm]))
s.append(Spacer(1, 10))

# ---------------------------------------------------------------- out of scope
s.append(P(f"{n + 3}. What is outside our scope", H2))
s.append(P("To set clear expectations, the following are not part of our standard offering. Where relevant, "
           "we can refer customers to trusted partners."))
s += bullets([
    "Custom software development from scratch (beyond integrations and configuration).",
    "Website design, branding and digital marketing.",
    "Physical security such as guards, CCTV monitoring staff or building alarms (CCTV network connectivity is "
    "in scope).",
    "Electrical wiring of buildings beyond IT power distribution and UPS.",
    "Legal advice on regulatory compliance (we provide technical controls and evidence).",
    "Consumer or personal device repair.",
])
s.append(callout("When a request includes something outside this catalog, it should be noted as "
                 "<b>outside the current service list</b> and raised with the account manager, rather than "
                 "quoted."))

# ---------------------------------------------------------------- appendix A
s.append(PageBreak())
s.append(P("Appendix A: Request keyword guide", H1))
s.append(P("Customers describe problems in their own words. This guide links common phrases to the service "
           "area and the services most likely to apply. It is a starting point for discovery, not a final "
           "answer."))
s.append(table(["Customer says...", "Service area", "Likely services"],
               KEYWORDS, [86 * mm, 40 * mm, 44 * mm]))
s.append(Spacer(1, 10))
s.append(P("Worked example", H2))
s.append(callout("<i>\"We are a 60-person logistics company with one office and a small warehouse. Our internet "
                 "keeps going down, staff get strange emails and two people clicked something last month. Our "
                 "server is an old PC under a desk and the backup has never been tested. We also want invoicing "
                 "software. Budget is small.\"</i>"))
s.append(Spacer(1, 6))
s.append(table(["Need", "Service area", "Services", "Priority"], [
    ("Possible compromise after clicked links; ongoing phishing", "Security",
     "SEC-07, SEC-04, SEC-06, SEC-03", "High"),
    ("Untested backup on an old PC acting as server", "Data Centre and Backup", "DCB-06, DCB-07, DCB-02 or CLD-03",
     "High"),
    ("Internet keeps going down", "Network Infrastructure", "NET-01, NET-04", "Medium"),
    ("Invoicing software", "Business Software (ERP)", "ERP-01, ERP-02", "Low"),
], [62 * mm, 38 * mm, 46 * mm, 24 * mm]))
s.append(Spacer(1, 6))
s.append(P("Given the small budget, a phased approach fits: first confirm no ongoing compromise and get a tested "
           "backup, then stabilise the internet, then implement invoicing.", NOTE))

# ---------------------------------------------------------------- appendix B
s.append(PageBreak())
s.append(P("Appendix B: Glossary", H1))
s.append(table(["Term", "Meaning"], [(f"<b>{a}</b>", b) for a, b in GLOSSARY], [40 * mm, 130 * mm]))
s.append(Spacer(1, 16))
s.append(P(f"{COMPANY}  |  Service Catalog v1.0  |  October 2026", NOTE))

doc.build(s)
print("done")
