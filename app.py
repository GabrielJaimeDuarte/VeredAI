import gradio as gr
import requests
import json
import base64
from fpdf import FPDF
import datetime
import os

# ─── Configuración ───────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gemma3:4b"

PROMPT_SISTEMA = """Eres asistente médico de apoyo para médicos rurales en Colombia.

Enfermedades endémicas por región:
- Amazonas/Chocó/Pacífico: malaria, leishmaniasis, fiebre amarilla
- Chocó/Costa: rickettsia, dengue, chikungunya
- Nariño/Putumayo: leishmaniasis cutánea (úlcera indolora), chagas
- Zonas rurales generales: leptospirosis, tétanos, rabia
- Tétanos: herida + trismo (no puede abrir la boca) + espasmos musculares = tétanos, siempre EMERGENCIA
- Anafilaxia: picadura + ronchas + dificultad respiratoria = anafilaxia, siempre EMERGENCIA

Convulsión febril simple en menor de 5 años sin antecedentes = convulsión febril benigna (primera opción).

Responde SIEMPRE en este formato:

DIAGNÓSTICOS POSIBLES:
- (3 máximo, más probable primero según región y síntomas)

MANEJO INICIAL:
- (4 pasos máximo, prácticos para zona rural)

SEÑALES DE ALARMA:
- (3 máximo)

URGENCIA: (LEVE / MODERADO / URGENTE / EMERGENCIA)

Sé breve. El médico está en campo."""

# ─── Función principal de consulta ───────────────────────────
def consultar(sintomas, imagen):
    if not sintomas.strip() and imagen is None:
        return "⚠️ Por favor describe los síntomas o sube una imagen.", ""

    prompt = f"{PROMPT_SISTEMA}\n\nCASO: {sintomas if sintomas.strip() else 'Ver imagen adjunta'}"

    payload = {
        "model": MODELO,
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_predict": 400,
            "temperature": 0.3,
            "top_p": 0.9
        }
    }

    if imagen is not None:
        import PIL.Image
        import io
        img = PIL.Image.fromarray(imagen)
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        payload["images"] = [img_b64]

    try:
        respuesta_completa = ""
        with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=300) as r:
            r.raise_for_status()
            for linea in r.iter_lines():
                if linea:
                    chunk = json.loads(linea)
                    if "response" in chunk:
                        respuesta_completa += chunk["response"]
                        yield respuesta_completa, sintomas
    except requests.exceptions.ConnectionError:
        yield "❌ Ollama no está corriendo. Escribe: ollama serve", ""
    except Exception as e:
        yield f"❌ Error: {str(e)}", ""

# ─── Generar reporte PDF ──────────────────────────────────────
def generar_pdf(respuesta, sintomas):
    if not respuesta or respuesta.startswith("❌") or respuesta.startswith("⚠️"):
        return None

    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(20, 20, 20)

    # Encabezado
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Reporte de Orientacion Clinica", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"Fecha: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
    pdf.cell(0, 6, "Asistente Medico Rural - Powered by Gemma 4 (Offline)", ln=True, align="C")
    pdf.ln(5)

    # Línea separadora
    pdf.set_draw_color(100, 100, 100)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(5)

    # Síntomas descritos
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Descripcion del caso:", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, sintomas if sintomas.strip() else "Consulta por imagen")
    pdf.ln(4)

    # Orientación clínica
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Orientacion clinica:", ln=True)
    pdf.set_font("Helvetica", "", 11)
    
    # Limpiar texto para PDF (quitar caracteres especiales)
    texto_limpio = respuesta.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, texto_limpio)
    pdf.ln(4)

    # Aviso legal
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(3)
    pdf.multi_cell(0, 5, "AVISO: Este reporte es una orientacion de apoyo generada por IA. No reemplaza el juicio clinico del profesional de salud. Siempre use su criterio medico para la toma de decisiones.")

    # Guardar
    ruta = os.path.join("C:\\MedicoRural", "reporte_medico.pdf")
    pdf.output(ruta)
    return ruta

# ─── Interfaz Gradio ─────────────────────────────────────────
with gr.Blocks(title="Asistente Médico Rural", theme=gr.themes.Soft()) as app:
    
    gr.Markdown("""
    # 🏥 Asistente Médico Rural
    ### Orientación clínica offline para zonas rurales de Colombia
    *Powered by Gemma 4 · 100% sin internet · Solo apoyo al profesional de salud*
    """)

    with gr.Row():
        with gr.Column(scale=1):
            imagen = gr.Image(label="📷 Imagen médica (opcional)", type="numpy", height=250)
            sintomas = gr.Textbox(
                label="📝 Describe los síntomas del paciente",
                placeholder="Ej: Paciente masculino 45 años, fiebre de 3 días, tos seca, dolor en pecho al respirar...",
                lines=6
            )
            btn_consultar = gr.Button("🔍 Consultar orientación clínica", variant="primary", size="lg")

        with gr.Column(scale=1):
            respuesta = gr.Textbox(label="📋 Orientación clínica", lines=18, interactive=False)
            btn_pdf = gr.Button("📄 Exportar reporte PDF", variant="secondary")
            pdf_output = gr.File(label="Reporte generado")

    # Estado interno para pasar síntomas al PDF
    estado_sintomas = gr.State("")

    gr.Markdown("""
    ---
    ⚠️ **Aviso importante:** Esta herramienta es un apoyo de orientación clínica. 
    No reemplaza el juicio del profesional de salud. Ante emergencias, active siempre los protocolos de derivación.
    """)

    # Eventos
    btn_consultar.click(
    fn=consultar,
    inputs=[sintomas, imagen],
    outputs=[respuesta, estado_sintomas],
    show_progress=False
    )

    btn_pdf.click(
        fn=generar_pdf,
        inputs=[respuesta, estado_sintomas],
        outputs=[pdf_output]
    )

if __name__ == "__main__":
    print("🏥 Iniciando Asistente Médico Rural...")
    print("📡 Abre tu navegador en: http://localhost:7860")
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)