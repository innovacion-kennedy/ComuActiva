import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]

GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0/me/drive/root:/Documentos/Requisitos"


def subir_a_onedrive(nombre_archivo, contenido_archivo):
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )

    result = app.acquire_token_for_client(scopes=SCOPE)

    if "access_token" in result:
        print("🔐 Token adquirido correctamente.")
        headers = {
            "Authorization": f"Bearer {result['access_token']}",
            "Content-Type": "application/octet-stream"
        }

        upload_url = f"{GRAPH_API_ENDPOINT}/{nombre_archivo}:/content"
        print(f"📤 Subiendo archivo a URL: {upload_url}")

        response = requests.put(upload_url, headers=headers, data=contenido_archivo)
        print("🧾 Resultado:", response.status_code, response.text)

        if response.status_code in [200, 201]:
            return True, "✅ Archivo subido correctamente a OneDrive."
        else:
            return False, f"❌ Error al subir archivo: {response.status_code} - {response.text}"
    else:
        print("❌ Error al obtener el token:", result)
        return False, "❌ No se pudo obtener el token de acceso."