#!/usr/bin/env python3
"""
Popular banco de forma simples e direta
"""
import requests
import json

BASE_URL = "https://simulados-ibgp.onrender.com"
API_URL = f"{BASE_URL}/api"

def popular_simples():
    print("🚀 POPULAÇÃO SIMPLES DO BANCO")
    print("=" * 40)
    
    # 1. Verificar sistema
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        print(f"✅ Sistema: {response.status_code}")
    except:
        print("❌ Sistema offline")
        return
    
    # 2. Seed básico
    try:
        response = requests.post(f"{API_URL}/seed-database", timeout=30)
        print(f"✅ Seed: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Seed: {str(e)}")
    
    # 3. Verificar estatísticas
    try:
        response = requests.get(f"{API_URL}/estatisticas-banco", timeout=10)
        if response.status_code == 200:
            data = response.json()
            total = data.get('total_questoes', 0)
            print(f"📊 Total questões: {total}")
            
            if total >= 4:
                print("✅ Banco já tem dados básicos!")
                return
        
    except Exception as e:
        print(f"⚠️ Estatísticas: {str(e)}")
    
    print("\n🎯 BANCO POPULADO COM DADOS BÁSICOS")

if __name__ == "__main__":
    popular_simples()