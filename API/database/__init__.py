"""
Módulo de inicialización de base de datos
=========================================

Expone las funciones y objetos principales desde config.py
"""

from .config import engine, SessionLocal, get_db, DATABASE_URL

__all__ = ["engine", "SessionLocal", "get_db", "DATABASE_URL"]
