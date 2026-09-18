import asyncio
import logging
from app.nocodb.operations import (
    buscar_registro_inicial, crear_cliente, actualizar_cliente,
    crear_educacion_formal, crear_educacion_complementaria,
    crear_experiencia_laboral, crear_habilidad
)
from app.ai.agents import (
    extraer_datos_personales, extraer_educacion, extraer_cursos,
    extraer_experiencia, extraer_habilidades, redactar_perfil
)
from app.ai.compiler import compilar_expediente

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def procesar_candidato(id_slack: str) -> dict:
    try:
        logger.info(f"Buscando registro para {id_slack}...")
        registro = await buscar_registro_inicial(id_slack)
        if not registro:
            return {"status": "error", "message": "Registro inicial no encontrado."}
        
        texto_crudo = registro.get("Datos Crudos", "")
        
        logger.info("Extrayendo datos en paralelo (Fase 1)...")
        datos_personales, educacion, cursos, experiencia = await asyncio.gather(
            extraer_datos_personales(texto_crudo),
            extraer_educacion(texto_crudo),
            extraer_cursos(texto_crudo),
            extraer_experiencia(texto_crudo)
        )
        
        logger.info("Guardando en NocoDB...")
        async def guardar_edu():
            for item in educacion.educacion:
                await crear_educacion_formal({"ID_Slack": id_slack, **item.model_dump(exclude_unset=True)})
                
        async def guardar_cur():
            for item in cursos.cursos:
                await crear_educacion_complementaria({"ID_Slack": id_slack, **item.model_dump(exclude_unset=True)})
                
        async def guardar_exp():
            for item in experiencia.experiencia:
                await crear_experiencia_laboral({"ID_Slack": id_slack, **item.model_dump(exclude_unset=True)})

        # Guardamos todo y CAPTURAMOS el resultado de crear_cliente
        resultados = await asyncio.gather(
            crear_cliente({"ID_Slack": id_slack, **datos_personales.model_dump(exclude_unset=True)}),
            guardar_edu(),
            guardar_cur(),
            guardar_exp()
        )
        
        # NocoDB devuelve el registro creado, incluyendo su 'Id' interno
        cliente_db = resultados[0]
        id_interno = cliente_db.get("Id")
        
        logger.info("Compilando expediente y extrayendo habilidades...")
        expediente = compilar_expediente(experiencia, educacion, cursos)
        habilidades = await extraer_habilidades(expediente)
        
        for hab in habilidades.habilidades:
            await crear_habilidad({"ID_Slack": id_slack, **hab.model_dump()})
            
        texto_habs = "\n=== HABILIDADES ===\n" + "\n".join([f"- {h.Habilidad} ({h.Tipo})" for h in habilidades.habilidades])
        expediente_final = expediente + texto_habs
        
        logger.info("Redactando perfil ejecutivo...")
        perfil = await redactar_perfil(expediente_final)
        
        logger.info("Actualizando perfil del cliente en NocoDB...")
        # Pasamos el 'Id' interno exacto de NocoDB para la actualización
        await actualizar_cliente({"Id": id_interno, **perfil.model_dump(exclude_unset=True)})
        
        return {"status": "success", "message": "Candidato procesado y guardado correctamente."}
        
    except Exception as e:
        logger.error(f"Error procesando candidato: {e}")
        return {"status": "error", "message": str(e)}