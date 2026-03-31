# SmartStitch - 3D Humanoid Tailoring E-commerce

FastAPI + HTML/CSS/JS prototype for custom garment ordering with measurement-driven 3D humanoid previews.

## Features implemented
- Login split: **Public user** and **Garment user**.
- Public flow: category selection (women/men/kids), dress selection, material/color upload section, skin-tone color recommendations, measurement form, and generated 3D model gallery.
- 3D viewer: rotatable humanoid avatar rendered via Three.js and scaled by measurements.
- Generates 20 design variants and supports prompt-based additional custom model creation.
- Order placement workflow with shipping details.
- Garment dashboard with order-stage bars, payment table, and CSV export (Excel-compatible).
- Postgres for users/orders/payments and MongoDB for generated model snapshots.
- Twilio SMS + SMTP email notifications for new orders.

## Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python FastAPI
- 3D Engine: Three.js/WebGL (WebXR-ready hook)
- Databases: PostgreSQL + MongoDB
- Notifications: Twilio + email SMTP (Nodemailer-compatible architecture can call same SMTP account from a Node service)
- Storage: AWS-ready (add S3 uploads in `app/routes/api.py`)

## Run locally
```bash
docker compose up -d
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000

## Notes
- Replace placeholder notification credentials in `.env`.
- For production AR preview, integrate WebXR ARButton and/or ARCore scene viewer on mobile devices.
- For real humanoid meshes (men/women/kids like reference image), store GLB files in S3 + Mongo metadata and load via Three.js GLTFLoader.
