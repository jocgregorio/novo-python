import json
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from app.core.config import settings
from app.ai.schemas import (
    DatosPersonales, EducacionResponse, CursosResponse,
    ExperienciaResponse, HabilidadesResponse, PerfilResponse
)

openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
anthropic_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

# Nombre exacto configurado en tu workflow original de n8n
ANTHROPIC_MODEL = "claude-sonnet-4-5-20250929"


async def extraer_datos_personales(texto_crudo: str) -> DatosPersonales:
    prompt = f"""Eres un asistente experto en extracción de datos. Revisa el siguiente texto desestructurado de un candidato y extrae sus datos personales.
Reglas estrictas:
1. Si un dato no existe en el texto, devuelve null. No inventes absolutamente nada.
2. Extrae el título profesional basándote en su perfil si está implícito.
3. La direccion debe ser: Calle o Zona, Ciudad y Provincia.

Texto a analizar:
{texto_crudo}"""
    
    completion = await openai_client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format=DatosPersonales,
    )
    return completion.choices[0].message.parsed


async def extraer_educacion(texto_crudo: str) -> EducacionResponse:
    prompt = f"""Eres un asistente experto en extracción de datos. Revisa el texto desestructurado y extrae ÚNICAMENTE la información sobre educación formal (universidad, técnico, bachillerato). IGNORA experiencia laboral, cursos extra o datos personales.
Reglas estrictas:
1. Si no hay educación formal, devuelve lista vacía.
2. Para las fechas, extrae solo el año o el texto tal como aparece.

Texto a analizar:
{texto_crudo}"""

    completion = await openai_client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format=EducacionResponse,
    )
    return completion.choices[0].message.parsed


async def extraer_cursos(texto_crudo: str) -> CursosResponse:
    prompt = f"""Eres un asistente experto en extracción de datos. Revisa el texto desestructurado y extrae ÚNICAMENTE la educación complementaria (cursos, certificaciones, talleres). IGNORA educación formal, experiencia laboral o datos personales.
Reglas estrictas:
1. Si no hay formación complementaria, devuelve lista vacía.

Texto a analizar:
{texto_crudo}"""

    completion = await openai_client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format=CursosResponse,
    )
    return completion.choices[0].message.parsed


async def extraer_experiencia(texto_crudo: str) -> ExperienciaResponse:
    system_prompt = """Eres un estructurador de datos estricto. PROHIBIDO usar bloques de razonamiento o pensamiento (extended thinking). PROHIBIDO generar texto fuera del JSON."""
    
    user_prompt = f"""Eres un asistente experto en redacción de currículums y extracción de datos. Revisa el texto desestructurado del candidato y extrae su experiencia laboral. 
Tu tarea es redactar y estructurar cada experiencia laboral creando un máximo de 6 funciones y 3 logros clave por cada cargo, ciñéndote estrictamente a la realidad operativa del texto proporcionado.

REGLAS DE REDACCIÓN (ESTRICTAS):
1. Fórmula de funciones: Qué hice + Cómo lo hice + Qué logré (Acción, contexto, resultado).
2. Longitud: Cada función debe tener entre 145 y 160 caracteres.
3. Estilo: Utiliza verbos en infinitivo. El tono debe ser completamente humano, directo y pragmático. ESTRICTAMENTE PROHIBIDO usar clichés vacíos o exageraciones corporativas.
4. Realismo en Logros: Si el texto original no menciona cifras, puedes inferir logros lógicos para el rol, pero ESTÁ PROHIBIDO inventar métricas de volumen absoluto absurdas. Limítate a métricas relativas conservadoras y creíbles.
5. Los logros redactados en primera persona.
6. Formatea funciones y logros como bloque de texto con saltos de línea (\\n) y guiones (-).

Texto a analizar:
{texto_crudo}"""

    response = await anthropic_client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=4096,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": '{"experiencia": ['}
        ]
    )
    raw_json = '{"experiencia": [' + response.content[0].text
    data = json.loads(raw_json)
    return ExperienciaResponse(**data)


async def extraer_habilidades(expediente_cv: str) -> HabilidadesResponse:
    prompt = f"""Eres un analista experto en reclutamiento y operaciones. Analiza el expediente laboral y educativo del candidato.
Tu tarea es extraer:
1. Exactamente 6 Habilidades Técnicas (Hard Skills) demostrables.
2. Exactamente 6 Habilidades Blandas (Soft Skills) inferidas.

Expediente a analizar:
{expediente_cv}"""

    completion = await openai_client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format=HabilidadesResponse,
    )
    return completion.choices[0].message.parsed


async def redactar_perfil(expediente_final: str) -> PerfilResponse:
    system_prompt = "Eres un consultor de carrera y headhunter experto. Responde únicamente en formato JSON."
    user_prompt = f"""Analiza el expediente completo del candidato (experiencia, educación y habilidades) y redacta su perfil profesional.
Debes generar:
1. "Titulo": Un título profesional corto y de alto impacto (ej. "Especialista en Logística y Distribución").
2. "Perfil": Un párrafo corto (máximo 4-5 líneas). 
   - Primera mitad: insights de mayor valor de su trayectoria (patrones de éxito, especialidad).
   - Segunda mitad: cómo aporta valor operativo y eficiencia a una nueva empresa.
   - Tono humano, directo y profesional con verbos de acción. Cero clichés vacíos.

Expediente a analizar:
{expediente_final}"""

    response = await anthropic_client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": "{"}
        ]
    )
    raw_json = "{" + response.content[0].text
    data = json.loads(raw_json)
    return PerfilResponse(**data)