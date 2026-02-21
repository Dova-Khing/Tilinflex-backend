from .usuarios import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioResponse
from .suscripciones import Suscripcion, SuscripcionCreate, SuscripcionUpdate, SuscripcionResponse
from .obras import Obra, ObraCreate, ObraUpdate, ObraResponse
from .categoria import Categoria, CategoriaCreate, CategoriaUpdate, CategoriaResponse
from .detalle_suscripcion import DetalleSuscripcion, DetalleSuscripcionCreate, DetalleSuscripcionUpdate, DetalleSuscripcionResponse
from .perfil import Perfil, PerfilCreate, PerfilUpdate, PerfilResponse
from .generos import Genero, GeneroCreate, GeneroUpdate, GeneroResponse
from .historial_reproduccion import HistorialReproduccion, HistorialReproduccionCreate, HistorialReproduccionUpdate, HistorialReproduccionResponse


__all__ = [
    "Usuario", "UsuarioCreate", "UsuarioUpdate", "UsuarioResponse",
    "Suscripcion", "SuscripcionCreate", "SuscripcionUpdate", "SuscripcionResponse",
    "Obra", "ObraCreate", "ObraUpdate", "ObraResponse",
    "Categoria", "CategoriaCreate", "CategoriaUpdate", "CategoriaResponse",
    "DetalleSuscripcion", "DetalleSuscripcionCreate", "DetalleSuscripcionUpdate", "DetalleSuscripcionResponse",
    "Perfil", "PerfilCreate", "PerfilUpdate", "PerfilResponse",
    "Genero", "GeneroCreate", "GeneroUpdate", "GeneroResponse",
    "HistorialReproduccion", "HistorialReproduccionCreate", "HistorialReproduccionUpdate", "HistorialReproduccionResponse"

]
