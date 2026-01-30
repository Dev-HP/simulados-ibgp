#!/usr/bin/env python3
"""
Verificar variáveis de ambiente em produção
"""
import requests
import json

BASE_URL = "https://simulados-ibgp.onrender.com"

def verificar_env():
    """Verifica se as variáveis de ambiente estão configuradas"""
    print("🔧 VERIFICANDO VARIÁVEIS DE AMBIENTE")
    print("=" * 50)
    
    # Criar endpoint temporário para verificar env vars
    # Como não temos acesso direto, vamos inferir pelos erros
    
    print("📊 Analisando status dos geradores...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/ai-generators-status", timeout=15)
        if response.status_code == 200:
            data = response.json()
            generators = data.get('generators', {})
            
            # Análise do Gemini
            gemini = generators.get('gemini', {})
            gemini_configured = gemini.get('api_key_configured', False)
            gemini_error = gemini.get('test_result', {}).get('error', '')
            
            print("🔵 GEMINI:")
            print(f"   - Sistema diz que API key está configurada: {gemini_configured}")
            print(f"   - Erro reportado: {gemini_error}")
            
            if gemini_configured and "not set" in gemini_error:
                print("   ❌ PROBLEMA: Inconsistência na configuração do Gemini")
                print("   💡 SOLUÇÃO: Verificar se GEMINI_API_KEY está no Render")
            
            # Análise do HuggingFace
            huggingface = generators.get('huggingface', {})
            hf_configured = huggingface.get('api_key_configured', False)
            hf_test = huggingface.get('test_result', {})
            
            print("\n🟠 HUGGINGFACE:")
            print(f"   - Sistema diz que API key está configurada: {hf_configured}")
            print(f"   - Status do teste: {hf_test.get('status', 'unknown')}")
            print(f"   - Modelos disponíveis: {hf_test.get('available_models', 0)}")
            
            if hf_configured and hf_test.get('status') == 'failed':
                print("   ❌ PROBLEMA: API key configurada mas teste falhou")
                print("   💡 POSSÍVEIS CAUSAS:")
                print("      - API key inválida ou expirada")
                print("      - Rate limiting do HuggingFace")
                print("      - Modelos indisponíveis")
                print("      - Problema de rede/timeout")
        
        else:
            print(f"❌ Erro ao obter status: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    
    print("\n" + "=" * 50)
    print("📋 RECOMENDAÇÕES:")
    print("1. 🔵 GEMINI: Verificar se GEMINI_API_KEY está configurada no Render")
    print("2. 🟠 HUGGINGFACE: Testar API key manualmente")
    print("3. 🔄 Fazer redeploy após corrigir as variáveis")
    print("4. 🧪 Testar novamente após correções")

if __name__ == "__main__":
    verificar_env()