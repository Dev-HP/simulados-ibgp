#!/usr/bin/env python3
"""
Verificação final do banco de questões
"""
import requests
from collections import Counter

API_URL = "https://simulados-ibgp.onrender.com"

print("=" * 60)
print("📊 STATUS FINAL DO BANCO DE QUESTÕES")
print("=" * 60)

try:
    response = requests.get(f"{API_URL}/api/questions?limit=200")
    
    if response.status_code == 200:
        questions = response.json()
        disciplinas = Counter([q['disciplina'] for q in questions])
        
        # Distribuição esperada do edital
        esperado = {
            "Informática": 30,
            "Português": 9,
            "Matemática": 6,
            "Raciocínio Lógico": 4,
            "Legislação": 7,
            "Conhecimentos Gerais": 4
        }
        
        print(f"\n✅ Total de questões no banco: {len(questions)}\n")
        
        print("📋 Comparação com o edital:")
        print("-" * 60)
        print(f"{'Disciplina':<25} {'Esperado':<12} {'Gerado':<12} {'Status'}")
        print("-" * 60)
        
        total_esperado = 0
        total_gerado = 0
        
        for disc, esp in esperado.items():
            gerado = disciplinas.get(disc, 0)
            total_esperado += esp
            total_gerado += gerado
            
            if gerado >= esp:
                status = "✅ OK"
            else:
                status = f"❌ Faltam {esp - gerado}"
            
            print(f"{disc:<25} {esp:<12} {gerado:<12} {status}")
        
        print("-" * 60)
        print(f"{'TOTAL':<25} {total_esperado:<12} {total_gerado:<12}")
        print("=" * 60)
        
        # Questões extras
        extras = total_gerado - total_esperado
        if extras > 0:
            print(f"\n💡 Você tem {extras} questões extras no banco!")
            print("   Isso é ótimo para ter mais variedade nas provas.")
        
        # Verificar se pode fazer prova
        print("\n🎯 PRONTO PARA USAR:")
        if all(disciplinas.get(disc, 0) >= esp for disc, esp in esperado.items()):
            print("   ✅ Sim! Você pode gerar provas completas agora.")
            print("\n📝 Para gerar uma prova, acesse:")
            print("   https://simulados-ibgp-1.onrender.com/prova-completa")
        else:
            print("   ⚠️  Ainda faltam questões em algumas disciplinas.")
        
        print("\n🔗 Links úteis:")
        print(f"   Backend API: {API_URL}")
        print(f"   Frontend: https://simulados-ibgp-1.onrender.com")
        print(f"   Login: teste / teste123")
        
    else:
        print(f"❌ Erro ao buscar questões: {response.status_code}")

except Exception as e:
    print(f"❌ Erro: {str(e)}")

print("\n" + "=" * 60)
