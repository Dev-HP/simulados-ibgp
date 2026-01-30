#!/usr/bin/env python3
"""
Diagnostica erros 404 no sistema
"""
import requests

def diagnosticar_404():
    print("🔍 DIAGNOSTICANDO ERROS 404")
    print("=" * 50)
    
    base_urls = [
        "https://simulados-ibgp.onrender.com",
        "https://simulados-ibgp-1.onrender.com"
    ]
    
    # Endpoints comuns que podem dar 404
    endpoints_teste = [
        "/",
        "/api/health",
        "/api/topics",
        "/api/questions",
        "/api/users/me",
        "/api/gemini/stats",
        "/favicon.ico",
        "/manifest.json",
        "/robots.txt"
    ]
    
    for base_url in base_urls:
        print(f"\n🌐 Testando: {base_url}")
        print("-" * 30)
        
        for endpoint in endpoints_teste:
            try:
                url = f"{base_url}{endpoint}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 404:
                    print(f"❌ 404: {endpoint}")
                elif response.status_code == 200:
                    print(f"✅ 200: {endpoint}")
                else:
                    print(f"⚠️  {response.status_code}: {endpoint}")
                    
            except Exception as e:
                print(f"💥 ERRO: {endpoint} - {e}")

if __name__ == "__main__":
    diagnosticar_404()