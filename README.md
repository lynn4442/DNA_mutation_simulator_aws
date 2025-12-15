# DNA Mutation Simulator - AWS Deployment

## Project Overview

A web-based DNA mutation simulator that demonstrates how genetic mutations (point mutations, insertions, and deletions) affect RNA transcription and protein synthesis. The application visualizes mutation effects through interactive charts and sequence comparisons.

**Live Website:** http://dna-mutation-env.eba-eaqsyvu6.us-west-2.elasticbeanstalk.com

---

## What Has Been Accomplished

### Application Development
**Flask Backend (`app.py`):**
- DNA to RNA transcription engine
- Protein synthesis from genetic code
- Three mutation types: point mutations, insertions, deletions
- Matplotlib-based statistical visualizations
- RESTful API endpoint for mutation generation

**Frontend Interface (`templates/index.html`):**
- Elegant gray color scheme design
- Playfair Display serif typography for headings
- Inter sans-serif for body text
- Responsive Bootstrap 5 layout
- Real-time mutation visualization
- Sample genes: Insulin, Hemoglobin, BRCA1, p53, CFTR

### AWS Infrastructure Deployed
- **Environment:** dna-mutation-env
- **Region:** us-west-2 (Oregon)
- **Platform:** Python 3.12
- **Instance:** t2.micro (Free Tier)
- **Status:** LIVE and accessible worldwide

### Project Structure
```
DNA_mutation_simulator_aws/
├── app.py                          # Flask application
├── requirements.txt                # Python dependencies
├── templates/
│   └── index.html                  # Frontend with elegant design
├── .ebextensions/
│   └── 01_flask.config            # Elastic Beanstalk configuration
└── .gitignore                      # Git ignore rules
```

---

## How The System Works

### Architecture

```
User Browser
    ↓
AWS Elastic Beanstalk (dna-mutation-env.eba-eaqsyvu6.us-west-2.elasticbeanstalk.com)
    ↓
EC2 Instance (t2.micro)
    ├── Nginx (Web Server)
    ├── Gunicorn (WSGI Server)
    └── Flask Application
        ├── DNA Mutation Logic
        ├── RNA Transcription
        ├── Protein Synthesis
        └── Matplotlib Visualization
```

### AWS Services in Use

**1. Amazon EC2 (Elastic Compute Cloud)**
- Running Amazon Linux 2 virtual server
- Python 3.12 installed
- All dependencies installed from requirements.txt
- Application running at /var/app/current/
- Serving HTTP traffic on port 80
- Instance type: t2.micro (1 vCPU, 1GB RAM)

**2. AWS Elastic Beanstalk**
- Automatically provisioned EC2 instance
- Installed Python environment
- Installed dependencies: Flask 3.1.2, matplotlib 3.10.8, numpy 1.26.4
- Configured WSGI server (Gunicorn)
- Deployed application code
- Monitors health every 30 seconds
- Auto-restarts application on crashes
- Aggregates logs to CloudWatch

**3. Amazon S3**
- Stores deployment packages (zipped code)
- Maintains version history
- Bucket: elasticbeanstalk-us-west-2-[account-id]

**4. AWS CloudWatch**
- Collects application logs
- Tracks performance metrics (CPU, memory, requests)
- Stores Flask print statements and errors
- Web server access/error logs

**5. AWS IAM**
- Manages deployment credentials
- EC2 instance profile for S3/CloudWatch access
- Service roles for Elastic Beanstalk operations

**6. Security Groups (Firewall)**
- Port 80 (HTTP): OPEN to all traffic (0.0.0.0/0)
- Port 443 (HTTPS): Not configured
- Port 22 (SSH): Restricted to EB management
- All other ports: BLOCKED

### Request Flow

1. User visits dna-mutation-env.eba-eaqsyvu6.us-west-2.elasticbeanstalk.com
2. DNS resolves to EC2 public IP address
3. Security Group allows port 80 traffic through
4. Nginx web server receives HTTP request
5. Nginx forwards request to Gunicorn WSGI server
6. Gunicorn passes request to Flask application
7. Flask routes request:
   - GET / → Renders index.html with sample genes
   - POST /mutate → Generates mutations, creates matplotlib charts
8. Flask sends response with HTML + base64-encoded PNG images
9. User's browser displays results with elegant gray styling

### Deployment Configuration

**File: `.ebextensions/01_flask.config`**
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app:application
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: "/var/app/current:$PYTHONPATH"
```

This tells Elastic Beanstalk:
- Find the `application` variable in app.py
- Use it as the WSGI entry point
- Set Python path for proper imports

**File: `app.py` (lines 286-287)**
```python
# Required for AWS Elastic Beanstalk
application = app
```

Elastic Beanstalk requires Flask app named `application`.

### Technology Stack

**Backend:**
- Python 3.12
- Flask 3.1.2 (Web framework)
- NumPy 1.26.4 (Numerical computations)
- Matplotlib 3.10.8 (Chart generation with Agg backend for server)
- Werkzeug 3.1.4 (WSGI utilities)

**Frontend:**
- Bootstrap 5.3.2
- Bootstrap Icons 1.11.2
- Google Fonts (Playfair Display, Inter)
- Vanilla JavaScript

**Infrastructure:**
- Nginx (Reverse proxy)
- Gunicorn (WSGI server)
- AWS Elastic Beanstalk

---

## Application Features

### Mutation Types
1. **Point Mutation** - Single nucleotide substitution (A→T, G→C, etc.)
2. **Insertion** - Adds 1-3 nucleotides (may cause frameshift)
3. **Deletion** - Removes 1-3 nucleotides (may cause frameshift)

### Visualizations Generated
Four statistical charts per simulation:
1. Mutation Types Distribution (Bar chart)
2. Mutation Positions (Histogram)
3. Protein Effects (unchanged/shorter/longer/changed)
4. Amino Acid Changes (Histogram)

### Sample Genes
- Insulin (114 bases)
- Hemoglobin (93 bases)
- BRCA1 (81 bases)
- p53 (114 bases)
- CFTR (114 bases)

---

## Cost Structure

**Current Costs (AWS Free Tier - First 12 Months):**
- EC2 t2.micro: 750 hours/month FREE
- Data Transfer: 15 GB/month FREE
- Elastic Beanstalk: FREE (only pay for resources)
- S3 Storage: Negligible (<1 MB)
- CloudWatch: Basic monitoring FREE

**Total: $0.00/month**

**After Free Tier:**
- EC2 t2.micro: ~$8.50/month
- Data transfer: $0.09/GB after 15GB
- Estimated: ~$10-15/month for low traffic

---

## What Is Missing to Complete GitHub Deployment Goal

### Project Goal
Deploy a website from GitHub to AWS with automated CI/CD pipeline.

### Current Status
✅ Website is LIVE and WORKING on AWS
❌ Code is NOT in GitHub
❌ No automated deployment pipeline
❌ Manual deployment only (using `eb deploy` command)

### Missing Components

**1. GitHub Repository**
- Code exists only locally and on AWS
- Not pushed to GitHub
- No version control for collaboration
- No remote backup

**2. CI/CD Pipeline (GitHub Actions)**
- No automated deployment on code changes
- Must manually run `eb deploy` for updates
- No automated testing before deployment
- No deployment history tracking in GitHub

**3. GitHub Actions Workflow File**
Missing: `.github/workflows/deploy.yml`

This file would:
- Trigger on push to main branch
- Install dependencies
- Run tests
- Deploy to AWS Elastic Beanstalk automatically

**4. GitHub Secrets Configuration**
Need to add in GitHub repository settings:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION (us-west-2)
- EB_APPLICATION_NAME
- EB_ENVIRONMENT_NAME

**5. Automated Testing**
- No test suite configured
- No pre-deployment validation
- No continuous integration checks

---

## Intended vs Current Workflow

### Intended Workflow (NOT YET IMPLEMENTED)
```
Developer writes code
    ↓
git push to GitHub main branch
    ↓
GitHub Actions automatically triggered
    ↓
Run automated tests
    ↓
Build deployment package
    ↓
Deploy to AWS Elastic Beanstalk
    ↓
Live website updated automatically
```

### Current Workflow (MANUAL)
```
Developer writes code locally
    ↓
Manual command: eb deploy
    ↓
Live website updated
    ↓
No GitHub involved
```

---

## Steps to Complete GitHub Integration

### Step 1: Push Code to GitHub
```bash
# If git not initialized
git init
git add .
git commit -m "DNA mutation simulator with elegant gray design"

# Create repository on GitHub, then:
git remote add origin https://github.com/[username]/dna-mutation-simulator.git
git push -u origin main
```

### Step 2: Create GitHub Actions Workflow
Create file: `.github/workflows/deploy.yml`
```yaml
name: Deploy to AWS Elastic Beanstalk

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install EB CLI
        run: pip install awsebcli

      - name: Deploy to Elastic Beanstalk
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          eb init -p python-3.12 dna-mutation-simulator --region us-west-2
          eb deploy dna-mutation-env
```

### Step 3: Configure GitHub Secrets
In GitHub repository settings → Secrets and variables → Actions:
1. Add `AWS_ACCESS_KEY_ID`
2. Add `AWS_SECRET_ACCESS_KEY`

### Step 4: Test Automated Deployment
```bash
# Make a change
echo "Test CI/CD" >> README.md

# Commit and push
git add README.md
git commit -m "Test automated deployment"
git push

# GitHub Actions will automatically deploy to AWS
```

---

## Local Development

### Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Access at http://localhost:5001
```

### Manual Deployment Commands
```bash
eb deploy           # Deploy code changes
eb status           # Check environment status
eb open             # Open website in browser
eb logs             # View application logs
eb terminate        # Delete environment (careful!)
```

---

## Files Not to Commit

`.gitignore` excludes:
- `venv/` - Virtual environment
- `__pycache__/` - Python bytecode
- `*.pyc` - Compiled files
- `.elasticbeanstalk/` - Contains sensitive local config

---

## Summary

### ✅ What Works
- Full-featured DNA mutation simulator
- Professional elegant gray design
- AWS deployment infrastructure
- Live website accessible worldwide
- Health monitoring and auto-recovery
- Production-ready Flask application

### ❌ What's Missing for GitHub Deployment Goal
- Code repository on GitHub
- CI/CD pipeline (GitHub Actions)
- Automated deployment on git push
- GitHub Secrets configuration
- Automated testing workflow

### Current State
The website is **DEPLOYED and FUNCTIONAL** on AWS, but deployment is **MANUAL**. To complete the project goal of "deploying from GitHub," you need GitHub integration and automation.

---

**Live URL:** http://dna-mutation-env.eba-eaqsyvu6.us-west-2.elasticbeanstalk.com

**Status:** PRODUCTION (Manual Deployment) | Missing: GitHub CI/CD Integration
