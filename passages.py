"""Predefined typing passages grouped by difficulty and language."""

import random
import re


DIFFICULTIES = {
    "easy": {
        "label": "Easy",
        "description": "Short, simple sentences (max 2 sentences)",
    },
    "medium": {
        "label": "Medium",
        "description": "Varied vocabulary and sentences (max 5 sentences)",
    },
    "hard": {
        "label": "Hard",
        "description": "Paragraphs with technical words, numbers, and punctuation",
    },
}

LANGUAGES = {
    "english": {"label": "English", "script": "latin"},
    "hindi": {"label": "Hindi (हिन्दी)", "script": "devanagari"},
    "gujarati": {"label": "Gujarati (ગુજરાતી)", "script": "gujarati"},
}

LENGTHS = {
    "short": {"label": "Short", "description": "About 20–50 words"},
    "medium": {"label": "Medium", "description": "About 50–100 words"},
    "long": {"label": "Long", "description": "About 100–200 words"},
    "custom": {"label": "Custom", "description": "Practice your own text"},
}

TIME_OPTIONS = (30, 60, 120)

PASSAGES = {
    "easy": [
        (
            "Today is a bright and peaceful day. "
            "I like to start my morning with a short walk and a cup of tea."
        ),
        (
            "Learning to type is fun and easy. "
            "Daily practice will help you get faster every week."
        ),
        (
            "The sun shines brightly through the window. "
            "It is a wonderful time to learn something new today."
        ),
        (
            "Reading books opens up new worlds. "
            "You can discover exciting stories on every page."
        ),
        (
            "A small step today leads to big progress tomorrow. "
            "Keep your eyes on the screen and stay relaxed."
        ),
        (
            "Music brings joy and comfort to our lives. "
            "Listening to a favorite song can make your day happy."
        ),
        (
            "Walking in nature clears the mind. "
            "Fresh air and green trees help us feel calm and happy."
        ),
        (
            "Cooking a simple meal is rewarding. "
            "Good food shared with friends makes every evening better."
        ),
        (
            "The blue ocean is vast and full of wonder. "
            "Watching gentle waves roll onto the sandy shore brings peace to your heart."
        ),
        (
            "Countless stars light up the clear night sky. "
            "Stargazing reminds us how big and beautiful our universe is."
        ),
        (
            "Dogs are loyal companions that bring happiness to every home. "
            "Playing fetch in the backyard is a great way to spend an afternoon."
        ),
        (
            "Raindrops patter softly against the glass. "
            "Sitting indoors with a warm cup of cocoa makes rainy days feel cozy."
        ),
        (
            "Practice makes progress in everything you choose to do. "
            "Focus on small improvements every single day."
        ),
        (
            "Planting seeds in rich soil requires care and patience. "
            "Watching green sprouts grow into colorful flowers is a joy."
        ),
    ],
    "medium": [
        (
            "Many useful inventions begin with a simple question about daily life. "
            "A person notices an everyday problem and wonders how to improve it. "
            "The first attempt is rarely perfect, so the creator tests and refines the design. "
            "With patience and practice, small changes lead to great results. "
            "Learning from mistakes is an important part of the journey."
        ),
        (
            "A college library is a great place to focus and study peacefully. "
            "Students come here to read books, write reports, and prepare for upcoming exams. "
            "The quiet atmosphere helps everyone stay organized and pay attention to detail. "
            "Sharing resources with classmates makes challenging projects much easier to handle. "
            "Building good study habits early will serve you well in the future."
        ),
        (
            "Taking care of our environment starts with small daily choices. "
            "Turning off extra lights and saving water can make a real difference over time. "
            "Many communities now recycle paper, glass, and plastic to reduce waste. "
            "Walking or cycling for short trips is also good for health and nature. "
            "Working together helps keep our parks clean and pleasant for everyone."
        ),
        (
            "Working on a group project requires good communication and planning. "
            "Each team member brings different skills and ideas to the table. "
            "When tasks are divided fairly, the workload becomes much lighter for everyone. "
            "Regular updates ensure that all members stay on the same page. "
            "Completing a project together builds trust and creates strong friendships."
        ),
        (
            "Traveling to new places allows us to experience different cultures and traditions. "
            "Trying local foods and meeting new people broadens our perspective on the world. "
            "Careful planning helps make any trip enjoyable and stress-free. "
            "Keeping a travel journal is a great way to preserve memories. "
            "Every journey teaches us something valuable about ourselves."
        ),
        (
            "Digital technology has changed how people learn and collaborate across distances. "
            "Online classes allow students to study at their own pace from almost anywhere. "
            "However, staying disciplined and managing screen time remain important challenges. "
            "Setting daily goals helps maintain focus and prevents unnecessary distractions. "
            "Balance is key to using technology productively."
        ),
        (
            "In the quiet town of Avonlea, the morning sun painted the hills in soft shades of gold and rose. "
            "Anne looked out her window with eyes wide with wonder, captivated by the blossom-covered trees. "
            "She believed that every new morning offered a fresh start and endless possibilities. "
            "With a grateful heart, she prepared for another day filled with curiosity and imagination."
        ),
        (
            "Astronomers use giant telescopes to peer billions of light-years into deep space. "
            "By analyzing distant light rays, scientists learn about the origins of stars and galaxies. "
            "Space exploration expands human knowledge and challenges our understanding of physics. "
            "Every cosmic discovery inspires future generations to look up at the night sky and dream."
        ),
        (
            "Ancient architects constructed magnificent stone monuments that have endured for thousands of years. "
            "The precision of their craftsmanship continues to amaze modern engineers and historians. "
            "These historical landmarks tell stories of cultural achievements, trade networks, and social organization. "
            "Preserving such heritage allows us to honor the past while learning for the future."
        ),
        (
            "Developing a growth mindset encourages us to view challenges as opportunities to learn rather than obstacles. "
            "When you encounter a difficult problem, persistence and strategy matter far more than initial talent. "
            "Taking breaks to reflect allows your mind to process complex information and discover fresh solutions. "
            "True success is built step by step through steady dedication."
        ),
        (
            "Coral reefs are among the most diverse marine ecosystems on planet Earth. "
            "Although they cover less than one percent of the ocean floor, they support thousands of fish species and aquatic plants. "
            "Protecting coral reefs requires reducing pollution and managing coastal development responsibly. "
            "Healthy oceans are essential for maintaining global ecological balance."
        ),
        (
            "The old bookstore at the corner of the avenue smelled of aged paper and roasted coffee beans. "
            "Shelves stretched up to the high ceiling, crammed with leather-bound volumes and forgotten classics. "
            "Visitors often lost track of time while wandering through the narrow aisles of stories. "
            "Every book held a unique journey waiting for a curious reader to open its cover."
        ),
    ],
    "hard": [
        (
            "Building robust software requires careful architectural planning, methodical testing, and rigorous code reviews. "
            "When an unhandled exception occurs in a production environment, engineers must analyze stack traces, inspect memory allocations, and trace state mutations to isolate the root cause. "
            "Refactoring legacy codebases often involves updating outdated dependencies, optimizing database queries (such as SQL JOIN operations), and maintaining strict API backwards compatibility. "
            "Clear documentation and type annotations make complex systems significantly easier to maintain over time."
        ),
        (
            "Empirical scientific research depends on precise measurement, reproducible methodologies, and objective statistical analysis. "
            "In trial #4B, researchers recorded a baseline temperature of 98.6°F while monitoring automated sensor arrays at 100ms intervals. "
            "Discrepancies between theoretical predictions and experimental datasets frequently reveal underlying variables or measurement errors. "
            "Documenting experimental parameters in detail enables peer reviewers to validate hypotheses, replicate findings, and advance scientific knowledge across multidisciplinary fields."
        ),
        (
            "Modern web applications leverage asynchronous event loops, reactive UI state management, and optimized network protocols to deliver low-latency user experiences. "
            "Deploying microservices to cloud environments requires configuring container orchestration (such as Kubernetes), managing API gateways, and implementing TLS/SSL encryption for data in transit. "
            "Monitoring tools aggregate metrics like CPU usage, response times (under 50ms), and error rates to ensure 99.99% service availability during peak traffic spikes."
        ),
        (
            "Algorithmic efficiency is fundamentally evaluated using Big-O notation to describe time and space complexity scaling behavior. "
            "Sorting algorithms like QuickSort achieve an average time complexity of O(N log N), whereas inefficient nested loops can quickly degrade performance to O(N²). "
            "When handling datasets exceeding 1,000,000 records, developers must select appropriate data structures—such as hash maps, binary search trees, or heap queues—to minimize memory overhead and execution latency."
        ),
        (
            "Financial cryptography and distributed ledger systems rely on cryptographic hash functions, public-key infrastructure (PKI), and consensus mechanisms to secure transactions. "
            "Decentralized protocols utilize zero-knowledge proofs (zk-SNARKs) to verify data integrity without exposing underlying sensitive credentials. "
            "Network throughput and block finality latency remain critical bottlenecks during periods of high transaction volume."
        ),
        (
            "Deep neural networks process multidimensional tensor representations through stacked convolutional and recurrent layers. "
            "During backward propagation, gradient descent algorithms adjust weight parameters (e.g., learning rate α = 0.001) to minimize loss metrics across training batches. "
            "Overfitting remains a critical concern, requiring techniques such as dropout regularization, early stopping, and L2 penalty terms."
        ),
        (
            "Macroeconomic policy decisions rely on quantitative indicators including Core CPI inflation rates, 10-year Treasury yield curves, and unemployment statistics (U-3 vs. U-6). "
            "Central banks manipulate benchmark interest rates to stabilize purchasing power while maintaining liquidity across interbank lending facilities. "
            "Volatility in global currency pairs often reflects shifting trade balances and geopolitical uncertainties."
        ),
        (
            "During trial run #87-C, spectrographic analysis revealed trace elements of Nitrogen (N₂), Methane (CH₄), and Carbon Dioxide (CO₂) at concentration levels below 0.05 ppm. "
            "Automated data pipelines processed 4,500 sensor readings per second, filtering anomalies via a 3-sigma standard deviation threshold. "
            "Precision calibration ensured an error margin of less than ±0.02% across all temperature sensors."
        ),
        (
            "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity. "
            "The period was so far like the present period, that some of its noisiest authorities insisted on its being received, for good or for evil, in the superlative degree of comparison only."
        ),
        (
            "Establishing zero-trust security architecture demands rigorous identity verification, mutual TLS authentication (mTLS), and granular role-based access control (RBAC). "
            "System administrators monitor audit logs for unauthorized API requests, anomalous IP addresses (e.g., 192.168.1.100:8443), and potential buffer overflow exploits. "
            "Cryptographic keys must be rotated regularly using Hardware Security Modules (HSM)."
        ),
    ],
}

# ---------------------------------------------------------------------------
# Hindi passages
# ---------------------------------------------------------------------------
HINDI_PASSAGES = {
    "easy": [
        (
            "आज का दिन बहुत सुंदर है। "
            "मैं सुबह टहलने जाता हूँ और ताज़ी हवा का आनंद लेता हूँ।"
        ),
        (
            "पढ़ाई करना बहुत ज़रूरी है। "
            "हर दिन थोड़ा-थोड़ा पढ़ने से ज्ञान बढ़ता है।"
        ),
        (
            "बच्चे खेल के मैदान में खुशी से खेलते हैं। "
            "उनकी हँसी सुनकर मन प्रसन्न हो जाता है।"
        ),
        (
            "सूर्य उदय होने पर प्रकृति जाग उठती है। "
            "पक्षी मधुर गीत गाने लगते हैं।"
        ),
        (
            "मेहनत और लगन से हर काम सफल होता है। "
            "कभी हार मत मानो और आगे बढ़ते रहो।"
        ),
        (
            "किताबें हमारी सबसे अच्छी दोस्त होती हैं। "
            "वे हमें नई दुनिया से परिचित कराती हैं।"
        ),
        (
            "स्वस्थ रहने के लिए प्रतिदिन व्यायाम करना चाहिए। "
            "संतुलित भोजन भी उतना ही आवश्यक है।"
        ),
        (
            "नदी का पानी निर्मल और शीतल होता है। "
            "उसकी कल-कल की आवाज़ मन को शांत करती है।"
        ),
    ],
    "medium": [
        (
            "भारत एक विविधताओं से भरा देश है। "
            "यहाँ अनेक भाषाएँ, संस्कृतियाँ और परंपराएँ एक साथ फलती-फूलती हैं। "
            "उत्तर की बर्फीली पहाड़ियों से लेकर दक्षिण के नीले समुद्र तक, यह देश अद्भुत है। "
            "यहाँ का इतिहास गर्व और वीरता की कहानियों से भरा पड़ा है। "
            "हमें अपनी इस विरासत को संजो कर रखना चाहिए।"
        ),
        (
            "विज्ञान और तकनीक ने हमारे जीवन को बहुत आसान बना दिया है। "
            "मोबाइल फ़ोन और इंटरनेट ने दूरियाँ कम कर दी हैं। "
            "आज हम घर बैठे दुनिया के किसी भी कोने से जानकारी प्राप्त कर सकते हैं। "
            "लेकिन तकनीक का सही उपयोग करना भी उतना ही महत्वपूर्ण है। "
            "इसे सीखने और सिखाने के साधन के रूप में अपनाएँ।"
        ),
        (
            "पर्यावरण की सुरक्षा हम सभी की जिम्मेदारी है। "
            "पेड़-पौधे लगाने से वायु शुद्ध होती है और बारिश अच्छी होती है। "
            "प्लास्टिक का उपयोग कम करके हम नदियों और समुद्र को साफ रख सकते हैं। "
            "सौर ऊर्जा और पवन ऊर्जा जैसे नवीकरणीय स्रोतों को अपनाना चाहिए। "
            "एक हरा-भरा भविष्य बनाना हम सभी का कर्तव्य है।"
        ),
        (
            "शिक्षा जीवन की सबसे बड़ी पूँजी है। "
            "एक शिक्षित व्यक्ति न केवल अपना बल्कि समाज का भी उत्थान करता है। "
            "विद्यालय केवल किताबी ज्ञान नहीं देते, बल्कि जीवन के मूल्य भी सिखाते हैं। "
            "अनुशासन, सहयोग और ईमानदारी शिक्षा के साथ-साथ सीखे जाते हैं। "
            "इसलिए प्रत्येक बच्चे को शिक्षा का अवसर मिलना चाहिए।"
        ),
    ],
    "hard": [
        (
            "आधुनिक अर्थव्यवस्था में डिजिटल मुद्रा और ब्लॉकचेन तकनीक का महत्व तेज़ी से बढ़ रहा है। "
            "विकेन्द्रीकृत वित्तीय प्रणालियाँ (DeFi) पारंपरिक बैंकिंग को चुनौती दे रही हैं। "
            "क्रिप्टोग्राफ़िक एल्गोरिदम जैसे SHA-256 और RSA-2048 डेटा सुरक्षा की रीढ़ हैं। "
            "नीति-निर्माताओं को नवाचार और विनियमन के बीच संतुलन बनाना होगा।"
        ),
        (
            "कृत्रिम बुद्धिमत्ता (AI) और मशीन लर्निंग ने स्वास्थ्य-सेवा, शिक्षा तथा उद्योग में क्रांति ला दी है। "
            "न्यूरल नेटवर्क के माध्यम से कंप्यूटर अब चित्र पहचान और प्राकृतिक भाषा प्रसंस्करण में मानव-स्तर की क्षमता प्राप्त कर चुके हैं। "
            "एल्गोरिदम के प्रशिक्षण के लिए टेराबाइट डेटा और GPU क्लस्टर की आवश्यकता होती है। "
            "इस तकनीक के नैतिक उपयोग को सुनिश्चित करना शोधकर्ताओं की प्राथमिकता है।"
        ),
        (
            "भारत की जनगणना 2011 के अनुसार देश की साक्षरता दर 74.04% थी, जो 2001 की तुलना में 9.2% अधिक है। "
            "ग्रामीण और शहरी क्षेत्रों में शिक्षा की गुणवत्ता में अभी भी व्यापक अंतर है। "
            "सरकारी योजनाएँ जैसे 'बेटी बचाओ, बेटी पढ़ाओ' और 'मिड-डे मील' इस खाई को पाटने का प्रयास कर रही हैं। "
            "डिजिटल शिक्षा प्लेटफ़ॉर्म दूरदराज़ के क्षेत्रों तक पहुँच बढ़ाने में सहायक सिद्ध हो रहे हैं।"
        ),
    ],
}

# ---------------------------------------------------------------------------
# Gujarati passages
# ---------------------------------------------------------------------------
GUJARATI_PASSAGES = {
    "easy": [
        (
            "આજ નો દિવસ ખૂબ સુંદર છે. "
            "હું સવારે ચાલવા જઉ છું અને ताजी हवाનો આનંદ માણું છું."
        ),
        (
            "ભણવું ખૂબ જ જરૂરી છે. "
            "દરરોજ થોડું-થોડું ભણવાથી જ્ઞાન વધે છે."
        ),
        (
            "બાળકો મેદાનમાં ખૂબ ખુશીથી રમે છે. "
            "તેમનો ઉલ્લાસ જોઈ મન પ્રસન્ન થઈ જાય છે."
        ),
        (
            "સૂર્ય ઊગતા પ્રકૃતિ જાગી ઊઠે છે. "
            "પક્ષીઓ મીઠા સૂર ગાવા લાગે છે."
        ),
        (
            "પ્રામાણિકતા અને મહેનત ક્યારેય નિષ્ફળ જતા નથી. "
            "હિંમત રાખો અને આગળ વધતા રહો."
        ),
        (
            "પુસ્તકો આપણા સૌથી સારા મિત્ર છે. "
            "તે આપણને નવી દુનિયા સાથે પરિચય કરાવે છે."
        ),
        (
            "સ્વસ્થ રહેવા માટે રોજ કસરત કરવી જોઈએ. "
            "સંતુલિત આહાર પણ એટલો જ જરૂરી છે."
        ),
        (
            "નદીનું પાણી નિર્મળ અને ઠંડું હોય છે. "
            "તેનો ખળ-ખળ અવાજ મનને શાંત કરે છે."
        ),
    ],
    "medium": [
        (
            "ગુજરાત ભારતનું એક સમૃદ્ધ અને ઐતિહાસિક રાજ્ય છે. "
            "અહીંની સંસ્કૃતિ, ભોજન, કળા અને ઉત્સવો ખૂબ વૈવિધ્યસભર છે. "
            "નવરાત્રિ, ઉત્તરાયણ અને દિવાળી અહીં ધૂમધામથી ઊજવાય છે. "
            "ગુજરાતી ઉદ્યોગ-સાહસિક ભાવના આખી દુનિયામાં પ્રખ્યાત છે. "
            "આ ભૂમિ ગાંધીજી અને સરદાર પટેલ જેવા મહાપુરુષોની ભૂમિ છે."
        ),
        (
            "વિજ્ઞાન અને ટેકનોલોજીએ આપણું જીવન સહેલું કરી દીધું છે. "
            "મોબાઇલ ફોન અને ઇન્ટરનેટ દ્વારા આખી દુનિયા હથેળીમાં આવી ગઈ છે. "
            "ઘરે બેઠા ખરીદી, ભણવું અને કામ કરવું આજે સામાન્ય બની ગયું છે. "
            "જોકે ટેકનોલોજીનો સાચો ઉપયોગ અને સ્ક્રીન-સમય પર નિયંત્રણ જરૂરી છે. "
            "ડિજિટલ સાક્ષરતા આજના સમયની સૌથી મોટી જરૂરિયાત છે."
        ),
        (
            "પર્યાવરણ રક્ષણ આપણી સૌની જવાબદારી છે. "
            "વૃક્ષો વાવવાથી હવા શુદ્ધ રહે છે અને ઓક્સિજન મળે છે. "
            "પ્લાસ્ટિકનો ઉપયોગ ઘટાડીને નદીઓ અને સમુદ્ર સ્વચ્છ રાખી શકાય છે. "
            "સૌર ઊર્જા જેવા નવીન સ્ત્રોત અપનાવવા જોઈએ. "
            "ભવિષ્યની પેઢી માટે સ્વચ્છ ભૂમિ, સ્વચ્છ જળ અને શ્વાસ-સ્વચ્છ હવા છોડવી જોઈએ."
        ),
        (
            "શિક્ષણ જીવનની સૌથી મૂલ્યવાન સંપત્તિ છે. "
            "ભણેલ-ગણેલ વ્યક્તિ પોતે ઉન્નત થઈ સમાજ સુધારે છે. "
            "શાળા માત્ર ચોપડીઓ નહીં, ચારિત્ર્ય ઘડવાનું ધામ છે. "
            "શિસ્ત, સહકાર અને સ્વ-શ્રદ્ધા ત્યાંથી જ શીખાય છે. "
            "તેથી દરેક બાળકને ભણવાની સમાન તક મળવી જ જોઈએ."
        ),
    ],
    "hard": [
        (
            "ભારતીય ચૂંટણી પ્રક્રિયામાં ઈ.વી.એમ. (ઇલેક્ટ્રૉનિક વૉટિંગ મશીન) અને VVPAT ની ભૂમિકા ખૂબ મહત્ત્વની છે. "
            "2019ની સામાન્ય ચૂંટણીમાં 91.05 કરોડ મતદારોમાંથી 67.4% એ મત આપ્યો. "
            "ચૂંટણી-પ્રક્રિયા, આચારસંહિતા અને ન્યાયયુક્ત પ્રતિનિધિત્વ લોકશાહીની ધરી છે. "
            "ટેકનોલૉજી, ડેટા-ઍનૅલિટિક્સ અને AI ભવિષ્યમાં ચૂંટણી-વ્યૂહ ઘડવામાં મહત્ત્વ ભજવશે."
        ),
        (
            "ISRO (ભારતીય અવકાશ સંશોધન સંગઠન)ના ચંદ્રયાન-3 મિશને 2023માં ઇતિહાસ રચ્યો. "
            "ચંદ્રના દક્ષિણ ધ્રુવ વિસ્તારમાં ઉતરાણ કરનારો ભારત પ્રથમ દેશ બન્યો. "
            "વિક્રમ લૅન્ડર અને પ્રજ્ઞાન રોવરે ચંદ્ર-સપાટીનો ડેટા 14 દિવસ સુધી ભેગો કર્યો. "
            "इस उपलब्धिले भारतीय वैज्ञानिकों की प्रतिभा और परिश्रम को विश्व के सामने सिद्ध किया।"
        ),
        (
            "ગુજરાત ઔદ્યોગિક વિકાસ નિગમ (GIDC)ની સ્થાપના 1962માં ઔદ્યોગિક ઇન્ફ્રાસ્ટ્રક્ચર વિકસાવવા થઈ હતી. "
            "આજે ગુજરાત ભારતના GDP માં 8.3% ફાળો આપે છે, અને 40,000+ ઔદ્યોગિક એકમો ધરાવે છે. "
            "GIFT City (Gujarat International Finance Tec-City) ભારતનું પ્રથમ ઑપરેશનલ સ્માર્ટ સિટી છે. "
            "ઊર્જા ક્ષેત્રે ગુજરાત 100% ગ્રામ-વિદ્યુતીકરણ પ્રાપ્ત કરનાર ભારતનું પ્રથમ રાજ્ય છે."
        ),
    ],
}

# Master language passage map
LANGUAGE_PASSAGES = {
    "english": PASSAGES,
    "hindi": HINDI_PASSAGES,
    "gujarati": GUJARATI_PASSAGES,
}


def get_sentences(text: str) -> list[str]:
    """Split text cleanly into sentences based on punctuation."""
    raw = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in raw if s.strip()]


def word_count(text: str) -> int:
    """Return total word count of text."""
    return len(text.split())


def get_target_word_range(length: str, time_limit: int = 60) -> tuple[int, int]:
    """Calculate target min and max words calibrated for time limit and paragraph length."""
    scale = {30: 0.55, 60: 1.0, 120: 1.85}.get(time_limit, 1.0)
    base_ranges = {
        "short": (20, 45),
        "medium": (45, 85),
        "long": (85, 160),
    }
    min_b, max_b = base_ranges.get(length, (45, 85))
    min_w = max(15, int(min_b * scale))
    max_w = max(25, int(max_b * scale))
    return (min_w, max_w)


def _fit_to_length(text: str, length: str, difficulty: str, time_limit: int = 60) -> str:
    """
    Trim a source passage to fit requested length and time limit without cutting sentences in half.
    Enforces maximum sentence limits based on difficulty:
    - Easy: max 2 sentences
    - Medium: max 5 sentences
    - Hard: paragraph level
    """
    if length == "custom":
        return text

    sentences = get_sentences(text)

    # Enforce maximum sentence count per difficulty
    if difficulty == "easy":
        sentences = sentences[:2]
    elif difficulty == "medium":
        sentences = sentences[:5]

    if not sentences:
        return text

    _min_words, max_words = get_target_word_range(length, time_limit)

    result_sentences = []
    current_words = 0

    for sentence in sentences:
        w_count = word_count(sentence)
        if current_words + w_count <= max_words or not result_sentences:
            result_sentences.append(sentence)
            current_words += w_count
        else:
            break

    return " ".join(result_sentences)


def choose_passage(
    difficulty: str,
    length: str,
    time_limit: int = 60,
    exclude: str = "",
    language: str = "english",
) -> str:
    """
    Efficiently select and format a passage matching difficulty, time limit, length,
    and language without breaking sentences or exceeding difficulty constraints.
    """
    if length == "custom":
        return exclude or ""

    # Resolve passage bank for the requested language
    passage_bank = LANGUAGE_PASSAGES.get(language, PASSAGES)

    if difficulty not in passage_bank:
        difficulty = "medium"

    options = passage_bank[difficulty]
    candidates = [p for p in options if p != exclude] or options

    max_sentences = {"easy": 2, "medium": 5, "hard": None}.get(difficulty)
    min_words, _max_words = get_target_word_range(length, time_limit)

    # Find the candidate that best fits the target word range out of the box
    best_candidate = None
    best_score = float("inf")

    for cand in candidates:
        s_list = get_sentences(cand)
        if max_sentences is not None:
            s_list = s_list[:max_sentences]
        w = word_count(" ".join(s_list))
        score = abs(w - min_words)
        if score < best_score:
            best_score = score
            best_candidate = cand

    source = best_candidate or random.choice(candidates)
    sentences = get_sentences(source)
    if max_sentences is not None:
        sentences = sentences[:max_sentences]

    # If long mode or 120s test requires more words, append complete sentences up to max_sentences
    if word_count(" ".join(sentences)) < min_words and (max_sentences is None or len(sentences) < max_sentences):
        additions = [p for p in candidates if p != source]
        random.shuffle(additions)
        for addition in additions:
            for s in get_sentences(addition):
                if max_sentences is not None and len(sentences) >= max_sentences:
                    break
                sentences.append(s)
                if word_count(" ".join(sentences)) >= min_words:
                    break
            if max_sentences is not None and len(sentences) >= max_sentences:
                break
            if word_count(" ".join(sentences)) >= min_words:
                break

    full_text = " ".join(sentences)
    return _fit_to_length(full_text, length, difficulty, time_limit=time_limit)