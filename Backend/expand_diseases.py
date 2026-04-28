"""
Script to expand disease_info.json with comprehensive crop disease data.
Adds diseases for crops that only had 'healthy' entries and adds more
Indian-relevant crop diseases with pesticide recommendations.
"""
import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "disease_info.json")

# Load existing data
with open(DATA_PATH, "r") as f:
    data = json.load(f)

# ── NEW DISEASE ENTRIES ────────────────────────────────────────────────────────
# These are additional entries that enrich the knowledge base beyond PlantVillage

new_entries = {
    # ── BLUEBERRY DISEASES ─────────────────────────────────────────────────
    "Blueberry___Mummy_berry": {
        "display_name": "Blueberry Mummy Berry",
        "description": "Mummy berry is caused by the fungus Monilinia vaccinii-corymbosi. It is the most economically important disease of blueberries, causing shoot blight and fruit mummification.",
        "symptoms": [
            "Sudden wilting and browning of new shoots and flower clusters",
            "Infected berries appear normal initially but turn tan, then gray and shriveled",
            "Mummified berries fall to ground and overwinter",
            "Brown discoloration at base of infected shoots"
        ],
        "pesticides": [
            "Propiconazole 25% EC (1 mL/L)",
            "Fenbuconazole 24% SC (0.7 mL/L)",
            "Chlorothalonil 75% WP (2 g/L)",
            "Indar (Fenbuconazole) at bloom stage"
        ],
        "prevention": [
            "Rake and remove mummified berries from under bushes",
            "Apply 2-3 inches of fresh mulch to bury mummies",
            "Plant resistant varieties when available",
            "Apply fungicide at bud break and during bloom",
            "Ensure good air circulation through pruning"
        ],
        "severity": "High"
    },
    "Blueberry___Botrytis_blight": {
        "display_name": "Blueberry Botrytis Blight (Gray Mold)",
        "description": "Botrytis blight is caused by Botrytis cinerea. It affects flowers and fruit, causing gray mold especially during cool, wet weather.",
        "symptoms": [
            "Gray fuzzy mold on flowers and developing fruit",
            "Blighted blossoms turn brown and cling to stems",
            "Fruit rots with gray mold covering",
            "Shoot tips may wilt and die back"
        ],
        "pesticides": [
            "Captan 50% WP (2 g/L)",
            "Iprodione 50% WP (1 g/L)",
            "Fenhexamid 50% WG (1 g/L)",
            "Cyprodinil + Fludioxonil (Switch fungicide)"
        ],
        "prevention": [
            "Ensure good air circulation through pruning",
            "Avoid overhead irrigation during bloom",
            "Harvest fruit promptly when ripe",
            "Remove dead flowers and infected fruit",
            "Maintain proper plant spacing"
        ],
        "severity": "Moderate"
    },
    "Blueberry___Anthracnose": {
        "display_name": "Blueberry Anthracnose Fruit Rot",
        "description": "Anthracnose fruit rot is caused by Colletotrichum acutatum. It causes soft rot of ripe fruit, especially in warm, wet conditions.",
        "symptoms": [
            "Soft, sunken lesions on ripe or ripening fruit",
            "Orange spore masses on fruit surface in humid conditions",
            "Fruit shrivels and drops prematurely",
            "Infections can remain latent until fruit ripens"
        ],
        "pesticides": [
            "Azoxystrobin 23% SC (1 mL/L)",
            "Pyraclostrobin 20% WG (0.5 g/L)",
            "Captan 50% WP (2 g/L)",
            "Chlorothalonil 75% WP (2 g/L)"
        ],
        "prevention": [
            "Prune to improve air circulation and light penetration",
            "Harvest fruit frequently and promptly",
            "Avoid overhead irrigation",
            "Remove infected fruit and debris from field",
            "Apply fungicides from bloom through harvest"
        ],
        "severity": "High"
    },

    # ── RASPBERRY DISEASES ─────────────────────────────────────────────────
    "Raspberry___Anthracnose": {
        "display_name": "Raspberry Anthracnose",
        "description": "Raspberry anthracnose is caused by Elsinoe veneta. It produces sunken, gray-centered lesions on canes, leaves, and fruit.",
        "symptoms": [
            "Small, purplish spots on young canes",
            "Spots enlarge to oval, sunken lesions with gray centers and purple borders",
            "Bark may crack at lesion sites",
            "Fruit may be small, dry, and seedy"
        ],
        "pesticides": [
            "Copper hydroxide 77% WP (2 g/L) — dormant spray",
            "Captan 50% WP (2 g/L)",
            "Pyraclostrobin 20% WG (0.5 g/L)",
            "Lime sulfur (dormant application)"
        ],
        "prevention": [
            "Remove and destroy old fruiting canes after harvest",
            "Thin canes to improve air circulation",
            "Avoid overhead irrigation",
            "Apply dormant spray of lime sulfur or copper",
            "Plant resistant varieties"
        ],
        "severity": "Moderate"
    },
    "Raspberry___Late_leaf_rust": {
        "display_name": "Raspberry Late Leaf Rust",
        "description": "Late leaf rust is caused by Pucciniastrum americanum. It causes premature defoliation and weakens canes.",
        "symptoms": [
            "Small yellow pustules on lower leaf surfaces",
            "Upper leaf surface shows yellow spots",
            "Premature leaf drop in late summer",
            "Weakened canes produce less fruit the following year"
        ],
        "pesticides": [
            "Myclobutanil 10% WP (1 g/L)",
            "Propiconazole 25% EC (1 mL/L)",
            "Mancozeb 75% WP (2.5 g/L)",
            "Copper oxychloride 50% WP (3 g/L)"
        ],
        "prevention": [
            "Remove wild brambles near cultivated plantings",
            "Ensure good air circulation through proper spacing",
            "Remove fallen leaves in autumn",
            "Apply fungicide when rust first appears",
            "Plant resistant varieties"
        ],
        "severity": "Moderate"
    },
    "Raspberry___Botrytis_fruit_rot": {
        "display_name": "Raspberry Gray Mold (Botrytis Fruit Rot)",
        "description": "Gray mold caused by Botrytis cinerea is the most common post-harvest disease of raspberries, causing soft rot with gray fuzzy mold.",
        "symptoms": [
            "Soft, light brown rot on ripe fruit",
            "Gray fuzzy mold covering affected berries",
            "Fruit leaks juice and collapses",
            "Disease spreads rapidly to adjacent berries"
        ],
        "pesticides": [
            "Captan 50% WP (2 g/L)",
            "Fenhexamid 50% WG (1 g/L)",
            "Iprodione 50% WP (1 g/L)",
            "Cyprodinil + Fludioxonil combination"
        ],
        "prevention": [
            "Harvest fruit frequently in dry conditions",
            "Ensure good air circulation through cane thinning",
            "Avoid overhead irrigation during fruiting",
            "Remove and destroy infected fruit promptly",
            "Cool harvested fruit immediately to 0-2°C"
        ],
        "severity": "High"
    },

    # ── SOYBEAN DISEASES ───────────────────────────────────────────────────
    "Soybean___Rust": {
        "display_name": "Soybean Rust (Asian Soybean Rust)",
        "description": "Asian soybean rust is caused by Phakopsora pachyrhizi. It is one of the most destructive diseases of soybean worldwide, capable of causing 80% yield loss.",
        "symptoms": [
            "Small, tan to dark brown lesions on lower leaves",
            "Lesions produce tan to reddish-brown pustules on leaf undersides",
            "Rapid yellowing and premature defoliation",
            "Pods may also develop lesions in severe cases"
        ],
        "pesticides": [
            "Propiconazole 25% EC (1 mL/L)",
            "Tebuconazole 25.9% EC (1 mL/L)",
            "Azoxystrobin 23% SC (1 mL/L)",
            "Trifloxystrobin 25% + Tebuconazole 50% WG (0.7 g/L)"
        ],
        "prevention": [
            "Plant early-maturing varieties to escape peak rust season",
            "Monitor fields regularly from flowering stage",
            "Apply fungicide at first sign of rust",
            "Avoid late planting",
            "Destroy volunteer soybean plants"
        ],
        "severity": "Very High"
    },
    "Soybean___Septoria_brown_spot": {
        "display_name": "Soybean Septoria Brown Spot",
        "description": "Septoria brown spot is caused by Septoria glycines. It is one of the most common foliar diseases of soybeans.",
        "symptoms": [
            "Small, irregular, dark brown spots on lower leaves",
            "Spots may merge causing large necrotic areas",
            "Premature yellowing and defoliation of lower leaves",
            "Usually starts on unifoliate and lower trifoliate leaves"
        ],
        "pesticides": [
            "Mancozeb 75% WP (2.5 g/L)",
            "Carbendazim 50% WP (1 g/L)",
            "Azoxystrobin 23% SC (1 mL/L)",
            "Thiophanate-methyl 70% WP (1 g/L)"
        ],
        "prevention": [
            "Rotate with non-host crops like corn or wheat",
            "Bury crop residues through tillage",
            "Use resistant varieties",
            "Maintain balanced fertility",
            "Apply foliar fungicide if disease appears before pod fill"
        ],
        "severity": "Moderate"
    },
    "Soybean___Bacterial_blight": {
        "display_name": "Soybean Bacterial Blight",
        "description": "Bacterial blight is caused by Pseudomonas savastanoi pv. glycinea. It causes angular leaf spots, especially after storms with wind-driven rain.",
        "symptoms": [
            "Small, angular, water-soaked spots on leaves",
            "Spots turn yellow-brown to dark brown with yellow halos",
            "Centers of spots may dry and fall out",
            "Symptoms appear on upper canopy after storms"
        ],
        "pesticides": [
            "Copper hydroxide 77% WP (2 g/L)",
            "Copper oxychloride 50% WP (3 g/L)",
            "Streptomycin sulphate (0.5 g/L)",
            "No highly effective chemical controls — focus on prevention"
        ],
        "prevention": [
            "Use certified disease-free seed",
            "Rotate crops for at least one year",
            "Avoid working in fields when foliage is wet",
            "Plant resistant varieties",
            "Bury infected crop residues"
        ],
        "severity": "Low"
    },

    # ── ADDITIONAL INDIAN CROP DISEASES ────────────────────────────────────
    # Rice (major Indian crop)
    "Rice___Blast": {
        "display_name": "Rice Blast",
        "description": "Rice blast is caused by Magnaporthe oryzae. It is the most important disease of rice worldwide, attacking leaves, nodes, and panicles.",
        "symptoms": [
            "Diamond-shaped or elliptical spots with gray centers and brown margins on leaves",
            "Spots may coalesce to kill entire leaves",
            "Neck rot causing panicle to break and hang (neck blast)",
            "Node blackening leading to stem breakage"
        ],
        "pesticides": [
            "Tricyclazole 75% WP (0.6 g/L)",
            "Isoprothiolane 40% EC (1.5 mL/L)",
            "Carbendazim 50% WP (1 g/L)",
            "Edifenphos 50% EC (1 mL/L)",
            "Kasugamycin 3% SL (2 mL/L)"
        ],
        "prevention": [
            "Use blast-resistant varieties",
            "Avoid excessive nitrogen fertilization",
            "Maintain proper water management in paddies",
            "Treat seeds with fungicide before sowing",
            "Remove and destroy infected crop residues",
            "Maintain proper spacing between plants"
        ],
        "severity": "Very High"
    },
    "Rice___Brown_spot": {
        "display_name": "Rice Brown Spot",
        "description": "Brown spot is caused by Bipolaris oryzae (Cochliobolus miyabeanus). It causes oval brown spots on leaves and grain discoloration.",
        "symptoms": [
            "Oval to circular brown spots with gray centers on leaves",
            "Spots surrounded by yellow halo",
            "Grain discoloration affecting quality",
            "Seedling blight if seed is infected"
        ],
        "pesticides": [
            "Mancozeb 75% WP (2.5 g/L)",
            "Propiconazole 25% EC (1 mL/L)",
            "Carbendazim 50% WP (1 g/L)",
            "Edifenphos 50% EC (1 mL/L)"
        ],
        "prevention": [
            "Use certified seed and treat with fungicide",
            "Maintain balanced nutrition especially potassium and silicon",
            "Ensure proper water management",
            "Remove infected crop residues",
            "Use resistant varieties"
        ],
        "severity": "Moderate"
    },
    "Rice___Bacterial_leaf_blight": {
        "display_name": "Rice Bacterial Leaf Blight",
        "description": "Bacterial leaf blight is caused by Xanthomonas oryzae pv. oryzae. It is one of the most serious diseases of rice in Asia.",
        "symptoms": [
            "Water-soaked streaks along leaf veins",
            "Streaks enlarge and turn yellow to white",
            "Leaves dry up from tips and margins",
            "Milky bacterial ooze on leaf surface in early morning"
        ],
        "pesticides": [
            "Streptomycin sulphate + Tetracycline (Streptocycline — 0.5 g/L)",
            "Copper oxychloride 50% WP (3 g/L)",
            "Copper hydroxide 77% WP (2 g/L)",
            "No highly effective chemical cure — resistant varieties preferred"
        ],
        "prevention": [
            "Plant resistant varieties (recommended by IRRI/local stations)",
            "Avoid clipping seedling tips during transplanting",
            "Drain fields during severe outbreaks",
            "Avoid excess nitrogen fertilization",
            "Use balanced NPK with extra potassium"
        ],
        "severity": "Very High"
    },
    "Rice___Sheath_blight": {
        "display_name": "Rice Sheath Blight",
        "description": "Sheath blight is caused by Rhizoctonia solani. It attacks leaf sheaths near water level, causing oval lesions that expand upward.",
        "symptoms": [
            "Oval or irregular greenish-gray lesions on leaf sheaths near water line",
            "Lesions enlarge and merge, moving upward",
            "Affected sheaths and leaves dry up and turn brown",
            "White mycelial growth visible on lesions in humid conditions"
        ],
        "pesticides": [
            "Hexaconazole 5% SC (2 mL/L)",
            "Propiconazole 25% EC (1 mL/L)",
            "Validamycin 3% SL (2 mL/L)",
            "Carbendazim 50% WP (1 g/L)"
        ],
        "prevention": [
            "Avoid dense planting — maintain proper spacing",
            "Manage nitrogen application carefully",
            "Drain water periodically to lower humidity",
            "Use seed treatment with Trichoderma viride",
            "Remove sclerotia from fields before planting"
        ],
        "severity": "High"
    },

    # Wheat (major Indian crop)
    "Wheat___Rust_stripe": {
        "display_name": "Wheat Stripe (Yellow) Rust",
        "description": "Stripe rust is caused by Puccinia striiformis f. sp. tritici. It forms yellow-orange pustules arranged in stripes along leaf veins.",
        "symptoms": [
            "Yellow to orange pustules arranged in long stripes between leaf veins",
            "Leaves turn yellow and dry up",
            "Green islands may remain between stripe patterns",
            "Spores released in powdery masses"
        ],
        "pesticides": [
            "Propiconazole 25% EC (1 mL/L)",
            "Tebuconazole 25.9% EC (1 mL/L)",
            "Triadimefon 25% WP (1 g/L)",
            "Mancozeb 75% WP (2.5 g/L)"
        ],
        "prevention": [
            "Plant resistant varieties recommended for your region",
            "Timely sowing to avoid peak rust season",
            "Monitor fields regularly from tillering stage",
            "Apply fungicide at first sign of rust",
            "Avoid excessive nitrogen fertilization"
        ],
        "severity": "Very High"
    },
    "Wheat___Leaf_rust": {
        "display_name": "Wheat Leaf (Brown) Rust",
        "description": "Leaf rust is caused by Puccinia triticina. It is the most common rust disease of wheat, producing small, round, orange-brown pustules on leaves.",
        "symptoms": [
            "Small, round to oval, orange-brown pustules scattered on leaf surface",
            "Pustules mostly on upper leaf surface",
            "Premature leaf drying in severe infections",
            "Reduced grain filling and shriveled kernels"
        ],
        "pesticides": [
            "Propiconazole 25% EC (1 mL/L)",
            "Tebuconazole 25.9% EC (1 mL/L)",
            "Mancozeb 75% WP (2.5 g/L)",
            "Triadimefon 25% WP (1 g/L)"
        ],
        "prevention": [
            "Grow rust-resistant varieties",
            "Apply fungicides at first appearance of pustules",
            "Avoid late sowing",
            "Maintain balanced fertilization",
            "Destroy volunteer wheat plants"
        ],
        "severity": "High"
    },
    "Wheat___Powdery_mildew": {
        "display_name": "Wheat Powdery Mildew",
        "description": "Powdery mildew of wheat is caused by Blumeria graminis f. sp. tritici. It produces white powdery patches on leaves and stems.",
        "symptoms": [
            "White to grayish powdery patches on leaves, stems, and heads",
            "Patches turn gray-brown as they age",
            "Leaves may yellow and die prematurely",
            "Reduced tillering and grain fill"
        ],
        "pesticides": [
            "Propiconazole 25% EC (1 mL/L)",
            "Triadimefon 25% WP (1 g/L)",
            "Sulphur 80% WP (3 g/L)",
            "Tebuconazole 25.9% EC (1 mL/L)"
        ],
        "prevention": [
            "Use resistant varieties",
            "Avoid excessive nitrogen application",
            "Ensure proper plant spacing",
            "Apply foliar fungicide at first sign",
            "Avoid dense sowing"
        ],
        "severity": "Moderate"
    },

    # Cotton (important Indian crop)
    "Cotton___Bacterial_blight": {
        "display_name": "Cotton Bacterial Blight (Angular Leaf Spot)",
        "description": "Bacterial blight is caused by Xanthomonas citri pv. malvacearum. It causes angular water-soaked lesions on leaves, stems, and bolls.",
        "symptoms": [
            "Small, angular, water-soaked spots on leaves between veins",
            "Spots turn brown to black with age",
            "Black arm symptom — dark lesions on stems and petioles",
            "Boll rot with sunken, dark spots on immature bolls"
        ],
        "pesticides": [
            "Copper hydroxide 77% WP (2 g/L)",
            "Copper oxychloride 50% WP (3 g/L)",
            "Streptomycin sulphate + Tetracycline (Streptocycline — 0.5 g/L)",
            "Seed treatment with Carboxin 37.5% + Thiram 37.5% DS (3 g/kg seed)"
        ],
        "prevention": [
            "Use acid-delinted, treated seed",
            "Plant resistant varieties (consult local Krishi Vigyan Kendra)",
            "Practice crop rotation with non-host crops",
            "Remove and destroy infected plant debris",
            "Avoid working in fields when foliage is wet"
        ],
        "severity": "High"
    },
    "Cotton___Bollworm_damage": {
        "display_name": "Cotton Bollworm Damage",
        "description": "American bollworm (Helicoverpa armigera) is the most destructive pest of cotton in India. Larvae bore into bolls and feed on developing seeds and lint.",
        "symptoms": [
            "Bore holes in squares, flowers, and bolls",
            "Frass (excrement) at entry points",
            "Damaged bolls may rot or drop prematurely",
            "Larvae visible inside open bolls"
        ],
        "pesticides": [
            "Emamectin benzoate 5% SG (0.4 g/L)",
            "Chlorantraniliprole 18.5% SC (0.3 mL/L)",
            "Spinosad 45% SC (0.3 mL/L)",
            "Neem oil 1500 ppm (5 mL/L) — for early instars",
            "Bt (Bacillus thuringiensis) var. kurstaki (2 g/L)"
        ],
        "prevention": [
            "Install pheromone traps to monitor adult moths",
            "Use Bt cotton varieties (approved GM varieties)",
            "Intercrop with trap crops like marigold or pigeon pea",
            "Release Trichogramma parasitoid wasps",
            "Practice crop rotation and destroy crop stubble after harvest"
        ],
        "severity": "Very High"
    },
    "Cotton___Leaf_curl_virus": {
        "display_name": "Cotton Leaf Curl Virus (CLCuV)",
        "description": "Cotton leaf curl virus is transmitted by the whitefly Bemisia tabaci. It is a devastating disease in Indian and Pakistani cotton regions.",
        "symptoms": [
            "Upward or downward curling of leaves",
            "Thickening and darkening of leaf veins (enations)",
            "Leaf-like outgrowths on underside of leaves",
            "Stunted plant growth and reduced boll formation"
        ],
        "pesticides": [
            "No cure for virus — control the whitefly vector",
            "Imidacloprid 17.8% SL (0.3 mL/L)",
            "Thiamethoxam 25% WG (0.3 g/L)",
            "Diafenthiuron 50% WP (1 g/L)",
            "Neem oil 1500 ppm (5 mL/L)"
        ],
        "prevention": [
            "Plant CLCuV-resistant or tolerant varieties",
            "Early sowing to escape peak whitefly period",
            "Install yellow sticky traps for whitefly monitoring",
            "Uproot and destroy infected plants",
            "Avoid growing alternate whitefly hosts nearby"
        ],
        "severity": "Very High"
    },

    # Groundnut / Peanut (important Indian crop)
    "Groundnut___Tikka_leaf_spot": {
        "display_name": "Groundnut Tikka Disease (Early & Late Leaf Spot)",
        "description": "Tikka disease includes early leaf spot (Cercospora arachidicola) and late leaf spot (Cercosporidium personatum). These are the most common diseases of groundnut in India.",
        "symptoms": [
            "Dark brown circular spots on upper leaf surface (early leaf spot)",
            "Black spots mainly on lower leaf surface (late leaf spot)",
            "Severe defoliation reducing pod yield",
            "Dark lesions on petioles and stems"
        ],
        "pesticides": [
            "Mancozeb 75% WP (2.5 g/L)",
            "Chlorothalonil 75% WP (2 g/L)",
            "Carbendazim 50% WP (1 g/L)",
            "Hexaconazole 5% SC (2 mL/L)",
            "Tebuconazole 25.9% EC (1 mL/L)"
        ],
        "prevention": [
            "Use resistant varieties (ICGV series)",
            "Treat seeds with Thiram or Carbendazim",
            "Remove and destroy crop debris",
            "Practice crop rotation (2-3 years)",
            "Apply foliar fungicides at 30-35 days after sowing"
        ],
        "severity": "High"
    },
    "Groundnut___Rust": {
        "display_name": "Groundnut Rust",
        "description": "Groundnut rust is caused by Puccinia arachidis. It produces orange-brown pustules on leaf undersides.",
        "symptoms": [
            "Small, orange-brown to reddish-brown pustules on lower leaf surface",
            "Corresponding light spots on upper surface",
            "Severe infection causes premature defoliation",
            "Reduced pod and kernel development"
        ],
        "pesticides": [
            "Mancozeb 75% WP (2.5 g/L)",
            "Chlorothalonil 75% WP (2 g/L)",
            "Hexaconazole 5% SC (2 mL/L)",
            "Propiconazole 25% EC (1 mL/L)"
        ],
        "prevention": [
            "Plant resistant varieties",
            "Timely sowing to avoid peak disease period",
            "Remove volunteer groundnut plants",
            "Apply foliar fungicide at disease onset",
            "Practice crop rotation with cereals"
        ],
        "severity": "High"
    },

    # Sugarcane (major Indian crop)
    "Sugarcane___Red_rot": {
        "display_name": "Sugarcane Red Rot",
        "description": "Red rot is caused by Colletotrichum falcatum. It is the most serious disease of sugarcane in India, causing internal red discoloration of the stalk.",
        "symptoms": [
            "Yellowing and drying of leaves from tip downward",
            "Red discoloration inside cane when split open",
            "White patches within red-rotted tissue (diagnostic feature)",
            "Shrunken and hollowed canes",
            "Alcohol-like smell from infected canes"
        ],
        "pesticides": [
            "Carbendazim 50% WP (1 g/L) — sett treatment",
            "Thiophanate-methyl 70% WP (1 g/L) — sett treatment",
            "Mancozeb 75% WP (2.5 g/L)",
            "Sett treatment with Trichoderma viride (10 g/L for 15 min)"
        ],
        "prevention": [
            "Use disease-free seed cane (setts) from registered nurseries",
            "Treat setts with fungicide before planting",
            "Plant resistant varieties (consult local cane research station)",
            "Practice crop rotation with non-host crops",
            "Rogue out and destroy infected clumps immediately"
        ],
        "severity": "Very High"
    },
    "Sugarcane___Smut": {
        "display_name": "Sugarcane Smut (Whip Smut)",
        "description": "Smut of sugarcane is caused by Sporisorium scitamineum. It produces a distinctive black whip-like structure from the growing point.",
        "symptoms": [
            "Long, black whip-like structure emerging from the top of the cane",
            "Whip composed of black spore mass covered by thin membrane",
            "Thin, pencil-like tillers (grass-like shoots)",
            "Reduced cane thickness and sugar content"
        ],
        "pesticides": [
            "Seed treatment with Propiconazole 25% EC (1 mL/L) for 15 min",
            "Hot water treatment of setts at 52°C for 30 minutes",
            "Carbendazim 50% WP — sett dip (1 g/L for 15 min)",
            "Triadimefon 25% WP (1 g/L — sett treatment)"
        ],
        "prevention": [
            "Use smut-free setts from disease-free nurseries",
            "Hot water treatment of seed cane at 52°C for 30 minutes",
            "Remove and burn smut whips before they open and release spores",
            "Rogue out infected clumps from the field",
            "Plant resistant varieties"
        ],
        "severity": "High"
    },

    # Chilli / Hot Pepper (important Indian crop)
    "Chilli___Leaf_curl_virus": {
        "display_name": "Chilli Leaf Curl Virus",
        "description": "Chilli leaf curl is caused by a begomovirus transmitted by the whitefly Bemisia tabaci. It causes severe curling and puckering of leaves.",
        "symptoms": [
            "Upward curling and puckering of leaves",
            "Leaves become small and deformed",
            "Internode shortening giving bushy appearance",
            "Drastic reduction in fruit set and yield"
        ],
        "pesticides": [
            "No cure for virus — control the whitefly vector",
            "Imidacloprid 17.8% SL (0.3 mL/L)",
            "Thiamethoxam 25% WG (0.3 g/L)",
            "Fipronil 5% SC (1.5 mL/L)",
            "Neem oil 1500 ppm (5 mL/L)"
        ],
        "prevention": [
            "Use virus-free nursery seedlings",
            "Grow under insect-proof net (40 mesh) in nursery",
            "Install yellow sticky traps to monitor whiteflies",
            "Uproot and destroy infected plants early",
            "Avoid growing chilli near cotton or tomato"
        ],
        "severity": "Very High"
    },
    "Chilli___Anthracnose_fruit_rot": {
        "display_name": "Chilli Anthracnose (Fruit Rot / Die Back)",
        "description": "Anthracnose of chilli is caused by Colletotrichum capsici and related species. It causes fruit rot and die-back of branches.",
        "symptoms": [
            "Sunken, dark, circular lesions on ripe fruit",
            "Concentric rings of dark fruiting bodies on lesions",
            "Tip die-back of branches progressing downward",
            "Flower drop and reduced fruit set"
        ],
        "pesticides": [
            "Mancozeb 75% WP (2.5 g/L)",
            "Carbendazim 50% WP (1 g/L)",
            "Copper oxychloride 50% WP (3 g/L)",
            "Azoxystrobin 23% SC (1 mL/L)",
            "Seed treatment with Thiram (3 g/kg)"
        ],
        "prevention": [
            "Use disease-free seeds from healthy fruits",
            "Treat seeds with Thiram or Carbendazim",
            "Practice crop rotation (2-3 years)",
            "Avoid overhead irrigation during fruiting",
            "Collect and destroy infected fruits from field"
        ],
        "severity": "High"
    },
    "Chilli___Powdery_mildew": {
        "display_name": "Chilli Powdery Mildew",
        "description": "Powdery mildew of chilli is caused by Leveillula taurica. It produces white powdery patches mainly on the lower leaf surface.",
        "symptoms": [
            "White powdery patches on lower leaf surface",
            "Yellow spots on corresponding upper surface",
            "Severe defoliation exposing fruit to sunscald",
            "Reduced fruit size and quality"
        ],
        "pesticides": [
            "Sulphur 80% WP (3 g/L) — avoid in hot weather above 35°C",
            "Dinocap 48% EC (1 mL/L)",
            "Myclobutanil 10% WP (1 g/L)",
            "Azoxystrobin 23% SC (1 mL/L)"
        ],
        "prevention": [
            "Use resistant varieties",
            "Ensure adequate spacing for air circulation",
            "Avoid water stress",
            "Apply sulfur-based fungicide preventively",
            "Remove severely infected leaves"
        ],
        "severity": "Moderate"
    },

    # Mango (important Indian fruit tree)
    "Mango___Anthracnose": {
        "display_name": "Mango Anthracnose",
        "description": "Anthracnose is caused by Colletotrichum gloeosporioides. It is the most important pre- and post-harvest disease of mango worldwide.",
        "symptoms": [
            "Black spots on flowers causing blossom blight",
            "Dark, sunken lesions on fruit",
            "Leaf spots and twig die-back",
            "Post-harvest black decay of ripe fruit"
        ],
        "pesticides": [
            "Carbendazim 50% WP (1 g/L)",
            "Mancozeb 75% WP (2.5 g/L)",
            "Copper oxychloride 50% WP (3 g/L)",
            "Azoxystrobin 23% SC (1 mL/L)",
            "Hot water treatment of fruit at 52°C for 5 min (post-harvest)"
        ],
        "prevention": [
            "Spray fungicide at panicle emergence and again at fruit set",
            "Prune canopy for better air circulation and light",
            "Remove dead wood and mummified fruit",
            "Harvest fruit carefully to avoid wounds",
            "Hot water dip of fruit after harvest to control latent infections"
        ],
        "severity": "High"
    },
    "Mango___Powdery_mildew": {
        "display_name": "Mango Powdery Mildew",
        "description": "Powdery mildew of mango is caused by Oidium mangiferae. It affects flowers, young fruit, and leaves, causing heavy flower and fruit drop.",
        "symptoms": [
            "White powdery coating on flowers, panicles, and young leaves",
            "Flower and fruitlet drop",
            "Malformed and stunted fruit",
            "Distorted young leaves"
        ],
        "pesticides": [
            "Sulphur 80% WP (3 g/L)",
            "Dinocap 48% EC (1 mL/L)",
            "Tridemorph 80% EC (0.5 mL/L)",
            "Myclobutanil 10% WP (1 g/L)"
        ],
        "prevention": [
            "Spray sulphur at panicle emergence (before flowering)",
            "Repeat spray during full bloom if weather is cool and humid",
            "Prune trees for proper air circulation",
            "Avoid excessive nitrogen fertilization",
            "Remove and destroy affected panicles"
        ],
        "severity": "Moderate"
    },

    # Banana (major Indian fruit crop)
    "Banana___Panama_wilt": {
        "display_name": "Banana Panama Wilt (Fusarium Wilt)",
        "description": "Panama disease is caused by Fusarium oxysporum f. sp. cubense. It is one of the most destructive diseases of banana worldwide, causing total plant death.",
        "symptoms": [
            "Yellowing of older leaves starting from margins",
            "Leaves collapse and hang around the pseudostem (skirt-like)",
            "Longitudinal splitting of pseudostem base",
            "Reddish-brown discoloration in vascular tissue when pseudostem is cut"
        ],
        "pesticides": [
            "No effective chemical cure available",
            "Carbendazim 50% WP (2 g/L) — soil drench for suppression",
            "Trichoderma viride (50 g/plant as bio-control agent)",
            "Pseudomonas fluorescens (20 g/L — rhizome treatment)"
        ],
        "prevention": [
            "Use disease-free tissue culture plantlets",
            "Practice crop rotation (3-5 years with rice or sugarcane)",
            "Avoid moving soil from infested to clean fields",
            "Treat rhizomes with fungicide + bio-agents before planting",
            "Maintain soil pH above 6.0",
            "Do not use furrow irrigation from infested areas"
        ],
        "severity": "Very High"
    },
    "Banana___Sigatoka_leaf_spot": {
        "display_name": "Banana Sigatoka Leaf Spot",
        "description": "Sigatoka leaf spot includes Yellow Sigatoka (Mycosphaerella musicola) and Black Sigatoka (M. fijiensis). These are the most economically important leaf diseases of banana.",
        "symptoms": [
            "Yellow streaks on leaves that turn brown with gray centers",
            "Streaks enlarge into oval spots with dark borders",
            "Dark brown to black lesions (Black Sigatoka)",
            "Premature drying and death of large leaf areas",
            "Premature fruit ripening and reduced bunch weight"
        ],
        "pesticides": [
            "Mancozeb 75% WP (2.5 g/L)",
            "Propiconazole 25% EC (1 mL/L)",
            "Carbendazim 50% WP (1 g/L)",
            "Chlorothalonil 75% WP (2 g/L)",
            "Mineral oil (agricultural grade) + fungicide for better coverage"
        ],
        "prevention": [
            "De-leaf infected leaves and remove from field",
            "Maintain proper spacing between plants",
            "Ensure good drainage to reduce humidity",
            "Apply fungicide before monsoon season",
            "Use resistant varieties (Poovan, Monthan)"
        ],
        "severity": "High"
    },

    # Onion (important Indian vegetable)
    "Onion___Purple_blotch": {
        "display_name": "Onion Purple Blotch",
        "description": "Purple blotch is caused by Alternaria porri. It is the most important foliar disease of onion in India.",
        "symptoms": [
            "Small, sunken, whitish spots that enlarge into purple-brown lesions",
            "Lesions develop concentric rings",
            "Affected leaves bend and break at lesion point",
            "Severe defoliation reducing bulb size"
        ],
        "pesticides": [
            "Mancozeb 75% WP (2.5 g/L)",
            "Chlorothalonil 75% WP (2 g/L)",
            "Tebuconazole 25.9% EC (1 mL/L)",
            "Copper oxychloride 50% WP (3 g/L)",
            "Add sticker (Teepol) at 1 mL/L for better adherence"
        ],
        "prevention": [
            "Practice crop rotation (2-3 years)",
            "Use healthy bulbs for planting",
            "Maintain proper plant spacing for air circulation",
            "Avoid overhead irrigation",
            "Start protective fungicide sprays before symptoms appear"
        ],
        "severity": "High"
    },

    # Mustard / Rapeseed (important Indian oilseed)
    "Mustard___White_rust": {
        "display_name": "Mustard White Rust (Albugo)",
        "description": "White rust is caused by Albugo candida. It produces white blister-like pustules on leaves, stems, and inflorescence of mustard.",
        "symptoms": [
            "White, shiny, blister-like pustules on lower leaf surface",
            "Corresponding yellow spots on upper surface",
            "Distorted and swollen inflorescence (staghead symptom)",
            "Flowers become sterile — no seed formation in affected heads"
        ],
        "pesticides": [
            "Metalaxyl 8% + Mancozeb 64% WP (Ridomil Gold — 2.5 g/L)",
            "Mancozeb 75% WP (2.5 g/L)",
            "Copper oxychloride 50% WP (3 g/L)",
            "Seed treatment with Metalaxyl 35% WS (6 g/kg seed)"
        ],
        "prevention": [
            "Use resistant varieties",
            "Treat seeds with Metalaxyl before sowing",
            "Practice crop rotation with non-cruciferous crops",
            "Remove and destroy infected plant debris",
            "Timely sowing to avoid peak disease period"
        ],
        "severity": "High"
    },

    # Turmeric (important Indian spice crop)
    "Turmeric___Rhizome_rot": {
        "display_name": "Turmeric Rhizome Rot",
        "description": "Rhizome rot is caused by Pythium aphanidermatum. It is the most destructive disease of turmeric, causing complete rotting of the underground rhizome.",
        "symptoms": [
            "Yellowing and wilting of lower leaves",
            "Soft, watery rot of rhizome",
            "Foul smell from infected rhizome",
            "Collar region becomes soft and water-soaked",
            "Plants pull out easily from soil"
        ],
        "pesticides": [
            "Metalaxyl 8% + Mancozeb 64% WP (Ridomil Gold — 2.5 g/L) — soil drench",
            "Copper oxychloride 50% WP (3 g/L) — soil drench",
            "Trichoderma viride (50 g/plant — soil application)",
            "Rhizome treatment with Mancozeb 75% WP (3 g/L) for 30 min before planting"
        ],
        "prevention": [
            "Select healthy, disease-free seed rhizomes",
            "Treat rhizomes with fungicide + bio-agent before planting",
            "Ensure good soil drainage",
            "Practice crop rotation (3 years minimum)",
            "Apply Trichoderma viride enriched FYM at planting",
            "Drench soil with fungicide at first sign of wilting"
        ],
        "severity": "Very High"
    }
}

# Merge new entries into existing data
data.update(new_entries)

# Write the expanded JSON
with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Expanded disease_info.json from 38 to {len(data)} entries!")
print(f"\nNew crops/diseases added:")
for key in sorted(new_entries.keys()):
    crop = key.split("___")[0].replace("_", " ")
    disease = new_entries[key]["display_name"]
    print(f"  • {crop}: {disease}")
