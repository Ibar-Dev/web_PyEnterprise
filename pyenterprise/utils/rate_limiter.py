"""
Rate Limiter para proteger contra ataques de fuerza bruta
"""

from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List


class LoginRateLimiter:
    """
    Rate limiter simple para intentos de login.
    Bloquea después de X intentos fallidos en Y minutos.
    """
    
    def __init__(self, max_attempts: int = 5, window_minutes: int = 15):
        """
        Args:
            max_attempts: Número máximo de intentos permitidos
            window_minutes: Ventana de tiempo en minutos para contar intentos
        """
        self.attempts: Dict[str, List[datetime]] = defaultdict(list)
        self.max_attempts = max_attempts
        self.window = timedelta(minutes=window_minutes)
    
    def is_blocked(self, identifier: str) -> bool:
        """
        Verifica si un identificador (email, IP) está bloqueado.
        
        Args:
            identifier: Email o IP a verificar
            
        Returns:
            True si está bloqueado, False si puede intentar
        """
        now = datetime.now()
        
        # Limpiar intentos antiguos fuera de la ventana
        self.attempts[identifier] = [
            attempt_time for attempt_time in self.attempts[identifier]
            if now - attempt_time < self.window
        ]
        
        # Verificar si ha excedido el límite
        return len(self.attempts[identifier]) >= self.max_attempts
    
    def add_attempt(self, identifier: str):
        """
        Registra un intento fallido.
        
        Args:
            identifier: Email o IP que intentó login
        """
        self.attempts[identifier].append(datetime.now())
    
    def reset(self, identifier: str):
        """
        Resetea los intentos para un identificador (al hacer login exitoso).
        
        Args:
            identifier: Email o IP a resetear
        """
        if identifier in self.attempts:
            del self.attempts[identifier]
    
    def get_remaining_time(self, identifier: str) -> int:
        """
        Obtiene el tiempo restante de bloqueo en minutos.
        
        Args:
            identifier: Email o IP a verificar
            
        Returns:
            Minutos restantes de bloqueo
        """
        if not self.attempts[identifier]:
            return 0
        
        oldest_attempt = min(self.attempts[identifier])
        time_since_oldest = datetime.now() - oldest_attempt
        remaining = self.window - time_since_oldest
        
        return max(0, int(remaining.total_seconds() / 60))


# Instancia global del rate limiter
login_rate_limiter = LoginRateLimiter(max_attempts=5, window_minutes=15)
