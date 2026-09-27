"""
CivicPulse Synthetic Municipal Complaints Generator (500 Records)
Reproducible Seed: 42
Generates: data/complaints_500.csv and data/complaints_500.json
"""

import csv
import json
import random
from pathlib import Path
from collections import Counter

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "data"

# CivicPulse Official Category Configuration
CATEGORIES_SPEC = {
    "Water Supply": {
        "subcategories": ["Pipeline Rupture", "Contaminated Water", "No Supply / Low Pressure", "Erratic Supply", "Tanker Issue"],
        "essential": True,
        "base_risk": "high"
    },
    "Electricity": {
        "subcategories": ["Live Wire / Sparking", "Transformer Failure", "Power Outage / Blackout", "Voltage Fluctuation", "Tilted Pole"],
        "essential": True,
        "base_risk": "high"
    },
    "Roads": {
        "subcategories": ["Dangerous Pothole", "Collapsed Road / Crater", "Broken Divider", "Open Trench / Debris", "Speed Breaker"],
        "essential": False,
        "base_risk": "medium"
    },
    "Sanitation": {
        "subcategories": ["Open Manhole", "Sewage Overflow", "Choked Drain / Gutter", "Public Toilet Hygiene", "Stench / Biowaste"],
        "essential": True,
        "base_risk": "high"
    },
    "Garbage/Waste": {
        "subcategories": ["Overflowing Dumpster", "Littering / Debris", "Uncollected Waste", "Illegal Dumping", "Dead Animal Removal"],
        "essential": True,
        "base_risk": "medium"
    },
    "Streetlights": {
        "subcategories": ["Broken Bulb / Dark Street", "Flickering Light", "Damaged Pole", "Exposed Streetlight Wire", "Timer Fault"],
        "essential": False,
        "base_risk": "medium"
    },
    "Public Safety": {
        "subcategories": ["Hit-and-Run", "Fire Emergency", "Theft / Robbery", "Violent Incident / Assault", "Dangerous Stray Animal"],
        "essential": False,
        "base_risk": "critical"
    },
    "Drainage": {
        "subcategories": ["Monsoon Flooding", "Blocked Culvert", "Stormwater Gutter Overflow", "Waterlogged Road", "Sump Pump Failure"],
        "essential": True,
        "base_risk": "high"
    },
    "Parks": {
        "subcategories": ["Broken Swings / Playground", "Damaged Bench / Walking Track", "Overgrown Grass", "Fountain Fault", "Boundary Damage"],
        "essential": False,
        "base_risk": "low"
    },
    "Healthcare": {
        "subcategories": ["Hospital Emergency / No Doctor", "Medicine Shortage", "Disease Outbreak / Dengue", "Ambulance Delay", "Clinic Hygiene"],
        "essential": True,
        "base_risk": "critical"
    },
    "Public Transport": {
        "subcategories": ["Bus Breakdown / Cancelled", "Rash Driving", "Bus Shelter Damaged", "Fare Overcharging", "Route Deviation"],
        "essential": True,
        "base_risk": "medium"
    },
    "Infrastructure": {
        "subcategories": ["Bridge Crack / Sinking", "Unsafe Dilapidated Building", "Boundary Wall Collapse", "Footbridge Damage", "Subway Flooding"],
        "essential": False,
        "base_risk": "high"
    },
    "Environment": {
        "subcategories": ["Industrial Air Pollution", "Severe Noise Pollution", "Illegal Tree Felling", "Chemical Odor / Fumes", "Dust from Construction"],
        "essential": False,
        "base_risk": "medium"
    },
    "Other": {
        "subcategories": ["Certificate Delay", "Staff Grievance", "Encroachment", "Tax Discrepancy", "General Civic Inquiry"],
        "essential": False,
        "base_risk": "low"
    }
}

LOCATIONS = [
    "Sector 14 Market Chowk", "Railway Station Road", "Maharaj Bada", "Thatipur Main Crossing",
    "Hazira Circle", "Morar Colony", "City Center Phase 2", "Gandhi Nagar Block B",
    "Lashkar Outer Ring Road", "VIP Road near Airport", "Govindpuri Lane 4",
    "Sadar Bazaar Main Gali", "Ward 12 Primary School Road", "Patel Nagar Bus Stand",
    "Civil Hospital Outer Gate", "Industrial Area Sector 3", "Subhash Nagar Park Road",
    "Fort View Enclave", "Anand Nagar", "Kampoo Road"
]

HINDI_LOCATIONS = [
    "सेक्टर 14 मार्केट चौक", "रेलवे स्टेशन रोड", "महाराज बाड़ा", "थाटीपुर चौराहा",
    "हजीरा सर्कल", "मुरार कॉलोनी", "सिटी सेंटर", "गांधी नगर ब्लॉक बी",
    "लश्कर आउटर रिंग रोड", "वीआईपी रोड", "सदर बाजार", "वार्ड 12 सरकारी स्कूल के पास",
    "सिविल अस्पताल गेट 2", "इंडस्ट्रियल एरिया", "आनंद नगर"
]

def generate_records():
    records = []
    rec_id = 1

    # Base seed samples for core categories
    # Each entry: (category, subcategory, text_en, text_hi, text_hinglish, typos, safety_risk, severity, priority)
    templates = [
        # 1. WATER SUPPLY
        ("Water Supply", "Pipeline Rupture", 
         "Main high-pressure water supply pipeline burst near {loc}, thousands of liters of clean drinking water flooding streets and basements.",
         "{loc} के पास मुख्य पेयजल पाइपलाइन फूट गई है, लाखों लीटर साफ पानी सड़क और बेसमेंट में भर रहा है।",
         "{loc} ke paas main water line phoot gayi hai, bohot zyada drinking water waste ho raha hai aur waterlogging ho gayi.",
         "Mian water pipline bursted near {loc}, clean watr wasting on road.",
         55, 85, "CRITICAL"),

        ("Water Supply", "Contaminated Water",
         "Contaminated brownish dirty water with foul sewer smell coming through municipal taps in {loc} for {dur}. Multiple families falling sick.",
         "{loc} में पिछले {dur} से नलों में सीवर का बदबूदार गंदा पानी आ रहा है, कई बच्चे उल्टी-दस्त से बीमार हैं।",
         "{loc} me municipal taps se black dirty water aa raha hai {dur} se, peene layak nahi hai infection ka darr hai.",
         "Drity stinking watr comming in house taps at {loc} since {dur}.",
         65, 80, "CRITICAL"),

        ("Water Supply", "No Supply / Low Pressure",
         "Complete water supply shutdown in {loc} for {dur}. Residents have zero drinking water and private tankers charging exorbitant rates.",
         "{loc} में पिछले {dur} से पानी की एक बूंद नहीं आई है, पूरी कॉलोनी में हाहाकार मचा हुआ है।",
         "{loc} me {dur} se bilkul paani nahi aaya, residents are buying private water tankers at high price.",
         "No watr supply in {loc} for {dur}, please restrore.",
         30, 60, "HIGH"),

        ("Water Supply", "Tanker Issue",
         "Municipal drinking water tanker failed to arrive in {loc} despite scheduled slot during peak summer heat.",
         "{loc} में नगर निगम का पानी का टैंकर समय पर नहीं पहुंचा, लोग धूप में खाली बर्तन लेकर खड़े हैं।",
         "{loc} me water tanker dispatch nahi hua, public pareshan hai paani ke bina.",
         "Watr tanker did not arive at {loc}.",
         20, 45, "MEDIUM"),

        # 2. ELECTRICITY
        ("Electricity", "Live Wire / Sparking",
         "Snaped 11kV live electric wire hanging dangerously across pedestrian footpath outside school gate in {loc}. Sparking in puddle.",
         "{loc} में स्कूल गेट के ठीक बाहर 11kV का हाई-वोल्टेज करंट वाला तार टूटकर लटक रहा है, बारिश के पानी में स्पार्किंग हो रही है।",
         "{loc} me school ke samne live high tension wire gir gaya hai, continuously spark ho raha hai bada current lag sakta hai.",
         "Liev electrc wire hanging near school in {loc}, dangrous spark.",
         95, 95, "CRITICAL"),

        ("Electricity", "Transformer Failure",
         "Distribution transformer exploded with loud blast and caught fire near residential building in {loc}, black smoke billowing.",
         "{loc} में रिहायशी इमारत के पास ट्रांसफार्मर में जोरदार धमाका हुआ और भीषण आग लग गई है।",
         "{loc} me transformer blast ho gaya aur aag lag gayi hai, immediate electricity cut aur fire brigade chahiye.",
         "Transfomer blased and burnig in {loc}.",
         90, 92, "CRITICAL"),

        ("Electricity", "Power Outage / Blackout",
         "Continuous power outage for {dur} in {loc}. Inverters dead, senior citizens and patients facing severe distress.",
         "{loc} में पिछले {dur} से बिजली पूरी तरह गुल है, भीषण गर्मी में मरीज और बुजुर्ग बेहाल हैं।",
         "{loc} me {dur} se light gayab hai, blackout chal raha hai transformer repair nahi hua.",
         "Total power cut in {loc} since {dur}.",
         35, 65, "HIGH"),

        ("Electricity", "Voltage Fluctuation",
         "Severe voltage fluctuations between 120V and 310V in {loc} burning home appliances and tube lights.",
         "{loc} में बिजली का वोल्टेज बहुत तेजी से कम-ज्यादा हो रहा है, फ्रिज और टीवी जल चुके हैं।",
         "{loc} me severe voltage fluctuation ho raha hai appliances jal rahe hain.",
         "Voltge fluctuation damging electronics in {loc}.",
         40, 55, "MEDIUM"),

        # 3. ROADS
        ("Roads", "Collapsed Road / Crater",
         "Road has caved in creating a 5-foot deep crater on main corridor in {loc}. Two-wheelers falling and multiple riders injured.",
         "{loc} में मुख्य सड़क अचानक 5 फीट धंस गई है, दो बाइक सवार गिरकर गंभीर रूप से घायल हो गए हैं।",
         "{loc} me road cave in ho gayi hai bohot bada crater ban gaya, kal raat 2 log gir kar hospital pahunch gaye.",
         "Deep crator on mein road at {loc}, pepole faling.",
         85, 88, "CRITICAL"),

        ("Roads", "Dangerous Pothole",
         "Cluster of 8 deep jagged potholes near blind turn on {loc}. Constant skidding and bumper damage to cars.",
         "{loc} के अंधे मोड़ पर गहरे नुकीले गड्ढे हैं, आए दिन गाड़ियां फिसल रही हैं और दुर्घटनाएं हो रही हैं।",
         "{loc} me road pe bohot saare dangerous potholes hain, heavy traffic jam aur daily accidents ho rahe hain.",
         "Hug pothole on turn at {loc} repare immidiately.",
         50, 70, "HIGH"),

        ("Roads", "Broken Divider",
         "Concrete road divider broken and dislodged in {loc}, vehicles taking illegal dangerous head-on U-turns.",
         "{loc} में सीमेंट का डिवाइडर टूट गया है, लोग उल्टी दिशा से वाहन निकाल रहे हैं जिससे हादसे हो रहे हैं।",
         "{loc} me divider toota hua hai, wrong side driving ho rahi hai crash hone ka risk hai.",
         "Brokn devider in {loc}.",
         40, 55, "MEDIUM"),

        ("Roads", "Open Trench / Debris",
         "Contractor left 40-meter uncovered trench with loose gravel across road in {loc} with zero signage.",
         "{loc} में सड़क के बीचोंबीच 40 मीटर लंबा गहरा गड्ढा खोदकर बिना किसी चेतावनी बोर्ड के छोड़ दिया गया है।",
         "{loc} me road khod ke chhod diya hai contractor ne, gravel spread hai bikes skid ho rahi hain.",
         "Open trnch on road side in {loc}.",
         45, 60, "MEDIUM"),

        # 4. SANITATION
        ("Sanitation", "Open Manhole",
         "Open uncovered sewer manhole right in the middle of pedestrian walking path near market in {loc}. Fatal falling risk at night.",
         "{loc} में बाजार के पैदल रास्ते पर बिना ढक्कन का खुला मैनहोल है, अंधेरे में किसी की भी जान जा सकती है।",
         "{loc} me market ke footpath pe open sewer manhole hai bina kisi cover ke, bacche gir sakte hain.",
         "Opn sewer manhol on footpath in {loc} dangreous.",
         90, 92, "CRITICAL"),

        ("Sanitation", "Sewage Overflow",
         "Blocked underground sewer line overflowing filthy black sewage on colony street in {loc} for {dur}. Foul smell everywhere.",
         "{loc} में पिछले {dur} से सीवर लाइन चोक होने से गंदा काला पानी पूरी सड़क पर बह रहा है, घरों के दरवाजे तक भर गया है।",
         "{loc} me sewer overflow ho raha hai {dur} se, footpath aur road gande paani se bhari hai.",
         "Sewge ovrflow on road at {loc} for {dur}.",
         60, 75, "HIGH"),

        ("Sanitation", "Public Toilet Hygiene",
         "Public toilet complex in {loc} has choked flush, non-functional taps, and feces piled up with no maintenance.",
         "{loc} का सार्वजनिक शौचालय पूरी तरह चोक है, गंदगी और दुर्गंध से आसपास खड़े रहना भी मुश्किल है।",
         "{loc} me public toilet condition is extremely unhygienic, no water in taps.",
         "Publc tolet dirty and choked at {loc}.",
         30, 50, "MEDIUM"),

        # 5. GARBAGE / WASTE
        ("Garbage/Waste", "Overflowing Dumpster",
         "Massive municipal garbage dump in {loc} not cleared for {dur}. Rotten waste spilled across road, stray dogs scavenging.",
         "{loc} में पिछले {dur} से कचरा पेटी खाली नहीं की गई है, सड़ा हुआ कूड़ा सड़क पर बिखर गया है और आवारा कुत्ते घूम रहे हैं।",
         "{loc} me {dur} se kooda nahi uthaya gaya, pura garbage open road pe spread hai aur smell aa rahi hai.",
         "Garbg not picked up from {loc} for {dur}.",
         35, 60, "MEDIUM"),

        ("Garbage/Waste", "Dead Animal Removal",
         "Dead stray cow/pig decomposing on roadside in {loc} for 2 days, causing unbearable stench and severe infection hazard.",
         "{loc} में सड़क किनारे 2 दिन से मृत पशु पड़ा सड़ रहा है, तीव्र दुर्गंध से सांस लेना मुश्किल है।",
         "{loc} me dead animal pada hua hai 2 din se, please sanitary squad bhejiye urgently.",
         "Ded animl on roadside at {loc}.",
         65, 80, "HIGH"),

        ("Garbage/Waste", "Littering / Debris",
         "Construction rubble and plastic waste dumped illegally on community green belt in {loc}.",
         "{loc} में ग्रीन बेल्ट पर अवैध रूप से भारी मात्रा में मलबा और प्लास्टिक कचरा फेंक दिया गया है।",
         "{loc} me road side illegal debris and construction waste dump kar diya hai.",
         "Illegl dumping of malba in {loc}.",
         20, 40, "LOW"),

        # 6. STREETLIGHTS
        ("Streetlights", "Broken Bulb / Dark Street",
         "Entire 800-meter stretch of streetlights dark in {loc} for {dur}. Pitch dark at night, woman safety and theft concern.",
         "{loc} में पिछले {dur} से पूरी सड़क की स्ट्रीट लाइटें बंद हैं, शाम होते ही घना अंधेरा छा जाता है जिससे अपराध का खतरा है।",
         "{loc} me complete darkness hai {dur} se, street lights nahi jal rahi ladies safe feel nahi karti.",
         "Stret lights not workng in {loc} since {dur}.",
         45, 65, "MEDIUM"),

        ("Streetlights", "Exposed Streetlight Wire",
         "Bottom inspection door of streetlight pole broken in {loc}, raw uninsulated live wires accessible to playing children.",
         "{loc} में खंभे के नीचे का जंक्शन बॉक्स खुला है, नंगे बिजली के तार बाहर निकले हैं जहां बच्चे खेलते हैं।",
         "{loc} me street light pole ke open wires hain low height pe, kisi bache ko current lag sakta hai.",
         "Opn live wire in streetlite pole at {loc}.",
         85, 88, "CRITICAL"),

        ("Streetlights", "Damaged Pole",
         "Iron streetlight pole struck by truck in {loc}, leaning at 60 degree angle over roadway.",
         "{loc} में स्ट्रीट लाइट का लोहे का खंभा झुक गया है और सड़क पर गिर सकता है।",
         "{loc} me pole tedha ho gaya hai collision ke baad, kabhi bhi road pe crash ho sakta hai.",
         "Light pole tilted in {loc}.",
         55, 70, "HIGH"),

        # 7. PUBLIC SAFETY
        ("Public Safety", "Hit-and-Run",
         "Hit and run incident in {loc}: A speeding black SUV struck a pedestrian and fled toward highway. Victim seriously injured, vehicle plate fragment MP07 AB 2.",
         "{loc} में हिट एंड रन: तेज रफ्तार काली गाड़ी ने पैदल यात्री को जोरदार टक्कर मारी और भाग गई। व्यक्ति सड़क पर गंभीर घायल पड़ा है।",
         "{loc} me hit and run accident hua, car hit a pedestrian and fled toward highway, victim injured bleeding heavily.",
         "Hit and run accidnt at {loc}, persn injured, vehicl fled.",
         95, 96, "CRITICAL"),

        ("Public Safety", "Fire Emergency",
         "Major fire broke out in chemical storage shop in {loc}, huge flames and thick poisonous smoke entering adjacent apartments.",
         "{loc} में रासायनिक गोदाम में भीषण आग लग गई है, ऊंची लपटें और जहरीला धुआं घरों में घुस रहा है।",
         "{loc} me godown me massive fire lag gayi hai, surrounding buildings evacuate karwani pad rahi hai.",
         "Huge fire blaze in shop at {loc} urgnt fire truck.",
         98, 98, "CRITICAL"),

        ("Public Safety", "Theft / Robbery",
         "Armed chain snatching and robbery by two men on black motorbike with country pistols in {loc} around 8 PM.",
         "{loc} में शाम 8 बजे बाइक सवार दो अज्ञात बदमाशों ने तमंचे की नोक पर महिला से चेन और बैग लूट लिया।",
         "{loc} me gun point robbery hui hai market se aate waqt, police patrolling badhaiye.",
         "Robbry with weapn in {loc}.",
         80, 85, "CRITICAL"),

        ("Public Safety", "Dangerous Stray Animal",
         "Pack of 6 aggressive rabid stray dogs attacking school children and cyclists in {loc}, 3 people bitten today.",
         "{loc} में पागल आवारा कुत्तों का झुंड लोगों पर हमला कर रहा है, आज 3 बच्चों को बुरी तरह काट लिया है।",
         "{loc} me stray dogs attacking pedestrians, rabies risk hai dog catcher team bhejiye.",
         "Agressiv stray dog biting peple in {loc}.",
         75, 80, "HIGH"),

        # 8. DRAINAGE
        ("Drainage", "Monsoon Flooding",
         "Stormwater drain choked in {loc}. Torrential rainwater backflowing into 30 houses with 3-foot waterlogging.",
         "{loc} में बरसाती नाला चोक होने से 3 फीट गंदा पानी 30 से अधिक घरों के अंदर घुस गया है, संपत्ति बर्बाद हो रही है।",
         "{loc} me drainage blocked hai, 3 feet water logging ho gayi hai aur water gharon me enter kar raha hai.",
         "Water loging in houses at {loc} drain chokd.",
         70, 85, "CRITICAL"),

        ("Drainage", "Blocked Culvert",
         "Culvert bridge under road in {loc} completely jammed with silt and plastic bottles, runoff overflowing onto road.",
         "{loc} में पुलिया के नीचे नाला प्लास्टिक और कचरे से पूरी तरह पट गया है, पानी सड़क के ऊपर से बह रहा है।",
         "{loc} me culvert choked hone se water logging ho rahi hai roads pe.",
         "Drain pulia chokd at {loc}.",
         40, 60, "MEDIUM"),

        # 9. PARKS
        ("Parks", "Broken Swings / Playground",
         "Children iron slide in municipal park at {loc} has rusted broken sharp edge, caused deep cut to 6-year-old child.",
         "{loc} के पार्क में बच्चों का लोहे का झूला टूट गया है और धारदार पत्ती निकली हुई है जिससे बच्चे को गहरा घाव लगा।",
         "{loc} ke park me swings broken hain aur rusted iron exposed hai jo dangerous hai kids ke liye.",
         "Brokn childrn swing in park at {loc}.",
         65, 75, "HIGH"),

        ("Parks", "Damaged Bench / Walking Track",
         "Wooden park benches have broken slats and walking track paving is uneven in {loc}.",
         "{loc} के सार्वजनिक पार्क में बेंच टूटी पड़ी हैं और वॉकिंग ट्रैक की टाइलें उखड़ गई हैं।",
         "{loc} park me benches tooti hui hain repair chahiye.",
         "Park bench brokn at {loc}.",
         10, 25, "LOW"),

        ("Parks", "Overgrown Grass",
         "Wild bushes and knee-high grass in community park at {loc} harboring snakes and mosquitoes.",
         "{loc} के पार्क में बड़ी-बड़ी घास और झाड़ियां उग आई हैं, सांप-बिच्छू निकलने का डर है।",
         "{loc} park me grass cutting nahi hui hai kaafi time se.",
         "Grass overgroan in park at {loc}.",
         15, 30, "LOW"),

        # 10. HEALTHCARE
        ("Healthcare", "Hospital Emergency / No Doctor",
         "Civil dispensary in {loc} has no doctor or nursing staff present during emergency hours, trauma patient bleeding outside.",
         "{loc} के प्राथमिक स्वास्थ्य केंद्र में इमरजेंसी में कोई डॉक्टर उपस्थित नहीं है, सड़क हादसे का मरीज तड़प रहा है।",
         "{loc} ke hospital emergency me koi doctor nahi hai, urgent medical assistance needed.",
         "No docter in hospitl at {loc} emergency.",
         95, 95, "CRITICAL"),

        ("Healthcare", "Disease Outbreak / Dengue",
         "Over 15 confirmed dengue and viral fever cases reported in {loc} due to stagnant water, urgent mosquito fogging required.",
         "{loc} में रुके हुए पानी से 15 से ज्यादा लोग डेंगू और मलेरिया से पीड़ित हैं, तुरंत फागिंग कराई जाए।",
         "{loc} me dengue outbreak ho gaya hai, municipal fogging and larvae spray karwayein.",
         "Dengue casis in {loc} need foging.",
         70, 80, "HIGH"),

        ("Healthcare", "Medicine Shortage",
         "Free medicine dispensary in {loc} running out of basic ORS, fever paracetamol, and diabetes tablets for 3 weeks.",
         "{loc} के सरकारी दवा केंद्र में आवश्यक दवाएं और ओआरएस उपलब्ध नहीं हैं, गरीब मरीज परेशान हैं।",
         "{loc} dispensery me basic medicines out of stock hain pichle 3 weeks se.",
         "No medicins in gov clinic {loc}.",
         35, 50, "MEDIUM"),

        # 11. PUBLIC TRANSPORT
        ("Public Transport", "Rash Driving",
         "City bus route 7 driver driving recklessly at 80 km/h in narrow market zone in {loc}, narrowly missed schoolchildren.",
         "{loc} के बाजार में सिटी बस चालक अत्यधिक तेज गति और लापरवाही से गाड़ी चला रहा है, बड़ा हादसा हो सकता है।",
         "{loc} me city bus rash driving kar rahi hai continuously in market area.",
         "City bus rash drivng at {loc}.",
         60, 70, "HIGH"),

        ("Public Transport", "Bus Breakdown / Cancelled",
         "Morning commuter bus consistently breaks down near {loc} causing hundreds of office workers to get stranded.",
         "{loc} पर सुबह की नगर बस आए दिन खराब हो जाती है जिससे दैनिक यात्रियों को भारी परेशानी होती है।",
         "{loc} pe daily bus breakdown ho jati hai, route timing irregular hai.",
         "Bus breakdwn daily at {loc}.",
         25, 45, "MEDIUM"),

        # 12. INFRASTRUCTURE
        ("Infrastructure", "Bridge Crack / Sinking",
         "Flyover expansion joint in {loc} has widened by 4 inches and concrete chunks are crumbling down onto traffic below.",
         "{loc} के फ्लाईओवर के जॉइंट में 4 इंच चौड़ी दरार आ गई है और कंक्रीट का मलबा नीचे वाहनों पर गिर रहा है।",
         "{loc} flyover bridge joint me severe crack aa gaya hai aur concrete gir raha hai, structural audit chahiye.",
         "Bridg crack expnsion joint at {loc}.",
         92, 94, "CRITICAL"),

        ("Infrastructure", "Boundary Wall Collapse",
         "Municipal school 10-foot boundary wall has tilted dangerously toward road in {loc} following heavy rains.",
         "{loc} में भारी बारिश के बाद स्कूल की 10 फीट ऊंची चारदीवारी झुक गई है और किसी भी समय गिर सकती है।",
         "{loc} me old boundary wall is tilting towards main road, collapse hazard.",
         "Wall collaps hazard near road {loc}.",
         75, 80, "HIGH"),

        # 13. ENVIRONMENT
        ("Environment", "Industrial Air Pollution",
         "Chemical factory near {loc} releasing thick black acrid chemical smoke and sulfur smell every night after 11 PM.",
         "{loc} के पास रासायनिक फैक्ट्री रात 11 बजे के बाद जहरीला काला धुआं छोड़ती है जिससे लोगों का दम घुट रहा है।",
         "{loc} me night time toxic chemical fumes release ho rahe hain industrial area se, breathing difficulty ho rahi hai.",
         "Air polluton toxic smk from factory at {loc}.",
         65, 75, "HIGH"),

        ("Environment", "Severe Noise Pollution",
         "Unlicensed commercial diesel generator running 24x7 without acoustic enclosure directly beneath bedrooms in {loc}.",
         "{loc} में आवासीय फ्लैट्स के नीचे अवैध तेज आवाज वाला जनरेटर 24 घंटे चल रहा है जिससे ध्वनि प्रदूषण हो रहा है।",
         "{loc} me heavy noise pollution ho raha hai illegal commercial generator se.",
         "Noise polution by big genrator in {loc}.",
         25, 45, "MEDIUM"),

        # 14. OTHER
        ("Other", "Certificate Delay",
         "Birth and death certificate counter at zonal municipal office in {loc} has kept application pending for 45 days.",
         "{loc} नगर निगम कार्यालय में जन्म प्रमाण पत्र का आवेदन 45 दिन से बिना किसी कारण के अटका हुआ है।",
         "{loc} municipal ward office me birth certificate issue nahi kar rahe 45 days se.",
         "Certifcat delay in ward offce {loc}.",
         10, 30, "LOW"),

        ("Other", "Encroachment",
         "Illegal commercial vendor stalls encroaching 70% of pedestrian walkway outside shopping complex in {loc}.",
         "{loc} में फुटपाथ पर अवैध रूप से दुकानें लगाकर रास्ता रोक लिया गया है, पैदल चलने वालों को सड़क पर चलना पड़ रहा है।",
         "{loc} me complete footpath encroachment ho gaya hai illegal shops se.",
         "Footpatah encrochment by illegal stalls at {loc}.",
         20, 45, "MEDIUM")
    ]

    durations = ["2 hours", "6 hours", "24 hours", "2 days", "4 days", "1 week", "2 weeks"]
    durations_hi = ["2 घंटे", "6 घंटे", "24 घंटे", "2 दिन", "4 दिन", "1 हफ्ते", "2 हफ्ते"]

    # We need EXACTLY 500 records with rich variation across categories, languages, lengths, and styles
    total_target = 500
    seen_texts = set()
    
    # 1. Generate 7 English variants per template (35 * 7 = 245)
    for tmpl in templates:
        cat, subcat, en_t, hi_t, hing_t, typo_t, s_risk, sev, prio = tmpl
        locs_chosen = random.sample(LOCATIONS, min(7, len(LOCATIONS)))
        for loc in locs_chosen:
            dur = random.choice(durations)
            text = en_t.format(loc=loc, dur=dur)
            if text not in seen_texts and len(records) < total_target:
                seen_texts.add(text)
                p_score = sev if prio == "CRITICAL" else max(15, sev - random.randint(0, 5))
                records.append({
                    "id": f"SYN-{rec_id:04d}",
                    "complaint_text": text,
                    "language": "en",
                    "category": cat,
                    "subcategory": subcat,
                    "sentiment": "very_negative" if prio in ["CRITICAL", "HIGH"] else "negative",
                    "severity": round(sev / 20.0, 1), # 1.0 - 5.0 scale
                    "public_impact": round(random.randint(60, 95) / 20.0, 1) if prio in ["CRITICAL", "HIGH"] else round(random.randint(20, 55) / 20.0, 1),
                    "safety_risk": round(s_risk / 20.0, 1),
                    "service_disruption": round(random.randint(50, 90) / 20.0, 1) if CATEGORIES_SPEC.get(cat, {}).get("essential") else round(random.randint(10, 40) / 20.0, 1),
                    "duration": dur,
                    "priority": prio,
                    "priority_score": p_score
                })
                rec_id += 1

    # 2. Generate 2 Hindi Devanagari variants per template (35 * 2 = 70)
    for tmpl in templates:
        cat, subcat, en_t, hi_t, hing_t, typo_t, s_risk, sev, prio = tmpl
        locs_chosen = random.sample(HINDI_LOCATIONS, min(2, len(HINDI_LOCATIONS)))
        for loc in locs_chosen:
            dur = random.choice(durations_hi)
            text = hi_t.format(loc=loc, dur=dur)
            if text not in seen_texts and len(records) < total_target:
                seen_texts.add(text)
                p_score = sev if prio == "CRITICAL" else max(15, sev - random.randint(0, 5))
                records.append({
                    "id": f"SYN-{rec_id:04d}",
                    "complaint_text": text,
                    "language": "hi",
                    "category": cat,
                    "subcategory": subcat,
                    "sentiment": "very_negative" if prio in ["CRITICAL", "HIGH"] else "negative",
                    "severity": round(sev / 20.0, 1),
                    "public_impact": round(random.randint(60, 95) / 20.0, 1) if prio in ["CRITICAL", "HIGH"] else round(random.randint(20, 55) / 20.0, 1),
                    "safety_risk": round(s_risk / 20.0, 1),
                    "service_disruption": round(random.randint(50, 90) / 20.0, 1) if CATEGORIES_SPEC.get(cat, {}).get("essential") else round(random.randint(10, 40) / 20.0, 1),
                    "duration": dur,
                    "priority": prio,
                    "priority_score": p_score
                })
                rec_id += 1

    # 3. Generate 2 Hinglish variants per template (35 * 2 = 70)
    for tmpl in templates:
        cat, subcat, en_t, hi_t, hing_t, typo_t, s_risk, sev, prio = tmpl
        locs_chosen = random.sample(LOCATIONS, min(2, len(LOCATIONS)))
        for loc in locs_chosen:
            dur = random.choice(durations)
            text = hing_t.format(loc=loc, dur=dur)
            if text not in seen_texts and len(records) < total_target:
                seen_texts.add(text)
                p_score = sev if prio == "CRITICAL" else max(15, sev - random.randint(0, 5))
                records.append({
                    "id": f"SYN-{rec_id:04d}",
                    "complaint_text": text,
                    "language": "hinglish",
                    "category": cat,
                    "subcategory": subcat,
                    "sentiment": "negative",
                    "severity": round(sev / 20.0, 1),
                    "public_impact": round(random.randint(50, 85) / 20.0, 1),
                    "safety_risk": round(s_risk / 20.0, 1),
                    "service_disruption": round(random.randint(40, 80) / 20.0, 1),
                    "duration": dur,
                    "priority": prio,
                    "priority_score": p_score
                })
                rec_id += 1

    # 4. Generate 2 Typo / Casual variants per template (35 * 2 = 70)
    for tmpl in templates:
        cat, subcat, en_t, hi_t, hing_t, typo_t, s_risk, sev, prio = tmpl
        locs_chosen = random.sample(LOCATIONS, min(2, len(LOCATIONS)))
        for loc in locs_chosen:
            dur = random.choice(durations)
            text = typo_t.format(loc=loc, dur=dur)
            if text not in seen_texts and len(records) < total_target:
                seen_texts.add(text)
                p_score = sev if prio == "CRITICAL" else max(15, sev - random.randint(0, 5))
                records.append({
                    "id": f"SYN-{rec_id:04d}",
                    "complaint_text": text,
                    "language": "en",
                    "category": cat,
                    "subcategory": subcat,
                    "sentiment": "negative",
                    "severity": round(sev / 20.0, 1),
                    "public_impact": round(random.randint(40, 75) / 20.0, 1),
                    "safety_risk": round(s_risk / 20.0, 1),
                    "service_disruption": round(random.randint(30, 70) / 20.0, 1),
                    "duration": dur,
                    "priority": prio,
                    "priority_score": p_score
                })
                rec_id += 1

    # Pass 5: Short / Ambiguous / Low Priority complaints to round out to exact 500
    short_extras = [
        ("Water Supply", "Pipeline Rupture", "Water leakage on street", "en", "LOW", 1.5, 20),
        ("Water Supply", "No Supply / Low Pressure", "पानी नहीं आ रहा", "hi", "LOW", 2.0, 30),
        ("Electricity", "Power Outage / Blackout", "Power cut in colony", "en", "LOW", 2.0, 25),
        ("Electricity", "Power Outage / Blackout", "Light chali gayi hai", "hinglish", "LOW", 2.0, 25),
        ("Roads", "Dangerous Pothole", "Pothole on main road", "en", "MEDIUM", 2.5, 45),
        ("Roads", "Dangerous Pothole", "सड़क पर गड्ढा", "hi", "MEDIUM", 2.5, 45),
        ("Sanitation", "Sewage Overflow", "Gutter overflow", "en", "MEDIUM", 3.0, 50),
        ("Sanitation", "Sewage Overflow", "नाली चोक हो गई है", "hi", "MEDIUM", 3.0, 50),
        ("Garbage/Waste", "Overflowing Dumpster", "Garbage not picked", "en", "LOW", 2.0, 30),
        ("Garbage/Waste", "Overflowing Dumpster", "कचरा पड़ा है", "hi", "LOW", 2.0, 30),
        ("Streetlights", "Broken Bulb / Dark Street", "Street light not working", "en", "LOW", 1.5, 25),
        ("Streetlights", "Broken Bulb / Dark Street", "खंभे की लाइट बंद है", "hi", "LOW", 1.5, 25),
        ("Parks", "Damaged Bench / Walking Track", "Broken bench in park", "en", "LOW", 1.0, 20),
        ("Parks", "Overgrown Grass", "पार्क में घास बड़ी हो गई", "hi", "LOW", 1.0, 15),
        ("Public Safety", "Dangerous Stray Animal", "Stray dogs barking loudly at night", "en", "LOW", 1.5, 25),
        ("Public Safety", "Hit-and-Run", "गाड़ी ने टक्कर मार दी और भाग गया", "hi", "CRITICAL", 4.8, 90),
        ("Drainage", "Monsoon Flooding", "Water accumulation after rain", "en", "MEDIUM", 2.5, 45),
        ("Healthcare", "Clinic Hygiene", "Dispensary floor is dirty", "en", "LOW", 1.5, 20),
        ("Other", "Staff Grievance", "Officer not sitting on seat", "en", "LOW", 1.0, 15),
        ("Other", "Certificate Delay", "कागजात बनने में देरी हो रही है", "hi", "LOW", 1.0, 15)
    ]

    while len(records) < total_target:
        for item in short_extras:
            if len(records) >= total_target:
                break
            cat, subcat, txt, lang, prio, sev, p_score = item
            variant_text = f"{txt} near Sector {random.randint(1, 20)}"
            if variant_text not in seen_texts:
                seen_texts.add(variant_text)
                records.append({
                    "id": f"SYN-{rec_id:04d}",
                    "complaint_text": variant_text,
                    "language": lang,
                    "category": cat,
                    "subcategory": subcat,
                    "sentiment": "negative" if prio != "LOW" else "neutral",
                    "severity": sev,
                    "public_impact": round(random.randint(20, 50) / 20.0, 1),
                    "safety_risk": round(random.randint(10, 40) / 20.0, 1),
                    "service_disruption": round(random.randint(10, 40) / 20.0, 1),
                    "duration": "1 day",
                    "priority": prio,
                    "priority_score": p_score
                })
                rec_id += 1

    # Truncate to exact 500 if slightly exceeded
    records = records[:500]
    return records

def print_dataset_statistics(records):
    print("=" * 60)
    print("CIVICPULSE SYNTHETIC COMPLAINT DATASET (500 RECORDS) REPORT")
    print("=" * 60)
    print(f"Total Generated Records: {len(records)}")

    # Category breakdown
    cat_counts = Counter(r["category"] for r in records)
    print("\n--- Examples per Category ---")
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat:<20}: {count:>3} ({count/len(records)*100:.1f}%)")

    # Priority breakdown
    prio_counts = Counter(r["priority"] for r in records)
    print("\n--- Examples per Priority ---")
    for prio in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        c = prio_counts.get(prio, 0)
        print(f"  {prio:<10}: {c:>3} ({c/len(records)*100:.1f}%)")

    # Language breakdown
    lang_counts = Counter(r["language"] for r in records)
    print("\n--- Examples per Language ---")
    for lang, count in sorted(lang_counts.items(), key=lambda x: -x[1]):
        print(f"  {lang:<10}: {count:>3} ({count/len(records)*100:.1f}%)")

    # Severity distribution
    sev_bins = {"Low (1.0-2.5)": 0, "Medium (2.6-3.5)": 0, "High (3.6-4.4)": 0, "Critical (4.5-5.0)": 0}
    for r in records:
        s = r["severity"]
        if s <= 2.5: sev_bins["Low (1.0-2.5)"] += 1
        elif s <= 3.5: sev_bins["Medium (2.6-3.5)"] += 1
        elif s <= 4.4: sev_bins["High (3.6-4.4)"] += 1
        else: sev_bins["Critical (4.5-5.0)"] += 1

    print("\n--- Examples per Severity Range ---")
    for b_name, count in sev_bins.items():
        print(f"  {b_name:<20}: {count:>3} ({count/len(records)*100:.1f}%)")

    # Duplicate check
    unique_texts = set(r["complaint_text"].strip() for r in records)
    dupes = len(records) - len(unique_texts)
    print(f"\n--- Duplicates Detected: {dupes} ---")
    print(f"Random Seed Used: {RANDOM_SEED}")
    print("=" * 60)

def main():
    records = generate_records()
    assert len(records) == 500, f"Expected 500 records, got {len(records)}"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIR / "complaints_500.csv"
    json_path = OUTPUT_DIR / "complaints_500.json"

    # Write CSV
    fieldnames = [
        "id", "complaint_text", "language", "category", "subcategory",
        "sentiment", "severity", "public_impact", "safety_risk",
        "service_disruption", "duration", "priority", "priority_score"
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    # Write JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(records)} records to:")
    print(f"  -> {csv_path}")
    print(f"  -> {json_path}")
    print_dataset_statistics(records)

if __name__ == "__main__":
    main()
