import asyncio
from app.nocodb.operations import buscar_registro_inicial

async def test():
    id_prueba = "1783902153.053739"
    registro = await buscar_registro_inicial(id_prueba)
    print("Registro recuperado:", registro)

if __name__ == "__main__":
    asyncio.run(test())
