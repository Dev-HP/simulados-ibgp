#!/usr/bin/env python3
"""
Verificação urgente do status da API
"""
import requests
import time

def verificar_status():
    print("🚨 VERIFICAÇÃO URGENTE DE STATUS")
    print("=" * 50)
    
    urls = [
        "https://simulados-ibgp.onrender.com/health",
        "https://simulados-ibgp.onrender.com/api/health",
        "https://simulados-ibgp.onrender.com/",
        "https://simulados-ibgp-1.onrender.com/"
    ]
    
    for url in urls:
        try:
            print(f"\n🔍 Testando: {url}")
            response = requests.get(url, timeout=15)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ OK: {response.text[:100]}...")
            else:
                print(f"   ❌ ERRO: {response.text[:200]}...")
                
        except Exception as e:
            print(f"   💥 FALHA: {e}")
    
    print("\n" + "=" * 50)
    print("🔍 DIAGNÓSTICO:")
    
    # Testar se é problema de deploy
    try:
        response = requests.get("https://simulados-ibgp.onrender.com/health", timeout=30)
        if response.status_code == 200:
            print("✅ API está funcionando - problema pode ser temporário")
        else:
            print(f"❌ API com problema: {response.status_code}")
    except:
        print("💥 API completamente fora do ar - deploy falhou!")

if __name__ == "__main__":
    verificar_status()