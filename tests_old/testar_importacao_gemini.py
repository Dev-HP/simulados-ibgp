#!/usr/bin/env python3
"""
Testar se a importação do GeminiQuestionGenerator funciona
"""
import sys
import os

# Adicionar o diretório da API ao path
sys.path.insert(0, os.path.join(os.getcwd(), 'api'))

def testar_importacao():
    """Testa a importação do GeminiQuestionGenerator"""
    print("🔍 TESTANDO IMPORTAÇÃO DO GEMINI")
    print("=" * 40)
    
    try:
        print("1. Testando importação...")
        from services.gemini_generator import GeminiQuestionGenerator
        print("✅ GeminiQuestionGenerator importado com sucesso")
        
        print("\n2. Verificando classe...")
        print(f"   Classe: {GeminiQuestionGenerator}")
        print(f"   Métodos: {[m for m in dir(GeminiQuestionGenerator) if not m.startswith('_')]}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {str(e)}")
        return False
        
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")
        return False

def verificar_arquivo():
    """Verifica se o arquivo existe"""
    print("\n3. Verificando arquivo...")
    
    gemini_path = os.path.join('api', 'services', 'gemini_generator.py')
    
    if os.path.exists(gemini_path):
        print(f"✅ Arquivo existe: {gemini_path}")
        
        # Verificar conteúdo
        with open(gemini_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'class GeminiQuestionGenerator' in content:
            print("✅ Classe GeminiQuestionGenerator encontrada no arquivo")
        else:
            print("❌ Classe GeminiQuestionGenerator NÃO encontrada no arquivo")
            
    else:
        print(f"❌ Arquivo não existe: {gemini_path}")

if __name__ == "__main__":
    verificar_arquivo()
    testar_importacao()