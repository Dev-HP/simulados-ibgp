#!/usr/bin/env python3
"""
Script para testar rate limiting do Gemini API
"""
import requests
import time
import sys

API_URL = "http://localhost:8000"

def get_token():
    """Faz login e retorna token"""
    response = requests.post(
        f"{API_URL}/api/token",
        data={"username": "teste", "password": "teste123"}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"❌ Erro no login: {response.status_code}")
        sys.exit(1)

def test_rate_limit(token):
    """Testa limite de requisições por minuto"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("🧪 Testando limite de 55 requisições/minuto...")
    print("=" * 60)
    
    success_count = 0
    blocked_count = 0
    
    for i in range(60):
        try:
            response = requests.post(
                f"{API_URL}/api/generate-with-ai",
                params={
                    "topic_id": 1,
                    "quantity": 1,
                    "use_references": False
                },
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 429:
                blocked_count += 1
                print(f"\n🚫 Bloqueado na requisição {i+1}")
                print(f"📝 Mensagem: {response.json()['detail']}")
                print(f"\n✅ Teste PASSOU!")
                print(f"   - Requisições bem-sucedidas: {success_count}")
                print(f"   - Requisições bloqueadas: {blocked_count}")
                print(f"   - Rate limiting funcionando corretamente!")
                return True
                
            elif response.status_code == 200:
                success_count += 1
                print(f"✓ Requisição {i+1}: OK", end="\r")
                
            else:
                print(f"\n⚠️  Erro inesperado na requisição {i+1}: {response.status_code}")
                print(f"   Resposta: {response.text}")
                
        except requests.exceptions.Timeout:
            print(f"\n⏱️  Timeout na requisição {i+1}")
            
        except Exception as e:
            print(f"\n❌ Erro na requisição {i+1}: {str(e)}")
        
        time.sleep(0.5)
    
    print(f"\n⚠️  Teste FALHOU!")
    print(f"   - Nenhuma requisição foi bloqueada após 60 tentativas")
    print(f"   - Rate limiting pode não estar funcionando")
    return False

def check_stats():
    """Verifica estatísticas do Gemini"""
    print("\n📊 Verificando estatísticas...")
    print("=" * 60)
    
    response = requests.get(f"{API_URL}/api/gemini-stats")
    
    if response.status_code == 200:
        stats = response.json()
        print(f"✅ Status: {stats['status']}")
        print(f"📈 Uso no último minuto: {stats['usage']['last_minute']}/{stats['limits']['per_minute']}")
        print(f"📈 Uso hoje: {stats['usage']['today']}/{stats['limits']['per_day']}")
        print(f"🚫 Requisições bloqueadas: {stats['usage']['blocked']}")
        print(f"⏳ Restante (minuto): {stats['remaining']['minute']}")
        print(f"⏳ Restante (dia): {stats['remaining']['day']}")
        return True
    else:
        print(f"❌ Erro ao buscar estatísticas: {response.status_code}")
        return False

def main():
    print("\n" + "=" * 60)
    print("🧪 TESTE DE RATE LIMITING - GEMINI API")
    print("=" * 60)
    
    # 1. Fazer login
    print("\n1️⃣  Fazendo login...")
    token = get_token()
    print("✅ Login bem-sucedido!")
    
    # 2. Verificar estatísticas iniciais
    print("\n2️⃣  Estatísticas iniciais:")
    check_stats()
    
    # 3. Testar rate limiting
    print("\n3️⃣  Testando rate limiting:")
    result = test_rate_limit(token)
    
    # 4. Verificar estatísticas finais
    print("\n4️⃣  Estatísticas finais:")
    check_stats()
    
    # 5. Resultado final
    print("\n" + "=" * 60)
    if result:
        print("🎉 TESTE COMPLETO: PASSOU")
        print("   Rate limiting está funcionando corretamente!")
    else:
        print("❌ TESTE COMPLETO: FALHOU")
        print("   Rate limiting pode não estar funcionando!")
    print("=" * 60 + "\n")
    
    return 0 if result else 1

if __name__ == "__main__":
    sys.exit(main())
