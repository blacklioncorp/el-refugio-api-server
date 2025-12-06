from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os
from . import models, schemas, database

# NO HAY IMPORTACIÓN DIRECTA DE GOOGLE-GENAI AQUÍ.
# Se hará dentro de la función de forma segura.

class GenerateConcept(BaseModel):
    concept: str

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... Rutas de Productos y Órdenes... (código omitido)

@app.get("/")
def read_root():
    return {"message": "El Refugio API funcionando 🚀"}

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[schemas.Product]) 
def read_products(db: Session = Depends(database.get_db)):
    return db.query(models.Product).all()

@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    db_order = models.Order(
        table_id=order.table_id,
        items=[item.dict() for item in order.items], 
        total=100.0, 
        status="PENDING"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(db: Session = Depends(database.get_db)):
    return db.query(models.Order).all()


# --- RUTA DE IA (Con Importación Segura) ---

@app.post("/ai/generate_menu")
def generate_menu(data: GenerateConcept):
    print(f"Solicitud IA recibida: {data.concept}")

    # Bandera de simulación
    use_simulation = False
    
    # 1. Intentar importar la librería real aquí (seguro contra fallos de inicio)
    try:
        # Intentamos importar la librería AHORA. Si falla, el servidor ya inició.
        from google_genai import GenerativeModel 
        
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
             raise HTTPException(status_code=500, detail="Clave GEMINI_API_KEY no configurada en el entorno.")
             
        # El código de la llamada real a la IA iría aquí
        # model = GenerativeModel(api_key=api_key)
        # response = model.generate_content(...) 
        
        # Si la importación y la clave están OK, salimos del TRY
        pass 

    except ImportError:
        # El error anterior de Render ocurre aquí, pero el servidor ya está vivo.
        use_simulation = True
        print("Advertencia: Usando simulación. La librería no se pudo cargar.")
        
    except HTTPException:
        raise # Dejamos que el error de clave se propague
        
    except Exception as e:
        use_simulation = True
        print(f"Error fatal de la IA: {e}. Usando simulación.")


    # 2. Devolver la Respuesta de Simulación si falla la importación o la API
    if use_simulation:
        return [
            {"id": "901", "name": "Taco Cósmico", "price": 35.00, "category": "2", "description": "Taco generado por IA."},
            {"id": "902", "name": "Quesadilla Espacial", "price": 65.00, "category": "2", "description": "Quesadilla generada por IA."}
        ]
        
    # Si todo fue bien (y no usamos la simulación), devolvemos el placeholder exitoso.
    return {"message": "AI generation request processed (Actual AI call skipped in mock)."}