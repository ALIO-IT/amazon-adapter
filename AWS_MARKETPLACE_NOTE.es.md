# Nota Sobre la Documentación de la API de AWS Marketplace

[Lea esta nota en otros idiomas: [English](AWS_MARKETPLACE_NOTE.md) | **Español** | [Português](AWS_MARKETPLACE_NOTE.pt.md)]

## ⚠️ Aclaración Importante

El archivo PDF `marketplace-api.pdf` en este directorio es documentación para **AWS Marketplace API**, que **NO** es la API correcta para este proyecto.

## Dos Sistemas Amazon Diferentes

### 1. Amazon Seller Central (Lo Que Usa Este Proyecto) ✅

**Propósito**: Vender productos físicos en el mercado minorista de Amazon.com

**Tipos de Productos**:
- Autopartes (nuestro enfoque)
- Electrónica de consumo
- Ropa
- Libros
- Artículos para el hogar
- Cualquier producto físico vendido en Amazon

**Métodos de Carga**:
- Carga de archivo CSV/Texto vía interfaz web de Seller Central
- Selling Partner API (SP-API) para acceso programático

**Lo Que Implementamos**:
- ✅ Generación de archivos CSV para carga en Seller Central
- ✅ Formato de categoría de Autopartes
- ✅ Formato de gestión de inventario

**Ubicación de Documentación**:
- Ayuda de Amazon Seller Central: https://sellercentral.amazon.com/help
- Documentos SP-API: https://developer-docs.amazon.com/sp-api/

**Acceso**:
- Requiere: Cuenta de Amazon Seller
- Inicio de sesión: sellercentral.amazon.com

---

### 2. AWS Marketplace (El PDF Que Tiene) ❌

**Propósito**: Vender productos de software y SaaS en AWS Marketplace

**Tipos de Productos**:
- Amazon Machine Images (AMIs)
- Productos en contenedores
- Aplicaciones SaaS
- Modelos de machine learning
- Productos de datos
- Productos de servidor

**Métodos de Carga**:
- AWS Marketplace Catalog API
- Consola de Gestión
- Llamadas de API con credenciales AWS IAM

**Lo Que NO Cubre**:
- ❌ Listados de productos físicos
- ❌ Autopartes
- ❌ Productos minoristas de consumo
- ❌ Mercado de Amazon.com

**Documentación**:
- AWS Marketplace: https://aws.amazon.com/marketplace/
- Referencia de API: El archivo PDF en este directorio

**Acceso**:
- Requiere: Cuenta AWS con registro de vendedor en marketplace
- Diferente de Amazon Seller Central

## ¿Por Qué la Confusión?

Ambos servicios son de Amazon pero sirven propósitos completamente diferentes:

| Característica | Amazon Seller Central | AWS Marketplace |
|----------------|----------------------|-----------------|
| **Plataforma** | Amazon.com minorista | Plataforma AWS Cloud |
| **Productos** | Bienes físicos | Software/SaaS |
| **Clientes** | Consumidores minoristas | Usuarios de AWS cloud |
| **Formato de Carga** | Archivos CSV | Llamadas API (JSON) |
| **Nuestro Proyecto** | ✅ SÍ - Esto es lo que apuntamos | ❌ NO - Sistema incorrecto |
| **Ejemplo** | Pastillas de freno, filtros, baterías | AMI WordPress, SaaS de monitoreo |
| **Precios** | Precios fijos por artículo | Facturación basada en uso |
| **Cumplimiento** | Enviar artículos físicos | Desplegar software |

## Lo Que Hace Nuestro Adaptador

```
Su CSV de Inventario (formato AutoZone)
          ↓
    Nuestro Adaptador
          ↓
CSV de Amazon Seller Central (formato compatible)
          ↓
Cargar en el Sitio Web de Amazon Seller Central
          ↓
Productos Listados en Amazon.com
```

## Lo Que Hace la API de AWS Marketplace (No Nosotros)

```
Paquete de Software/AMI
          ↓
API de Catálogo de AWS Marketplace
          ↓
Listar en AWS Marketplace
          ↓
Clientes AWS Despliegan en Su Infraestructura
```

## Documentación Correcta para Este Proyecto

### Carga CSV de Amazon Seller Central

**Qué referenciar**: Plantillas específicas por categoría de Amazon Seller Central

**Cómo acceder**:
1. Iniciar sesión en sellercentral.amazon.com
2. Ir a: **Inventario** → **Agregar Productos mediante Carga**
3. Hacer clic: **Descargar una Plantilla de Archivo de Inventario**
4. Seleccionar: **Automotriz y Deportes Motorizados**
5. Descargar la plantilla para ver los campos requeridos

**Secciones clave**:
- Campos requeridos (product-id, title, price, etc.)
- Campos específicos de automotriz (datos de compatibilidad)
- Valores válidos (tipos de condición, códigos de impuestos)
- Límites de caracteres
- Formatos de datos

### Nuestro Cumplimiento

Consulte [AMAZON_COMPLIANCE.es.md](AMAZON_COMPLIANCE.es.md) para documentación detallada de cómo nuestro adaptador cumple con los requisitos de Amazon Seller Central.

## Si Desea Integrar con SP-API (Futuro)

Si desea cargar productos programáticamente en lugar de usar archivos CSV:

**Selling Partner API (SP-API)**:
- Documentación: https://developer-docs.amazon.com/sp-api/
- Qué hace: Acceso programático a funciones de Seller Central
- Características: Cargas de productos, sincronización de inventario, gestión de pedidos
- Autenticación: OAuth 2.0 + AWS Signature V4
- Formato: JSON (no XML/JSON como AWS Marketplace)

**Esto sería una mejora futura** para llamar directamente a las APIs de Amazon en lugar de generar archivos CSV.

## Resumen

✅ **Usar para nuestro proyecto**: Documentación de Amazon Seller Central
❌ **No usar**: API de AWS Marketplace (el PDF que tiene)

La documentación de la API de AWS Marketplace es útil si está vendiendo:
- Software como Servicio (SaaS)
- Amazon Machine Images
- Aplicaciones en contenedores
- Modelos de ML

Pero como estamos vendiendo **autopartes físicas**, necesitamos la documentación de **Amazon Seller Central** en su lugar.

## ¿Necesita Ayuda?

- **Ayuda de Seller Central**: https://sellercentral.amazon.com/help
- **Documentación SP-API**: https://developer-docs.amazon.com/sp-api/
- **Nuestros Documentos de Cumplimiento**: [AMAZON_COMPLIANCE.es.md](AMAZON_COMPLIANCE.es.md)
- **Plantilla de Autopartes**: Descargar desde Seller Central (vea los pasos anteriores)

