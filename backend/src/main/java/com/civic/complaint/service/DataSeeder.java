package com.civic.complaint.service;

import com.civic.complaint.entity.*;
import com.civic.complaint.repository.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
@SuppressWarnings("null")
public class DataSeeder implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(DataSeeder.class);

    private final UserRepository userRepo;
    private final DepartmentRepository deptRepo;
    private final CategoryRepository catRepo;
    private final SLARuleRepository slaRuleRepo;
    private final ComplaintRepository complaintRepo;
    private final ComplaintAnalysisRepository analysisRepo;
    private final SLARecordRepository slaRecordRepo;
    private final PasswordEncoder passwordEncoder;

    public DataSeeder(UserRepository userRepo, DepartmentRepository deptRepo,
                      CategoryRepository catRepo, SLARuleRepository slaRuleRepo,
                      ComplaintRepository complaintRepo, ComplaintAnalysisRepository analysisRepo,
                      SLARecordRepository slaRecordRepo, PasswordEncoder passwordEncoder) {
        this.userRepo = userRepo;
        this.deptRepo = deptRepo;
        this.catRepo = catRepo;
        this.slaRuleRepo = slaRuleRepo;
        this.complaintRepo = complaintRepo;
        this.analysisRepo = analysisRepo;
        this.slaRecordRepo = slaRecordRepo;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public void run(String... args) {
        seedUsers();
        seedDepartments();
        seedCategories();
        seedSLARules();
        seedComplaints();
        log.info("✅ Data seeding complete");
    }

    private void seedUsers() {
        if (userRepo.count() > 0) return;

        userRepo.save(User.builder()
                .username("admin")
                .email("admin@complaint-system.gov.in")
                .passwordHash(passwordEncoder.encode("admin123"))
                .fullName("Rajesh Kumar (System Administrator)")
                .role(Role.ADMIN)
                .build());

        userRepo.save(User.builder()
                .username("authority")
                .email("authority@complaint-system.gov.in")
                .passwordHash(passwordEncoder.encode("authority123"))
                .fullName("Dr. Priya Sharma (Municipal Commissioner)")
                .role(Role.HIGHER_AUTHORITY)
                .build());

        userRepo.save(User.builder()
                .username("citizen")
                .email("citizen@example.com")
                .passwordHash(passwordEncoder.encode("citizen123"))
                .fullName("Amit Patel")
                .mobile("9876543210")
                .role(Role.CITIZEN)
                .build());

        userRepo.save(User.builder()
                .username("citizen2")
                .email("citizen2@example.com")
                .passwordHash(passwordEncoder.encode("citizen123"))
                .fullName("Sunita Verma")
                .mobile("9876543211")
                .role(Role.CITIZEN)
                .build());

        log.info("  → Seeded 4 users (admin/authority/citizen/citizen2)");
    }

    private void seedDepartments() {
        if (deptRepo.count() > 0) return;

        String[][] depts = {
            {"Water Department", "Handles water supply, pipeline, and distribution issues"},
            {"Electricity Department", "Manages power supply, transformers, and electrical infrastructure"},
            {"Public Works", "Roads, bridges, drainage, and general infrastructure"},
            {"Sanitation Department", "Waste collection, sewage, and cleanliness"},
            {"Health Department", "Public health, hospitals, and disease control"},
            {"Transport Department", "Public transport, bus services, and traffic"},
            {"Safety Department", "Public safety, fire services, and emergency response"},
            {"Environmental Services", "Pollution control, green spaces, and environment"},
            {"Education Department", "Schools, colleges, and educational services"},
            {"Administrative Services", "Government offices, certificates, and permits"},
            {"Finance Department", "Billing, payments, and financial services"}
        };

        for (String[] d : depts) {
            deptRepo.save(Department.builder().name(d[0]).description(d[1]).build());
        }
        log.info("  → Seeded {} departments", depts.length);
    }

    private void seedCategories() {
        if (catRepo.count() > 0) return;

        Object[][] cats = {
            {"Water", "Water supply and distribution issues", "high", true, "Water Department"},
            {"Road", "Road conditions and maintenance", "medium", false, "Public Works"},
            {"Electricity", "Power supply and electrical infrastructure", "high", true, "Electricity Department"},
            {"Sanitation", "Sanitation and hygiene issues", "high", true, "Sanitation Department"},
            {"Garbage", "Waste collection and disposal", "medium", true, "Sanitation Department"},
            {"Drainage", "Drainage and flooding issues", "high", true, "Public Works"},
            {"Street Light", "Street lighting problems", "medium", false, "Electricity Department"},
            {"Traffic", "Traffic management issues", "medium", false, "Transport Department"},
            {"Public Safety", "Safety and security concerns", "critical", false, "Safety Department"},
            {"Pollution", "Environmental pollution", "medium", false, "Environmental Services"},
            {"Healthcare", "Healthcare facility issues", "critical", true, "Health Department"},
            {"Public Transport", "Bus, metro, and transport issues", "medium", true, "Transport Department"},
            {"Parks", "Parks and green spaces", "low", false, "Environmental Services"},
            {"Property/Construction", "Construction and property issues", "medium", false, "Public Works"},
            {"Other", "Uncategorized complaints", "low", false, "Administrative Services"}
        };

        for (Object[] c : cats) {
            catRepo.save(Category.builder()
                    .name((String) c[0])
                    .description((String) c[1])
                    .riskLevel((String) c[2])
                    .isEssentialService((Boolean) c[3])
                    .defaultDepartment((String) c[4])
                    .build());
        }
        log.info("  → Seeded {} categories", cats.length);
    }

    private void seedSLARules() {
        if (slaRuleRepo.count() > 0) return;

        slaRuleRepo.save(SLARule.builder().priority(Priority.CRITICAL).responseHours(1).resolutionHours(4).build());
        slaRuleRepo.save(SLARule.builder().priority(Priority.HIGH).responseHours(4).resolutionHours(12).build());
        slaRuleRepo.save(SLARule.builder().priority(Priority.MEDIUM).responseHours(24).resolutionHours(48).build());
        slaRuleRepo.save(SLARule.builder().priority(Priority.LOW).responseHours(72).resolutionHours(168).build());

        log.info("  → Seeded 4 SLA rules");
    }

    private void seedComplaints() {
        if (complaintRepo.count() >= 40) return;

        User citizen = userRepo.findByUsername("citizen").orElse(null);
        Long citizenId = citizen != null ? citizen.getId() : 1L;

        log.info("  → Seeding 40 realistic synthetic demo complaints across 4 priority tiers...");

        // ==========================================
        // 10 CRITICAL DEMO COMPLAINTS
        // ==========================================
        createDemoComplaint("GWA-8921", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Major Water Pipeline Burst Flooding Sector 14",
                "A high-pressure primary water transmission pipeline has burst near the central market intersection. Water is flooding basement shops and threatening electrical transformers.",
                "Water", Priority.CRITICAL, 92, ComplaintStatus.IN_PROGRESS,
                "Sector 14 Central Market Chowk", 28.6139, 77.2090, 3,
                0.94, "negative", "critical",
                "Severe water pipeline rupture with property damage and electrical hazard risk.",
                "High pressure pipeline failure posing imminent risk to public infrastructure and shops.",
                "Emergency dispatch of municipal water pipeline rapid response team.", false);

        createDemoComplaint("GWA-4512", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Sparking 11kV Electric Wire Hanging over School Gate",
                "Live high voltage electrical cable snapped after storm and is dangling directly above the main pedestrian entrance of Primary School. Sparking continuously in rainwater.",
                "Public Safety", Priority.CRITICAL, 96, ComplaintStatus.ASSIGNED,
                "Opposite Gate 2, Government Primary School, Sector 8", 28.6200, 77.2150, 2,
                0.97, "urgent", "critical",
                "Live 11kV electrical wire over school entrance; critical electrocution danger.",
                "Immediate life safety risk flagged due to high voltage proximity to schoolchildren and water.",
                "Cut power supply to feeder immediately and dispatch emergency lineman team.", false);

        createDemoComplaint("GWA-9001", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Hit-and-Run Incident with Pedestrian Injury",
                "A speeding black SUV struck a pedestrian near railway crossing and escaped towards highway. Victim unconscious on road with head injury. Part of plate MP07 AB 2.",
                "Public Safety", Priority.CRITICAL, 98, ComplaintStatus.ASSIGNED,
                "Railway Station Outer Ring Road", 28.6150, 77.2080, 1,
                0.98, "urgent", "critical",
                "Hit-and-run collision with serious pedestrian injury and fleeing suspect vehicle.",
                "Hard safety trigger: life-threatening trauma and police emergency response required.",
                "Alert emergency medical services and traffic control room immediately.", false);

        createDemoComplaint("GWA-9002", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Chemical Storage Godown Fire in Dense Residential Pocket",
                "Thick black toxic smoke and large flames erupting from unauthorized chemical storage facility adjacent to 4-storey residential apartments.",
                "Public Safety", Priority.CRITICAL, 97, ComplaintStatus.IN_PROGRESS,
                "Industrial Area Phase 1 Lane 4", 28.6280, 77.2250, 1,
                0.96, "urgent", "critical",
                "Active chemical fire threatening multi-family dwellings with toxic fumes.",
                "Hard safety trigger: fire emergency and hazardous inhalation danger.",
                "Dispatch fire tenders and initiate perimeter evacuation.", false);

        createDemoComplaint("GWA-9003", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Open Deep Sewer Manhole on Unlit Walking Path",
                "Concrete cover missing from 12-foot deep main trunk sewer on busy pedestrian path outside vegetable market. Complete darkness at night.",
                "Sanitation", Priority.CRITICAL, 91, ComplaintStatus.SUBMITTED,
                "Subzi Mandi Main Walkway, Ward 15", 28.6320, 77.2120, 4,
                0.93, "negative", "critical",
                "Uncovered 12-foot sewer shaft on pedestrian thoroughfare posing fatal fall hazard.",
                "Hard safety trigger: severe fall danger to pedestrians and cyclists.",
                "Barricade opening immediately with reflective cones and install reinforced cover.", false);

        createDemoComplaint("GWA-9004", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] ICU Oxygen Supply Disruption at Civil Hospital",
                "Central oxygen manifold pressure dropping dangerously in civil trauma hospital; emergency ward struggling with backup cylinders.",
                "Healthcare", Priority.CRITICAL, 99, ComplaintStatus.IN_PROGRESS,
                "Civil Hospital Trauma Center, Block A", 28.6180, 77.2050, 1,
                0.99, "urgent", "critical",
                "Hospital oxygen supply failure directly impacting critical patients.",
                "Hard safety trigger: hospital emergency and life support threat.",
                "Immediate technician dispatch and emergency liquid medical oxygen tanker reroute.", false);

        createDemoComplaint("GWA-9005", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Flyover Structural Concrete Spalling over Highway",
                "Large concrete chunks falling from underside of bypass flyover onto moving vehicular traffic below. Rebar exposed and sagging.",
                "Infrastructure", Priority.CRITICAL, 94, ComplaintStatus.ASSIGNED,
                "National Highway 44 Flyover Pier 18", 28.6410, 77.2350, 2,
                0.95, "urgent", "critical",
                "Structural spalling of overpass bridge deck endangering high-speed traffic below.",
                "Hard safety trigger: structural collapse risk over active traffic corridor.",
                "Close lower lane to traffic and dispatch structural engineering inspection squad.", false);

        createDemoComplaint("GWA-9006", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Severe Monsoon Gutter Backflow Inundating 30 Homes",
                "Choked storm drain caused toxic rainwater and sewage mixture to enter 30 ground floor houses with 3-foot water level.",
                "Drainage", Priority.CRITICAL, 89, ComplaintStatus.IN_PROGRESS,
                "Govindpuri Low-Lying Enclave", 28.6250, 77.2180, 3,
                0.91, "negative", "critical",
                "Extensive residential flooding with hazardous sewer water affecting vulnerable families.",
                "Rule 3b trigger: essential drainage failure causing property loss and disease hazard.",
                "Deploy high-capacity mobile dewatering pumps and suction tankers.", false);

        createDemoComplaint("GWA-9007", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Transformer Explosion and Burning Oil Spill",
                "500kVA pole-mounted transformer exploded with loud blast, spraying flaming transformer oil onto roadside shop awnings.",
                "Electricity", Priority.CRITICAL, 95, ComplaintStatus.ASSIGNED,
                "Chawri Bazaar Electric Substation Junction", 28.6350, 77.2280, 2,
                0.96, "urgent", "critical",
                "Exploded transformer with flaming oil spill in dense commercial market.",
                "Hard safety trigger: electrical fire and active structural hazard.",
                "Isolate feeder line and dispatch foam tender with electrical breakdown unit.", false);

        createDemoComplaint("GWA-9008", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] High-Pressure Domestic PNG Pipeline Fracture",
                "Excavation backhoe fractured domestic piped natural gas line; loud hissing sound and overwhelming mercaptan gas odor across 3 streets.",
                "Public Safety", Priority.CRITICAL, 97, ComplaintStatus.IN_PROGRESS,
                "Model Town Sector 3 Main Road", 28.6450, 77.2400, 1,
                0.98, "urgent", "critical",
                "Fractured pressurized natural gas main presenting catastrophic ignition risk.",
                "Hard safety trigger: toxic gas leak and explosion danger.",
                "Isolate gas sectional valve, prohibit vehicular traffic, and evacuate perimeter.", false);

        // ==========================================
        // 10 HIGH DEMO COMPLAINTS
        // ==========================================
        createDemoComplaint("GWA-7734", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Deep Pothole Crater Causing Two-Wheeler Accidents",
                "A 3-foot wide and 10-inch deep pothole on the inner ring road right after the flyover descent has caused 4 motorbike falls in the last 24 hours.",
                "Road", Priority.HIGH, 76, ComplaintStatus.IN_PROGRESS,
                "Inner Ring Road, South Flyover Exit", 28.6300, 77.2200, 8,
                0.91, "negative", "high",
                "Large crater on high-speed arterial corridor causing recurring accidents.",
                "High vehicular density and documented accident frequency elevate priority.",
                "Deploy cold-mix asphalt quick repair crew and place safety cones.", false);

        createDemoComplaint("GWA-7001", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Blocked Sewer Line Overflowing Raw Effluent on Street",
                "Main municipal sewer line blocked for 3 days; dark foul-smelling effluent flooding entire residential lane, residents unable to step out.",
                "Sanitation", Priority.HIGH, 78, ComplaintStatus.ASSIGNED,
                "Lane 6, Gandhi Nagar Extension", 28.6220, 77.2140, 8,
                0.89, "negative", "high",
                "Raw sewage overflow on colony lane posing acute biological and health hazard.",
                "Essential sanitation service failure exceeding 48 hours.",
                "Deploy sewer jetting machine and dislodge obstruction.", false);

        createDemoComplaint("GWA-7002", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Dead Bovine Carcass Decomposing on Public Footpath",
                "Dead stray cow lying on open roadside for 3 days, causing unbearable stench, maggots, and severe disease transmission hazard.",
                "Garbage", Priority.HIGH, 74, ComplaintStatus.SUBMITTED,
                "Outer Ring Road near Dairy Farm", 28.6380, 77.2320, 6,
                0.88, "negative", "high",
                "Unattended animal carcass on pedestrian pathway creating biohazard.",
                "Sanitary hazard in public view requiring expedited municipal removal.",
                "Dispatch dead animal disposal squad with lime disinfectant powder.", false);

        createDemoComplaint("GWA-7003", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Prolonged Total Power Outage Exceeding 72 Hours",
                "Entire neighborhood of 250 families without electricity for 3 consecutive days due to burnt underground cable. Inverters exhausted.",
                "Electricity", Priority.HIGH, 82, ComplaintStatus.IN_PROGRESS,
                "Thatipur Colony Sector 2", 28.6190, 77.2110, 6,
                0.92, "negative", "high",
                "Extended electrical blackout over 72 hours affecting large residential pocket.",
                "Extended essential service disruption rule applied.",
                "Install temporary mobile generator or splice cable fault immediately.", false);

        createDemoComplaint("GWA-7004", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] 1-Kilometer Dark Streetlight Circuit in Crime-Prone Stretch",
                "Entire lighting circuit dark for 10 days along poorly patrolled transit road; multiple instances of bag snatching reported.",
                "Street Light", Priority.HIGH, 72, ComplaintStatus.ASSIGNED,
                "Hazira Circle towards Bypass", 28.6420, 77.2370, 8,
                0.87, "negative", "high",
                "Extensive lighting failure creating public safety and crime vulnerability.",
                "Public safety concern in poorly lit transit corridor.",
                "Inspect central timer control panel and replace blown contactor.", false);

        createDemoComplaint("GWA-7005", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Aggressive Stray Dog Pack Biting Schoolchildren",
                "Pack of 8 ferocious dogs residing in abandoned lot has attacked 4 pedestrians and bitten 2 children in the past 48 hours.",
                "Public Safety", Priority.HIGH, 79, ComplaintStatus.IN_PROGRESS,
                "Ward 12 Primary School Lane", 28.6160, 77.2070, 6,
                0.90, "negative", "high",
                "Aggressive animal behavior causing documented bite injuries to children.",
                "Active public injury and rabies hazard.",
                "Deploy municipal animal control team for capture and vaccination.", false);

        createDemoComplaint("GWA-7006", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Cluster of 15 Dengue Cases Demanding Immediate Vector Control",
                "Over 15 confirmed dengue hospitalizations in Block B due to stagnant water in nearby open plots. Urgent fogging needed.",
                "Healthcare", Priority.HIGH, 80, ComplaintStatus.SUBMITTED,
                "Block B Residential Enclave", 28.6290, 77.2210, 8,
                0.91, "negative", "high",
                "Vector-borne disease cluster threatening broader community outbreak.",
                "Public health emergency threshold reached.",
                "Deploy thermal smoke fogging machines and distribute abate larvicide.", false);

        createDemoComplaint("GWA-7007", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Municipal Primary School Boundary Wall Tilted Dangerously",
                "12-foot brick boundary wall leaning at 15 degrees towards pedestrian street after foundation softening from rain. Risk of collapse.",
                "Infrastructure", Priority.HIGH, 77, ComplaintStatus.ASSIGNED,
                "Girls High School Outer Boundary", 28.6210, 77.2130, 8,
                0.89, "negative", "high",
                "Unstable masonry perimeter wall threatening pedestrian collapse.",
                "Structural collapse hazard adjacent to children's walkway.",
                "Install temporary structural shoring and barricade sidewalk.", false);

        createDemoComplaint("GWA-7008", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Heavy Toxic Industrial Chemical Emissions at Night",
                "Chemical fabrication plant dumping acrid sulfurous fumes into air between midnight and 4 AM, causing eye burning and cough in colony.",
                "Pollution", Priority.HIGH, 73, ComplaintStatus.IN_PROGRESS,
                "Sector 3 Industrial Buffer Zone", 28.6470, 77.2430, 10,
                0.86, "negative", "high",
                "Unpermitted toxic air emissions causing acute respiratory irritation.",
                "Environmental and public health non-compliance.",
                "Dispatch pollution control inspection officer with air sampling meter.", false);

        createDemoComplaint("GWA-7009", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Reckless High-Speed Driving by City Bus Drivers",
                "City transit buses regularly racing each other through dense 20-foot bazaar road at 70 km/h, near-misses daily.",
                "Public Transport", Priority.HIGH, 71, ComplaintStatus.SUBMITTED,
                "Sadar Bazaar Main Road", 28.6170, 77.2060, 10,
                0.85, "negative", "high",
                "Public transport safety violations creating pedestrian collision risk.",
                "High pedestrian density coupled with dangerous vehicle speeds.",
                "Issue strict driver reprimand and deploy transit enforcement marshals.", false);

        // ==========================================
        // 10 MEDIUM DEMO COMPLAINTS
        // ==========================================
        createDemoComplaint("GWA-2309", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Overflowing Garbage Dumpster Near Community Clinic",
                "Secondary waste container has not been cleared for 4 days. Waste spilled onto footpath, severe stench and hygiene risk for patients visiting clinic.",
                "Garbage", Priority.MEDIUM, 52, ComplaintStatus.SUBMITTED,
                "Main Gate, Health Dispensary, Block D", 28.6400, 77.2300, 36,
                0.88, "negative", "medium",
                "Solid waste overflow obstructing dispensary footpath.",
                "Public health hazard due to medical facility proximity; medium priority.",
                "Reroute compactor truck for priority morning clearance.", false);

        createDemoComplaint("GWA-5001", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Erratic Drinking Water Supply Timing with Low Pressure",
                "Water arrives only for 20 minutes at 3 AM with insufficient pressure to reach rooftop tanks. Residents forced to stay awake.",
                "Water", Priority.MEDIUM, 48, ComplaintStatus.IN_PROGRESS,
                "Govindpuri Lane 8", 28.6260, 77.2190, 24,
                0.87, "negative", "medium",
                "Inadequate municipal water pressure disrupting household routines.",
                "Service delivery inconsistency without acute contamination.",
                "Regulate booster valves at zonal distribution reservoir.", false);

        createDemoComplaint("GWA-5002", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Uncovered Pipeline Trench with Loose Gravel on Roadway",
                "Contractor dug trench across street 2 weeks ago and filled only with loose gravel. Vehicles getting stuck during peak hours.",
                "Road", Priority.MEDIUM, 54, ComplaintStatus.ASSIGNED,
                "Maharaj Bada Link Road", 28.6145, 77.2095, 30,
                0.86, "negative", "medium",
                "Incomplete utility road reinstatement obstructing traffic flow.",
                "Moderate traffic disruption and vehicle undercarriage damage risk.",
                "Direct contractor to execute final bitumen resurfacing within 48 hours.", false);

        createDemoComplaint("GWA-5003", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Damaged Concrete Road Divider Allowing Illegal U-Turns",
                "Three segments of center median barrier smashed by truck, allowing scooters to take dangerous blind turns across opposing traffic.",
                "Road", Priority.MEDIUM, 56, ComplaintStatus.SUBMITTED,
                "Lashkar Outer Ring Road", 28.6330, 77.2230, 36,
                0.89, "negative", "medium",
                "Broken median barrier encouraging hazardous traffic maneuvers.",
                "Traffic safety deficiency requiring physical restoration.",
                "Install replacement precast concrete median blocks.", false);

        createDemoComplaint("GWA-5004", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Public Toilet Complex Taps Non-Functional and Flush Choked",
                "Community toilet block in market has dry taps and 3 choked stalls, causing unsanitary conditions for shopkeepers.",
                "Sanitation", Priority.MEDIUM, 50, ComplaintStatus.IN_PROGRESS,
                "Central Market Bus Stand Toilets", 28.6360, 77.2270, 24,
                0.88, "negative", "medium",
                "Civic sanitary convenience malfunction creating localized nuisance.",
                "Essential public hygiene amenity failure.",
                "Dispatch plumbing repair team to clear traps and restore water feed.", false);

        createDemoComplaint("GWA-5005", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Metal Streetlight Pole Leaning at 20 Degrees after Bump",
                "Delivery van grazed tubular steel lighting pole. Pole is tilted noticeably away from vertical; light still functions.",
                "Street Light", Priority.MEDIUM, 45, ComplaintStatus.ASSIGNED,
                "City Center Phase 2 Avenue", 28.6240, 77.2170, 36,
                0.85, "neutral", "medium",
                "Mechanically compromised lighting pole requiring plumb straightening.",
                "Non-urgent structural defect without immediate fall risk.",
                "Deploy crane utility truck to realign base bolts and grout.", false);

        createDemoComplaint("GWA-5006", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Silt Blockage in Stormwater Culvert under Crossroad",
                "Culvert under junction is 60% packed with sediment and plastic bottles, causing ponding of water during afternoon showers.",
                "Drainage", Priority.MEDIUM, 53, ComplaintStatus.SUBMITTED,
                "Patel Nagar Crossing Culvert", 28.6270, 77.2220, 30,
                0.86, "negative", "medium",
                "Culvert throat constriction predisposing junction to monsoon waterlogging.",
                "Preventative drainage clearance required before heavy rainfall.",
                "Deploy manual desilting gang to excavate accumulated silt.", false);

        createDemoComplaint("GWA-5007", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Frequent Commuter Bus Breakdowns on Route 7",
                "Morning 8:30 AM office commuter bus breaks down 3 days a week, stranding over 100 passengers on highway.",
                "Public Transport", Priority.MEDIUM, 46, ComplaintStatus.ASSIGNED,
                "VIP Road Bus Stop 4", 28.6430, 77.2390, 40,
                0.84, "negative", "medium",
                "Chronic transit fleet unreliability impacting daily commuters.",
                "Service delivery defect without physical hazard.",
                "Replace aging bus fleet on Route 7 with newly certified vehicles.", false);

        createDemoComplaint("GWA-5008", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Commercial Diesel Generator Noise Exceeding Permissible Decibels",
                "Commercial bakery generator operating without acoustic enclosure vibrating adjoining residential common wall throughout day.",
                "Pollution", Priority.MEDIUM, 47, ComplaintStatus.IN_PROGRESS,
                "Commercial Complex Basement, Sector 14", 28.6148, 77.2098, 48,
                0.87, "negative", "medium",
                "Noise and vibration nuisance in violation of residential zoning standards.",
                "Environmental standards grievance affecting resident quiet enjoyment.",
                "Serve compliance notice requiring acoustic canopy installation.", false);

        createDemoComplaint("GWA-5009", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Pedestrian Walkway Encroached by Commercial Display Kiosks",
                "Footpath outside shopping complex completely blocked by illegal advertising billboards and mannequin stands, forcing walking in traffic.",
                "Other", Priority.MEDIUM, 44, ComplaintStatus.SUBMITTED,
                "Sector 12 Shopping Arcades", 28.6510, 77.2410, 48,
                0.85, "neutral", "medium",
                "Sidewalk obstruction causing minor pedestrian spillover into roadway.",
                "Public space encroachment issue.",
                "Direct municipal enforcement squad to issue notices and remove unauthorized kiosks.", false);

        // ==========================================
        // 10 LOW DEMO COMPLAINTS
        // ==========================================
        createDemoComplaint("GWA-1188", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Broken Wooden Bench in Children Park",
                "Slats of one bench in the central walking park are detached and need nailing or replacement.",
                "Parks", Priority.LOW, 20, ComplaintStatus.RESOLVED,
                "Pocket C Green Park, Sector 12", 28.6500, 77.2400, 120,
                0.95, "neutral", "low",
                "Minor recreational park amenity maintenance.",
                "Non-hazardous routine park furniture repair.",
                "Schedule carpentry team for next routine maintenance cycle.", true);

        createDemoComplaint("GWA-1001", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Slight Drip from Public Drinking Fountain Spigot",
                "Water cooler tap in civic library forecourt has slow drip of approximately 1 drop every 10 seconds. No flooding.",
                "Water", Priority.LOW, 18, ComplaintStatus.RESOLVED,
                "Central Public Library Garden", 28.6215, 77.2135, 120,
                0.94, "neutral", "low",
                "Minor plumbing valve leak with negligible water loss.",
                "Routine civic amenity maintenance.",
                "Replace rubber faucet washer during scheduled weekly rounds.", true);

        createDemoComplaint("GWA-1002", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Overgrown Lawn Grass in Community Garden",
                "Walking track lawn grass is knee-high; request routine mowing before weekend community gathering.",
                "Parks", Priority.LOW, 22, ComplaintStatus.IN_PROGRESS,
                "Shivaji Park Sector 9", 28.6175, 77.2085, 96,
                0.93, "neutral", "low",
                "Routine horticulture lawn care request.",
                "Aesthetic and leisure maintenance without safety danger.",
                "Dispatch garden motorized lawnmower crew.", false);

        createDemoComplaint("GWA-1003", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Streetlight Timer 15 Minutes Out of Synchronization",
                "Automated streetlights in quiet residential close switch on 15 minutes before sunset while still bright.",
                "Street Light", Priority.LOW, 15, ComplaintStatus.RESOLVED,
                "Gulmohar Enclave Lane 2", 28.6310, 77.2215, 120,
                0.96, "neutral", "low",
                "Minor timing drift on automated photocell / timer relay.",
                "Operational energy efficiency adjustment.",
                "Recalibrate astronomical clock controller at distribution panel.", true);

        createDemoComplaint("GWA-1004", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Tree Pruning Branches Piled on Park Boundary",
                "Dry branches trimmed from neem trees last week are piled neatly in park corner awaiting pickup.",
                "Garbage", Priority.LOW, 25, ComplaintStatus.SUBMITTED,
                "Nehru Memorial Park East Gate", 28.6285, 77.2255, 96,
                0.92, "neutral", "low",
                "Horticultural green waste awaiting bulk logistics collection.",
                "Low priority non-odorous vegetative residue.",
                "Schedule open-bed truck for garden green waste pickup.", false);

        createDemoComplaint("GWA-1005", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Administrative Delay in Birth Certificate Processing",
                "Online birth certificate application submitted 25 days ago; status showing pending at document verification.",
                "Other", Priority.LOW, 19, ComplaintStatus.IN_PROGRESS,
                "Zonal Municipal Civic Center", 28.6195, 77.2115, 120,
                0.95, "neutral", "low",
                "Routine administrative certificate backlog enquiry.",
                "Non-urgent clerical workflow delay.",
                "Notify registrar desk to expedite certificate verification.", false);

        createDemoComplaint("GWA-1006", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Faded Bus Route Timetable Poster at Transit Shelter",
                "Printed paper schedule on passenger bus stop shelter is sun-faded and difficult to read.",
                "Public Transport", Priority.LOW, 16, ComplaintStatus.RESOLVED,
                "Subhash Nagar Bus Stop", 28.6235, 77.2165, 120,
                0.94, "neutral", "low",
                "Public transit information signage aesthetic wear.",
                "Informational amenity refresh.",
                "Laminate and mount updated transit timetable printout.", true);

        createDemoComplaint("GWA-1007", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Hairline Surface Crazing on Sidewalk Pavers",
                "Pedestrian walkway tiles show fine surface weathering cracks; pavers remain stable and firm underfoot.",
                "Road", Priority.LOW, 14, ComplaintStatus.SUBMITTED,
                "Anand Nagar Walkway", 28.6345, 77.2265, 120,
                0.93, "neutral", "low",
                "Cosmetic surface weathering on pedestrian pavers without trip hazard.",
                "Low priority infrastructure wear.",
                "Log for long-term paving upgrade cycle.", false);

        createDemoComplaint("GWA-1008", citizenId, "Amit Patel", "9876543210",
                "[SYNTHETIC DEMO DATA] Non-Aggressive Stray Dog Barking Intermittently at Night",
                "Single stray dog barks when night watchman passes on bicycle; request sterilization and checkup.",
                "Public Safety", Priority.LOW, 21, ComplaintStatus.SUBMITTED,
                "Fort View Enclave Back Lane", 28.6465, 77.2425, 96,
                0.91, "neutral", "low",
                "Isolated nighttime disturbance without aggression or bite hazard.",
                "Standard animal birth control and welfare request.",
                "Enroll animal in upcoming area ABC / sterilization camp.", false);

        createDemoComplaint("GWA-1009", citizenId, "Sunita Verma", "9876543211",
                "[SYNTHETIC DEMO DATA] Municipal Park Nameboard Lettering Peeling Off",
                "Two brass letters on entrance welcome board of Gandhi Park are detached.",
                "Parks", Priority.LOW, 12, ComplaintStatus.RESOLVED,
                "Gandhi Memorial Park Entrance", 28.6155, 77.2088, 120,
                0.95, "neutral", "low",
                "Park signage aesthetic detachment.",
                "Minor park aesthetic maintenance.",
                "Affix brass lettering with industrial adhesive.", true);

        log.info("  → Successfully seeded 40 realistic synthetic demo complaints (10 Critical, 10 High, 10 Medium, 10 Low).");
    }

    private void createDemoComplaint(String ticketId, Long citizenId, String citizenName, String mobile,
                                     String topic, String description, String category,
                                     Priority priority, int pScore, ComplaintStatus status,
                                     String address, double lat, double lon, int slaHours,
                                     double confidence, String sentiment, String riskLevel,
                                     String summary, String reasoning, String action,
                                     boolean isResolved) {
        if (complaintRepo.findByTicketId(ticketId).isPresent()) return;

        LocalDateTime deadline = LocalDateTime.now().plusHours(slaHours);
        LocalDateTime resolvedAt = isResolved ? LocalDateTime.now().minusHours(2) : null;

        Complaint c = complaintRepo.save(Complaint.builder()
                .ticketId(ticketId)
                .citizenId(citizenId)
                .citizenName(citizenName)
                .mobile(mobile)
                .topic(topic)
                .description(description)
                .category(category)
                .priority(priority)
                .priorityScore(pScore)
                .status(status)
                .address(address)
                .latitude(lat)
                .longitude(lon)
                .slaDeadline(deadline)
                .resolvedAt(resolvedAt)
                .build());

        analysisRepo.save(ComplaintAnalysis.builder()
                .complaint(c)
                .priority(priority)
                .priorityScore(pScore)
                .urgencyScore(Math.min(100, pScore + 3))
                .severityScore(pScore)
                .impactScore(Math.max(10, pScore - 5))
                .safetyScore(priority == Priority.CRITICAL ? 90 : (priority == Priority.HIGH ? 70 : 30))
                .durationScore(40)
                .confidence(confidence > 1.0 ? confidence / 100.0 : confidence)
                .sentiment(sentiment)
                .riskLevel(riskLevel)
                .aiSummary(summary)
                .reasoningSummary(reasoning)
                .recommendedAction(action)
                .build());

        slaRecordRepo.save(SLARecord.builder()
                .complaint(c)
                .priority(priority)
                .slaDeadline(deadline)
                .resolvedAt(resolvedAt)
                .isBreached(false)
                .resolutionTimeMinutes(isResolved ? 120 : null)
                .build());
    }
}
