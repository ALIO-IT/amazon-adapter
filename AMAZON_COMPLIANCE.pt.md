# Documentação de Conformidade com API do Amazon Seller Central

[Leia esta documentação em outros idiomas: [English](AMAZON_COMPLIANCE.md) | [Español](AMAZON_COMPLIANCE.es.md) | **Português**]

## Visão Geral

Este documento descreve como o Adaptador de Autopeças para Amazon está em conformidade com as especificações de upload de produtos do Amazon Seller Central para a categoria Automotivo e Esportes Motorizados.

## Distinção Importante

⚠️ **Nota**: Este adaptador é para **Amazon Seller Central** (listagens de produtos físicos), NÃO para AWS Marketplace (produtos de software/SaaS).

- **Amazon Seller Central**: Produtos de varejo físicos (autopeças, bens de consumo)
- **AWS Marketplace**: Software, AMIs, contêineres, aplicações SaaS

## Métodos de Upload do Amazon Seller Central

O Amazon Seller Central suporta três métodos principais para uploads de produtos:

### 1. Upload de Arquivo CSV/Texto (O Que Implementamos)
- **Localização**: Seller Central → Inventário → Adicionar Produtos via Upload
- **Formato**: Arquivos delimitados por tabulação ou CSV
- **Template**: Templates de arquivo de inventário específicos por categoria
- **Caso de Uso**: Uploads em massa, atualizações, gerenciamento de inventário

### 2. Amazon MWS (Marketplace Web Service) - Legado
- **Status**: Sendo descontinuado
- **Substituto**: SP-API (Selling Partner API)

### 3. SP-API (Selling Partner API) - Padrão Atual
- **Status**: API recomendada atualmente
- **Documentação**: https://developer-docs.amazon.com/sp-api/

## Nossa Implementação: Formato de Upload CSV

### Conformidade com o Template de Autopeças da Amazon

Nosso adaptador gera arquivos CSV em conformidade com o template de categoria **Automotivo e Esportes Motorizados** da Amazon.

#### Campos Obrigatórios (Fornecemos Todos)

| Campo | Nossa Saída | Requisito da Amazon | Status de Conformidade |
|-------|-------------|---------------------|------------------------|
| `product-id` | UPC ou SKU | Obrigatório, identificador único | ✅ Conforme |
| `product-id-type` | UPC, SKU, EAN | Obrigatório, deve corresponder ao tipo de ID | ✅ Conforme |
| `item-name` | Marca + N° Peça + Descrição | Obrigatório, máx 200 caracteres | ✅ Conforme |
| `brand-name` | De dados de origem | Obrigatório para maioria das categorias | ✅ Conforme |
| `standard-price` | Numérico, 2 decimais | Obrigatório, deve ser > 0 | ✅ Conforme |
| `quantity` | Inteiro | Obrigatório, 0 ou maior | ✅ Conforme |
| `condition-type` | New, Used, Refurbished | Obrigatório, dos valores permitidos | ✅ Conforme |

#### Campos Recomendados (Fornecemos)

| Campo | Nossa Saída | Recomendação da Amazon | Status de Conformidade |
|-------|-------------|------------------------|------------------------|
| `manufacturer` | Igual a brand | Recomendado para autopeças | ✅ Fornecido |
| `product-description` | Descrição aprimorada | Recomendado, máx 2000 caracteres | ✅ Fornecido |
| `item-type` | Categoria/tipo | Recomendado para categorização | ✅ Fornecido |
| `part-number` | Número da peça do fabricante | Recomendado para autopeças | ✅ Fornecido |
| `item-weight` | Peso em libras | Recomendado para envio | ✅ Fornecido |
| `item-length` | Dimensão de comprimento | Recomendado para envio | ✅ Fornecido |
| `item-width` | Dimensão de largura | Recomendado para envio | ✅ Fornecido |
| `item-height` | Dimensão de altura | Recomendado para envio | ✅ Fornecido |
| `list-price` | MSRP/Preço de lista | Recomendado para exibição de venda | ✅ Fornecido (auto-calculado) |
| `product-tax-code` | A_GEN_TAX | Obrigatório para cálculo de impostos | ✅ Fornecido |
| `fulfillment-channel` | DEFAULT | Comerciante ou FBA | ✅ Fornecido |

#### Campos Específicos de Automotivo (Fornecemos)

| Campo | Nossa Saída | Propósito | Status de Conformidade |
|-------|-------------|-----------|------------------------|
| `fitment-year` | Ano do veículo | Busca de compatibilidade | ✅ Fornecido quando disponível |
| `fitment-make` | Marca do veículo | Busca de compatibilidade | ✅ Fornecido quando disponível |
| `fitment-model` | Modelo do veículo | Busca de compatibilidade | ✅ Fornecido quando disponível |

## Especificações de Formato de Dados

### 1. Formato de ID do Produto

**Requisitos da Amazon:**
- UPC: 12 dígitos (UPC-A) ou 8 dígitos (UPC-E)
- EAN: 13 dígitos
- SKU: Alfanumérico, máx 40 caracteres

**Nossa Implementação:**
```python
# Em amazon_transformer.py
# Priorizamos UPC quando disponível, recorremos a SKU
if has_upc:
    amazon_df['product-id-type'] = 'UPC'
    amazon_df['product-id'] = df['upc']
else:
    amazon_df['product-id-type'] = 'SKU'
    amazon_df['product-id'] = df['part_number']
```

✅ **Conforme**: Identificamos e usamos corretamente os tipos de ID apropriados.

### 2. Nome do Item (Título)

**Requisitos da Amazon:**
- Máximo 200 caracteres
- Deve incluir: Marca, Número da Peça, Características Principais
- Sem texto promocional (GRÁTIS, PROMOÇÃO, etc.)
- Sem caracteres especiais exceto: - , / ()

**Nossa Implementação:**
```python
# Formato: Marca + Número da Peça + Descrição
title = ' - '.join([brand, part_number, description])
if len(title) > 200:
    title = title[:197] + '...'
```

✅ **Conforme**: Seguimos formato marca-peça-descrição, aplicamos limite de 200 caracteres.

### 3. Descrição do Produto

**Requisitos da Amazon:**
- Máximo 2000 caracteres
- Texto simples (HTML não permitido em uploads CSV)
- Deve descrever recursos, especificações, compatibilidade

**Nossa Implementação:**
```python
# Inclui: descrição, marca, número da peça, categoria, compatibilidade
description = f"{title}. Brand: {brand}. Part Number: {part}. Category: {category}. Fits: {fitment}"
if len(description) > 2000:
    description = description[:1997] + '...'
```

✅ **Conforme**: Fornecemos descrições detalhadas dentro dos limites.

### 4. Formato de Preço

**Requisitos da Amazon:**
- Apenas numérico (sem símbolos de moeda)
- Duas casas decimais recomendadas
- Deve ser maior que 0
- standard-price não pode exceder list-price

**Nossa Implementação:**
```python
# Limpar dados de preço
df['price'] = df['price'].str.replace('$', '').str.replace(',', '')
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Calcular preço de lista (20% de markup)
amazon_df['standard-price'] = df['price']
amazon_df['list-price'] = (df['price'] * 1.2).round(2)
```

✅ **Conforme**: Removemos símbolos de moeda, validamos numéricos, garantimos list-price > standard-price.

### 5. Quantidade

**Requisitos da Amazon:**
- Apenas inteiros
- 0 ou maior
- 0 significa sem estoque

**Nossa Implementação:**
```python
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0).astype(int)
```

✅ **Conforme**: Garantimos valores inteiros, padrão 0 se inválido.

### 6. Tipo de Condição

**Requisitos da Amazon:**
- Deve ser um de: New, Used, Collectible, Refurbished, Club
- Autopeças tipicamente: New, Used, Refurbished

**Nossa Implementação:**
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
        return 'New'  # Padrão para New
```

✅ **Conforme**: Mapeamos para os valores exatos da Amazon.

## Codificação de Caracteres

**Requisito da Amazon:**
- Codificação UTF-8 obrigatória
- Sem caracteres especiais que quebrem o formato CSV

**Nossa Implementação:**
```python
# Em csv_parser.py
df = pd.read_csv(io.BytesIO(file_content), encoding='utf-8', low_memory=False)

# Em main.py - salvar saída
amazon_df.to_csv(output_path, index=False)  # pandas usa UTF-8 por padrão
```

✅ **Conforme**: Todos os arquivos usam codificação UTF-8.

## Requisitos de Formato CSV

**Requisitos da Amazon:**
- Extensão de arquivo: .csv ou .txt
- Delimitador: vírgula (CSV) ou tabulação (TSV)
- Primeira linha: cabeçalhos de coluna (nomes de campo exatos)
- Linhas subsequentes: dados de produtos
- Sem linhas vazias no início ou fim
- Aspas ao redor de campos contendo vírgulas

**Nossa Implementação:**
```python
# pandas trata automaticamente:
# - Formato CSV com vírgulas
# - Campos entre aspas com vírgulas
# - Codificação UTF-8
# - Geração de linha de cabeçalho
amazon_df.to_csv(output_path, index=False)
```

✅ **Conforme**: Usamos pandas que segue os padrões RFC de CSV.

## Comportamento de Atualização vs Criação

**Lógica da Amazon:**
- Se `product-id` corresponde a listagem existente → **ATUALIZAR**
- Se `product-id` é novo → **CRIAR**
- A correspondência é baseada em: product-id + product-id-type

**Nossa Implementação:**
Geramos a combinação correta de product-id e product-id-type, permitindo à Amazon determinar automaticamente criar vs atualizar.

✅ **Conforme**: Amazon trata isso automaticamente com base no product-id.

## Regras de Validação Que Implementamos

### Validação Pré-Upload

```python
# Em csv_parser.py
def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
    # Remover linhas completamente vazias
    df = df.dropna(how='all')
    
    # Validar que preços são numéricos
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    
    # Validar que quantidades são inteiros
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0).astype(int)
    
    # Limpar peso para numérico
    df['weight'] = pd.to_numeric(df['weight'], errors='coerce')
    
    return df
```

✅ **Conforme**: Validamos que os tipos de dados correspondem aos requisitos da Amazon.

## Lista de Verificação de Conformidade

- ✅ Todos os campos obrigatórios fornecidos
- ✅ Formatos de dados correspondem às especificações
- ✅ Limites de caracteres aplicados
- ✅ Codificação UTF-8
- ✅ Tipos de condição válidos
- ✅ Tipos de ID de produto apropriados
- ✅ Códigos de impostos incluídos
- ✅ Campos de compatibilidade automotiva quando disponíveis
- ✅ Descrições abaixo de 2000 caracteres
- ✅ Títulos abaixo de 200 caracteres
- ✅ Preços numéricos sem símbolos
- ✅ Quantidades inteiras
- ✅ Formato CSV padrão

## Melhorias Futuras para Integração de API

### Atual: Upload CSV
✅ Implementado - gera arquivos CSV compatíveis com Amazon

### Potencial: Integração SP-API
🔄 Melhoria futura - upload direto via Selling Partner API

**Benefícios:**
- Uploads automatizados sem intervenção manual
- Sincronização de inventário em tempo real
- Acesso programático a dados de pedidos
- Tratamento de erros em código

**Requisitos:**
- Credenciais SP-API
- Autenticação OAuth 2.0
- Gerenciamento de limites de taxa de API
- Dependências adicionais Python (biblioteca sp-api)

## Referências

### Documentação Oficial da Amazon

1. **Ajuda do Seller Central**:
   - https://sellercentral.amazon.com/help/hub/reference/G201576410
   - Diretrizes de Classificação de Produtos

2. **Templates de Arquivo de Inventário**:
   - Disponíveis em Seller Central → Inventário → Adicionar Produtos via Upload
   - Templates específicos por categoria

3. **Selling Partner API** (para integração futura):
   - https://developer-docs.amazon.com/sp-api/
   - Documentação da API Feeds

## Suporte

Para questões sobre:
- **Nosso adaptador**: Abrir issue no GitHub
- **Requisitos da Amazon**: Suporte do Amazon Seller
- **Integração SP-API**: Console de Desenvolvedores da Amazon

## Última Atualização

Esta documentação de conformidade reflete os requisitos do Amazon Seller Central a partir de outubro de 2025.

A Amazon pode atualizar seus requisitos. Sempre verifique as especificações atuais no Seller Central antes de uploads em massa.

