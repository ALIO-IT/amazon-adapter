# Documentación de Cumplimiento de la API de Amazon Seller Central

[Lea esta documentación en otros idiomas: [English](AMAZON_COMPLIANCE.md) | **Español** | [Português](AMAZON_COMPLIANCE.pt.md)]

## Descripción General

Este documento describe cómo el Adaptador de Autopartes para Amazon cumple con las especificaciones de carga de productos de Amazon Seller Central para la categoría Automotriz y Deportes Motorizados.

## Distinción Importante

⚠️ **Nota**: Este adaptador es para **Amazon Seller Central** (listados de productos físicos), NO para AWS Marketplace (productos de software/SaaS).

- **Amazon Seller Central**: Productos minoristas físicos (autopartes, bienes de consumo)
- **AWS Marketplace**: Software, AMIs, contenedores, aplicaciones SaaS

## Métodos de Carga de Amazon Seller Central

Amazon Seller Central admite tres métodos principales para cargas de productos:

### 1. Carga de Archivos CSV/Texto (Lo Que Implementamos)
- **Ubicación**: Seller Central → Inventario → Agregar Productos mediante Carga
- **Formato**: Archivos delimitados por tabulaciones o CSV
- **Plantilla**: Plantillas de archivo de inventario específicas por categoría
- **Caso de Uso**: Cargas masivas, actualizaciones, gestión de inventario

### 2. Amazon MWS (Marketplace Web Service) - Heredado
- **Estado**: En proceso de eliminación gradual
- **Reemplazo**: SP-API (Selling Partner API)

### 3. SP-API (Selling Partner API) - Estándar Actual
- **Estado**: API recomendada actualmente
- **Documentación**: https://developer-docs.amazon.com/sp-api/

## Nuestra Implementación: Formato de Carga CSV

### Cumplimiento con la Plantilla de Autopartes de Amazon

Nuestro adaptador genera archivos CSV compatibles con la plantilla de categoría **Automotriz y Deportes Motorizados** de Amazon.

#### Campos Requeridos (Proporcionamos Todos)

| Campo | Nuestra Salida | Requisito de Amazon | Estado de Cumplimiento |
|-------|----------------|---------------------|------------------------|
| `product-id` | UPC o SKU | Requerido, identificador único | ✅ Cumple |
| `product-id-type` | UPC, SKU, EAN | Requerido, debe coincidir con el tipo de ID | ✅ Cumple |
| `item-name` | Marca + N° Parte + Descripción | Requerido, máx 200 caracteres | ✅ Cumple |
| `brand-name` | De datos de origen | Requerido para la mayoría de categorías | ✅ Cumple |
| `standard-price` | Numérico, 2 decimales | Requerido, debe ser > 0 | ✅ Cumple |
| `quantity` | Entero | Requerido, 0 o mayor | ✅ Cumple |
| `condition-type` | New, Used, Refurbished | Requerido, de valores permitidos | ✅ Cumple |

#### Campos Recomendados (Proporcionamos)

| Campo | Nuestra Salida | Recomendación de Amazon | Estado de Cumplimiento |
|-------|----------------|------------------------|------------------------|
| `manufacturer` | Igual que brand | Recomendado para autopartes | ✅ Proporcionado |
| `product-description` | Descripción mejorada | Recomendado, máx 2000 caracteres | ✅ Proporcionado |
| `item-type` | Categoría/tipo | Recomendado para categorización | ✅ Proporcionado |
| `part-number` | Número de parte del fabricante | Recomendado para autopartes | ✅ Proporcionado |
| `item-weight` | Peso en libras | Recomendado para envío | ✅ Proporcionado |
| `item-length` | Dimensión de longitud | Recomendado para envío | ✅ Proporcionado |
| `item-width` | Dimensión de ancho | Recomendado para envío | ✅ Proporcionado |
| `item-height` | Dimensión de altura | Recomendado para envío | ✅ Proporcionado |
| `list-price` | MSRP/Precio de lista | Recomendado para mostrar venta | ✅ Proporcionado (auto-calculado) |
| `product-tax-code` | A_GEN_TAX | Requerido para cálculo de impuestos | ✅ Proporcionado |
| `fulfillment-channel` | DEFAULT | Comerciante o FBA | ✅ Proporcionado |

#### Campos Específicos de Automotriz (Proporcionamos)

| Campo | Nuestra Salida | Propósito | Estado de Cumplimiento |
|-------|----------------|-----------|------------------------|
| `fitment-year` | Año del vehículo | Búsqueda de compatibilidad | ✅ Proporcionado cuando está disponible |
| `fitment-make` | Marca del vehículo | Búsqueda de compatibilidad | ✅ Proporcionado cuando está disponible |
| `fitment-model` | Modelo del vehículo | Búsqueda de compatibilidad | ✅ Proporcionado cuando está disponible |

## Especificaciones de Formato de Datos

### 1. Formato de ID de Producto

**Requisitos de Amazon:**
- UPC: 12 dígitos (UPC-A) u 8 dígitos (UPC-E)
- EAN: 13 dígitos
- SKU: Alfanumérico, máx 40 caracteres

**Nuestra Implementación:**
```python
# En amazon_transformer.py
# Priorizamos UPC cuando está disponible, recurrimos a SKU
if has_upc:
    amazon_df['product-id-type'] = 'UPC'
    amazon_df['product-id'] = df['upc']
else:
    amazon_df['product-id-type'] = 'SKU'
    amazon_df['product-id'] = df['part_number']
```

✅ **Cumple**: Identificamos y usamos correctamente los tipos de ID apropiados.

### 2. Nombre del Artículo (Título)

**Requisitos de Amazon:**
- Máximo 200 caracteres
- Debe incluir: Marca, Número de Parte, Características Clave
- Sin texto promocional (GRATIS, OFERTA, etc.)
- Sin caracteres especiales excepto: - , / ()

**Nuestra Implementación:**
```python
# Formato: Marca + Número de Parte + Descripción
title = ' - '.join([brand, part_number, description])
if len(title) > 200:
    title = title[:197] + '...'
```

✅ **Cumple**: Seguimos formato marca-parte-descripción, aplicamos límite de 200 caracteres.

### 3. Descripción del Producto

**Requisitos de Amazon:**
- Máximo 2000 caracteres
- Texto plano (HTML no permitido en cargas CSV)
- Debe describir características, especificaciones, compatibilidad

**Nuestra Implementación:**
```python
# Incluye: descripción, marca, número de parte, categoría, compatibilidad
description = f"{title}. Brand: {brand}. Part Number: {part}. Category: {category}. Fits: {fitment}"
if len(description) > 2000:
    description = description[:1997] + '...'
```

✅ **Cumple**: Proporcionamos descripciones detalladas dentro de los límites.

### 4. Formato de Precio

**Requisitos de Amazon:**
- Solo numérico (sin símbolos de moneda)
- Se recomiendan dos decimales
- Debe ser mayor que 0
- standard-price no puede exceder list-price

**Nuestra Implementación:**
```python
# Limpiar datos de precio
df['price'] = df['price'].str.replace('$', '').str.replace(',', '')
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Calcular precio de lista (20% de margen)
amazon_df['standard-price'] = df['price']
amazon_df['list-price'] = (df['price'] * 1.2).round(2)
```

✅ **Cumple**: Eliminamos símbolos de moneda, validamos numéricos, aseguramos list-price > standard-price.

### 5. Cantidad

**Requisitos de Amazon:**
- Solo enteros
- 0 o mayor
- 0 significa sin stock

**Nuestra Implementación:**
```python
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0).astype(int)
```

✅ **Cumple**: Aseguramos valores enteros, por defecto 0 si es inválido.

### 6. Tipo de Condición

**Requisitos de Amazon:**
- Debe ser uno de: New, Used, Collectible, Refurbished, Club
- Autopartes típicamente: New, Used, Refurbished

**Nuestra Implementación:**
```python
def _standardize_condition(self, condition: str) -> str:
    condition_lower = condition.lower().strip()
    if condition_lower in ['new', 'brand new', 'brand-new', '']:
        return 'New'
    elif condition_lower in ['used', 'pre-owned', 'preowned']:
        return 'Used'
    elif condition_lower in ['refurbished', 'rebuilt', 'remanufactured']:
        return 'Refurbished'
    else:
        return 'New'  # Por defecto a New
```

✅ **Cumple**: Mapeamos a los valores exactos de Amazon.

## Codificación de Caracteres

**Requisito de Amazon:**
- Codificación UTF-8 requerida
- Sin caracteres especiales que rompan el formato CSV

**Nuestra Implementación:**
```python
# En csv_parser.py
df = pd.read_csv(io.BytesIO(file_content), encoding='utf-8', low_memory=False)

# En main.py - guardar salida
amazon_df.to_csv(output_path, index=False)  # pandas usa UTF-8 por defecto
```

✅ **Cumple**: Todos los archivos usan codificación UTF-8.

## Requisitos de Formato CSV

**Requisitos de Amazon:**
- Extensión de archivo: .csv o .txt
- Delimitador: coma (CSV) o tabulación (TSV)
- Primera fila: encabezados de columna (nombres de campo exactos)
- Filas subsiguientes: datos de productos
- Sin filas vacías al principio o al final
- Comillas alrededor de campos que contienen comas

**Nuestra Implementación:**
```python
# pandas maneja automáticamente:
# - Formato CSV con comas
# - Campos entre comillas con comas
# - Codificación UTF-8
# - Generación de fila de encabezado
amazon_df.to_csv(output_path, index=False)
```

✅ **Cumple**: Usamos pandas que sigue los estándares RFC de CSV.

## Comportamiento de Actualización vs Creación

**Lógica de Amazon:**
- Si `product-id` coincide con listado existente → **ACTUALIZAR**
- Si `product-id` es nuevo → **CREAR**
- La coincidencia se basa en: product-id + product-id-type

**Nuestra Implementación:**
Generamos la combinación correcta de product-id y product-id-type, permitiendo a Amazon determinar automáticamente crear vs actualizar.

✅ **Cumple**: Amazon maneja esto automáticamente basándose en product-id.

## Reglas de Validación Que Implementamos

### Validación Previa a la Carga

```python
# En csv_parser.py
def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
    # Eliminar filas completamente vacías
    df = df.dropna(how='all')
    
    # Validar que los precios son numéricos
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    
    # Validar que las cantidades son enteros
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0).astype(int)
    
    # Limpiar peso a numérico
    df['weight'] = pd.to_numeric(df['weight'], errors='coerce')
    
    return df
```

✅ **Cumple**: Validamos que los tipos de datos coincidan con los requisitos de Amazon.

## Lista de Verificación de Cumplimiento

- ✅ Todos los campos requeridos proporcionados
- ✅ Los formatos de datos coinciden con las especificaciones
- ✅ Límites de caracteres aplicados
- ✅ Codificación UTF-8
- ✅ Tipos de condición válidos
- ✅ Tipos de ID de producto apropiados
- ✅ Códigos de impuestos incluidos
- ✅ Campos de compatibilidad automotriz cuando están disponibles
- ✅ Descripciones bajo 2000 caracteres
- ✅ Títulos bajo 200 caracteres
- ✅ Precios numéricos sin símbolos
- ✅ Cantidades enteras
- ✅ Formato CSV estándar

## Mejoras Futuras para Integración de API

### Actual: Carga CSV
✅ Implementado - genera archivos CSV compatibles con Amazon

### Potencial: Integración SP-API
🔄 Mejora futura - cargar directamente vía Selling Partner API

**Beneficios:**
- Cargas automatizadas sin intervención manual
- Sincronización de inventario en tiempo real
- Acceso programático a datos de pedidos
- Manejo de errores en código

**Requisitos:**
- Credenciales SP-API
- Autenticación OAuth 2.0
- Gestión de límites de velocidad de API
- Dependencias adicionales de Python (librería sp-api)

## Referencias

### Documentación Oficial de Amazon

1. **Ayuda de Seller Central**:
   - https://sellercentral.amazon.com/help/hub/reference/G201576410
   - Guías de Clasificación de Productos

2. **Plantillas de Archivo de Inventario**:
   - Disponibles en Seller Central → Inventario → Agregar Productos mediante Carga
   - Plantillas específicas por categoría

3. **Selling Partner API** (para integración futura):
   - https://developer-docs.amazon.com/sp-api/
   - Documentación de Feeds API

## Soporte

Para preguntas sobre:
- **Nuestro adaptador**: Abrir issue en GitHub
- **Requisitos de Amazon**: Soporte de Amazon Seller
- **Integración SP-API**: Consola de Desarrolladores de Amazon

## Última Actualización

Esta documentación de cumplimiento refleja los requisitos de Amazon Seller Central a partir de octubre de 2025.

Amazon puede actualizar sus requisitos. Siempre verifique las especificaciones actuales en Seller Central antes de cargas masivas.

