"""Esquemas estructurados del expediente profesional."""

from typing import Annotated, Literal

from pydantic import BaseModel, Field, StringConstraints, model_validator


DescripcionExperiencia = Annotated[str, StringConstraints(min_length=145, max_length=160)]


class DatosPersonales(BaseModel):
    Nombres: str = ""
    Apellidos: str = ""
    Email: str = ""
    Telefono: str = ""
    Direccion: str = ""
    LinkedIn: str = ""
    Titulo_Profesional: str = ""


class EducacionItem(BaseModel):
    Grado: str = ""
    Casa_de_Estudios: str = ""
    Ano_de_Egreso: str = ""


class EducacionResponse(BaseModel):
    items: list[EducacionItem] = Field(default_factory=list)


class CursoItem(BaseModel):
    Formacion: str = ""
    Instituto: str = ""
    Duracion: str = ""
    Ano_de_Finalizacion: str = ""


class CursosResponse(BaseModel):
    items: list[CursoItem] = Field(default_factory=list)


class ExperienciaItem(BaseModel):
    Cargo: str = ""
    Empresa: str = ""
    Fecha_Ingreso: str = ""
    Fecha_Egreso: str = ""
    Funciones: list[DescripcionExperiencia] = Field(default_factory=list)
    Logros: list[DescripcionExperiencia] = Field(default_factory=list)


class ExperienciaResponse(BaseModel):
    items: list[ExperienciaItem] = Field(default_factory=list)


class HabilidadItem(BaseModel):
    Habilidad: str
    Tipo: Literal["Habilidad Técnica", "Habilidad Blanda"]


class HabilidadesResponse(BaseModel):
    items: list[HabilidadItem] = Field(min_length=12, max_length=12)

    @model_validator(mode="after")
    def validar_distribucion(self) -> "HabilidadesResponse":
        tecnicas = sum(item.Tipo == "Habilidad Técnica" for item in self.items)
        blandas = sum(item.Tipo == "Habilidad Blanda" for item in self.items)
        if tecnicas != 6 or blandas != 6:
            raise ValueError("Se requieren exactamente 6 habilidades técnicas y 6 blandas.")
        return self


class PerfilResponse(BaseModel):
    Titulo: str = ""
    Perfil: str = ""
