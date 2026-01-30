#!/usr/bin/env python3
"""
Verificar documentação da API para encontrar endpoints corretos
"""
import requests

BASE_URL = "https://simulados-ibgp.onrender.com"

def verificar_documentacao():
    """Verifica a documentação da API"""
    print("📚 VERIFICANDO DOCUMENTAÇÃO DA API")
    print("=" * 40)
    
    # Acessar documentação
    try:
        print("1. Acessando /docs...")
        response = requests.get(f"{BASE_URL}/docs", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Documentação acessível")
            print(f"   URL: {BASE_URL}/docs")
        
    except Exception as e:
        print(f"❌ Erro ao acessar docs: {str(e)}")
    
    # Verificar OpenAPI spec
    try:
        print("\n2. Acessando OpenAPI spec...")
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            spec = response.json()
            print("✅ OpenAPI spec obtido")
            
            # Procurar endpoints relacionados a questões
            paths = spec.get('paths', {})
            print(f"\n📋 Endpoints encontrados ({len(paths)} total):")
            
            question_endpoints = []
            for path, methods in paths.items():
                if 'question' in path.lower() or 'generate' in path.lower():
                    for method, details in methods.items():
                        if method.upper() in ['GET', 'POST', 'PUT', 'DELETE']:
                            summary = details.get('summary', 'Sem descrição')
                            question_endpoints.append((method.upper(), path, summary))
            
            if question_endpoints:
                print("\n🎯 Endpoints relacionados a questões:")
                for method, path, summary in question_endpoints:
                    print(f"   {method} {path}")
                    print(f"      {summary}")
            else:
                print("\n❌ Nenhum endpoint de questões encontrado")
                
            # Mostrar todos os endpoints
            print(f"\n📝 Todos os endpoints:")
            for path, methods in paths.items():
                methods_list = [m.upper() for m in methods.keys() if m.upper() in ['GET', 'POST', 'PUT', 'DELETE']]
                if methods_list:
                    print(f"   {', '.join(methods_list)} {path}")
        
    except Exception as e:
        print(f"❌ Erro ao acessar OpenAPI: {str(e)}")

if __name__ == "__main__":
    verificar_documentacao()