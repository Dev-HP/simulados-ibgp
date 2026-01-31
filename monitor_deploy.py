#!/usr/bin/env python3
"""
Monitora o deploy do Render e verifica quando o CORS estiver funcionando
"""
import requests
import time
from datetime import datetime

BACKEND = "https://simulados-ibgp.onrender.com"

print("🔍 Monitorando deploy do Render...\n")
print("Aguardando CORS headers...\n")

tentativas = 0
max_tentativas = 30  # 5 minutos (30 x 10 segundos)

while tentativas < max_tentativas:
    tentativas += 1
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    try:
        response = requests.get(f"{BACKEND}/api/questions?limit=1", timeout=10)
        
        # Verificar CORS header
        cors_origin = response.headers.get('access-control-allow-origin', None)
        
        if cors_origin:
            print(f"\n✅ [{timestamp}] CORS FUNCIONANDO!")
            print(f"   Access-Control-Allow-Origin: {cors_origin}")
            print(f"\n🎉 Deploy concluído com sucesso!")
            print(f"\n📝 Você pode acessar o frontend agora:")
            print(f"   https://simulados-ibgp-1.onrender.com")
            print(f"\n🔑 Login: teste / teste123")
            break
        else:
            print(f"⏳ [{timestamp}] Tentativa {tentativas}/{max_tentativas} - Aguardando CORS...")
            time.sleep(10)  # Aguardar 10 segundos
    
    except Exception as e:
        print(f"❌ [{timestamp}] Erro: {str(e)[:50]}")
        time.sleep(10)

if tentativas >= max_tentativas:
    print(f"\n⚠️  Timeout após {max_tentativas} tentativas")
    print(f"   O deploy pode estar demorando mais que o esperado.")
    print(f"\n💡 Verifique manualmente:")
    print(f"   1. Acesse: https://dashboard.render.com")
    print(f"   2. Verifique os logs do serviço 'simulados-ibgp'")
    print(f"   3. Aguarde o deploy concluir (pode levar 5-10 minutos)")
