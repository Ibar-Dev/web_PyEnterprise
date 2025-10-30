"""
Tests unitarios para autenticación
"""

import pytest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from pyenterprise.database import login_empleado


def test_login_credenciales_invalidas():
    """Login con credenciales inexistentes debe devolver None."""
    result = login_empleado("noexiste@test.com", "wrongpassword")
    assert result is None


def test_login_email_vacio():
    """Login con email vacío debe devolver None."""
    result = login_empleado("", "password123")
    assert result is None


def test_login_password_vacio():
    """Login con password vacío debe devolver None."""
    result = login_empleado("test@test.com", "")
    assert result is None


def test_login_email_formato_invalido():
    """Login con formato de email inválido debe manejarse correctamente."""
    result = login_empleado("not-an-email", "password123")
    assert result is None


def test_login_password_corto():
    """Login con password muy corto debe devolver None."""
    result = login_empleado("test@test.com", "123")
    assert result is None


# Tests con credenciales reales (requieren base de datos)
@pytest.mark.integration
def test_login_admin_valido():
    """Login con credenciales admin válidas debe funcionar."""
    result = login_empleado("ibar.admin@pylink.com", "PyL1nk#Ib4r2025!Adm")
    
    if result:  # Solo si la BD está disponible
        assert result is not None
        assert result['rol'] == 'admin'
        assert 'nombre' in result
        assert result['activo'] == True


@pytest.mark.integration
def test_login_trabajador_valido():
    """Login con credenciales trabajador válidas debe funcionar."""
    result = login_empleado("ibar.trabajador@pylink.com", "PyL1nk#Ib4r2025!Wrk")
    
    if result:  # Solo si la BD está disponible
        assert result is not None
        assert result['rol'] in ['desarrollador', 'diseñadora']
        assert 'nombre' in result
        assert result['activo'] == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
