# Note About AWS Marketplace API Documentation

[Read this note in other languages: **English** | [Español](AWS_MARKETPLACE_NOTE.es.md) | [Português](AWS_MARKETPLACE_NOTE.pt.md)]

## ⚠️ Important Clarification

The PDF file `marketplace-api.pdf` in this directory is documentation for **AWS Marketplace API**, which is **NOT** the correct API for this project.

## Two Different Amazon Systems

### 1. Amazon Seller Central (What This Project Uses) ✅

**Purpose**: Selling physical products on Amazon.com retail marketplace

**Product Types**:
- Auto parts (our focus)
- Consumer electronics
- Clothing
- Books
- Home goods
- Any physical product sold on Amazon

**Upload Methods**:
- CSV/Text file upload via Seller Central web interface
- Selling Partner API (SP-API) for programmatic access

**What We Implement**:
- ✅ CSV file generation for Seller Central upload
- ✅ Auto Parts category format
- ✅ Inventory management format

**Documentation Location**:
- Amazon Seller Central Help: https://sellercentral.amazon.com/help
- SP-API Docs: https://developer-docs.amazon.com/sp-api/

**Access**:
- Requires: Amazon Seller account
- Login: sellercentral.amazon.com

---

### 2. AWS Marketplace (The PDF You Have) ❌

**Purpose**: Selling software and SaaS products on AWS Marketplace

**Product Types**:
- Amazon Machine Images (AMIs)
- Container products
- SaaS applications
- Machine learning models
- Data products
- Server products

**Upload Methods**:
- AWS Marketplace Catalog API
- Management Console
- API calls with AWS IAM credentials

**What It Does NOT Cover**:
- ❌ Physical product listings
- ❌ Auto parts
- ❌ Consumer retail products
- ❌ Amazon.com marketplace

**Documentation**:
- AWS Marketplace: https://aws.amazon.com/marketplace/
- API Reference: The PDF file in this directory

**Access**:
- Requires: AWS account with marketplace seller registration
- Different from Amazon Seller Central

## Why the Confusion?

Both services are from Amazon but serve completely different purposes:

| Feature | Amazon Seller Central | AWS Marketplace |
|---------|----------------------|-----------------|
| **Platform** | Amazon.com retail | AWS Cloud platform |
| **Products** | Physical goods | Software/SaaS |
| **Customers** | Retail consumers | AWS cloud users |
| **Upload Format** | CSV files | API calls (JSON) |
| **Our Project** | ✅ YES - This is what we target | ❌ NO - Wrong system |
| **Example** | Brake pads, filters, batteries | WordPress AMI, monitoring SaaS |
| **Pricing** | Fixed item prices | Usage-based billing |
| **Fulfillment** | Ship physical items | Deploy software |

## What Our Adapter Does

```
Your Inventory CSV (AutoZone format)
          ↓
    Our Adapter
          ↓
Amazon Seller Central CSV (compliant format)
          ↓
Upload to Amazon Seller Central Website
          ↓
Products Listed on Amazon.com
```

## What AWS Marketplace API Does (Not Us)

```
Software/AMI Package
          ↓
AWS Marketplace Catalog API
          ↓
List on AWS Marketplace
          ↓
AWS Customers Deploy to Their Infrastructure
```

## Correct Documentation for This Project

### Amazon Seller Central CSV Upload

**What to reference**: Amazon Seller Central's category-specific templates

**How to access**:
1. Log into sellercentral.amazon.com
2. Go to: **Inventory** → **Add Products via Upload**
3. Click: **Download an Inventory File Template**
4. Select: **Automotive & Powersports**
5. Download the template to see required fields

**Key sections**:
- Required fields (product-id, title, price, etc.)
- Automotive-specific fields (fitment data)
- Valid values (condition types, tax codes)
- Character limits
- Data formats

### Our Compliance

See [AMAZON_COMPLIANCE.md](AMAZON_COMPLIANCE.md) for detailed documentation of how our adapter meets Amazon Seller Central's requirements.

## If You Want to Integrate with SP-API (Future)

If you want to programmatically upload products instead of using CSV files:

**Selling Partner API (SP-API)**:
- Documentation: https://developer-docs.amazon.com/sp-api/
- What it does: Programmatic access to Seller Central functions
- Features: Product uploads, inventory sync, order management
- Authentication: OAuth 2.0 + AWS Signature V4
- Format: JSON (not XML/JSON like AWS Marketplace)

**This would be a future enhancement** to directly call Amazon's APIs instead of generating CSV files.

## Summary

✅ **Use for our project**: Amazon Seller Central documentation
❌ **Don't use**: AWS Marketplace API (the PDF you have)

The AWS Marketplace API documentation is useful if you're selling:
- Software as a Service (SaaS)
- Amazon Machine Images
- Container applications
- ML models

But since we're selling **physical auto parts**, we need **Amazon Seller Central** documentation instead.

## Need Help?

- **Seller Central Help**: https://sellercentral.amazon.com/help
- **SP-API Documentation**: https://developer-docs.amazon.com/sp-api/
- **Our Compliance Docs**: [AMAZON_COMPLIANCE.md](AMAZON_COMPLIANCE.md)
- **Auto Parts Template**: Download from Seller Central (see steps above)

