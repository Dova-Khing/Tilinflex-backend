"""
API de Historial de Reproduccion - Endpoints para gestion del historial de reproduccion.
Define las rutas HTTP para crear, consultar y actualizar el historial
de reproduccion de los usuarios en la plataforma.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from API.database.config import get_db
from API.src.crud.historial_reproducciones import HistorialReproduccionCRUD
from API.schemas import (
    HistorialReproduccionCreate,
    HistorialReproduccionUpdate,
    HistorialReproduccionResponse,
)

router = APIRouter(prefix="/historial", tags=["Historial Reproduccion"])


@router.post("/", response_model=HistorialReproduccionResponse, status_code=status.HTTP_201_CREATED)
def crear_historial(
    historial: HistorialReproduccionCreate, db: Session = Depends(get_db)
):
    """
    Crear un nuevo registro en el historial de reproduccion.

    Args:
        historial: Datos del historial a registrar.

    Returns:
        Historial de reproduccion creado.

    Raises:
        HTTPException 500: Si ocurre un error interno al crear el historial.
    """
    try:
        crud = HistorialReproduccionCRUD(db)
        return crud.crear_historial(
            tiempo_visto=historial.tiempo_visto,
            id_perfil=historial.id_perfil,
            id_obra=historial.id_obra,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el historial: {str(e)}"
        )


@router.get("/", response_model=List[HistorialReproduccionResponse])
def obtener_todos(db: Session = Depends(get_db)):
    """
    Obtener todos los registros del historial de reproduccion.

    Returns:
        Lista de registros del historial.

    Raises:
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = HistorialReproduccionCRUD(db)
        return crud.obtener_todos()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el historial: {str(e)}"
        )


@router.get("/{historial_id}", response_model=HistorialReproduccionResponse)
def obtener_historial_por_id(historial_id: UUID, db: Session = Depends(get_db)):
    """
    Obtener un registro del historial por su ID.

    Args:
        historial_id: Identificador unico del historial.

    Returns:
        Registro del historial correspondiente al ID.

    Raises:
        HTTPException 404: Si no se encuentra el historial.
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = HistorialReproduccionCRUD(db)
        historial = crud.obtener_por_id(historial_id)
        if not historial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Historial no encontrado"
            )
        return historial
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el historial: {str(e)}"
        )


@router.get("/perfil/{perfil_id}", response_model=List[HistorialReproduccionResponse])
def obtener_historial_por_perfil(perfil_id: UUID, db: Session = Depends(get_db)):
    """
    Obtener todos los registros del historial asociados a un perfil.

    Args:
        perfil_id: Identificador unico del perfil.

    Returns:
        Lista de registros del historial del perfil.

    Raises:
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = HistorialReproduccionCRUD(db)
        return crud.obtener_por_perfil(perfil_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el historial del perfil: {str(e)}"
        )


@router.get("/obra/{obra_id}", response_model=List[HistorialReproduccionResponse])
def obtener_historial_por_obra(obra_id: UUID, db: Session = Depends(get_db)):
    """
    Obtener todos los registros del historial asociados a una obra.

    Args:
        obra_id: Identificador unico de la obra.

    Returns:
        Lista de registros del historial de la obra.

    Raises:
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = HistorialReproduccionCRUD(db)
        return crud.obtener_por_obra(obra_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el historial de la obra: {str(e)}"
        )


@router.put("/{historial_id}", response_model=HistorialReproduccionResponse)
def actualizar_historial(
    historial_id: UUID,
    datos: HistorialReproduccionUpdate,
    db: Session = Depends(get_db),
):
    """
    Actualizar un registro del historial de reproduccion.

    Args:
        historial_id: Identificador unico del historial a actualizar.
        datos: Campos a actualizar del historial.

    Returns:
        Historial actualizado.

    Raises:
        HTTPException 404: Si no se encuentra el historial.
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = HistorialReproduccionCRUD(db)
        historial_actualizado = crud.actualizar_historial(
            historial_id, datos.dict(exclude_unset=True)
        )
        if not historial_actualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Historial no encontrado"
            )
        return historial_actualizado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el historial: {str(e)}"
        )
