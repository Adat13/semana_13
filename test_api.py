import urllib.request
import urllib.error
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def make_request(url, method="GET", data=None, headers=None):
    if headers is None:
        headers = {}
    
    req_data = None
    if data is not None:
        req_data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'

    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, response.read().decode('utf-8'), response.info()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8'), e.headers
    except urllib.error.URLError as e:
        return 0, str(e.reason), {}

def test_api():
    print("======================================================================")
    print("TESTING API ENDPOINTS - SEMANA 13 - TORIBIO ANSELMO DAVID ANGEL")
    print("======================================================================\n")

    # 1. Test GET /api/iglesias/ (List of Churches)
    print("--- 1. LISTADO DE IGLESIAS (GET /api/iglesias/) ---")
    status, body, _ = make_request(f"{BASE_URL}/api/iglesias/")
    print(f"Status Code: {status}")
    if status == 200:
        data = json.loads(body)
        print(f"Total Iglesias: {len(data)}")
        print(json.dumps(data, indent=2))
    print("\n" + "="*40 + "\n")

    # 2. Test GET /api/participantes/ (List of Participants - Paginated)
    print("--- 2. LISTADO DE PARTICIPANTES - PAGINADO (GET /api/participantes/) ---")
    status, body, _ = make_request(f"{BASE_URL}/api/participantes/")
    print(f"Status Code: {status}")
    if status == 200:
        data = json.loads(body)
        print(f"Count of all participants: {data.get('count')}")
        print(f"Next page link: {data.get('next')}")
        print(f"Previous page link: {data.get('previous')}")
        print("First 2 participants in page 1:")
        print(json.dumps(data.get('results')[:2], indent=2))
    print("\n" + "="*40 + "\n")

    # 3. Test Filter and Ordering (GET /api/participantes/?status=activo&ordering=-created)
    print("--- 3. FILTRADO Y ORDENAMIENTO (GET /api/participantes/?status=activo&ordering=-created) ---")
    status, body, _ = make_request(f"{BASE_URL}/api/participantes/?status=activo&ordering=-created")
    print(f"Status Code: {status}")
    if status == 200:
        data = json.loads(body)
        print(f"Count of active participants: {data.get('count')}")
        print("Active participants in this page:")
        for idx, p in enumerate(data.get('results')):
            print(f"  {idx+1}. {p['nombre_completo']} | Status: {p['status']} | Created: {p['created']}")
    print("\n" + "="*40 + "\n")

    # 4. Test Custom Endpoints (@action)
    # 4a. Get summary stats: GET /api/participantes/resumen/
    print("--- 4a. ENDPOINT CUSTOM DE RESUMEN (GET /api/participantes/resumen/) ---")
    status, body, _ = make_request(f"{BASE_URL}/api/participantes/resumen/")
    print(f"Status Code: {status}")
    if status == 200:
        print(json.dumps(json.loads(body), indent=2))
    print("\n" + "="*40 + "\n")

    # 4b. Change state: POST /api/participantes/3/cambiar-estado/
    print("--- 4b. ENDPOINT CUSTOM CAMBIAR ESTADO (POST /api/participantes/3/cambiar-estado/) ---")
    status, body, _ = make_request(f"{BASE_URL}/api/participantes/3/cambiar-estado/", method="POST", data={"status": "activo"})
    print(f"Status Code: {status}")
    if status == 200:
        print(json.dumps(json.loads(body), indent=2))
    print("\n" + "="*40 + "\n")

    # 5. Fetch OpenAPI YAML Schema (GET /api/schema/)
    print("--- 5. ESQUEMA OPENAPI GENERADO AUTOMÁTICAMENTE (GET /api/schema/) ---")
    status, body, _ = make_request(f"{BASE_URL}/api/schema/")
    print(f"Status Code: {status}")
    if status == 200:
        print("Schema generated successfully. First 30 lines:")
        lines = body.splitlines()[:30]
        print("\n".join(lines))
    print("\n" + "="*40 + "\n")

    # 6. Test Throttling (Anonymous rate limit: 5 requests/minute)
    print("--- 6. PRUEBA DE THROTTLING (LÍMITE DE TASA A 5 REQ/MINUTO) ---")
    print("Making 6 rapid requests to /api/iglesias/...")
    throttled = False
    for i in range(1, 8):
        status, body, _ = make_request(f"{BASE_URL}/api/iglesias/")
        print(f" Request #{i} -> Status Code: {status}")
        if status == 429:
            print(">>> Success: 429 Too Many Requests detected!")
            print(f"Response: {body}")
            throttled = True
            break
        # Sleep very briefly to avoid overloading other things, but fast enough to trigger throttling
        time.sleep(0.1)
    if not throttled:
        print(">>> Warning: Throttling not triggered. Ensure rate limit settings are correct or request limit is low.")
    print("\n======================================================================")

if __name__ == "__main__":
    test_api()
