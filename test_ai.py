import asyncio
from app.nocodb.operations import buscar_registro_inicial
from app.ai.agents import extraer_datos_personales, extraer_educacion

async def main():
    reg = await buscar_registro_inicial("1783902153.053739")
    if not reg:
        print("No se encontró el registro.")
        return

    texto = reg.get("Datos Crudos", "")
    
    print("--- 1. Probando Extracción de Datos Personales (OpenAI) ---")
    datos = await extraer_datos_personales(texto)
    print(datos.model_dump_json(indent=2))

    print("\n--- 2. Probando Extracción de Educación (OpenAI) ---")
    edu = await extraer_educacion(texto)
    print(edu.model_dump_json(indent=2))

if __name__ == "__main__":
    asyncio.run(main())