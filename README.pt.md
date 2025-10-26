# Adaptador de Autopeças para Amazon 🚗

Uma aplicação web FastAPI que converte arquivos CSV de autopeças estilo AutoZone para o formato de upload da Amazon para listar produtos na Amazon.com.

## Características

- 🚀 **Rápido e Moderno**: Construído com FastAPI para alto desempenho
- 📊 **Análise CSV Flexível**: Detecta e mapeia automaticamente vários formatos de colunas
- 🎨 **Interface Web Bonita**: Upload de arquivos com arrastar e soltar com progresso em tempo real
- 🔄 **Transformação Inteligente de Dados**: Converte dados de autopeças para o formato exigido pela Amazon
- 📦 **Pronto para Upload**: Gera arquivos CSV compatíveis com Amazon
- 🏷️ **Otimizado para Autopeças**: Gerencia dados de compatibilidade (Ano, Marca, Modelo)

## Início Rápido

### Instalação

1. Clonar o repositório:
```bash
git clone https://github.com/ALIO-IT/amazon-adapter.git
cd amazon-adapter
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

### Executar a Aplicação

Iniciar o servidor:
```bash
python main.py
```

Ou usando uvicorn diretamente:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Abra seu navegador e navegue para: `http://localhost:8000`

## 📖 Documentação em Outros Idiomas

- [English](README.md) - English documentation
- [Español](README.es.md) - Documentación en español
- [Português](README.pt.md) - Você está aqui

## Exemplo Completo: De CSV AutoZone para Amazon

Aqui está um passo a passo completo mostrando o processo de transformação:

### Passo 1: Seus Dados de Origem (Formato AutoZone)

Você tem `meu_inventario.csv`:
```csv
Part Number,Description,Brand,Price,Quantity,Category,UPC,Weight,Length,Width,Height,Year,Make,Model,Condition
BRK-001,Brake Pad Set - Ceramic Front,AutoZone,45.99,25,Brakes,012345678901,3.5,10,8,2,2020,Toyota,Camry,New
FLT-234,Engine Air Filter,K&N,24.99,50,Filters,012345678902,0.8,12,9,3,2018,Honda,Civic,New
BAT-123,Automotive Battery 800 CCA,DieHard,149.99,15,Batteries,012345678905,45.2,12,7,9,,,Any,New
```

### Passo 2: Executar o Conversor

**Opção A: Usando a Interface Web**
```
1. Ir para http://localhost:8000
2. Arrastar e soltar meu_inventario.csv
3. Clicar em "Convert to Amazon Format"
4. Download: amazon_auto_parts_20251026_143022.csv
```

**Opção B: Usando a API**
```bash
curl -X POST "http://localhost:8000/convert" \
  -F "file=@meu_inventario.csv" \
  -o resultado.json

# Resposta:
# {
#   "message": "File converted successfully",
#   "output_file": "amazon_auto_parts_20251026_143022.csv",
#   "rows_processed": 3,
#   "rows_output": 3
# }
```

### Passo 3: Sua Saída Pronta para Amazon

O conversor gera `amazon_auto_parts_20251026_143022.csv`:

```csv
product-id,product-id-type,item-name,brand-name,manufacturer,product-description,item-type,standard-price,list-price,quantity,product-tax-code,condition-type,part-number,item-weight,item-length,item-width,item-height,fulfillment-channel,fitment-year,fitment-make,fitment-model
012345678901,UPC,AutoZone - BRK-001 - Brake Pad Set - Ceramic Front,AutoZone,AutoZone,"Brake Pad Set - Ceramic Front. Brand: AutoZone. Part Number: BRK-001. Category: Brakes. Fits: 2020 Toyota Camry",Brakes,45.99,55.19,25,A_GEN_TAX,New,BRK-001,3.5,10,8,2,DEFAULT,2020,Toyota,Camry
```

### Passo 4: Upload para Amazon

1. Fazer login no Amazon Seller Central
2. Ir para **Inventário** → **Adicionar Produtos via Upload**
3. Selecionar template de categoria **Autopeças**
4. Upload `amazon_auto_parts_20251026_143022.csv`
5. Amazon processa seus 3 produtos instantaneamente!

### O Que Mudou? (Comparação Detalhada)

| Campo | Antes (AutoZone) | Depois (Amazon) | Transformação |
|-------|------------------|-----------------|----------------|
| **ID** | Part Number: BRK-001 | product-id: 012345678901 | Usou UPC como ID principal |
| **Tipo de ID** | N/A | product-id-type: UPC | Detectou presença de UPC automaticamente |
| **Título** | Description: Brake Pad Set... | item-name: AutoZone - BRK-001 - Brake Pad Set... | Combinou Marca + SKU + Descrição |
| **Preço** | Price: 45.99 | standard-price: 45.99 | Mapeamento direto |
| **Preço de Lista** | N/A | list-price: 55.19 | Calculado automaticamente (120% do preço) |
| **Descrição** | Description: Brake Pad Set... | product-description: Brake Pad Set...(detalhada) | Aprimorada com categoria, compatibilidade |
| **Compatibilidade** | Year/Make/Model em colunas separadas | fitment-year, fitment-make, fitment-model | Extraído e formatado |
| **Impostos** | N/A | product-tax-code: A_GEN_TAX | Código padrão atribuído automaticamente |

### Desempenho

- **Tempo de Processamento:** < 1 segundo para 100 produtos
- **Processamento em Massa:** Testado com mais de 10.000 produtos
- **Eficiente em Memória:** Processa arquivos de até 50MB

## Uso

### Interface Web

1. Abrir a interface web em `http://localhost:8000`
2. Arrastar e soltar seu arquivo CSV ou clicar para navegar
3. Clicar em "Convert to Amazon Format"
4. Baixar o arquivo CSV pronto para Amazon

**Fluxo de Trabalho de Exemplo:**
```
1. Navegar para http://localhost:8000
2. Soltar seu arquivo "inventario_autozone.csv" na área de upload
3. Clicar em "Convert to Amazon Format"
4. Sistema processa: "✅ Success! Processed 150 rows"
5. Clicar em "Download Amazon CSV"
6. Upload do arquivo baixado no Amazon Seller Central
```

### Endpoints da API

Para documentação detalhada da API, exemplos de código e casos de uso, consulte a [versão completa em inglês](README.md#api-endpoints).

## Formato CSV de Entrada

A aplicação suporta formatos CSV flexíveis. Detectará e mapeará automaticamente nomes de colunas comuns:

### Nomes de Colunas Suportados

| Tipo de Dado | Nomes de Coluna Aceitos |
|--------------|-------------------------|
| **Número da Peça** | part number, part_number, sku, item number, part#, product_id |
| **Descrição** | description, title, product name, name, item description |
| **Marca** | brand, manufacturer, make, mfr, vendor |
| **Preço** | price, unit price, cost, msrp, retail_price |
| **Quantidade** | quantity, qty, stock, inventory, available |
| **Categoria** | category, type, product_type, classification |
| **UPC** | upc, barcode, ean, gtin |
| **Peso** | weight, item_weight, shipping_weight |
| **Dimensões** | length, width, height (com variações) |
| **Compatibilidade de Veículo** | year, make, model (com variações) |
| **Condição** | condition, item_condition |

## Conformidade com a API da Amazon

✅ **Este adaptador está em total conformidade com as especificações de upload de produtos do Amazon Seller Central.**

**Importante**: Este adaptador foi projetado para **Amazon Seller Central** (produtos de varejo físicos), NÃO para AWS Marketplace (software/SaaS).

Para informações detalhadas sobre conformidade, consulte:
- [AMAZON_COMPLIANCE.pt.md](AMAZON_COMPLIANCE.pt.md) - Documentação de conformidade em português
- [AWS_MARKETPLACE_NOTE.pt.md](AWS_MARKETPLACE_NOTE.pt.md) - Nota sobre diferenças de APIs

### Resumo Rápido de Conformidade

| Requisito | Status | Implementação |
|-----------|--------|----------------|
| Campos Obrigatórios | ✅ Todos fornecidos | product-id, product-id-type, item-name, brand-name, standard-price, quantity, condition-type |
| Tipos de ID de Produto | ✅ Conforme | UPC (12 dígitos), EAN (13 dígitos), SKU (alfanumérico) |
| Limites de Caracteres | ✅ Aplicados | Título: 200 caracteres, Descrição: 2000 caracteres |
| Formato de Preço | ✅ Validado | Apenas numérico, 2 decimais, sem símbolos de moeda |
| Valores de Condição | ✅ Padronizados | New, Used, Refurbished (valores da Amazon) |
| Codificação UTF-8 | ✅ Obrigatória | Todos os arquivos gerados em UTF-8 |
| Campos de Autopeças | ✅ Suportados | Dados de compatibilidade (ano, marca, modelo) |
| Códigos de Impostos | ✅ Incluídos | A_GEN_TAX para bens tributáveis gerais |

## Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **Pandas**: Manipulação de dados e processamento CSV
- **Uvicorn**: Servidor ASGI
- **Python 3.8+**: Linguagem de programação

## Casos de Uso do Mundo Real

### Caso de Uso 1: Upload em Massa de Inventário de Autopeças

**Cenário:** Você tem 500 pastilhas de freio de vários fabricantes em seu CSV formato AutoZone.

**Passos:**
1. Exportar inventário do seu sistema POS/ERP para CSV
2. Upload na interface web do adaptador
3. Baixar o arquivo formatado para Amazon
4. Upload no Amazon Seller Central → Inventário → Adicionar Produtos via Upload

**Tempo Economizado:** Entrada manual levaria ~8 horas. Com o adaptador: 2 minutos.

### Caso de Uso 5: Atualização de Listagens Existentes na Amazon

**Cenário:** Você precisa atualizar preços, quantidades ou descrições para produtos já listados na Amazon.

**Como Funciona:**  
Quando a Amazon recebe um CSV com um `product-id` que corresponde a uma listagem existente, ela **atualiza** o item em vez de criar um novo.

Para documentação completa de casos de uso, scripts e exemplos, consulte a [versão em inglês](README.md#real-world-use-cases).

## Solução de Problemas

### Problemas Comuns e Soluções

#### Problema 1: "Only CSV files are accepted"
**Problema:** O arquivo enviado não é reconhecido como CSV.
**Solução:**
- Garantir que o arquivo tenha extensão `.csv`
- Exportar do Excel como formato "CSV UTF-8"
- Verificar se o arquivo não está corrompido

#### Problema 2: Dados ausentes ou incorretos na saída
**Problema:** Alguns campos estão vazios ou têm valores incorretos.
**Solução:**
```python
# Verificar se os nomes das colunas correspondem aos formatos suportados
# Editar adapter/csv_parser.py para adicionar mapeamentos personalizados

self.column_mappings = {
    'part_number': ['part number', 'sku', 'SUA_COLUNA_PERSONALIZADA'],
    # Adicione seus nomes de coluna personalizados aqui
}
```

## Desenvolvimento

### Executar Testes

O projeto inclui um script de teste completo:

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar script de teste
python test_conversion.py
```

## Estrutura do Projeto

```
amazon-adapter/
├── main.py                 # Aplicação FastAPI
├── adapter/
│   ├── __init__.py
│   ├── csv_parser.py       # Lógica de análise CSV
│   └── amazon_transformer.py  # Transformação para formato Amazon
├── uploads/                # Diretório de upload temporário
├── outputs/                # Arquivos CSV da Amazon gerados
├── requirements.txt        # Dependências Python
├── sample_autozone.csv     # Arquivo de amostra
├── README.md              # Documentação em inglês
├── README.es.md           # Documentación en español
└── README.pt.md           # Documentação em português (este arquivo)
```

## Licença

Licença MIT

## Contribuir

Contribuições são bem-vindas! Por favor, sinta-se à vontade para enviar um Pull Request.

## Suporte

Para problemas ou questões, por favor abra uma issue no GitHub.

---

**Nota:** Para a documentação completa com todos os exemplos de código, casos de uso detalhados e scripts de automação, consulte a [versão em inglês](README.md).
