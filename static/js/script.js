/* Browser-side timer, live interactive paragraph canvas, typing sound effects, and result submission. */
(function () {
  const configElement = document.getElementById("test-config");
  if (!configElement) return;

  const config = JSON.parse(configElement.textContent);
  window.localStorage.setItem("smartTypingLastPassage", config.passage);
  window.localStorage.setItem("smartTypingIsCustom", config.is_custom ? "true" : "false");
  
  const passageCard = document.getElementById("passage-card");
  const passageDisplay = document.getElementById("passage-display");
  const input = document.getElementById("typing-input");
  const message = document.getElementById("test-message");
  const timeRemaining = document.getElementById("time-remaining");
  const progressElement = document.getElementById("progress");
  const wpmElement = document.getElementById("wpm");
  const accuracyElement = document.getElementById("accuracy");
  const errorsElement = document.getElementById("errors");
  const correctElement = document.getElementById("correct-chars");
  const restartBtn = document.getElementById("restart-test-btn");
  const focusHint = document.getElementById("focus-hint");
  const soundToggleBtn = document.getElementById("sound-toggle-btn");

  // Paragraph change & switcher references
  const newPassageBtn = document.getElementById("new-passage-btn");
  const changePassageBtn = document.getElementById("change-passage-btn");
  const lengthPillButtons = document.querySelectorAll(".length-pill");
  const passageSelect = document.getElementById("passage-select");
  const passageToast = document.getElementById("passage-toast");
  const currentLengthTag = document.getElementById("current-length-tag");

  // Custom passage modal references
  const customModal = document.getElementById("custom-paragraph-modal");
  const openCustomModalBtn = document.getElementById("open-custom-modal-btn");
  const closeModalBtn = document.getElementById("close-modal-btn");
  const cancelModalBtn = document.getElementById("cancel-modal-btn");
  const applyCustomModalBtn = document.getElementById("apply-custom-modal-btn");
  const modalCustomText = document.getElementById("modal-custom-text");
  const modalCharCount = document.getElementById("modal-char-count");
  const modalWordCount = document.getElementById("modal-word-count");
  const modalError = document.getElementById("modal-error");

  // Sync lang attribute to hidden input so the correct script font is applied
  if (passageDisplay && input) {
    const lang = passageDisplay.getAttribute("lang");
    if (lang) input.setAttribute("lang", lang);
  }

  let timerId = null;
  let startTime = null;
  let elapsedSeconds = 0;
  let hasFinished = false;
  let lastTypedLength = 0;

  // Sound settings
  let soundEnabled = window.localStorage.getItem("smartTypingSoundEnabled") !== "false";

  function updateSoundUI() {
    if (soundToggleBtn) {
      soundToggleBtn.innerHTML = soundEnabled ? "🔊 Sound: ON" : "🔇 Sound: OFF";
      soundToggleBtn.classList.toggle("button-active", soundEnabled);
    }
  }

  if (soundToggleBtn) {
    soundToggleBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      soundEnabled = !soundEnabled;
      window.localStorage.setItem("smartTypingSoundEnabled", soundEnabled ? "true" : "false");
      updateSoundUI();
      focusInput();
    });
    updateSoundUI();
  }

  // Typing.com Official Sound Engine (Exact Audio Assets & Sprites)
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  let audioCtx = null;
  let keySpriteBuffer = null;
  let errorAudioBuffer = null;
  let starAudioBuffer = null;
  let popAudioBuffer = null;

  function getAudioContext() {
    if (!audioCtx) {
      audioCtx = new AudioContext();
    }
    if (audioCtx.state === "suspended") {
      audioCtx.resume();
    }
    return audioCtx;
  }

  // Exact Typing.com keysprite slices [startSeconds, durationSeconds]
  const KEY_SPRITE_SLICES = [
    [0.000, 0.250],
    [0.750, 0.334],
    [1.584, 0.315],
    [2.399, 0.305],
    [3.203, 0.309],
    [4.012, 0.286],
    [4.798, 0.329],
    [5.628, 0.307],
    [6.435, 0.302],
    [7.237, 0.313],
    [8.050, 0.343],
    [8.893, 0.288]
  ];
  const SPACE_SLICE = [12.069, 0.382];

  async function loadAudioBuffer(url) {
    try {
      const res = await fetch(url);
      if (!res.ok) return null;
      const arr = await res.arrayBuffer();
      const ctx = getAudioContext();
      return await ctx.decodeAudioData(arr);
    } catch (e) {
      return null;
    }
  }

  function initTypingAudio() {
    loadAudioBuffer("/static/audio/keysprite.mp3").then(buf => { keySpriteBuffer = buf; });
    loadAudioBuffer("/static/audio/error.mp3").then(buf => { errorAudioBuffer = buf; });
    loadAudioBuffer("/static/audio/star.mp3").then(buf => { starAudioBuffer = buf; });
    loadAudioBuffer("/static/audio/pop.mp3").then(buf => { popAudioBuffer = buf; });
  }

  initTypingAudio();

  // Resume AudioContext on initial user gesture (required by browser autoplay policy)
  document.addEventListener("click", () => {
    if (audioCtx && audioCtx.state === "suspended") audioCtx.resume();
  }, { once: true });
  document.addEventListener("keydown", () => {
    if (audioCtx && audioCtx.state === "suspended") audioCtx.resume();
  }, { once: true });

  function playKeySound(isSpace = false, isError = false) {
    if (!soundEnabled) return;
    try {
      const ctx = getAudioContext();

      if (isError) {
        if (errorAudioBuffer) {
          const src = ctx.createBufferSource();
          src.buffer = errorAudioBuffer;
          const gainNode = ctx.createGain();
          gainNode.gain.value = 1.0;
          src.connect(gainNode);
          gainNode.connect(ctx.destination);
          src.start(0);
          return;
        }
      }

      if (keySpriteBuffer) {
        const slice = isSpace ? SPACE_SLICE : KEY_SPRITE_SLICES[Math.floor(Math.random() * KEY_SPRITE_SLICES.length)];
        const src = ctx.createBufferSource();
        src.buffer = keySpriteBuffer;
        const gainNode = ctx.createGain();
        gainNode.gain.value = 1.0;
        src.connect(gainNode);
        gainNode.connect(ctx.destination);
        src.start(0, slice[0], slice[1]);
        return;
      }
    } catch (e) {}
  }

  function playSuccessChime() {
    if (!soundEnabled) return;
    try {
      const ctx = getAudioContext();
      if (starAudioBuffer) {
        const src = ctx.createBufferSource();
        src.buffer = starAudioBuffer;
        const gainNode = ctx.createGain();
        gainNode.gain.value = 0.95;
        src.connect(gainNode);
        gainNode.connect(ctx.destination);
        src.start(0);
        return;
      }
    } catch (e) {}
  }

  function playPopSound() {
    if (!soundEnabled) return;
    try {
      const ctx = getAudioContext();
      if (popAudioBuffer) {
        const src = ctx.createBufferSource();
        src.buffer = popAudioBuffer;
        const gainNode = ctx.createGain();
        gainNode.gain.value = 0.85;
        src.connect(gainNode);
        gainNode.connect(ctx.destination);
        src.start(0);
      }
    } catch (e) {}
  }

  function renderPassage(typedText) {
    if (!passageDisplay) return;
    passageDisplay.innerHTML = "";
    let activeSpan = null;
    
    Array.from(config.passage).forEach((character, index) => {
      const span = document.createElement("span");
      span.textContent = character;
      if (index < typedText.length) {
        span.className = typedText[index] === character ? "char-correct" : "char-incorrect";
      } else if (index === typedText.length) {
        span.className = "char-current";
        activeSpan = span;
      } else {
        span.className = "char-pending";
      }
      passageDisplay.appendChild(span);
    });

    if (activeSpan && passageDisplay.scrollHeight > passageDisplay.clientHeight) {
      activeSpan.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }
  }

  function formatSeconds(seconds) {
    return String(Math.max(0, seconds)).padStart(2, "0");
  }

  function calculateStats() {
    const typedText = input.value;
    let correct = 0;
    for (let index = 0; index < typedText.length; index += 1) {
      if (typedText[index] === config.passage[index]) correct += 1;
    }
    const incorrect = Math.max(0, typedText.length - correct);
    const totalTyped = correct + incorrect;
    const accuracy = totalTyped ? (correct / totalTyped) * 100 : 100;

    // Use precise high-res timer if started
    let timeInSeconds = elapsedSeconds;
    if (startTime !== null) {
      timeInSeconds = (performance.now() - startTime) / 1000;
    }
    timeInSeconds = Math.max(timeInSeconds, 0.2); // avoid division by zero
    const minutes = timeInSeconds / 60;
    const wpm = (correct / 5) / minutes;
    const progressPercent = Math.min(100, Math.round((typedText.length / config.passage.length) * 100));

    return {
      wpm: Math.max(0, wpm),
      accuracy,
      errors: incorrect,
      correctChars: correct,
      incorrectChars: incorrect,
      typedLength: typedText.length,
      progressPercent,
      exactTimeTaken: Math.max(1, Math.round(timeInSeconds))
    };
  }

  function updateStats() {
    const stats = calculateStats();
    if (wpmElement) wpmElement.textContent = Math.round(stats.wpm);
    if (accuracyElement) accuracyElement.innerHTML = `${Math.round(stats.accuracy)}<small>%</small>`;
    if (errorsElement) errorsElement.textContent = stats.errors;
    if (correctElement) correctElement.textContent = stats.correctChars;
    if (progressElement) progressElement.innerHTML = `${stats.progressPercent}<small>%</small>`;
    if (timeRemaining) timeRemaining.innerHTML = `${formatSeconds(Math.ceil(config.time_limit - elapsedSeconds))}<small>s</small>`;
    renderPassage(input.value);
    return stats;
  }

  function startTimer() {
    if (startTime !== null) return;
    startTime = performance.now();
    timerId = window.setInterval(() => {
      elapsedSeconds = Math.floor((performance.now() - startTime) / 1000);
      updateStats();
      if (elapsedSeconds >= config.time_limit) finishTest("Time is up! Here is your final result.");
    }, 250);
  }

  /* ── Phonetic Transliteration State (Hindi / Gujarati) ───────────────────── */
  const isIndic = config.language === "hindi" || config.language === "gujarati";
  let romanWordBuffer = "";
  let committedIndicText = "";

  function resetTest() {
    if (timerId) window.clearInterval(timerId);
    timerId = null;
    startTime = null;
    elapsedSeconds = 0;
    hasFinished = false;
    lastTypedLength = 0;
    romanWordBuffer = "";
    committedIndicText = "";
    input.disabled = false;
    input.value = "";
    message.textContent = "";
    message.className = "test-message";
    updateStats();
    focusInput();
  }

  async function finishTest(reason) {
    if (hasFinished) return;
    hasFinished = true;
    
    // Stop the timer immediately!
    if (timerId) window.clearInterval(timerId);

    const stats = calculateStats();
    input.disabled = true;
    message.textContent = reason;
    message.className = "test-message visible";
    playSuccessChime();

    try {
      const response = await fetch("/save-result", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          wpm: stats.wpm,
          accuracy: stats.accuracy,
          errors: stats.errors,
          correct_chars: stats.correctChars,
          incorrect_chars: stats.incorrectChars,
          time_taken: stats.exactTimeTaken,
          difficulty: config.difficulty,
          paragraph_length: config.paragraph_length
        })
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Could not save the result.");
      window.location.href = result.redirect;
    } catch (error) {
      message.textContent = `${reason} We could not save this result yet. ${error.message}`;
      input.disabled = false;
      hasFinished = false;
    }
  }

  function focusInput() {
    if (input && !hasFinished) {
      input.focus();
      if (passageCard) passageCard.classList.add("focused");
      if (focusHint) focusHint.textContent = "Typing Active";
    }
  }

  function blurInput() {
    if (passageCard) passageCard.classList.remove("focused");
    if (focusHint) focusHint.textContent = "Click anywhere to focus";
  }

  if (passageCard) {
    passageCard.addEventListener("click", focusInput);
  }
  if (passageDisplay) {
    passageDisplay.addEventListener("click", focusInput);
  }

  /* ── Phonetic Transliteration Engine ─────────────────────────────────────── */
  const CONSONANT_MAP = [
    { k: "shhr", hi: "ष्र", gu: "ષ્ર" },
    { k: "tthr", hi: "ठ्र", gu: "ઠ્ર" },
    { k: "ddhr", hi: "ढ्र", gu: "ઢ્ર" },
    { k: "chhr", hi: "छ्र", gu: "છ્ર" },
    { k: "chh", hi: "छ", gu: "છ" },
    { k: "tth", hi: "ठ", gu: "ઠ" },
    { k: "ddh", hi: "ढ", gu: "ઢ" },
    { k: "shh", hi: "ष", gu: "ષ" },
    { k: "ksh", hi: "क्ष", gu: "ક્ષ" },
    { k: "gya", hi: "ज्ञ", gu: "જ્ઞ" },
    { k: "jny", hi: "ज्ञ", gu: "જ્ઞ" },
    { k: "shr", hi: "श्र", gu: "શ્ર" },
    { k: "kh",  hi: "ख", gu: "ખ" },
    { k: "gh",  hi: "घ", gu: "ઘ" },
    { k: "ng",  hi: "ङ", gu: "ઙ" },
    { k: "ch",  hi: "च", gu: "ચ" },
    { k: "jh",  hi: "झ", gu: "ઝ" },
    { k: "ny",  hi: "ञ", gu: "ઞ" },
    { k: "tt",  hi: "ट", gu: "ટ" },
    { k: "th",  hi: "थ", gu: "થ" },
    { k: "Th",  hi: "ठ", gu: "ઠ" },
    { k: "dd",  hi: "ड", gu: "ડ" },
    { k: "dh",  hi: "ध", gu: "ધ" },
    { k: "Dh",  hi: "ढ", gu: "ઢ" },
    { k: "ph",  hi: "फ", gu: "ફ" },
    { k: "bh",  hi: "भ", gu: "ભ" },
    { k: "sh",  hi: "श", gu: "શ" },
    { k: "Sh",  hi: "ष", gu: "ષ" },
    { k: "gy",  hi: "ज्ञ", gu: "જ્ઞ" },
    { k: "tr",  hi: "त्र", gu: "ત્ર" },
    { k: "ld",  hi: "ळ", gu: "ળ" },
    { k: "k",   hi: "क", gu: "ક" },
    { k: "g",   hi: "ग", gu: "ગ" },
    { k: "c",   hi: "च", gu: "ચ" },
    { k: "j",   hi: "ज", gu: "જ" },
    { k: "z",   hi: "ज़", gu: "ઝ" },
    { k: "T",   hi: "ट", gu: "ટ" },
    { k: "t",   hi: "त", gu: "ત" },
    { k: "D",   hi: "ड", gu: "ડ" },
    { k: "d",   hi: "द", gu: "દ" },
    { k: "N",   hi: "ण", gu: "ણ" },
    { k: "n",   hi: "न", gu: "ન" },
    { k: "p",   hi: "प", gu: "પ" },
    { k: "f",   hi: "फ", gu: "ફ" },
    { k: "b",   hi: "ब", gu: "બ" },
    { k: "m",   hi: "म", gu: "મ" },
    { k: "y",   hi: "य", gu: "ય" },
    { k: "r",   hi: "र", gu: "ર" },
    { k: "l",   hi: "ल", gu: "લ" },
    { k: "L",   hi: "ळ", gu: "ળ" },
    { k: "v",   hi: "व", gu: "વ" },
    { k: "w",   hi: "व", gu: "વ" },
    { k: "s",   hi: "स", gu: "સ" },
    { k: "S",   hi: "श", gu: "શ" },
    { k: "h",   hi: "ह", gu: "હ" },
    { k: "x",   hi: "क्ष", gu: "ક્ષ" },
    { k: "q",   hi: "क", gu: "ક" }
  ];

  const VOWEL_MAP = [
    { k: "aaa", ind_hi: "आ", ind_gu: "આ", mat_hi: "ा", mat_gu: "ા" },
    { k: "aau", ind_hi: "औ", ind_gu: "ઔ", mat_hi: "ौ", mat_gu: "ૌ" },
    { k: "aai", ind_hi: "ऐ", ind_gu: "ઐ", mat_hi: "ै", mat_gu: "ૈ" },
    { k: "aa",  ind_hi: "आ", ind_gu: "આ", mat_hi: "ा", mat_gu: "ા" },
    { k: "ee",  ind_hi: "ई", ind_gu: "ઈ", mat_hi: "ी", mat_gu: "ી" },
    { k: "ii",  ind_hi: "ई", ind_gu: "ઈ", mat_hi: "ी", mat_gu: "ી" },
    { k: "oo",  ind_hi: "ऊ", ind_gu: "ઊ", mat_hi: "ू", mat_gu: "ૂ" },
    { k: "uu",  ind_hi: "ऊ", ind_gu: "ઊ", mat_hi: "ू", mat_gu: "ૂ" },
    { k: "ai",  ind_hi: "ऐ", ind_gu: "ઐ", mat_hi: "ै", mat_gu: "ૈ" },
    { k: "au",  ind_hi: "औ", ind_gu: "ઔ", mat_hi: "ौ", mat_gu: "ૌ" },
    { k: "ou",  ind_hi: "औ", ind_gu: "ઔ", mat_hi: "ौ", mat_gu: "ૌ" },
    { k: "ri",  ind_hi: "ऋ", ind_gu: "ઋ", mat_hi: "ृ", mat_gu: "ૃ" },
    { k: "ru",  ind_hi: "ऋ", ind_gu: "ઋ", mat_hi: "ृ", mat_gu: "ૃ" },
    { k: "a",   ind_hi: "अ", ind_gu: "અ", mat_hi: "",  mat_gu: "" },
    { k: "A",   ind_hi: "आ", ind_gu: "આ", mat_hi: "ा", mat_gu: "ા" },
    { k: "i",   ind_hi: "इ", ind_gu: "ઇ", mat_hi: "ि", mat_gu: "િ" },
    { k: "I",   ind_hi: "ई", ind_gu: "ઈ", mat_hi: "ी", mat_gu: "ી" },
    { k: "u",   ind_hi: "उ", ind_gu: "ઉ", mat_hi: "ु", mat_gu: "ુ" },
    { k: "U",   ind_hi: "ऊ", ind_gu: "ઊ", mat_hi: "ू", mat_gu: "ૂ" },
    { k: "e",   ind_hi: "ए", ind_gu: "એ", mat_hi: "े", mat_gu: "ે" },
    { k: "E",   ind_hi: "ए", ind_gu: "એ", mat_hi: "े", mat_gu: "ે" },
    { k: "o",   ind_hi: "ओ", ind_gu: "ઓ", mat_hi: "ो", mat_gu: "ો" },
    { k: "O",   ind_hi: "ओ", ind_gu: "ઓ", mat_hi: "ो", mat_gu: "ો" }
  ];

  const VIRAMA = { hindi: "्", gujarati: "્" };
  const ANUSVARA = { hindi: "ं", gujarati: "ં" };
  const VISARGA = { hindi: "ः", gujarati: "ઃ" };

  const WORD_OVERRIDES = {
    hindi: {
      "hai": "है", "hain": "हैं", "me": "में", "mein": "में", "main": "मैं",
      "bhi": "भी", "ho": "हो", "hoon": "हूँ", "huun": "हूँ", "hu": "हूँ", "hun": "हूँ",
      "aaj": "आज", "ka": "का", "ki": "की", "kee": "की", "ke": "के", "ko": "को",
      "se": "से", "aur": "और", "yeh": "यह", "woh": "वह", "voh": "वह",
      "tha": "था", "thi": "थी", "the": "थे", "nahi": "नहीं", "nahin": "नहीं",
      "bharat": "भारत", "bhaarat": "भारत", "namaste": "नमस्ते"
    },
    gujarati: {
      "chhe": "છે", "che": "છે", "chho": "છો", "cho": "છો", "chhu": "છું",
      "ma": "માં", "maa": "માં", "pan": "પણ", "ane": "અને", "te": "તે",
      "nathi": "નથી", "aaj": "આજ", "aaje": "આજે", "kem": "કેમ",
      "bhojan": "ભોજન", "gujarat": "ગુજરાત", "bharat": "ભારત", "bharatnu": "ભારતનું",
      "namaste": "નમસ્તે"
    }
  };

  function transliterateWord(roman, lang, expectedWord = "") {
    if (!roman) return "";
    const lower = roman.toLowerCase();

    // 1. Direct dictionary match
    if (WORD_OVERRIDES[lang]?.[lower]) {
      const match = WORD_OVERRIDES[lang][lower];
      if (expectedWord && expectedWord.startsWith(match)) return match;
      if (!expectedWord) return match;
    }

    // 2. Phonetic token parsing
    let res = "";
    let i = 0;
    const len = roman.length;

    while (i < len) {
      const rem = roman.slice(i);

      if (rem[0] === "M") {
        res += ANUSVARA[lang];
        i += 1;
        continue;
      }
      if (rem[0] === "H") {
        res += VISARGA[lang];
        i += 1;
        continue;
      }

      // Consonant match
      let matchedCons = null;
      for (const c of CONSONANT_MAP) {
        if (rem.startsWith(c.k)) {
          matchedCons = c;
          break;
        }
      }

      if (matchedCons) {
        i += matchedCons.k.length;
        const afterCons = roman.slice(i);

        let matchedVowel = null;
        for (const v of VOWEL_MAP) {
          if (afterCons.startsWith(v.k)) {
            matchedVowel = v;
            break;
          }
        }

        const consChar = lang === "hindi" ? matchedCons.hi : matchedCons.gu;

        if (matchedVowel) {
          i += matchedVowel.k.length;
          const matra = lang === "hindi" ? matchedVowel.mat_hi : matchedVowel.mat_gu;
          res += consChar + matra;

          // Nasal / Anusvara check
          const nextRem = roman.slice(i);
          if (nextRem[0] === "M") {
            res += ANUSVARA[lang];
            i += 1;
          } else if ((nextRem[0] === "n" || nextRem[0] === "m") && nextRem.length > 1) {
            const afterN = nextRem.slice(1);
            const isStopCons = CONSONANT_MAP.some(c => afterN.startsWith(c.k) && c.k !== "h" && c.k !== "y" && c.k !== "v" && c.k !== "w" && c.k !== "r" && c.k !== "l");
            if (isStopCons) {
              res += ANUSVARA[lang];
              i += 1;
            }
          }
        } else {
          // No following vowel
          if (i < len) {
            res += consChar + VIRAMA[lang];
          } else {
            res += consChar;
          }
        }
        continue;
      }

      // Independent vowel match
      let matchedVowel = null;
      for (const v of VOWEL_MAP) {
        if (rem.startsWith(v.k)) {
          matchedVowel = v;
          break;
        }
      }

      if (matchedVowel) {
        i += matchedVowel.k.length;
        const indVowel = lang === "hindi" ? matchedVowel.ind_hi : matchedVowel.ind_gu;
        res += indVowel;

        const nextRem = roman.slice(i);
        if (nextRem[0] === "M") {
          res += ANUSVARA[lang];
          i += 1;
        } else if ((nextRem[0] === "n" || nextRem[0] === "m") && nextRem.length > 1) {
          const afterN = nextRem.slice(1);
          const isStopCons = CONSONANT_MAP.some(c => afterN.startsWith(c.k) && c.k !== "h" && c.k !== "y" && c.k !== "v" && c.k !== "w" && c.k !== "r" && c.k !== "l");
          if (isStopCons) {
            res += ANUSVARA[lang];
            i += 1;
          }
        }
        continue;
      }

      res += rem[0];
      i += 1;
    }

    // 3. Align with expected word if provided
    if (expectedWord) {
      if (expectedWord === res || expectedWord.startsWith(res)) return res;

      const resChars = Array.from(res);
      const expChars = Array.from(expectedWord).slice(0, resChars.length);
      if (resChars.length === expChars.length) {
        let compatible = true;
        for (let idx = 0; idx < resChars.length; idx++) {
          const r = resChars[idx];
          const e = expChars[idx];
          if (r === e) continue;
          const isEquiv = 
            (r === "न" && e === "ण") || (r === "ન" && e === "ણ") ||
            (r === "श" && e === "ष") || (r === "શ" && e === "ષ") ||
            (r === "ि" && e === "ी") || (r === "િ" && e === "ી") ||
            (r === "ी" && e === "ि") || (r === "ી" && e === "િ") ||
            (r === "ु" && e === "ू") || (r === "ુ" && e === "ૂ") ||
            (r === "ू" && e === "ु") || (r === "ૂ" && e === "ુ") ||
            (r === "ा" && e === "")  || (r === ""  && e === "ा") ||
            (r === "ા" && e === "")  || (r === ""  && e === "ા") ||
            (r === "ँ" && e === "ं") || (r === "ં" && e === "ઁ");
          if (!isEquiv) {
            compatible = false;
            break;
          }
        }
        if (compatible) return expChars.join("");
      }
    }

    return res;
  }

  function getExpectedWord() {
    const remainingPassage = config.passage.slice(committedIndicText.length);
    const match = remainingPassage.match(/^[^\s।,.-]+/);
    return match ? match[0] : "";
  }

  function removeLastGrapheme(str) {
    if (!str) return "";
    if (typeof Intl !== "undefined" && Intl.Segmenter) {
      const seg = new Intl.Segmenter();
      const segments = [...seg.segment(str)];
      if (segments.length > 0) {
        return str.slice(0, segments[segments.length - 1].index);
      }
    }
    return Array.from(str).slice(0, -1).join("");
  }

  function updateIndicInputValue() {
    const transliteratedWord = transliterateWord(romanWordBuffer, config.language, getExpectedWord());
    input.value = committedIndicText + transliteratedWord;
    input.dispatchEvent(new Event("input", { bubbles: true }));
  }

  function handleIndicLetter(char) {
    romanWordBuffer += char;
    updateIndicInputValue();
  }

  function handleIndicSpace() {
    if (romanWordBuffer.length > 0) {
      const transliteratedWord = transliterateWord(romanWordBuffer, config.language, getExpectedWord());
      committedIndicText += transliteratedWord + " ";
      romanWordBuffer = "";
    } else {
      committedIndicText += " ";
    }
    input.value = committedIndicText;
    input.dispatchEvent(new Event("input", { bubbles: true }));
  }

  function handleIndicPunctuation(punct) {
    if (romanWordBuffer.length > 0) {
      const transliteratedWord = transliterateWord(romanWordBuffer, config.language, getExpectedWord());
      committedIndicText += transliteratedWord;
      romanWordBuffer = "";
    }
    let actualPunct = punct;
    if (punct === ".") {
      const remainingPassage = config.passage.slice(committedIndicText.length);
      if (remainingPassage.startsWith("।") || (!remainingPassage.startsWith(".") && isIndic)) {
        actualPunct = "।";
      }
    }
    committedIndicText += actualPunct;
    input.value = committedIndicText;
    input.dispatchEvent(new Event("input", { bubbles: true }));
  }

  function handleIndicBackspace() {
    if (romanWordBuffer.length > 0) {
      romanWordBuffer = romanWordBuffer.slice(0, -1);
      updateIndicInputValue();
    } else if (committedIndicText.length > 0) {
      committedIndicText = removeLastGrapheme(committedIndicText);
      input.value = committedIndicText;
      input.dispatchEvent(new Event("input", { bubbles: true }));
    }
  }

  if (input) {
    input.addEventListener("focus", focusInput);
    input.addEventListener("blur", blurInput);

    if (isIndic) {
      input.addEventListener("keydown", (e) => {
        if (hasFinished) return;
        if (e.ctrlKey || e.metaKey || e.altKey) return;

        if (e.key === "Backspace") {
          e.preventDefault();
          handleIndicBackspace();
          return;
        }

        if (e.key === " " || e.key === "Spacebar") {
          e.preventDefault();
          handleIndicSpace();
          return;
        }

        if (e.key === "." || e.key === "।") {
          e.preventDefault();
          handleIndicPunctuation(".");
          return;
        }

        if (e.key.length === 1) {
          if (/^[a-zA-Z]$/.test(e.key)) {
            e.preventDefault();
            handleIndicLetter(e.key);
            return;
          } else if (/^[0-9,;:\-–—!?'"()\/\\%]$/.test(e.key)) {
            e.preventDefault();
            handleIndicPunctuation(e.key);
            return;
          }
        }
      });
    }

    input.addEventListener("input", () => {
      if (hasFinished) return;
      const currentLength = input.value.length;
      
      // Play sound feedback for keystroke
      if (currentLength > lastTypedLength) {
        const charIndex = currentLength - 1;
        const typedChar = input.value[charIndex];
        const targetChar = config.passage[charIndex];
        const isSpace = typedChar === " ";
        const isError = typedChar !== targetChar;

        playKeySound(isSpace, isError);
      } else if (currentLength < lastTypedLength) {
        playKeySound(false, false);
      }
      lastTypedLength = currentLength;

      if (input.value.length > 0) startTimer();
      const stats = updateStats();

      // IF USER COMPLETES PARAGRAPH FASTER THAN TIMER: Stop timer immediately & finish test!
      if (input.value.length >= config.passage.length) {
        finishTest("🎉 Paragraph completed! Time stopped & results recorded.");
      } else {
        message.textContent = "";
        message.className = "test-message";
      }
    });

    input.addEventListener("paste", (event) => {
      event.preventDefault();
      message.textContent = "Please type the passage manually instead of pasting.";
      message.className = "test-message visible warning";
    });
  }

  /* ── Dynamic Paragraph Switching & Modal Logic ─────────────────────────── */
  let isChangingPassage = false;

  function showToast(msg) {
    if (!passageToast) return;
    passageToast.textContent = msg;
    passageToast.classList.add("show");
    window.clearTimeout(passageToast._timeout);
    passageToast._timeout = window.setTimeout(() => {
      passageToast.classList.remove("show");
    }, 2400);
  }

  function applyNewPassage(data) {
    config.passage = data.passage;
    config.paragraph_length = data.paragraph_length || config.paragraph_length;
    config.is_custom = !!data.is_custom;

    window.localStorage.setItem("smartTypingLastPassage", config.passage);
    window.localStorage.setItem("smartTypingIsCustom", config.is_custom ? "true" : "false");

    if (currentLengthTag) {
      currentLengthTag.textContent = config.is_custom
        ? "Custom passage"
        : `${config.paragraph_length.charAt(0).toUpperCase() + config.paragraph_length.slice(1)} passage`;
    }

    // Update active length pill
    lengthPillButtons.forEach((pill) => {
      if (pill.dataset.length === config.paragraph_length) {
        pill.classList.add("active");
      } else {
        pill.classList.remove("active");
      }
    });

    // Update URL query parameters without reloading
    try {
      const url = new URL(window.location.href);
      url.searchParams.set("difficulty", config.difficulty);
      url.searchParams.set("paragraph_length", config.paragraph_length);
      url.searchParams.set("time_limit", config.time_limit);
      url.searchParams.set("language", config.language);
      if (config.is_custom) {
        url.searchParams.set("is_custom", "1");
      } else {
        url.searchParams.delete("is_custom");
      }
      window.history.replaceState({}, "", url.toString());
    } catch (e) {}

    resetTest();
    playPopSound();

    const words = data.word_count || config.passage.trim().split(/\s+/).length;
    showToast(config.is_custom ? "✓ Custom paragraph loaded!" : `✓ Paragraph loaded (${words} words)`);
  }

  async function fetchNewPassage(opts = {}) {
    if (isChangingPassage) return;
    isChangingPassage = true;

    if (newPassageBtn) newPassageBtn.disabled = true;
    if (changePassageBtn) changePassageBtn.disabled = true;

    try {
      if (opts.customText) {
        const res = await fetch("/api/custom-passage", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ custom_passage: opts.customText })
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.error || "Failed to set custom passage");
        }
        applyNewPassage(data);
        closeModal();
      } else {
        const targetLength = opts.length || config.paragraph_length;
        const params = new URLSearchParams({
          difficulty: config.difficulty,
          paragraph_length: targetLength,
          time_limit: config.time_limit,
          language: config.language,
          exclude: config.passage || ""
        });
        if (opts.index !== undefined && opts.index !== null && opts.index !== "") {
          params.set("passage_index", opts.index);
        }

        const res = await fetch(`/api/new-passage?${params.toString()}`);
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.error || "Failed to fetch new passage");
        }
        applyNewPassage(data);
      }
    } catch (err) {
      if (message) {
        message.textContent = err.message || "Failed to update passage.";
        message.className = "test-message visible warning";
      }
    } finally {
      isChangingPassage = false;
      if (newPassageBtn) newPassageBtn.disabled = false;
      if (changePassageBtn) changePassageBtn.disabled = false;
      if (passageSelect) passageSelect.value = "";
    }
  }

  function openModal() {
    if (!customModal) return;
    customModal.classList.add("open");
    customModal.setAttribute("aria-hidden", "false");
    if (modalCustomText) {
      modalCustomText.value = config.is_custom ? config.passage : "";
      updateModalCounts();
      modalCustomText.focus();
    }
    if (modalError) modalError.style.display = "none";
  }

  function closeModal() {
    if (!customModal) return;
    customModal.classList.remove("open");
    customModal.setAttribute("aria-hidden", "true");
    if (modalError) modalError.style.display = "none";
    focusInput();
  }

  function updateModalCounts() {
    if (!modalCustomText) return;
    const len = modalCustomText.value.length;
    const words = modalCustomText.value.trim() ? modalCustomText.value.trim().split(/\s+/).length : 0;
    if (modalCharCount) modalCharCount.textContent = `${len.toLocaleString()} / 5,000 characters`;
    if (modalWordCount) modalWordCount.textContent = `${words} word${words === 1 ? "" : "s"}`;
  }

  if (openCustomModalBtn) {
    openCustomModalBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      openModal();
    });
  }
  if (closeModalBtn) closeModalBtn.addEventListener("click", closeModal);
  if (cancelModalBtn) cancelModalBtn.addEventListener("click", closeModal);
  if (customModal) {
    customModal.addEventListener("click", (e) => {
      if (e.target === customModal) closeModal();
    });
  }
  if (modalCustomText) {
    modalCustomText.addEventListener("input", updateModalCounts);
  }
  if (applyCustomModalBtn) {
    applyCustomModalBtn.addEventListener("click", () => {
      const text = modalCustomText ? modalCustomText.value.trim() : "";
      if (!text) {
        if (modalError) {
          modalError.textContent = "Please enter some text for your custom paragraph.";
          modalError.style.display = "block";
        }
        return;
      }
      fetchNewPassage({ customText: text });
    });
  }

  if (newPassageBtn) {
    newPassageBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      fetchNewPassage();
    });
  }

  if (changePassageBtn) {
    changePassageBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      fetchNewPassage();
    });
  }

  lengthPillButtons.forEach((pill) => {
    pill.addEventListener("click", (e) => {
      e.stopPropagation();
      const len = pill.dataset.length;
      if (len === "custom") {
        openModal();
      } else {
        fetchNewPassage({ length: len });
      }
    });
  });

  if (passageSelect) {
    passageSelect.addEventListener("change", (e) => {
      const idx = e.target.value;
      if (idx !== "") {
        fetchNewPassage({ index: idx });
      }
    });
  }

  if (restartBtn) {
    restartBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      resetTest();
    });
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      if (customModal && customModal.classList.contains("open")) {
        closeModal();
      } else {
        resetTest();
      }
    } else if (e.altKey && (e.key === "n" || e.key === "N")) {
      e.preventDefault();
      fetchNewPassage();
    }
  });

  renderPassage("");
  focusInput();
})();