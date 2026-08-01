import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()


def humanizar_recomendacion(datos_prolog: dict) -> str:
    """Toma la estructura devuelta por Prolog y genera una explicación

    humanizada y empática mediante Gemini.
    """
    datos_limpios = datos_prolog.copy()

    if hasattr(datos_limpios.get("perfil"), "model_dump"):
        datos_limpios["perfil"] = datos_limpios["perfil"].model_dump()

    json_str = json.dumps(datos_limpios, ensure_ascii=False)

    system_instruction = (
        "Eres un asistente de salud y bienestar empático y profesional. "
        "Tu única tarea es tomar los datos lógicos estructurados que te proporciona el motor de inferencia de Prolog "
        "y redactarlos en un consejo humano, motivador, claro y cálido dirigido al usuario.\n\n"
        "REGLAS ESTRICTAS:\n"
        "1. No debes agregar alimentos, restricciones, ejercicios o hábitos de descanso que no estén explícitamente en los datos de Prolog.\n"
        "2. No inventes diagnósticos ni cambies las indicaciones lógicas.\n"
        "3. Estructura la respuesta de forma amigable usando viñetas o párrafos breves."
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"Datos estructurados de Prolog: {json_str}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3,
            ),
        )
        return response.text
    except Exception as e:
        return f"Error al generar la recomendación humanizada: {str(e)}"