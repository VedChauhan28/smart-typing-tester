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

  // Web Audio API Synthesizer for Typing Sounds
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  let audioCtx = null;

  function getAudioContext() {
    if (!audioCtx) {
      audioCtx = new AudioContext();
    }
    if (audioCtx.state === "suspended") {
      audioCtx.resume();
    }
    return audioCtx;
  }

  function playKeySound(isSpace = false, isError = false) {
    if (!soundEnabled) return;
    try {
      const ctx = getAudioContext();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      if (isError) {
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(140, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(50, ctx.currentTime + 0.08);
        gain.gain.setValueAtTime(0.12, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.08);
      } else if (isSpace) {
        osc.type = "triangle";
        osc.frequency.setValueAtTime(300, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(80, ctx.currentTime + 0.05);
        gain.gain.setValueAtTime(0.1, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.05);
      } else {
        osc.type = "sine";
        osc.frequency.setValueAtTime(1200 + Math.random() * 250, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(220, ctx.currentTime + 0.035);
        gain.gain.setValueAtTime(0.07 + Math.random() * 0.03, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.035);
      }

      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + (isError ? 0.08 : 0.04));
    } catch (e) {}
  }

  function playSuccessChime() {
    if (!soundEnabled) return;
    try {
      const ctx = getAudioContext();
      const notes = [523.25, 659.25, 783.99, 1046.50];
      notes.forEach((freq, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "sine";
        osc.frequency.value = freq;
        const startTime = ctx.currentTime + idx * 0.08;
        gain.gain.setValueAtTime(0.09, startTime);
        gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.25);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(startTime);
        osc.stop(startTime + 0.25);
      });
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

  function resetTest() {
    if (timerId) window.clearInterval(timerId);
    timerId = null;
    startTime = null;
    elapsedSeconds = 0;
    hasFinished = false;
    lastTypedLength = 0;
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

  if (input) {
    input.addEventListener("focus", focusInput);
    input.addEventListener("blur", blurInput);

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

  if (restartBtn) {
    restartBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      resetTest();
    });
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      resetTest();
    }
  });

  renderPassage("");
  focusInput();
})();