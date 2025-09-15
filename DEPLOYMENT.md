# Windborne Deployment Guide

This guide will help you deploy both the frontend and backend to Vercel.

## Prerequisites

1. Install Vercel CLI: `npm i -g vercel`
2. Have a Vercel account
3. Have the project files ready

## Backend Deployment

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Deploy to Vercel:
   ```bash
   vercel
   ```

3. Follow the prompts:
   - Link to existing project or create new one
   - Choose your Vercel account
   - Accept default settings

4. Note the deployment URL (e.g., `https://your-backend-app.vercel.app`)

## Frontend Deployment

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Set the backend URL environment variable:
   ```bash
   vercel env add VITE_API_URL
   ```
   Enter your backend URL when prompted (e.g., `https://your-backend-app.vercel.app`)

3. Deploy to Vercel:
   ```bash
   vercel
   ```

4. Follow the prompts and accept default settings

## Environment Variables

### Backend
No additional environment variables needed for basic deployment.

### Frontend
- `VITE_API_URL`: The URL of your deployed backend (e.g., `https://your-backend-app.vercel.app`)

## Post-Deployment

1. Test both applications
2. Update any hardcoded URLs if needed
3. Configure custom domains if desired

## Troubleshooting

- If backend fails to deploy, check that all dependencies are in `requirements.txt`
- If frontend can't connect to backend, verify the `VITE_API_URL` environment variable
- Check Vercel function logs for any runtime errors
