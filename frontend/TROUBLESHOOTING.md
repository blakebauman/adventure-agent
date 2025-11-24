# Troubleshooting Guide

## Common Issues

### 1. CORS Errors

**Problem**: Browser console shows CORS errors when trying to connect to the API.

**Solution**: 
- The frontend is configured to use a Vite proxy in development mode
- Make sure you're running `npm run dev` (not building for production)
- The proxy automatically forwards `/api/*` requests to `http://localhost:2024`
- If you need to use a different API URL, set `VITE_API_URL` in `.env`

### 2. Connection Refused

**Problem**: "Failed to fetch" or "Connection refused" errors.

**Solution**:
- Ensure the LangGraph API server is running: `langgraph dev`
- Check that it's running on port 2024 (default)
- Verify the API is accessible: `curl http://localhost:2024/assistants`

### 3. Streaming Not Working

**Problem**: Messages don't appear in real-time, or streaming stops.

**Solution**:
- Check browser console for errors
- Verify the API server supports streaming (LangGraph API does by default)
- Check network tab to see if the stream endpoint is being called
- Look for errors in the terminal where `langgraph dev` is running

### 4. Backend Errors

**Problem**: Backend errors appear in terminal but frontend shows generic errors.

**Solution**:
- The frontend now shows more detailed error messages
- Check the browser console for full error details
- Common backend issues:
  - JSON parsing errors (check agent output formatting)
  - API key issues (check environment variables)
  - Schema validation errors (check structured output schemas)

### 5. Build Errors

**Problem**: `npm run build` fails or TypeScript errors.

**Solution**:
- Run `npm install` to ensure all dependencies are installed
- Check that `tailwindcss-animate` is installed (required for animations)
- Verify TypeScript version matches requirements
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`

## Debugging Tips

1. **Check Browser Console**: Open DevTools (F12) and check the Console tab for errors
2. **Check Network Tab**: See if API requests are being made and their responses
3. **Check Terminal**: Look at the `langgraph dev` output for backend errors
4. **Enable Verbose Logging**: Add `console.log` statements in the API client to see what's happening

## Environment Variables

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_URL=http://localhost:2024
```

Or use the proxy (default in development):
```env
# Leave VITE_API_URL unset to use Vite proxy (/api)
```

## Testing the Connection

1. **Test API directly**:
   ```bash
   curl http://localhost:2024/assistants
   ```

2. **Test from frontend**:
   - Open browser console
   - The chat interface should show the API URL in the header (dev mode)
   - Try sending a message and watch the Network tab

3. **Check proxy**:
   - In dev mode, requests to `/api/*` are proxied to `http://localhost:2024`
   - Check Vite dev server output for proxy logs

## Common Backend Errors (from terminal)

### JSON Parsing Error
```
Error in Geo agent: Expecting property name enclosed in double quotes
```
**Fix**: Check the agent's JSON output formatting

### Schema Validation Error
```
Invalid schema for response_format 'LocationGuideResponse'
```
**Fix**: Update the Pydantic schema to match OpenAI's requirements (add `additionalProperties: false`)

### 401 Unauthorized
```
HTTP Request: GET ... "HTTP/1.1 401 Unauthorized"
```
**Fix**: Check API keys in `.env` file (Recreation.gov, etc.)

### Blocking Calls Warning
```
Blocking call to socket.socket.connect
```
**Fix**: This is a warning, not an error. For production, convert to async or use `langgraph dev --allow-blocking` for development.

