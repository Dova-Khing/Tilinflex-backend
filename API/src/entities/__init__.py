from .usuarios import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioResponse
from .suscripciones import Suscripcion, SuscripcionCreate, SuscripcionUpdate, SuscripcionResponse
from .obras import Obra, ObraResponse
from .categoria import Categoria, CategoriaResponse
from .detalle_suscripcion import DetalleSuscripcion, DetalleSuscripcionCreate, DetalleSuscripcionUpdate, DetalleSuscripcionResponse
from .perfil import Perfil, PerfilCreate, PerfilUpdate, PerfilResponse
from .generos import Genero, GeneroResponse
from .historial_reproduccion import HistorialReproduccion, HistorialReproduccionCreate, HistorialReproduccionUpdate, HistorialReproduccionResponse


__all__ = [
    "Usuario", "UsuarioCreate", "UsuarioUpdate", "UsuarioResponse",
    "Suscripcion", "SuscripcionCreate", "SuscripcionUpdate", "SuscripcionResponse",
    "Obra", "ObraCreate", "ObraUpdate", "ObraResponse",
    "Categoria", "CategoriaResponse",
    "DetalleSuscripcion", "DetalleSuscripcionCreate", "DetalleSuscripcionUpdate", "DetalleSuscripcionResponse",
    "Perfil", "PerfilCreate", "PerfilUpdate", "PerfilResponse",
    "Genero", "GeneroCreate", "GeneroUpdate", "GeneroResponse",
    "HistorialReproduccion", "HistorialReproduccionCreate", "HistorialReproduccionUpdate", "HistorialReproduccionResponse"

]
