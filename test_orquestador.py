import asyncio
from app.workflows.orchestrator import procesar_candidato

async def main():
    # ID de prueba de Kagado Nalguisa
    id_prueba = "1783902153.053739" 
    print(f"Iniciando procesamiento completo para el candidato {id_prueba}...")
    
    resultado = await procesar_candidato(id_prueba)
    
    print("\n=== RESULTADO DEL ORQUESTADOR ===")
    print(resultado)

if __name__ == "__main__":
    asyncio.run(main())