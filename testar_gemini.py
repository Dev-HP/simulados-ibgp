#!/usr/bin/env python3
"""
Teste simples da API Gemini
"""

import os
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
    
    api_key = os.getenv('GEMINI_API_KEY')
    print(f"✅ API Key encontrada: {api_key[:20]}...")
    
    genai.configure(api_key=api_key)
    
    # Listar modelos disponíveis
    print("\n📋 Modelos disponíveis:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  • {model.name}")
    
    # Testar geração
    print("\n🤖 Testando geração com gemini-pro-latest...")
    model = genai.GenerativeModel('gemini-pro-latest')
    response = model.generate_content("Diga apenas 'OK' se você está funcionando")
    print(f"✅ Resposta: {response.text}")
    
except Exception as e:
    print(f"❌ Erro: {e}")
