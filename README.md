# 🏥 VeredAI
### Offline Clinical Support Assistant for Rural Doctors in Colombia
*Powered by Gemma 4 · 100% offline · No cloud · No internet required*

---

## 🌎 The Problem

In Colombia, there are **12,000+ veredas** (rural settlements) where the nearest doctor is hours away. Nurses and health workers make life-or-death decisions daily — often without specialist support, without internet, and without tools designed for their reality.

A nurse in Chocó facing a patient with fever and skin rashes shouldn't have to guess whether it's dengue, rickettsia, or something else. They need fast, practical, contextual guidance — right there in the field.

**VeredAI was built for them.**

---

## 💡 What is VeredAI?

VeredAI is a **privacy-preserving, fully offline clinical support assistant** for rural health workers in Colombia. It runs entirely on local hardware — no GPU required, no internet connection, no patient data ever leaves the device.

Using **Gemma 4 (4B edge model)** via Ollama, VeredAI:
- Analyzes symptoms described in natural Spanish
- Accepts medical images (wounds, rashes, skin conditions)
- Returns structured clinical guidance in seconds
- Exports a PDF report the patient can carry to a referral center
- Works in places where Google doesn't load

---

## 🇨🇴 Why Colombia? Why Veredas?

A **vereda** is the smallest rural territorial unit in Colombia — home to farmers, indigenous communities, and families far from urban healthcare. These communities face:

- No specialist access
- Unreliable or zero internet connectivity
- Endemic diseases specific to their region (malaria in Amazonas, rickettsia in Chocó, leishmaniasis in Nariño)
- Overworked rural nurses making decisions alone

VeredAI was calibrated specifically for **Colombian endemic diseases** — not generic tropical medicine, but the specific pathogens and conditions that appear in these exact communities.

---

## ⚙️ How It Works

```
Doctor/Nurse describes symptoms + optional photo
        ↓
VeredAI sends request to local Gemma 4 (Ollama)
        ↓
Gemma 4 processes entirely on-device (CPU, no GPU needed)
        ↓
Structured clinical guidance appears in real time (streaming)
        ↓
Optional: Export PDF report for patient referral
```

**Response format (always structured):**
```
DIAGNÓSTICOS POSIBLES:
- Most likely diagnosis first (region-aware)

MANEJO INICIAL:
- Practical steps for rural setting

SEÑALES DE ALARMA:
- When to escalate immediately

URGENCIA: LEVE / MODERADO / URGENTE / EMERGENCIA
```

---

## 🧪 Validated on 10 Real Clinical Cases

VeredAI was tested on 10 clinical scenarios representative of Colombian rural medicine:

| Case | Condition | Result |
|------|-----------|--------|
| 1 | Fever + rash, Chocó | ✅ Dengue/Rickettsia identified |
| 2 | Cyclic fever + spleen, Amazonas | ✅ Malaria prioritized |
| 3 | Snakebite + necrosis | ✅ URGENT, correct protocol |
| 4 | Pregnancy + hypertension | ✅ Preeclampsia identified (24s) |
| 5 | Non-healing ulcer, Nariño | ✅ Cutaneous leishmaniasis |
| 6 | Febrile seizure, child 3yo | ✅ Benign febrile seizure first |
| 7 | Chest pain + left arm radiation | ✅ AMI, aspirin recommended |
| 8 | Trismus + spasms after machete wound | ✅ Tetanus, EMERGENCY |
| 9 | Bee sting + generalized hives + dyspnea | ✅ Anaphylaxis, epinephrine first |
| 10 | Bloody diarrhea, child, Córdoba | ✅ Shigellosis identified |

---

## 🚀 Installation & Usage

### Requirements
- Windows / Linux / Mac
- Python 3.10+
- 8GB RAM minimum
- [Ollama](https://ollama.com) installed

### Setup

```bash
# 1. Install Ollama and download Gemma 4
ollama pull gemma3:4b

# 2. Clone this repo
git clone https://github.com/GabrielJaimeDuarte/VeredAI.git
cd VeredAI

# 3. Install dependencies
pip install requests pillow fpdf2 gradio

# 4. Run VeredAI
python app.py
```

### Usage
1. Open browser at `http://localhost:7860`
2. Describe patient symptoms in Spanish
3. Optionally upload a medical image
4. Click **"Consultar orientación clínica"**
5. Export PDF report if needed

---

## 🔒 Privacy & Safety

- **Zero data transmission** — everything runs locally
- **No patient data stored** — session-only memory
- **Explicit disclaimer** — VeredAI is a clinical support tool, not a diagnostic device. All decisions remain with the licensed health professional.
- **Designed for professionals** — not for direct patient self-diagnosis

---

## 🧠 Why Gemma 4?

- **Open weights** — can be deployed without cloud dependency
- **Edge-optimized** — 4B model runs on CPU, no GPU required
- **Multimodal** — accepts both text and images
- **Apache 2.0 license** — free for humanitarian use
- **Strong Spanish performance** — critical for Colombian rural context

---

## 📊 Technical Details

| Component | Details |
|-----------|---------|
| Model | Gemma 4 (gemma3:4b via Ollama) |
| Hardware | CPU only, tested on Intel i5 |
| RAM usage | ~4GB during inference |
| Response time | 60–120 seconds (streaming from second 5) |
| Interface | Gradio (web-based, local) |
| PDF export | fpdf2 |
| Language | Python 3.13 |

---

## 🏆 Hackathon Track

**Health & Sciences** — VeredAI addresses the critical gap in rural healthcare access using privacy-preserving, offline-first AI that works where infrastructure doesn't.

---

## 👨‍💻 Author

**Gabriel Jaime Duarte López**
Electronic Engineer · Colombia
Creator of [Nexro Plant AI](https://github.com/GabrielJaimeDuarte) — offline crop disease detection system

---

## ⚠️ Medical Disclaimer

VeredAI is an AI-powered clinical **support** tool intended for use by licensed healthcare professionals. It does not replace clinical judgment, physical examination, or laboratory diagnostics. All clinical decisions must be made by a qualified health professional. This tool is not a certified medical device.

---

*Built with ❤️ for the 12,000 veredas of Colombia · Gemma 4 Good Hackathon 2026*
