#!/usr/bin/env python3
"""
Teste com Gemini Flash (cota separada)
"""

import os
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
    
    api_key = os.getenv('GEMINI_API_KEY')
    print(f"✅ API Key: {api_key[:20]}...")
    
    genai.configure(api_key=api_key)
    
    # Testar com Flash (mais leve)
    print("\n🤖 Testando com gemini-2.5-flash...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Diga apenas 'OK' se funcionando")
    print(f"✅ Flash OK: {response.text}")
    
except Exception as e:
    print(f"❌ Erro Flash: {e}")
    
    try:
        # Testar com Flash Lite
        print("\n🤖 Testando com gemini-2.5-flash-lite...")
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content("Diga 'OK'")
        print(f"✅ Flash Lite OK: {response.text}")
        
    except Exception as e2:
        print(f"❌ Erro Flash Lite: {e2}")