# Twilio WhatsApp Integration Setup Guide

## ✅ Implementation Complete

The Twilio WhatsApp integration has been successfully implemented with a clean, extensible architecture.

## 📁 What Was Created

### New Files:
```
backend/app/
├── integrations/              # NEW: Messaging integrations folder
│   ├── __init__.py
│   ├── base_messenger.py      # Abstract interface
│   ├── twilio_messenger.py    # Twilio implementation (ACTIVE)
│   └── meta_messenger.py      # Meta stub (for future)
│
├── services/
│   └── messaging_service.py   # NEW: Factory for selecting messenger
│
└── api/
    └── whatsapp_webhook.py    # NEW: Webhook endpoint
```

### Updated Files:
- `app/config.py` - Added Twilio settings
- `app/main.py` - Registered webhook router
- `requirements.txt` - Added twilio package
- `.env.example` - Added configuration template

## 🚀 Setup Steps

### 1. Install Dependencies

```bash
cd backend
pip install twilio
```

### 2. Configure Environment

Update your `.env` file (or create one from `.env.example`):

```env
# For Testing (default - no real messages sent)
MESSAGING_PROVIDER=mock

# For Twilio WhatsApp (when ready)
MESSAGING_PROVIDER=twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+14155238886
```

### 3. Test Existing Endpoints (Still Work!)

```bash
# Start server
uvicorn app.main:app --reload

# Test with Postman
POST http://localhost:8000/message
Body: {"from": "+40741111111", "text": "show my parcels"}
```

✅ **Your existing `/message` endpoint works exactly as before!**

## 📱 Twilio WhatsApp Setup (When Ready)

### Step 1: Create Twilio Account
1. Go to https://www.twilio.com/try-twilio
2. Sign up for free trial
3. Get $15 credit for testing

### Step 2: Activate WhatsApp Sandbox
1. In Twilio Console, go to **Messaging** → **Try it out** → **Send a WhatsApp message**
2. Send "join [your-code]" to the Twilio WhatsApp number
3. You'll get a confirmation message

### Step 3: Get Credentials
1. Go to https://console.twilio.com/
2. Copy your **Account SID**
3. Copy your **Auth Token**
4. Note the **WhatsApp number** (e.g., +14155238886)

### Step 4: Set Up ngrok (for local testing)

```bash
# Download ngrok from https://ngrok.com/download

# Run ngrok
ngrok http 8000

# You'll see:
# Forwarding: https://abc123.ngrok.io -> http://localhost:8000
```

### Step 5: Configure Twilio Webhook

1. In Twilio Console, go to **WhatsApp Sandbox Settings**
2. Under "When a message comes in":
   - Enter: `https://abc123.ngrok.io/webhook/whatsapp`
   - Method: `POST`
3. Click **Save**

### Step 6: Update .env

```env
MESSAGING_PROVIDER=twilio
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+14155238886
```

### Step 7: Restart Server

```bash
uvicorn app.main:app --reload
```

### Step 8: Test!

1. Open WhatsApp on your phone
2. Send a message to the Twilio number: **"show my parcels"**
3. You should get a response back!

## 🧪 Testing Modes

### Mock Mode (Default)
```env
MESSAGING_PROVIDER=mock
```
- No real messages sent
- Perfect for development
- Logs messages to console

### Twilio Mode (Production)
```env
MESSAGING_PROVIDER=twilio
```
- Real WhatsApp messages via Twilio
- Requires valid credentials
- Uses ngrok for local testing

## 📋 Available Endpoints

### Existing (Unchanged)
- `POST /message` - Direct API call (for testing)
- `POST /link` - Link farmer accounts
- `GET /` - Health check

### New
- `POST /webhook/whatsapp` - Twilio webhook (receives WhatsApp messages)
- `GET /webhook/whatsapp` - Webhook verification (for Meta migration)

## 🔍 How It Works

```
User sends WhatsApp message
        ↓
Twilio receives it
        ↓
Twilio calls: POST /webhook/whatsapp
        ↓
Your FastAPI server processes it
        ↓
intent_service.handle_message() (existing code!)
        ↓
messenger.send_message() (Twilio)
        ↓
User gets response in WhatsApp
```

## 🛠️ Troubleshooting

### Server starts but ngrok URL doesn't work
- Make sure ngrok is running: `ngrok http 8000`
- Check Twilio webhook URL matches ngrok URL
- Verify webhook method is POST

### "Twilio credentials not configured" error
- Check `.env` file has all three variables:
  - TWILIO_ACCOUNT_SID
  - TWILIO_AUTH_TOKEN
  - TWILIO_PHONE_NUMBER
- Restart server after updating .env

### Messages not sending
- Check MESSAGING_PROVIDER=twilio in .env
- Verify Twilio account is active
- Check logs for error messages

### Webhook returns 500 error
- Check server logs: `uvicorn app.main:app --reload`
- Verify database is initialized
- Test with `/message` endpoint first

## 🎯 Next Steps

### To switch to Meta WhatsApp Business API later:

1. Implement `app/integrations/meta_messenger.py`
2. Update `.env`:
   ```env
   MESSAGING_PROVIDER=meta
   META_ACCESS_TOKEN=your_token
   META_PHONE_NUMBER_ID=your_id
   ```
3. **No other code changes needed!** 🎉

## 📚 Architecture Benefits

✅ **Clean Separation**: Webhook handling separate from business logic  
✅ **Easy Testing**: Use mock messenger for tests  
✅ **Future-Proof**: Switch providers by changing .env  
✅ **Existing Code Intact**: Your intent_service.py unchanged  
✅ **Extensible**: Add new messengers easily

## 📞 Support

If you encounter issues:
1. Check server logs
2. Verify .env configuration
3. Test with mock mode first
4. Use Postman to test `/message` endpoint

---

**Status**: ✅ Ready to use!  
**Tests**: ✅ All 39 tests passing  
**Breaking Changes**: ❌ None!
