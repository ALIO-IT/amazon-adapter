# Nota Sobre a Documentação da API do AWS Marketplace

[Leia esta nota em outros idiomas: [English](AWS_MARKETPLACE_NOTE.md) | [Español](AWS_MARKETPLACE_NOTE.es.md) | **Português**]

## ⚠️ Esclarecimento Importante

O arquivo PDF `marketplace-api.pdf` neste diretório é documentação para **AWS Marketplace API**, que **NÃO** é a API correta para este projeto.

## Dois Sistemas Amazon Diferentes

### 1. Amazon Seller Central (O Que Este Projeto Usa) ✅

**Propósito**: Vender produtos físicos no mercado de varejo da Amazon.com

**Tipos de Produtos**:
- Autopeças (nosso foco)
- Eletrônicos de consumo
- Roupas
- Livros
- Artigos para casa
- Qualquer produto físico vendido na Amazon

**Métodos de Upload**:
- Upload de arquivo CSV/Texto via interface web do Seller Central
- Selling Partner API (SP-API) para acesso programático

**O Que Implementamos**:
- ✅ Geração de arquivos CSV para upload no Seller Central
- ✅ Formato de categoria de Autopeças
- ✅ Formato de gerenciamento de inventário

**Localização da Documentação**:
- Ajuda do Amazon Seller Central: https://sellercentral.amazon.com/help
- Docs SP-API: https://developer-docs.amazon.com/sp-api/

**Acesso**:
- Requer: Conta Amazon Seller
- Login: sellercentral.amazon.com

---

### 2. AWS Marketplace (O PDF Que Você Tem) ❌

**Propósito**: Vender produtos de software e SaaS no AWS Marketplace

**Tipos de Produtos**:
- Amazon Machine Images (AMIs)
- Produtos em contêineres
- Aplicações SaaS
- Modelos de machine learning
- Produtos de dados
- Produtos de servidor

**Métodos de Upload**:
- AWS Marketplace Catalog API
- Console de Gerenciamento
- Chamadas de API com credenciais AWS IAM

**O Que NÃO Cobre**:
- ❌ Listagens de produtos físicos
- ❌ Autopeças
- ❌ Produtos de varejo para consumidores
- ❌ Marketplace da Amazon.com

**Documentação**:
- AWS Marketplace: https://aws.amazon.com/marketplace/
- Referência de API: O arquivo PDF neste diretório

**Acesso**:
- Requer: Conta AWS com registro de vendedor no marketplace
- Diferente do Amazon Seller Central

## Por Que a Confusão?

Ambos os serviços são da Amazon mas servem propósitos completamente diferentes:

| Característica | Amazon Seller Central | AWS Marketplace |
|----------------|----------------------|-----------------|
| **Plataforma** | Amazon.com varejo | Plataforma AWS Cloud |
| **Produtos** | Bens físicos | Software/SaaS |
| **Clientes** | Consumidores de varejo | Usuários de AWS cloud |
| **Formato de Upload** | Arquivos CSV | Chamadas API (JSON) |
| **Nosso Projeto** | ✅ SIM - Isto é o que almejamos | ❌ NÃO - Sistema errado |
| **Exemplo** | Pastilhas de freio, filtros, baterias | AMI WordPress, SaaS de monitoramento |
| **Preços** | Preços fixos por item | Cobrança baseada em uso |
| **Cumprimento** | Enviar itens físicos | Implantar software |

## O Que Nosso Adaptador Faz

```
Seu CSV de Inventário (formato AutoZone)
          ↓
    Nosso Adaptador
          ↓
CSV do Amazon Seller Central (formato compatível)
          ↓
Upload no Site do Amazon Seller Central
          ↓
Produtos Listados na Amazon.com
```

## O Que a API do AWS Marketplace Faz (Não Nós)

```
Pacote de Software/AMI
          ↓
API de Catálogo do AWS Marketplace
          ↓
Listar no AWS Marketplace
          ↓
Clientes AWS Implantam em Sua Infraestrutura
```

## Documentação Correta para Este Projeto

### Upload CSV do Amazon Seller Central

**O que referenciar**: Templates específicos por categoria do Amazon Seller Central

**Como acessar**:
1. Fazer login em sellercentral.amazon.com
2. Ir para: **Inventário** → **Adicionar Produtos via Upload**
3. Clicar: **Baixar um Template de Arquivo de Inventário**
4. Selecionar: **Automotivo e Esportes Motorizados**
5. Baixar o template para ver os campos obrigatórios

**Seções principais**:
- Campos obrigatórios (product-id, title, price, etc.)
- Campos específicos de automotivo (dados de compatibilidade)
- Valores válidos (tipos de condição, códigos de impostos)
- Limites de caracteres
- Formatos de dados

### Nossa Conformidade

Consulte [AMAZON_COMPLIANCE.pt.md](AMAZON_COMPLIANCE.pt.md) para documentação detalhada de como nosso adaptador atende aos requisitos do Amazon Seller Central.

## Se Você Deseja Integrar com SP-API (Futuro)

Se você deseja fazer upload de produtos programaticamente em vez de usar arquivos CSV:

**Selling Partner API (SP-API)**:
- Documentação: https://developer-docs.amazon.com/sp-api/
- O que faz: Acesso programático a funções do Seller Central
- Recursos: Uploads de produtos, sincronização de inventário, gerenciamento de pedidos
- Autenticação: OAuth 2.0 + AWS Signature V4
- Formato: JSON (não XML/JSON como AWS Marketplace)

**Isso seria uma melhoria futura** para chamar diretamente as APIs da Amazon em vez de gerar arquivos CSV.

## Resumo

✅ **Usar para nosso projeto**: Documentação do Amazon Seller Central
❌ **Não usar**: API do AWS Marketplace (o PDF que você tem)

A documentação da API do AWS Marketplace é útil se você está vendendo:
- Software como Serviço (SaaS)
- Amazon Machine Images
- Aplicações em contêineres
- Modelos de ML

Mas como estamos vendendo **autopeças físicas**, precisamos da documentação do **Amazon Seller Central** em vez disso.

## Precisa de Ajuda?

- **Ajuda do Seller Central**: https://sellercentral.amazon.com/help
- **Documentação SP-API**: https://developer-docs.amazon.com/sp-api/
- **Nossos Docs de Conformidade**: [AMAZON_COMPLIANCE.pt.md](AMAZON_COMPLIANCE.pt.md)
- **Template de Autopeças**: Baixar do Seller Central (veja os passos acima)

