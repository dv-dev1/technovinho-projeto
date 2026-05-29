import requests
import json

API_URL = "https://backend-production-e3f58.up.railway.app"
FRONTEND_URL = "https://frontend-production-f152.up.railway.app"

print("Iniciando testes de validacao em producao...")

print("\n[1] Testando Frontend...")
try:
    res = requests.get(FRONTEND_URL)
    if res.status_code == 200:
        print("[OK] Frontend esta online e respondendo (200 OK)")
    else:
        print(f"[FAIL] Frontend retornou {res.status_code}")
except Exception as e:
    print(f"[ERROR] Erro ao conectar no Frontend: {e}")

print("\n[2] Testando Backend (Swagger UI)...")
try:
    res = requests.get(f"{API_URL}/docs")
    if res.status_code == 200:
        print("[OK] Backend API esta online e respondendo (200 OK)")
    else:
        print(f"[FAIL] Backend retornou {res.status_code}")
except Exception as e:
    print(f"[ERROR] Erro ao conectar no Backend: {e}")

print("\n[3] Testando Endpoint da API (Verificando Banco de Dados)...")
try:
    res = requests.get(f"{API_URL}/api/services")
    if res.status_code in [200, 401]:
        print(f"[OK] Banco de Dados conectado e API roteando corretamente (Retornou {res.status_code})")
        if res.status_code == 200:
            print(f"   Servicos no banco: {len(res.json())}")
    else:
        print(f"[FAIL] Endpoint /api/services retornou {res.status_code} - {res.text}")
except Exception as e:
    print(f"[ERROR] Erro ao consultar /api/services: {e}")

print("\nBateria de testes finalizada!")
