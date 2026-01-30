"""
Teste rápido para verificar se o HuggingFace está funcionando com InferenceClient
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_huggingface_client():
    """Testa o InferenceClient do HuggingFace"""
    try:
        from huggingface_hub import InferenceClient
        
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not api_key:
            print("❌ HUGGINGFACE_API_KEY não configurada")
            return False
        
        print(f"✅ API Key configurada: {api_key[:10]}...")
        
        # Criar cliente
        client = InferenceClient(token=api_key)
        print("✅ InferenceClient criado")
        
        # Testar com modelo simples
        models_to_test = [
            "mistralai/Mistral-7B-Instruct-v0.3",
            "meta-llama/Llama-3.2-3B-Instruct",
            "google/gemma-2-2b-it"
        ]
        
        for model in models_to_test:
            try:
                print(f"\n🔄 Testando modelo: {model}")
                
                response = client.text_generation(
                    "Responda apenas: OK",
                    model=model,
                    max_new_tokens=50,
                    temperature=0.7
                )
                
                print(f"✅ Sucesso! Resposta: {response[:100]}")
                return True
                
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Erro com {model}: {error_msg[:200]}")
                
                if 'loading' in error_msg.lower():
                    print("   ⏳ Modelo está carregando, tente novamente em alguns segundos")
                elif '410' in error_msg:
                    print("   ⚠️ Endpoint deprecado - mas InferenceClient deve resolver isso")
                continue
        
        print("\n❌ Todos os modelos falharam")
        return False
        
    except ImportError:
        print("❌ huggingface_hub não instalado. Execute: pip install huggingface-hub")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 TESTE DO HUGGINGFACE INFERENCE CLIENT")
    print("=" * 50)
    
    success = test_huggingface_client()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ TESTE PASSOU - HuggingFace está funcionando!")
    else:
        print("❌ TESTE FALHOU - Verifique os logs acima")
