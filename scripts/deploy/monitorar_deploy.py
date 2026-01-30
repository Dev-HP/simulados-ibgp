#!/usr/bin/env python3
"""
Script para monitorar o deploy da API no Render em tempo real
"""

import requests
import time
from datetime import datetime

API_URL = "https://simulados-api-porto-velho.onrender.com"
HEALTH_ENDPOINT = f"{API_URL}/health"

def check_health():
    """Verifica o health check da API"""
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=10)
        return response.status_code == 200, response.status_code
    except requests.exceptions.RequestException as e:
        return False, str(e)

def main():
    print("=" * 60)
    print("🔍 MONITORANDO DEPLOY DA API NO RENDER")
    print("=" * 60)
    print(f"URL: {API_URL}")
    print(f"Health Check: {HEALTH_ENDPOINT}")
    print("=" * 60)
    print("\n⏳ Aguardando API ficar online...")
    print("(Pressione Ctrl+C para parar)\n")
    
    attempt = 0
    last_status = None
    
    while True:
        attempt += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        is_healthy, status = check_health()
        
        if is_healthy:
            print(f"\n{'=' * 60}")
            print(f"✅ API ESTÁ ONLINE!")
            print(f"{'=' * 60}")
            print(f"Status: {status}")
            print(f"Tentativas: {attempt}")
            print(f"Hora: {timestamp}")
            print(f"\n🎉 Deploy concluído com sucesso!")
            print(f"\n📍 Próximos passos:")
            print(f"1. Acesse: https://simulados-web-porto-velho.onrender.com")
            print(f"2. Vá para: /ai-generator")
            print(f"3. Clique em: 🚀 GERAR TODAS AS 60 QUESTÕES")
            break
        else:
            # Só imprime se o status mudou
            if status != last_status:
                print(f"[{timestamp}] Tentativa {attempt}: ❌ {status}")
                last_status = status
            else:
                # Imprime um ponto para mostrar que está rodando
                print(".", end="", flush=True)
        
        time.sleep(10)  # Aguarda 10 segundos entre tentativas

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Monitoramento interrompido pelo usuário")
        print("Execute novamente quando quiser verificar o status")
