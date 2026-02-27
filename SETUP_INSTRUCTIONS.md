# Setup Instructions - AI Question Generation & Theme Fix

## Current Status

✅ **Database**: 107 questions (56 NEET, 51 JEE)
✅ **AI System**: Fully implemented with GPT-3.5-turbo (cost-efficient)
✅ **Oxford Blue Theme**: Applied to all pages
✅ **Timer**: Working with auto-submit
✅ **Test Interface**: One question per page with navigator

## Issues to Fix

### 1. Oxford Blue Theme Not Showing
**Problem**: Browser cache is showing old CSS
**Solution**: Clear browser cache

**Windows - Chrome/Edge:**
1. Press `Ctrl + Shift + Delete`
2. Select "Cached images and files"
3. Click "Clear data"
4. OR simply press `Ctrl + F5` to hard refresh

**Windows - Firefox:**
1. Press `Ctrl + Shift + Delete`
2. Select "Cache"
3. Click "Clear Now"

### 2. Only 9 Questions Generating
**Problem**: No OpenAI API key configured
**Solution**: Add your OpenAI API key

#### Step-by-Step:

**A. Get OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

**B. Add Key to .env File:**
1. Open `.env` file in your project
2. Find this line:
   ```
   # OPENAI_API_KEY=sk-your-api-key-here
   ```
3. Remove the `#` and replace with your actual key:
   ```
   OPENAI_API_KEY=sk-proj-your-actual-key-here
   ```
4. Save the file

**C. Restart Application:**
```bash
python run.py
```

### 3. Timer Not Working
**Problem**: Timer should be working now
**Solution**: Clear browser cache and restart app

## Testing the Fixes

### Test 1: Verify Theme
1. Clear browser cache (`Ctrl + F5`)
2. Go to http://127.0.0.1:5000
3. Check if colors are Oxford Blue (#002147)
4. All pages should have the new theme

### Test 2: Verify AI Question Generation
1. Add OpenAI API key to `.env`
2. Restart app: `python run.py`
3. Start any test (Adaptive/Full Paper/Subject)
4. Check console output - should see:
   ```
   ✓ Generated X AI questions for Physics (Medium)
   ```

### Test 3: Verify Timer
1. Start a test
2. Timer should count down from test duration
3. At 5 minutes remaining: warning appears
4. At 0:00: test auto-submits

### Test 4: Verify Question Count
**Adaptive Test**: Should generate 30 questions
**Full Paper**: Should generate 180 questions (45+45+90 for NEET, 60+60+60 for JEE)
**Subject Test**: Should generate 30 questions

## Cost Information

### OpenAI Pricing (GPT-3.5-turbo)
- **Input**: $0.50 per 1M tokens
- **Output**: $1.50 per 1M tokens

### Estimated Costs:
- **30 questions**: ~$0.02 - $0.05
- **180 questions**: ~$0.10 - $0.30
- **1000 questions**: ~$1.00 - $2.00

**Note**: GPT-3.5-turbo is 10x cheaper than GPT-4!

## Fallback System

If AI generation fails or API key is not configured:
1. System uses database questions (107 available)
2. Combines AI + database if needed
3. No errors - graceful fallback

## Question Distribution

### NEET Full Paper (180 questions):
- Physics: 45 questions (30% Easy, 50% Medium, 20% Hard)
- Chemistry: 45 questions (30% Easy, 50% Medium, 20% Hard)
- Biology: 90 questions (30% Easy, 50% Medium, 20% Hard)

### JEE Full Paper (180 questions):
- Physics: 60 questions (30% Easy, 50% Medium, 20% Hard)
- Chemistry: 60 questions (30% Easy, 50% Medium, 20% Hard)
- Mathematics: 60 questions (30% Easy, 50% Medium, 20% Hard)

### Adaptive Test (30 questions):
- Distributed across all subjects
- Difficulty based on user level

## Troubleshooting

### "Only 9 questions appearing"
- Add OpenAI API key to `.env`
- Restart application
- Check console for AI generation messages

### "Theme not changing"
- Clear browser cache: `Ctrl + F5`
- Try different browser
- Check if `style.css` has Oxford Blue colors

### "Timer not counting down"
- Clear browser cache
- Check browser console for JavaScript errors
- Ensure JavaScript is enabled

### "API key not working"
- Verify key starts with `sk-`
- Check for extra spaces in `.env`
- Ensure you have OpenAI credits
- Check API key is active at https://platform.openai.com/api-keys

## Next Steps

1. ✅ Clear browser cache
2. ✅ Add OpenAI API key
3. ✅ Restart application
4. ✅ Test all features
5. ✅ Verify 30+ questions generate

## Support

If issues persist:
1. Check console output for errors
2. Verify `.env` file configuration
3. Ensure all dependencies installed: `pip install -r requirements.txt`
4. Check OpenAI account has credits
