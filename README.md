# Presales Request Intake Assistant

A serverless prototype that turns a customer's free-text request into a structured first pass for a presales engineer. Paste an email, web form message, call notes or chat transcript, and the assistant returns:

1. A short summary of the customer's situation
2. Requirements mapped to service areas and catalog service codes, each with a priority and a reason
3. An urgency rating (High, Medium or Low)
4. Information gaps
5. Discovery questions to ask the customer
6. A draft reply for an engineer to review and send

The engineer stays in charge: nothing is sent to the customer automatically, and every draft is reviewed first.

**Live demo:** https://lzn1dub7n9.execute-api.us-east-1.amazonaws.com/

> The demo uses a sample service catalog for a fictional IT company. It is a prototype built for demonstration, not a production system.

## The problem

Quote requests usually arrive as free text written by someone who is not technical. Before anyone can quote, an engineer has to read it, work out what the customer needs, decide which service areas it touches, spot what is missing and write a reply asking questions. That slows the first response and makes quality depend on who picks the request up.

This prototype prepares that first pass in seconds, so engineers start from a structured draft instead of a blank page.

## Architecture
<img width="1536" height="1024" alt="Serverless Presales Request Intake Architecture" src="https://github.com/user-attachments/assets/0b600cf6-5c6f-40b4-bceb-9a5277486b2a" />


| Step | Flow |
|------|------|
| 1 | The browser sends an HTTPS request to Amazon API Gateway (HTTP API) |
| 2 | API Gateway invokes the AWS Lambda function |
| 3 | Lambda reads the service catalog PDF from Amazon S3 |
| 4 | Lambda sends the catalog and the customer's request to Claude on Amazon Bedrock (Converse API) |
| 5 | Bedrock returns a structured JSON analysis |
| 6 | Lambda validates it against the catalog and returns it through API Gateway to the page |

`GET /` returns the web page and `POST /analyse` returns the analysis. Because the page and the API share one endpoint, no separate hosting or CORS setup is needed.

### AWS services

| Service | Purpose |
|---------|---------|
| Amazon API Gateway (HTTP API) | Public endpoint for the page and the API, with throttling |
| AWS Lambda (Python 3.12) | Serves the page, reads the catalog, calls Bedrock, validates output |
| Amazon S3 | Private, encrypted bucket holding the service catalog PDF |
| Amazon Bedrock | Runs Claude, which reads the catalog PDF natively |
| AWS IAM | Least-privilege role: read one catalog object, invoke Bedrock models |
| Amazon CloudWatch Logs | Lambda request and error logs, with retention set |
| AWS CloudFormation (SAM) | Deploys everything as one stack |

## Design choices

- **Whole catalog in every request.** The catalog is small, so the full PDF is passed to the model. This is more accurate than retrieval because no service can be missed. For a large document set (vendor datasheets, past proposals), the next step would be an Amazon Bedrock Knowledge Base.
- **Catalog in S3, not in code.** The service list can be updated by replacing one file, with no redeploy.
- **Stateless.** No customer data is stored. Each request is processed and returned.

## Safeguards

- Customer text is treated as data, so instructions written inside a request are ignored.
- The model may only map needs to catalog services. The Lambda checks every service area and code, and moves anything unknown to "Outside the current service list".
- No prices, brands or product models are produced; that belongs in a separate quotation step.
- The draft reply is signed `[Engineer name]` and never names a company.
- Input length is limited to 15–4,000 characters.
- The S3 bucket is private, encrypted and HTTPS-only. The API is throttled to limit abuse and cost.

## Repository structure

```
.
├── template.yaml            # CloudFormation (SAM) template: bucket, Lambda, HTTP API, IAM, logs
├── src/
│   ├── lambda_function.py   # Lambda handler
│   └── index.html           # Web page served at GET /
├── catalog/
│   ├── IT_Service_Catalog.pdf   # Sample service catalog (fictional company)
│   └── build_catalog.py         # Script that generates the PDF
├── scripts/
│   └── deploy.sh            # Deploys the stack and uploads the catalog
└── docs/
    └── architecture.png     # Architecture diagram
```


### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `ModelId` | `us.anthropic.claude-sonnet-5` | Bedrock model or inference profile ID |
| `CatalogKey` | `IT_Service_Catalog.pdf` | Catalog object name in the bucket |
| `LogRetentionDays` | `14` | CloudWatch log retention |

## Using the demo

1. Open the URL.
2. Choose an example request (logistics company with several issues, general enquiry, or payment fraud after phishing) or paste your own.
3. Select **Analyse request**. Results appear in about 10–25 seconds.


## Author

Chijioke Boniface
