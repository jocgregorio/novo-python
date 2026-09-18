"""Compilación de información estructurada a un expediente de texto plano."""

from app.ai.schemas import CursosResponse, EducacionResponse, ExperienciaResponse


def _formatear_lista(valores: list[str]) -> str:
    """Convierte una lista de textos en líneas legibles para el expediente."""
    return "\n".join(f"  - {valor}" for valor in valores) or "  - No especificado"


def compilar_expediente(
    experiencia_obj: ExperienciaResponse,
    educacion_obj: EducacionResponse,
    cursos_obj: CursosResponse,
) -> str:
    """Construye el expediente intermedio a partir de las respuestas Pydantic."""
    secciones = ["=== EXPERIENCIA LABORAL ===", ""]

    for experiencia in experiencia_obj.items:
        secciones.extend(
            [
                f"- Cargo: {experiencia.Cargo} en {experiencia.Empresa}",
                "  Funciones:",
                _formatear_lista(experiencia.Funciones),
                "  Logros:",
                _formatear_lista(experiencia.Logros),
            ]
        )

    secciones.extend(["", "=== EDUCACIÓN FORMAL ===", ""])
    for educacion in educacion_obj.items:
        secciones.append(f"- {educacion.Grado} en {educacion.Casa_de_Estudios}")

    secciones.extend(["", "=== EDUCACIÓN COMPLEMENTARIA ===", ""])
    for curso in cursos_obj.items:
        secciones.append(f"- {curso.Formacion} en {curso.Instituto}")

    return "\n".join(secciones)
