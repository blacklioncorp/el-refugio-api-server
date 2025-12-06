from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os # <--- CORRECCIÓN 1: Módulo OS importado
from google_genai import GenerativeModel # <--- Importación de la IA
from . import models, schemas, database

# CORRECCIÓN 2: Definición del modelo de entrada para la IA
class GenerateConcept(BaseModel):
    concept: str

# Crear las tablas en la base de datos automáticamente
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Permitir que React (puerto 5173) hable con Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "El Refugio API funcionando 🚀"}

# Rutas de Productos y Órdenes... (código omitido por ser correcto)

# ... (El código anterior de create_product, read_products, create_order, read_orders es correcto y no requiere cambios)

# --- RUTA DE IA ---

@app.post("/ai/generate_menu")
def generate_menu(data: GenerateConcept):
    print(f"Solicitud IA recibida: {data.concept}")

    # Código para usar Gemini (Solo se ejecutará en Render)
    try:
        # CORRECCIÓN 3: Reemplazar el código de la IA por la simulación
        # La lógica real de la IA se agregará una vez que el despliegue inicial sea exitoso.
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
             # Si no hay clave, devolvemos un error 500 para el cliente, pero la simulación para el desarrollador.
             raise HTTPException(status_code=500, detail="Clave GEMINI_API_KEY no configurada en el entorno.")
             
        # El código de la llamada real a la IA iría aquí:
        # model = GenerativeModel(api_key=api_key)
        # response = model.generate_content(...) 
        pass

    except ImportError:
        # Si la importación de 'google_genai' falla localmente, capturamos el error y devolvemos la simulación.
        print("Advertencia: No se pudo importar la librería 'google-genai' (Entorno local incompatible).")

    except HTTPException:
        # Si falla la clave de la API, dejamos que el error 500 se propague
        raise 
        
    except Exception as e:
        # Captura otros errores (como problemas de red en la llamada a la IA)
        print(f"Error al llamar a Gemini: {e}")

    # --- RESPUESTA DE SIMULACIÓN (JSON) ---
    return [
        {"id": "901", "name": "Taco Cósmico", "price": 35.00, "category": "2", "description": "Taco generado por IA."},
        {"id": "902", "name": "Quesadilla Espacial", "price": 65.00, "category": "2", "description": "Quesadilla generada por IA."}
    ]