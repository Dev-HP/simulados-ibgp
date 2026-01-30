"""
Gerenciador inteligente de quota do Gemini
Evita erro 429 monitorando uso em tempo real
"""
import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Optional
import google.generativeai as genai

class QuotaManager:
    """Gerencia quota do Gemini para evitar erro 429"""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY não encontrada")
        
        genai.configure(api_key=self.api_key)
        
        # Limites conhecidos (tier gratuito)
        self.limits = {
            "gemini-2.5-flash": {
                "rpm": 5,      # Requests por minuto
                "rpd": 20,     # Requests por dia
                "tpm": 250000  # Tokens por minuto
            },
            "gemini-2.5-flash-lite": {
                "rpm": 10,
                "rpd": 20,
                "tpm": 250000
            }
        }
        
        # Cache de uso (em memória - em produção usar Redis)
        self.usage_cache = {}
    
    def can_make_request(self, model_name: str) -> tuple[bool, str]:
        """
        Verifica se pode fazer requisição sem estourar quota
        Returns: (pode_fazer, motivo_se_nao_pode)
        """
        try:
            # Verificar quota atual via API
            quota_info = self._get_current_quota(model_name)
            
            if not quota_info:
                return True, "Quota info não disponível, tentando..."
            
            # Verificar RPD (mais crítico)
            if quota_info.get('rpd_used', 0) >= quota_info.get('rpd_limit', 20):
                return False, f"RPD esgotado: {quota_info['rpd_used']}/{quota_info['rpd_limit']}"
            
            # Verificar RPM
            if quota_info.get('rpm_used', 0) >= quota_info.get('rpm_limit', 5):
                return False, f"RPM esgotado: {quota_info['rpm_used']}/{quota_info['rpm_limit']}"
            
            return True, "OK"
            
        except Exception as e:
            # Se não conseguir verificar, permite (melhor tentar que bloquear)
            return True, f"Erro ao verificar quota: {e}"
    
    def _get_current_quota(self, model_name: str) -> Optional[Dict]:
        """Obtém informações atuais de quota (simulado)"""
        # Em um cenário real, isso viria da API do Google
        # Por ora, vamos simular baseado no cache local
        
        now = datetime.now()
        cache_key = f"{model_name}_{now.strftime('%Y-%m-%d')}"
        
        if cache_key not in self.usage_cache:
            self.usage_cache[cache_key] = {
                'rpd_used': 0,
                'rpm_used': 0,
                'last_request': None
            }
        
        usage = self.usage_cache[cache_key]
        limits = self.limits.get(model_name, self.limits["gemini-2.5-flash-lite"])
        
        # Reset RPM se passou 1 minuto
        if usage['last_request']:
            if (now - usage['last_request']).seconds >= 60:
                usage['rpm_used'] = 0
        
        return {
            'rpd_used': usage['rpd_used'],
            'rpd_limit': limits['rpd'],
            'rpm_used': usage['rpm_used'],
            'rpm_limit': limits['rpm']
        }
    
    def record_request(self, model_name: str):
        """Registra uma requisição feita"""
        now = datetime.now()
        cache_key = f"{model_name}_{now.strftime('%Y-%m-%d')}"
        
        if cache_key not in self.usage_cache:
            self.usage_cache[cache_key] = {
                'rpd_used': 0,
                'rpm_used': 0,
                'last_request': None
            }
        
        self.usage_cache[cache_key]['rpd_used'] += 1
        self.usage_cache[cache_key]['rpm_used'] += 1
        self.usage_cache[cache_key]['last_request'] = now
    
    def get_best_model(self) -> str:
        """Retorna o melhor modelo disponível no momento"""
        models_priority = [
            "gemini-2.5-flash-lite",  # Primeiro: menos restritivo
            "gemini-2.5-flash",       # Segundo: se lite não funcionar
            "gemini-2.0-flash"        # Terceiro: backup
        ]
        
        for model in models_priority:
            can_use, reason = self.can_make_request(model)
            if can_use:
                return model
        
        # Se todos estão bloqueados, retorna o lite (menor chance de erro)
        return "gemini-2.5-flash-lite"
    
    def get_quota_status(self) -> Dict:
        """Retorna status completo da quota"""
        status = {}
        
        for model_name in self.limits.keys():
            quota_info = self._get_current_quota(model_name)
            can_use, reason = self.can_make_request(model_name)
            
            status[model_name] = {
                'available': can_use,
                'reason': reason,
                'quota': quota_info
            }
        
        return status

# Instância global
quota_manager = QuotaManager()