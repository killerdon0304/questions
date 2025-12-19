function toggleDark() {
  document.documentElement.classList.toggle("dark");
}

/* ---------- TRANSLATE ---------- */
async function translateText() {
  const text = inputText.value;
  const target = targetLang.value;
  if (!text.trim()) return;

  loader.classList.remove("hidden");
  resultBox.classList.add("hidden");

  const res = await fetch("/translate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, target_lang: target })
  });

  const data = await res.json();

  loader.classList.add("hidden");
  resultBox.classList.remove("hidden");

  translatedText.innerText = data.translated;
  detectedLang.innerText = "Detected: " + (data.detected_lang || "auto");

  if (data.hinglish) {
    hinglishText.innerText = "(" + data.hinglish + ")";
    hinglishText.classList.remove("hidden");
  } else {
    hinglishText.innerText = "";
    hinglishText.classList.add("hidden");
  }

  saveHistory(text, data.translated);
  loadHistory();
}

/* ---------- COPY ---------- */
function copyText() {
  const btn = document.getElementById("copyBtn");
  const text = translatedText.innerText;
  if (!text) return;

  navigator.clipboard.writeText(text).then(() => {
    btn.innerText = "✅ Copied";
    setTimeout(() => (btn.innerText = "📋 Copy"), 1500);
  });
}

/* ---------- SPEAK ---------- */
function speakText() {
  const text = translatedText.innerText;
  if (!text) return;

  const btn = document.getElementById("speakBtn");
  const utter = new SpeechSynthesisUtterance(text);

  const target = targetLang.value;
  utter.lang = (target === "hi" || target === "bho") ? "hi-IN" : target;

  btn.innerText = "🔊 Speaking...";
  btn.classList.add("opacity-70");

  utter.onend = () => {
    btn.innerText = "🔊 Speak";
    btn.classList.remove("opacity-70");
  };

  speechSynthesis.cancel();
  speechSynthesis.speak(utter);
}

/* ---------- SPEECH TO TEXT ---------- */
function startSpeech() {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) return;

  const r = new SpeechRecognition();
  r.lang = "";
  r.start();

  r.onresult = e => {
    inputText.value = e.results[0][0].transcript;
  };
}

/* ---------- HISTORY ---------- */
function saveHistory(o, t) {
  let h = JSON.parse(localStorage.getItem("history") || "[]");
  h.unshift({ o, t });
  localStorage.setItem("history", JSON.stringify(h.slice(0, 30)));
}

function loadHistory() {
  let h = JSON.parse(localStorage.getItem("history") || "[]");
  historyBox.innerHTML = h.map(x =>
    `<div class="bg-slate-100 dark:bg-slate-600 rounded p-2">
      <div>${x.o}</div>
      <div class="text-xs text-gray-500">${x.t}</div>
    </div>`
  ).join("");
}

/* ---------- CLEAR HISTORY MODAL ---------- */
function openClearHistoryAlert() {
  alertModal.classList.remove("hidden");
  alertModal.classList.add("flex");
}

function closeAlert() {
  alertModal.classList.add("hidden");
  alertModal.classList.remove("flex");
}

function confirmClearHistory() {
  localStorage.removeItem("history");
  historyBox.innerHTML = "";
  closeAlert();
}

window.onload = () => {
  loadHistory();
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/static/sw.js");
  }
};
