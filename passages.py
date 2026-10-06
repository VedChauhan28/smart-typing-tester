"""Predefined typing passages grouped by difficulty."""

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


def choose_passage(difficulty: str, length: str, time_limit: int = 60, exclude: str = "") -> str:
    """
    Efficiently select and format a passage matching difficulty, time limit, and length
    without breaking sentences or exceeding difficulty constraints.
    """
    if length == "custom":
        return exclude or ""

    if difficulty not in PASSAGES:
        difficulty = "medium"

    options = PASSAGES[difficulty]
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