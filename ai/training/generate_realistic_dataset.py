import json
import random
from pathlib import Path

# Seed for reproducible evaluation
random.seed(42)

def build_dataset() -> list[dict]:
    dataset = []

    # 1. ROADS
    roads_en = [
        "Massive pothole on the main road causing severe traffic jams and two-wheeler skids near railway station.",
        "The road near Morar circle has completely broken down after recent rains with craters everywhere.",
        "Dangerous open trench left uncovered on the highway service lane without any warning signs or barricades.",
        "Speed breaker on VIP road is unmarked and damaged, cars are getting damaged daily.",
        "Road widening work was abandoned halfway leaving asphalt debris and loose gravel on the street.",
        "Deep pothole near City Center bridge almost caused a bus accident this morning.",
        "The asphalt has melted and formed deep ruts near the bus terminus causing vehicles to lose balance.",
        "Bridge approach road has developed severe cracks and is sinking slowly near Lashkar.",
        "Street pavement tiles are completely dislodged, pedestrians tripping frequently.",
        "Road divider is broken near Maharaj Bada, two-wheelers taking illegal dangerous U-turns.",
        "Heavy trucks have created 1-foot deep ditches on the industrial area bypass road.",
        "Newly laid road washed away within two days of light rain near Gwalior Fort road.",
        "Huge pothole right in front of the government school gate.",
        "Pothole",
        "Road is broken",
        "Deep ditch on highway"
    ]
    roads_hi = [
        "मुख्य सड़क पर बहुत बड़ा गड्ढा हो गया है, आए दिन गाड़ियां गिर रही हैं।",
        "रेलवे स्टेशन के पास सड़क पूरी तरह से उखड़ गई है और धूल उड़ रही है।",
        "थाटीपुर चौराहे पर डिवाइडर टूटा हुआ है जिससे दुर्घटना की संभावना बनी रहती है।",
        "सड़क पर बिना किसी चेतावनी के गहरा गड्ढा खोदकर छोड़ दिया गया है।",
        "सिटी सेंटर मेन रोड पर गिट्टी फैली हुई है, दोपहिया वाहन फिसल रहे हैं।",
        "हजीरा रोड पर जगह-जगह गड्ढे हैं, तुरंत मरम्मत करवाई जाए।",
        "सड़क खराब है",
        "रास्ते में बड़ा गड्ढा"
    ]
    roads_hinglish = [
        "Main road pe bohot bada pothole hai, kal ek biker gir gaya tha.",
        "Station road pura toot chuka hai, gaadi chalana mushkil ho gaya hai.",
        "Colony ki sadak pe deep craters hain, please patch work karwayein.",
        "Highway pe divider tuta hua hai accident ho sakta hai.",
        "Rasta bohot kharab hai gaadi nikalna mushkil hai."
    ]
    roads_typos = [
        "Bigt pot hole on mein road near station.",
        "The asphlat is completely destoyed, repaire needed urgntly.",
        "Deep ptholes and crcks on the highwy."
    ]

    # 2. WATER SUPPLY
    water_en = [
        "Drinking water pipeline has burst on Sector 4 road, thousands of gallons of clean water wasting.",
        "Contaminated black smelly sewage water is coming out of our municipal taps for the last 4 days.",
        "No water supply in the entire colony for 5 continuous days, residents are forced to buy private tankers.",
        "Low water pressure since last 2 weeks, water does not reach the first floor overhead tanks.",
        "Underground water pipe leaking under the road, creating a water puddle and weakening the foundation.",
        "Water supply timing is erratic, coming at 2 AM for only 10 minutes with mud.",
        "Municipal tanker did not arrive in our slum cluster despite repeated requests and 45 degree heat.",
        "Pipeline leakage near community hall has flooded the lane with potable water.",
        "Dead pigeon found in the overhead community water reservoir, water supply smells terrible.",
        "No water in taps for 3 days.",
        "Water pipeline leakage",
        "Dirty water supply"
    ]
    water_hi = [
        "पिछले 4 दिनों से हमारे इलाके में पीने का पानी बिल्कुल नहीं आ रहा है।",
        "नल से बदबूदार और पीला गंदा पानी आ रहा है जिससे लोग बीमार पड़ रहे हैं।",
        "वार्ड नंबर 12 में मुख्य पेयजल पाइपलाइन फूट गई है और पानी बर्बाद हो रहा है।",
        "पानी का प्रेशर बहुत कम है, टंकियां नहीं भर पा रही हैं।",
        "पाइपलाइन में सीवर का पानी मिल गया है, नलों से जहरीला पानी आ रहा है।",
        "पानी नहीं आ रहा",
        "गंदा पानी आ रहा है नलों में"
    ]
    water_hinglish = [
        "Pichle 3 din se paani ki supply band hai, tankers bhi nahi aa rahe.",
        "Nal me se dirty and smelly water aa raha hai, peene layak nahi hai.",
        "Main pipe burst ho gaya hai colony ke samne, bohot paani waste ho raha hai.",
        "Water pressure bohot low hai, please supply badhaiye."
    ]
    water_typos = [
        "Drinkng watr suply is completly stoped since 2 day.",
        "Pipline bursted on stret, watr leaking continously.",
        "Drity water comming in tap."
    ]

    # 3. ELECTRICITY
    elec_en = [
        "High voltage transformer caught fire and exploded with massive sparks near residential apartments.",
        "A live 440V electrical wire has snapped and is dangling over the public walkway where children play.",
        "Total blackout in Gandhi Nagar for the past 18 hours, transformer burnt and not replaced.",
        "Severe voltage fluctuation up to 300V is damaging refrigerators and televisions across our block.",
        "Electric pole is tilted dangerously at 45 degrees and held only by tension of live cables.",
        "Open electrical junction box on the footpath with exposed copper wires accessible to pedestrians.",
        "Continuous loud humming and spark bursts from the distribution transformer near the hospital.",
        "Street power cut every afternoon for 6 hours without any prior load shedding notice.",
        "Exposed live wire hanging from streetlight pole.",
        "Transformer sparking loudly",
        "Power cut for 24 hours"
    ]
    elec_hi = [
        "सड़क पर 440 वोल्ट का बिजली का नंगा तार टूट कर गिर गया है, तुरंत लाइन बंद करें।",
        "ट्रांसफार्मर में तेज धमाके के साथ आग लग गई है, जानमाल का भारी खतरा है।",
        "पिछले 24 घंटे से पूरी कॉलोनी में बिजली गुल है, भीषण गर्मी में त्राहि-त्राहि मची है।",
        "बिजली का खंभा झुक गया है और कभी भी मकान पर गिर सकता है।",
        "अत्यधिक वोल्टेज उतार-चढ़ाव से घरों के सभी उपकरण जल गए हैं।",
        "बिजली चली गई है",
        "करंट का तार खुला पड़ा है"
    ]
    elec_hinglish = [
        "Colony ka transformer blast ho gaya hai, light kal raat se gayab hai.",
        "Ghar ke bahar live wire zameen pe pada hai, kisi ko current lag sakta hai.",
        "Voltage bohot high aa raha hai appliances jal rahe hain.",
        "Bijli nahi aa rahi 12 ghante se, complaints register nahi ho rahi."
    ]
    elec_typos = [
        "Electrcity blackout in our area for 24 hrs.",
        "Live wrie hanging on rd dangerously.",
        "Transfomer sparking violntly."
    ]

    # 4. GARBAGE / WASTE
    garbage_en = [
        "Huge garbage dump has accumulated outside our apartment gate, not cleared for 10 days.",
        "Door-to-door municipal waste collection vehicle has not visited our street for two weeks.",
        "Dead stray cow decomposing on the roadside creating unbearable stench and health hazard.",
        "Overflowing green community dustbins with trash spilling onto the road and eaten by stray pigs.",
        "Construction debris and plastic sacks dumped illegally on the open ground overnight.",
        "Sanitation workers burning garbage heaps in the open, generating toxic choking black smoke.",
        "Garbage pile attracting packs of aggressive stray dogs attacking passersby.",
        "Trash rotting near vegetable market.",
        "Garbage not picked up",
        "Dustbin overflowing"
    ]
    garbage_hi = [
        "सड़क किनारे कचरे का बड़ा ढेर लगा है जिसकी दुर्गंध से सांस लेना मुश्किल हो गया है।",
        "कचरा उठाने वाली गाड़ी पिछले एक सप्ताह से हमारे मोहल्ले में नहीं आई है।",
        "सड़क पर मृत आवारा पशु पड़ा हुआ है, तुरंत हटवाने की कृपा करें।",
        "कूड़ेदान पूरी तरह भर चुके हैं और सारा कचरा सड़क पर बिखर रहा है।",
        "कूड़े में आग लगा दी गई है जिससे पूरे इलाके में जहरीला धुआं फैल रहा है।",
        "कचरा नहीं उठा",
        "कूड़े का ढेर लगा है"
    ]
    garbage_hinglish = [
        "Colony ke samne kachra dump kar diya gaya hai, koi safai nahi ho rahi.",
        "Door to door garbage van nahi aa rahi 8 din se.",
        "Road pe dead animal pada hai bohot badbu aa rahi hai.",
        "Kachre ka dher laga hua hai market ke pass."
    ]
    garbage_typos = [
        "Garbag dumpe is stinking and overflowng.",
        "Wste colection vehcle missing for 2 weks.",
        "Rotting trsh on street."
    ]

    # 5. SANITATION
    sanitation_en = [
        "Open manhole without cover on the middle of the road, fatal hazard for cars and school kids.",
        "Underground sewer line is completely choked, black sewage bubbling up from kitchen sinks.",
        "Open storm drain overflowing with human feces and stagnant wastewater into people's living rooms.",
        "Public toilet complex is locked, filth overflowing on the exterior walls with broken pipes.",
        "Sewer chamber cover is cracked and collapses under foot, immediate accident risk.",
        "Sewage water has flooded the entire lane up to knee height, foul smell entering houses.",
        "Drain cleaning silt left on the roadside has slid back into the gutter after rain.",
        "Open manhole on footpath",
        "Choked sewer line",
        "Overflowing drain"
    ]
    sanitation_hi = [
        "सड़क के बीचोंबीच मैनहोल का ढक्कन टूटा हुआ है, कोई भी गिरकर जान गंवा सकता है।",
        "सीवर लाइन चोक होने से गंदा पानी घरों के अंदर घुस रहा है।",
        "नाली का गंदा पानी सड़क पर बह रहा है जिससे डेंगू और मलेरिया का प्रकोप फैल रहा है।",
        "सार्वजनिक शौचालय में भयानक गंदगी और पानी की कोई व्यवस्था नहीं है।",
        "खुला मैनहोल",
        "सीवर उफन रहा है"
    ]
    sanitation_hinglish = [
        "Manhole ka cover gayab hai, raat me kisi ki jaan ja sakti hai.",
        "Seer line choke ho gayi hai pura rasta gande paani se bhara hai.",
        "Nali block hone se foul smell aa rahi hai colony me.",
        "Gutter ka paani bahar nikal raha hai."
    ]
    sanitation_typos = [
        "Open manholl on stret withot any lid or sing.",
        "Sewage leking and drane chokd up.",
        "Guttr overflowng on road."
    ]

    # 6. PARKS
    parks_en = [
        "Children's playground swings and slides are rusted with broken sharp metal edges injuring kids.",
        "Municipal park walking track is flooded with mud and completely taken over by stray cattle.",
        "Park benches have been vandalized, iron rods stolen and light poles broken.",
        "Wild bushes and congress grass growing 6 feet tall in the colony park, shelter for snakes.",
        "Illegal encroachment inside the public park by local vendors setting up kiosks.",
        "Park fountain has stagnant green mosquito breeding water for the past 6 months.",
        "Broken swing in children park",
        "Park is unmaintained",
        "Overgrown grass in garden"
    ]
    parks_hi = [
        "पार्क के बच्चों के झूले टूटे हुए हैं और नुकीले लोहे से बच्चों को चोट लग रही है।",
        "उद्यान में बड़ी-बड़ी झाड़ियां उग आई हैं और सांप-बिच्छू का डर बना हुआ है।",
        "पार्क की सभी लाइटें बंद हैं, शाम को असामाजिक तत्वों का डेरा रहता है।",
        "पार्क की बाउंड्री वॉल गिर गई है और आवारा मवेशी पौधों को नष्ट कर रहे हैं।",
        "पार्क में झूले टूटे हैं",
        "बगीचे की सफाई नहीं हुई"
    ]
    parks_hinglish = [
        "Park me bachon ke jhule toote hain, bench bhi gayab hain.",
        "Garden me ghas bohot badi ho gayi hai aur kachra pada hai.",
        "Walking track pura kharab hai lights bhi nahi jalti park me."
    ]
    parks_typos = [
        "Chidren playgroun swngs brokn in park.",
        "Publc gardn ovrgrown with weed."
    ]

    # 7. PUBLIC SAFETY (including Police, Hit-and-Run, Theft, Fire, Medical Emergencies)
    safety_en = [
        "A black SUV hit a pedestrian near the railway station around 8:30 PM and escaped toward the highway. The person appears to be injured. I could only see part of the number plate MP07 AB 2.",
        "Hit and run incident: speeding white sedan knocked down a cyclist at Morar square and fled toward bypass. Cyclist bleeding heavily.",
        "Major fire outbreak in a chemical godown near dense residential locality, thick toxic smoke spreading.",
        "Armed robbery at jewelry shop in Sarafa Bazaar, criminals fled on red motorcycle with partial plate 4521 toward highway.",
        "Two masked men on a black Pulsar bike snatched a gold chain from an elderly woman near City Center park, victim wounded.",
        "Ongoing violent clash with sharp weapons and stone pelting between two groups near Kila Gate, police backup needed immediately.",
        "Fire broke out in multi-story residential building, families trapped on 3rd floor, fire brigade required urgently.",
        "Pedestrian hit by rashly driven blue truck near bus depot, driver fled the spot leaving vehicle behind, victim unconscious.",
        "Suspicious bag left unattended near metro station ticketing counter emitting ticking sound.",
        "Car burglary and theft of laptop and cash from parked vehicle outside hospital at 3 PM.",
        "Major road collision between oil tanker and passenger bus on national highway, multiple severe injuries reported.",
        "Gas cylinder leakage and explosion threat inside crowded commercial complex.",
        "Hit and run near railway station",
        "Theft in house",
        "Fire in building",
        "Medical emergency accident"
    ]
    safety_hi = [
        "काले रंग की एसयूवी ने रेलवे स्टेशन के पास एक पैदल यात्री को टक्कर मार दी और हाईवे की तरफ भाग गई। व्यक्ति घायल है, नंबर प्लेट MP07 AB 2।",
        "थाटीपुर चौराहे पर तेज रफ्तार सफेद कार ने बाइक सवार को टक्कर मारी और फरार हो गया, घायल व्यक्ति को तत्काल अस्पताल की जरूरत है।",
        "सराफा बाजार में दुकान में घुसकर हथियारबंद लूट हुई, बदमाश लाल बाइक पर फरार हो गए।",
        "लकड़ी की टाल में भीषण आग लग गई है, आसपास के मकानों में आग फैलने का गंभीर खतरा है।",
        "सड़क पर दो गुटों में खूनी संघर्ष हो रहा है, चाकूबाजी में लोग घायल हुए हैं, तुरंत पुलिस भेजें।",
        "गाड़ी ने टक्कर मार दी और भाग गया",
        "घर में चोरी हो गई",
        "दुकान में आग लग गई है"
    ]
    safety_hinglish = [
        "Ek black SUV ne pedestrian ko hit kiya railway station ke paas aur highway ki taraf escape ho gaya. Injured person road pe hai.",
        "Raat ko 8:30 PM pe white car ne hit and run kiya near market, number plate partial dikhi MP07.",
        "Colony me ghar ka taala todkar chori ho gayi, cash and gold stolen.",
        "Cylinder blast hua shop me, aag lag gayi hai send fire brigade immediately.",
        "Police incident: roadside pe marpeet aur robbery hui hai, victim severely hurt."
    ]
    safety_typos = [
        "Blak SUV hit a persn and escpd towrds highway with partial plte MP07.",
        "Hit and run accidnt, pedestrin injurd and bleedng.",
        "Frie in apartmnt buikding send fire brigde urgetnly.",
        "Theft of vehcle outside markit."
    ]

    # 8. PUBLIC HEALTH / HEALTHCARE
    health_en = [
        "Civil Hospital emergency ward has no doctors or oxygen cylinders available, critical patients waiting on stretchers.",
        "Sudden dengue and chikungunya outbreak in Ward 15 with over 40 cases, health department inspection needed.",
        "Government dispensary is dispensing expired cough syrups and antibiotic medicines to patients.",
        "Dead insects and contamination found in midday meal food at primary school, 15 children hospitalized with food poisoning.",
        "No anti-rabies vaccine in the district hospital after surge in stray dog bite cases.",
        "Ambulance failed to arrive for pregnant woman in labor despite calling helpline for 2 hours.",
        "Hospital emergency without staff",
        "Dengue outbreak in colony",
        "Food poisoning at canteen"
    ]
    health_hi = [
        "सरकारी अस्पताल की इमरजेंसी में कोई डॉक्टर उपलब्ध नहीं है, मरीज तड़प रहे हैं।",
        "हमारे वार्ड में डेंगू के 30 से ज्यादा मरीज हो गए हैं, तत्काल स्वास्थ्य शिविर और दवा छिड़काव करवाया जाए।",
        "अस्पताल में कुत्ते के काटने का इंजेक्शन (एंटी रैबीज) उपलब्ध नहीं है।",
        "आंगनवाड़ी में दिए गए भोजन से बच्चों को फूड पॉइजनिंग हो गई है, बच्चे अस्पताल में भर्ती हैं।",
        "अस्पताल में दवा नहीं है",
        "इलाके में बीमारी फैल रही है"
    ]
    health_hinglish = [
        "Hospital me doctor nahi hai emergency case hai please send ambulance.",
        "Colony me dengue ke cases bohot badh gaye hain, fogging ki sakht zaroorat hai.",
        "Dispensary me expired medicines di ja rahi hain patients ko."
    ]
    health_typos = [
        "Hospitl emrgncy has no doctrs for injurd paitents.",
        "Dengu outbrek in our localty.",
        "Expred medcine sold in govrnmnt clinic."
    ]

    # 9. ENVIRONMENT
    env_en = [
        "Chemical dyeing unit discharging untreated toxic acidic red effluent into open storm drain.",
        "Illegal felling of 20 mature peepal and neem trees in green belt area by private builders.",
        "Continuous ear-splitting industrial generator noise running 24 hours in a silence zone near hospital.",
        "Stone crushing plant emitting heavy crystalline silica dust causing respiratory problems in village.",
        "Unauthorized burning of chemical plastic drums at midnight releasing acrid poisonous fumes.",
        "Toxic chemical discharge in river",
        "Illegal tree cutting",
        "Air pollution from factory"
    ]
    env_hi = [
        "फैक्ट्री से जहरीला रासायनिक पानी सीधे नाले में बहाया जा रहा है जिससे भूजल प्रदूषित हो रहा है।",
        "ग्रीन बेल्ट में हरे-भरे पेड़ों की अवैध कटाई की जा रही है, वन विभाग तुरंत कार्रवाई करे।",
        "अस्पताल के पास पूरी रात तेज आवाज में डीजे और जनरेटर बजता है जिससे मरीज सो नहीं पाते।",
        "धुआं और प्रदूषण बहुत ज्यादा है",
        "पेड़ अवैध रूप से काटे जा रहे हैं"
    ]
    env_hinglish = [
        "Factory se toxic dhuan nikal raha hai din raat, breathing problem ho rahi hai.",
        "Green belt me illegal ped kaate ja rahe hain builder dwara.",
        "Noise pollution bohot zyada hai hospital area me."
    ]
    env_typos = [
        "Toxc smoke and pulution from chemcal factry.",
        "Tree cuting illegaly in colony."
    ]

    # 10. OTHER (General admin, certificates, civil disputes, greetings, ambiguous)
    other_en = [
        "Applied for birth certificate 45 days ago, municipal portal still shows status as pending review.",
        "Property tax assessment receipt not generated after online UPI payment deduction of 4500 rupees.",
        "Trade license renewal application rejected without providing any valid explanation.",
        "Need information regarding the procedure to apply for street vendor identity card.",
        "The municipal counter staff was rude and refused to accept the pension verification form.",
        "Urgent help needed in our area.",
        "Please look into this issue immediately.",
        "Something is wrong in our locality.",
        "Thank you for solving my previous complaint.",
        "Everything is working fine now.",
        "Hello sir",
        "Urgent matter",
        "Status check for token 1234"
    ]
    other_hi = [
        "जन्म प्रमाण पत्र के लिए एक महीने पहले आवेदन किया था, अभी तक जारी नहीं हुआ।",
        "प्रॉपर्टी टैक्स का ऑनलाइन भुगतान कट गया लेकिन रसीद जनरेट नहीं हुई।",
        "कार्यालय में कर्मचारी समय पर नहीं बैठते और नागरिकों से अभद्र व्यवहार करते हैं।",
        "कृपया इस समस्या का समाधान करें।",
        "अति आवश्यक कार्य हेतु निवेदन।",
        "नमस्ते",
        "धन्यवाद"
    ]
    other_hinglish = [
        "Birth certificate apply kiya tha 1 month ho gaya abhi tak nahi mila.",
        "Property tax payment debit ho gaya receipt download nahi ho rahi.",
        "Sir urgent help chahiye colony me kuch issue hai please dekhein.",
        "Thank you sab theek ho gaya hai."
    ]
    other_typos = [
        "Certficate not recived aftr 30 days.",
        "Paymnt done but recipt not genrated.",
        "Pls help as son as posibl."
    ]

    # Add all grouped by category
    categories_data = [
        ("Roads", roads_en, roads_hi, roads_hinglish, roads_typos),
        ("Water Supply", water_en, water_hi, water_hinglish, water_typos),
        ("Electricity", elec_en, elec_hi, elec_hinglish, elec_typos),
        ("Garbage/Waste", garbage_en, garbage_hi, garbage_hinglish, garbage_typos),
        ("Sanitation", sanitation_en, sanitation_hi, sanitation_hinglish, sanitation_typos),
        ("Parks", parks_en, parks_hi, parks_hinglish, parks_typos),
        ("Public Safety", safety_en, safety_hi, safety_hinglish, safety_typos),
        ("Public Health", health_en, health_hi, health_hinglish, health_typos),
        ("Environment", env_en, env_hi, env_hinglish, env_typos),
        ("Other", other_en, other_hi, other_hinglish, other_typos),
    ]

    for cat_name, en_list, hi_list, hing_list, typo_list in categories_data:
        # English samples
        for text in en_list:
            dataset.append({
                "text": text,
                "category": cat_name,
                "language": "en"
            })
        # Hindi samples
        for text in hi_list:
            dataset.append({
                "text": text,
                "category": cat_name,
                "language": "hi"
            })
        # Hinglish samples
        for text in hing_list:
            dataset.append({
                "text": text,
                "category": cat_name,
                "language": "hinglish"
            })
        # Typo samples
        for text in typo_list:
            dataset.append({
                "text": text,
                "category": cat_name,
                "language": "en"
            })

    # Add syntactic and contextual combinations with varied wards/landmarks to reach ~600-800 unique realistic samples
    locations = [
        "near Railway Station", "at Maharaj Bada", "in Thatipur Colony", "near Hazira Chowk",
        "in City Center", "near Pinto Park", "in Morar Ward 4", "near Civil Lines",
        "in Dindayal Nagar", "near Gwalior Fort road", "at Kampoo", "in Ward 18"
    ]
    durations = ["for 3 days", "since yesterday", "for 2 weeks", "past 24 hours", "since 5 hours", "for 1 month"]
    
    # Generate variations with diverse sentence structures
    templates = [
        ("Roads", "Dangerous road condition {loc} {dur}, vehicle tires getting punctured and people slipping."),
        ("Roads", "The main street {loc} has completely deteriorated with deep potholes {dur}."),
        ("Water Supply", "Drinking water contamination reported {loc} {dur}, muddy water coming in taps."),
        ("Water Supply", "Main pipeline burst and massive water leakage {loc} {dur}."),
        ("Electricity", "Frequent power outages and electrical sparking from transformer {loc} {dur}."),
        ("Electricity", "Exposed high-voltage wire hanging low on street {loc} {dur} posing danger to citizens."),
        ("Garbage/Waste", "Severe garbage accumulation and rotting refuse {loc} {dur}, no cleaning van arrived."),
        ("Garbage/Waste", "Dead stray animal lying unattended {loc} {dur} spreading foul odor and flies."),
        ("Sanitation", "Overflowing open gutter and sewer drainage water flooding road {loc} {dur}."),
        ("Sanitation", "Broken open manhole on footpath {loc} {dur}, high accident risk for schoolchildren."),
        ("Parks", "Public park swings are broken and lawn overgrown with tall thorny grass {loc} {dur}."),
        ("Parks", "Park boundary wall broken and benches destroyed by vandals {loc} {dur}."),
        ("Public Safety", "Speeding vehicle hit a pedestrian and escaped {loc} {dur}, victim was injured and needs emergency help."),
        ("Public Safety", "Armed robbery and bike snatching incident reported {loc} {dur}, suspect fled on two-wheeler."),
        ("Public Safety", "Fire hazard and smoke billowing from warehouse {loc} {dur}, dispatch emergency team."),
        ("Public Health", "Hospital emergency ward overcrowded and lacking basic medicines {loc} {dur}."),
        ("Public Health", "Suspected dengue fever cases rising in multiple families {loc} {dur}."),
        ("Environment", "Chemical fumes and illegal burning of industrial waste {loc} {dur} causing asthma attacks."),
        ("Environment", "Illegal dumping of hazardous industrial effluent near canal {loc} {dur}."),
        ("Other", "Application status for residential license not updated on portal {loc} {dur}.")
    ]

    for cat_name, tmpl in templates:
        for _ in range(25):
            loc = random.choice(locations)
            dur = random.choice(durations)
            txt = tmpl.format(loc=loc, dur=dur)
            dataset.append({
                "text": txt,
                "category": cat_name,
                "language": "en"
            })

    # Hindi template variations
    hindi_locs = ["महाराज बाड़ा के पास", "थाटीपुर में", "हजीरा चौराहे पर", "मुरार में", "सिटी सेंटर में", "रेलवे स्टेशन के नजदीक", "वार्ड 12 में"]
    hindi_durs = ["3 दिन से", "कल रात से", "हफ्ते भर से", "पिछले 24 घंटे से", "5 दिन से"]
    
    hindi_templates = [
        ("Roads", "{loc} सड़क पर गहरा गड्ढा है {dur}, गाड़ियां दुर्घटनाग्रस्त हो रही हैं।"),
        ("Water Supply", "{loc} पीने का पानी बिल्कुल नहीं आ रहा है {dur}, जनता परेशान है।"),
        ("Electricity", "{loc} बिजली का खंभा झुक गया है और तार लटक रहे हैं {dur}।"),
        ("Garbage/Waste", "{loc} भारी कचरा पड़ा हुआ है {dur}, नगर निगम की गाड़ी नहीं आई।"),
        ("Sanitation", "{loc} खुला मैनहोल पड़ा है {dur}, किसी भी समय बड़ा हादसा हो सकता है।"),
        ("Parks", "{loc} पार्क में झूले टूटे हैं और गंदगी फैली है {dur}।"),
        ("Public Safety", "{loc} अज्ञात वाहन ने टक्कर मार दी और भाग गया {dur}, व्यक्ति को चोट लगी है।"),
        ("Public Health", "{loc} कई लोग बीमार पड़ रहे हैं {dur}, स्वास्थ्य जांच की आवश्यकता है।"),
        ("Environment", "{loc} रात में काला धुआं और तेज दुर्गंध आ रही है {dur}।"),
        ("Other", "{loc} नगर निगम कार्यालय में आवेदन दिया था {dur}, कोई सुनवाई नहीं हो रही।")
    ]

    for cat_name, tmpl in hindi_templates:
        for _ in range(12):
            loc = random.choice(hindi_locs)
            dur = random.choice(hindi_durs)
            txt = tmpl.format(loc=loc, dur=dur)
            dataset.append({
                "text": txt,
                "category": cat_name,
                "language": "hi"
            })

    # Deduplicate while preserving order
    seen = set()
    unique_dataset = []
    for item in dataset:
        clean_text = item["text"].strip()
        if clean_text not in seen:
            seen.add(clean_text)
            unique_dataset.append(item)

    return unique_dataset

if __name__ == "__main__":
    data = build_dataset()
    out_path = Path(__file__).parent.parent.parent / "data" / "synthetic_complaints.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(data)} realistic, balanced complaints written to {out_path}")
