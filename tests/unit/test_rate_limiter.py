"""
Tests unitarios para el Rate Limiter
"""

import pytest
from datetime import datetime, timedelta
from pyenterprise.utils.rate_limiter import LoginRateLimiter


def test_rate_limiter_permite_intentos_iniciales():
    """Debe permitir los primeros intentos dentro del límite."""
    limiter = LoginRateLimiter(max_attempts=3, window_minutes=5)
    
    # Los primeros 2 intentos deben ser permitidos
    assert not limiter.is_blocked("test@example.com")
    limiter.add_attempt("test@example.com")
    assert not limiter.is_blocked("test@example.com")
    limiter.add_attempt("test@example.com")
    assert not limiter.is_blocked("test@example.com")


def test_rate_limiter_bloquea_despues_limite():
    """Debe bloquear después de exceder el límite."""
    limiter = LoginRateLimiter(max_attempts=3, window_minutes=5)
    
    # Agregar 3 intentos
    for _ in range(3):
        limiter.add_attempt("test@example.com")
    
    # El cuarto intento debe estar bloqueado
    assert limiter.is_blocked("test@example.com")


def test_rate_limiter_reset():
    """Debe resetear correctamente los intentos."""
    limiter = LoginRateLimiter(max_attempts=3, window_minutes=5)
    
    # Agregar intentos hasta bloquear
    for _ in range(3):
        limiter.add_attempt("test@example.com")
    
    assert limiter.is_blocked("test@example.com")
    
    # Resetear
    limiter.reset("test@example.com")
    
    # Debe permitir nuevamente
    assert not limiter.is_blocked("test@example.com")


def test_rate_limiter_usuarios_independientes():
    """Diferentes usuarios deben tener contadores independientes."""
    limiter = LoginRateLimiter(max_attempts=3, window_minutes=5)
    
    # Bloquear usuario1
    for _ in range(3):
        limiter.add_attempt("user1@example.com")
    
    # usuario1 bloqueado, usuario2 no
    assert limiter.is_blocked("user1@example.com")
    assert not limiter.is_blocked("user2@example.com")


def test_rate_limiter_tiempo_restante():
    """Debe calcular correctamente el tiempo restante."""
    limiter = LoginRateLimiter(max_attempts=3, window_minutes=15)
    
    # Agregar intentos hasta bloquear
    for _ in range(3):
        limiter.add_attempt("test@example.com")
    
    # Debe tener aproximadamente 15 minutos restantes
    tiempo_restante = limiter.get_remaining_time("test@example.com")
    assert 14 <= tiempo_restante <= 15


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
