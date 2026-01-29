#!/usr/bin/env python3
"""
Monitora o deploy no Render e testa quando estiver pronto
"""

import requests
import time
from datetime import datetime

API_URL = "https://simulados-ibgp.onrender.com"

def check_health():
    """Verifica se API está respondendo"""
    try:
        response = requests.get(f"{API_URL}/api/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("="*60)
    print("🔍 MONITORANDO DEPLOY NO RENDER")
    print("="*60)
    print(f"\nAPI URL: {API_URL}")
    print(f"Iniciado em: {datetime.now().strftime('%H:%M:%S')}\n")
    
    print("Aguardando API ficar online...")
    print("(Render Free Tier pode demorar 30-60 segundos na primeira requisição)\n")
    
    attempts = 0
    max_attempts = 30  # 5 minutos (30 * 10 segundos)
    
    while attempts < max_attempts:
        attempts += 1
        print(f"[{attempts}/{max_attempts}] Tentando conectar... ", end="", flush=True)
        
        if check_health():
            print("✅ ONLINE!")
            print("\n" + "="*60)
            print("🎉 API ESTÁ FUNCIONANDO!")
            print("="*60)
            print(f"\n✅ Health check: {API_URL}/api/health")
            print(f"✅ Login: {API_URL}/login")
            print(f"✅ Dashboard: {API_URL}/dashboard")
            print("\n🔑 Credenciais:")
            print("   Usuário: teste")
            print("   Senha: teste123")
            print("\n📋 Próximos passos:")
            print("   1. Acessar o login")
            print("   2. Fazer login")
            print("   3. Testar sistema completo")
            print("\n💡 Para testar automaticamente, execute:")
            print("   python testar_producao_completo.py")
            print("\n" + "="*60)
            return 0
        else:
            print("❌ Offline")
            time.sleep(10)
    
    print("\n" + "="*60)
    print("⚠️  TIMEOUT - API não respondeu em 5 minutos")
    print("="*60)
    print("\n📋 Possíveis causas:")
    print("   1. Deploy ainda em andamento (aguarde mais)")
    print("   2. Erro no build (verificar logs no Render)")
    print("   3. Health check falhando")
    print("\n💡 Verificar:")
    print("   1. https://dashboard.render.com")
    print("   2. Ver logs do serviço")
    print("   3. Verificar se build passou")
    print("\n" + "="*60)
    return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
