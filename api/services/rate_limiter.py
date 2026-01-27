import time
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import deque

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Rate limiter para controlar uso da API Gemini.
    Limites do Free Tier:
    - 60 requisições por minuto
    - 1500 requisições por dia
    """
    
    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_day: int = 1500
    ):
        self.requests_per_minute = requests_per_minute
        self.requests_per_day = requests_per_day
        
        # Filas para rastrear requisições
        self.minute_requests = deque()
        self.day_requests = deque()
        
        # Estatísticas
        self.total_requests = 0
        self.blocked_requests = 0
        self.last_reset = datetime.now()
    
    def can_make_request(self) -> tuple[bool, Optional[str]]:
        """
        Verifica se pode fazer uma requisição.
        Retorna: (pode_fazer, mensagem_erro)
        """
        now = datetime.now()
        
        # Limpar requisições antigas (> 1 minuto)
        minute_ago = now - timedelta(minutes=1)
        while self.minute_requests and self.minute_requests[0] < minute_ago:
            self.minute_requests.popleft()
        
        # Limpar requisições antigas (> 1 dia)
        day_ago = now - timedelta(days=1)
        while self.day_requests and self.day_requests[0] < day_ago:
            self.day_requests.popleft()
        
        # Verificar limite por minuto
        if len(self.minute_requests) >= self.requests_per_minute:
            self.blocked_requests += 1
            wait_time = 60 - (now - self.minute_requests[0]).seconds
            return False, f"Limite de {self.requests_per_minute} requisições/minuto atingido. Aguarde {wait_time}s."
        
        # Verificar limite por dia
        if len(self.day_requests) >= self.requests_per_day:
            self.blocked_requests += 1
            hours_left = 24 - (now - self.day_requests[0]).seconds // 3600
            return False, f"Limite diário de {self.requests_per_day} requisições atingido. Aguarde {hours_left}h."
        
        return True, None
    
    def record_request(self):
        """Registra uma requisição feita"""
        now = datetime.now()
        self.minute_requests.append(now)
        self.day_requests.append(now)
        self.total_requests += 1
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas de uso"""
        now = datetime.now()
        
        # Limpar requisições antigas
        minute_ago = now - timedelta(minutes=1)
        day_ago = now - timedelta(days=1)
        
        minute_count = sum(1 for req in self.minute_requests if req > minute_ago)
        day_count = sum(1 for req in self.day_requests if req > day_ago)
        
        return {
            'requests_last_minute': minute_count,
            'requests_today': day_count,
            'limit_per_minute': self.requests_per_minute,
            'limit_per_day': self.requests_per_day,
            'remaining_minute': self.requests_per_minute - minute_count,
            'remaining_day': self.requests_per_day - day_count,
            'total_requests': self.total_requests,
            'blocked_requests': self.blocked_requests,
            'usage_percentage_minute': (minute_count / self.requests_per_minute) * 100,
            'usage_percentage_day': (day_count / self.requests_per_day) * 100
        }
    
    def wait_if_needed(self) -> Optional[float]:
        """
        Aguarda se necessário para respeitar rate limit.
        Retorna: tempo de espera em segundos (ou None)
        """
        can_make, error = self.can_make_request()
        
        if not can_make:
            # Calcular tempo de espera
            now = datetime.now()
            if self.minute_requests:
                oldest = self.minute_requests[0]
                wait_time = 60 - (now - oldest).seconds
                if wait_time > 0:
                    logger.warning(f"Rate limit reached. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    return wait_time
        
        return None

# Instância global do rate limiter
gemini_rate_limiter = RateLimiter(
    requests_per_minute=55,  # Margem de segurança (60 - 5)
    requests_per_day=1400    # Margem de segurança (1500 - 100)
)
