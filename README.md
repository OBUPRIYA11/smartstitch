# SmartStitch – AI 3D Clothing Customization Platform

This repository contains a full-stack starter implementation for the requested solution:

- **Web app (React + Three.js-ready)** for category navigation, measurement input, and design-variation carousel.
- **Mobile app (React Native/Expo)** for portable customization and AR-ready flow.
- **Backend (FastAPI)** exposing APIs for avatar scaling, prompt-to-JSON design edits, and multi-variation generation.

## Core Functional Coverage

### Public user flow
- Category selection (`women`, `men`, `kids`)
- Collection navigation per category
- Dress selection + customization state
- Manual measurement form + **Generate 3D Model** trigger

### Measurement-based avatar scaling
`POST /api/avatar/generate` converts measurements into parametric rig scales:
- Global scale from height
- Torso width from chest/waist/hip
- Shoulder, arm, leg, wrist, thigh, ankle scaling

### Design variation engine (same dress + same color)
`POST /api/designs/variations` creates multiple variations that keep color/fabric constraints while changing:
- Border
- Pattern
- Texture
- Sleeve style
- Pallu style
- Neck design

### AI prompt-based customization
`POST /api/designs/prompt` converts text instructions into structured JSON for runtime mesh/texture toggles.

### Order API scaffold
`POST /api/orders` accepts order details and returns an order id/status response shape.

## Repository structure

- `backend/` FastAPI services and schemas
- `web/` React web interface
- `mobile/` Expo React Native interface

## Next integration steps

1. Add PostgreSQL + MongoDB persistence adapters.
2. Integrate S3 uploads for reference images.
3. Add CV model endpoint for image feature extraction (`border`, `pattern`, `texture`, etc.).
4. Attach Three.js avatar mesh and modular garment layers.
5. Add AR modules: WebXR (web), ARCore bridge (mobile).
6. Integrate Twilio + Nodemailer for order notifications.
7. Build admin dashboard with status workflow and exports.
