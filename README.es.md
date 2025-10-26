# Adaptador de Autopartes para Amazon 🚗

Una aplicación web FastAPI que convierte archivos CSV de autopartes estilo AutoZone al formato de carga de Amazon para listar productos en Amazon.com.

## Características

- 🚀 **Rápido y Moderno**: Construido con FastAPI para alto rendimiento
- 📊 **Análisis CSV Flexible**: Detecta y mapea automáticamente varios formatos de columnas
- 🎨 **Interfaz Web Hermosa**: Carga de archivos con arrastrar y soltar con progreso en tiempo real
- 🔄 **Transformación Inteligente de Datos**: Convierte datos de autopartes al formato requerido de Amazon
- 📦 **Listo para Cargar**: Genera archivos CSV compatibles con Amazon
- 🏷️ **Optimizado para Autopartes**: Maneja datos de compatibilidad (Año, Marca, Modelo)

## Inicio Rápido

### Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/ALIO-IT/amazon-adapter.git
cd amazon-adapter
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

### Ejecutar la Aplicación

Iniciar el servidor:
```bash
python main.py
```

O usando uvicorn directamente:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Abra su navegador y navegue a: `http://localhost:8000`

## 📖 Documentación en Otros Idiomas

- [English](README.md) - Documentación en inglés
- [Español](README.es.md) - Estás aquí
- [Português](README.pt.md) - Documentação em português

## Ejemplo Completo: De CSV AutoZone a Amazon

Aquí hay un recorrido completo que muestra el proceso de transformación:

### Paso 1: Sus Datos de Origen (Formato AutoZone)

Tiene `mi_inventario.csv`:
```csv
Part Number,Description,Brand,Price,Quantity,Category,UPC,Weight,Length,Width,Height,Year,Make,Model,Condition
BRK-001,Brake Pad Set - Ceramic Front,AutoZone,45.99,25,Brakes,012345678901,3.5,10,8,2,2020,Toyota,Camry,New
FLT-234,Engine Air Filter,K&N,24.99,50,Filters,012345678902,0.8,12,9,3,2018,Honda,Civic,New
BAT-123,Automotive Battery 800 CCA,DieHard,149.99,15,Batteries,012345678905,45.2,12,7,9,,,Any,New
```

### Paso 2: Ejecutar el Convertidor

**Opción A: Usando la Interfaz Web**
```
1. Ir a http://localhost:8000
2. Arrastrar y soltar mi_inventario.csv
3. Hacer clic en "Convert to Amazon Format"
4. Descargar: amazon_auto_parts_20251026_143022.csv
```

**Opción B: Usando la API**
```bash
curl -X POST "http://localhost:8000/convert" \
  -F "file=@mi_inventario.csv" \
  -o resultado.json

# Respuesta:
# {
#   "message": "File converted successfully",
#   "output_file": "amazon_auto_parts_20251026_143022.csv",
#   "rows_processed": 3,
#   "rows_output": 3
# }
```

### Paso 3: Su Salida Lista para Amazon

El convertidor genera `amazon_auto_parts_20251026_143022.csv`:

```csv
product-id,product-id-type,item-name,brand-name,manufacturer,product-description,item-type,standard-price,list-price,quantity,product-tax-code,condition-type,part-number,item-weight,item-length,item-width,item-height,fulfillment-channel,fitment-year,fitment-make,fitment-model
012345678901,UPC,AutoZone - BRK-001 - Brake Pad Set - Ceramic Front,AutoZone,AutoZone,"Brake Pad Set - Ceramic Front. Brand: AutoZone. Part Number: BRK-001. Category: Brakes. Fits: 2020 Toyota Camry",Brakes,45.99,55.19,25,A_GEN_TAX,New,BRK-001,3.5,10,8,2,DEFAULT,2020,Toyota,Camry
```

### Paso 4: Cargar a Amazon

1. Iniciar sesión en Amazon Seller Central
2. Ir a **Inventario** → **Agregar Productos mediante Carga**
3. Seleccionar plantilla de categoría **Autopartes**
4. Cargar `amazon_auto_parts_20251026_143022.csv`
5. ¡Amazon procesa sus 3 productos instantáneamente!

### ¿Qué Cambió? (Comparación Detallada)

| Campo | Antes (AutoZone) | Después (Amazon) | Transformación |
|-------|------------------|------------------|----------------|
| **ID** | Part Number: BRK-001 | product-id: 012345678901 | Usó UPC como ID principal |
| **Tipo de ID** | N/A | product-id-type: UPC | Detectó presencia de UPC automáticamente |
| **Título** | Description: Brake Pad Set... | item-name: AutoZone - BRK-001 - Brake Pad Set... | Combinó Marca + SKU + Descripción |
| **Precio** | Price: 45.99 | standard-price: 45.99 | Mapeo directo |
| **Precio de Lista** | N/A | list-price: 55.19 | Calculado automáticamente (120% del precio) |
| **Descripción** | Description: Brake Pad Set... | product-description: Brake Pad Set...(detallada) | Mejorada con categoría, compatibilidad |
| **Compatibilidad** | Year/Make/Model en columnas separadas | fitment-year, fitment-make, fitment-model | Extraído y formateado |
| **Impuestos** | N/A | product-tax-code: A_GEN_TAX | Código estándar asignado automáticamente |

### Rendimiento

- **Tiempo de Procesamiento:** < 1 segundo para 100 productos
- **Procesamiento Masivo:** Probado con más de 10,000 productos
- **Eficiente en Memoria:** Procesa archivos de hasta 50MB

## Uso

### Interfaz Web

1. Abrir la interfaz web en `http://localhost:8000`
2. Arrastrar y soltar su archivo CSV o hacer clic para navegar
3. Hacer clic en "Convert to Amazon Format"
4. Descargar el archivo CSV listo para Amazon

**Flujo de Trabajo de Ejemplo:**
```
1. Navegar a http://localhost:8000
2. Soltar su archivo "inventario_autozone.csv" en el área de carga
3. Hacer clic en "Convert to Amazon Format"
4. Sistema procesa: "✅ Success! Processed 150 rows"
5. Hacer clic en "Download Amazon CSV"
6. Cargar el archivo descargado en Amazon Seller Central
```

### Endpoints de la API

Para documentación detallada de la API, ejemplos de código y casos de uso, consulte la [versión completa en inglés](README.md#api-endpoints).

## Formato CSV de Entrada

La aplicación admite formatos CSV flexibles. Detectará y mapeará automáticamente nombres de columnas comunes:

### Nombres de Columnas Soportados

| Tipo de Dato | Nombres de Columna Aceptados |
|--------------|------------------------------|
| **Número de Parte** | part number, part_number, sku, item number, part#, product_id |
| **Descripción** | description, title, product name, name, item description |
| **Marca** | brand, manufacturer, make, mfr, vendor |
| **Precio** | price, unit price, cost, msrp, retail_price |
| **Cantidad** | quantity, qty, stock, inventory, available |
| **Categoría** | category, type, product_type, classification |
| **UPC** | upc, barcode, ean, gtin |
| **Peso** | weight, item_weight, shipping_weight |
| **Dimensiones** | length, width, height (con variaciones) |
| **Compatibilidad de Vehículo** | year, make, model (con variaciones) |
| **Condición** | condition, item_condition |

## Cumplimiento con la API de Amazon

✅ **Este adaptador cumple completamente con las especificaciones de carga de productos de Amazon Seller Central.**

**Importante**: Este adaptador está diseñado para **Amazon Seller Central** (productos minoristas físicos), NO para AWS Marketplace (software/SaaS).

Para información detallada sobre cumplimiento, consulte:
- [AMAZON_COMPLIANCE.es.md](AMAZON_COMPLIANCE.es.md) - Documentación de cumplimiento en español
- [AWS_MARKETPLACE_NOTE.es.md](AWS_MARKETPLACE_NOTE.es.md) - Nota sobre diferencias de APIs

### Resumen Rápido de Cumplimiento

| Requisito | Estado | Implementación |
|-----------|--------|----------------|
| Campos Requeridos | ✅ Todos proporcionados | product-id, product-id-type, item-name, brand-name, standard-price, quantity, condition-type |
| Tipos de ID de Producto | ✅ Cumple | UPC (12 dígitos), EAN (13 dígitos), SKU (alfanumérico) |
| Límites de Caracteres | ✅ Aplicados | Título: 200 caracteres, Descripción: 2000 caracteres |
| Formato de Precio | ✅ Validado | Solo numérico, 2 decimales, sin símbolos de moneda |
| Valores de Condición | ✅ Estandarizados | New, Used, Refurbished (valores de Amazon) |
| Codificación UTF-8 | ✅ Requerida | Todos los archivos generados en UTF-8 |
| Campos de Autopartes | ✅ Soportados | Datos de compatibilidad (año, marca, modelo) |
| Códigos de Impuestos | ✅ Incluidos | A_GEN_TAX para bienes gravables generales |

## Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **Pandas**: Manipulación de datos y procesamiento CSV
- **Uvicorn**: Servidor ASGI
- **Python 3.8+**: Lenguaje de programación

## Casos de Uso del Mundo Real

### Caso de Uso 1: Carga Masiva de Inventario de Autopartes

**Escenario:** Tiene 500 pastillas de freno de varios fabricantes en su CSV formato AutoZone.

**Pasos:**
1. Exportar inventario de su sistema POS/ERP a CSV
2. Cargar en la interfaz web del adaptador
3. Descargar el archivo formateado para Amazon
4. Cargar en Amazon Seller Central → Inventario → Agregar Productos mediante Carga

**Tiempo Ahorrado:** La entrada manual tomaría ~8 horas. Con el adaptador: 2 minutos.

### Caso de Uso 5: Actualización de Listados Existentes en Amazon

**Escenario:** Necesita actualizar precios, cantidades o descripciones para productos ya listados en Amazon.

**Cómo Funciona:**  
Cuando Amazon recibe un CSV con un `product-id` que coincide con un listado existente, **actualiza** el artículo en lugar de crear uno nuevo.

Para documentación completa de casos de uso, scripts y ejemplos, consulte la [versión en inglés](README.md#real-world-use-cases).

## Solución de Problemas

### Problemas Comunes y Soluciones

#### Problema 1: "Only CSV files are accepted"
**Problema:** El archivo cargado no se reconoce como CSV.
**Solución:**
- Asegurar que el archivo tenga extensión `.csv`
- Exportar desde Excel como formato "CSV UTF-8"
- Verificar que el archivo no esté corrupto

#### Problema 2: Datos faltantes o incorrectos en la salida
**Problema:** Algunos campos están vacíos o tienen valores incorrectos.
**Solución:**
```python
# Verificar que los nombres de columna coincidan con los formatos soportados
# Editar adapter/csv_parser.py para agregar mapeos personalizados

self.column_mappings = {
    'part_number': ['part number', 'sku', 'SU_COLUMNA_PERSONALIZADA'],
    # Agregar sus nombres de columna personalizados aquí
}
```

## Desarrollo

### Ejecutar Pruebas

El proyecto incluye un script de prueba completo:

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar script de prueba
python test_conversion.py
```

## Estructura del Proyecto

```
amazon-adapter/
├── main.py                 # Aplicación FastAPI
├── adapter/
│   ├── __init__.py
│   ├── csv_parser.py       # Lógica de análisis CSV
│   └── amazon_transformer.py  # Transformación al formato Amazon
├── uploads/                # Directorio de carga temporal
├── outputs/                # Archivos CSV de Amazon generados
├── requirements.txt        # Dependencias de Python
├── sample_autozone.csv     # Archivo de muestra
├── README.md              # Documentación en inglés
├── README.es.md           # Documentación en español (este archivo)
└── README.pt.md           # Documentação em português
```

## Licencia

Licencia MIT

## Contribuir

¡Las contribuciones son bienvenidas! Por favor, siéntase libre de enviar un Pull Request.

## Soporte

Para problemas o preguntas, por favor abra un issue en GitHub.

---

**Nota:** Para la documentación completa con todos los ejemplos de código, casos de uso detallados, y scripts de automatización, consulte la [versión en inglés](README.md).
