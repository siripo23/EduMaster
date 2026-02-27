# CSS Troubleshooting Guide - Oxford Blue Theme

## Issue: Theme Colors Not Showing

You mentioned clearing cache but colors still not changing. Let's diagnose and fix this.

## Step 1: Test CSS Loading

1. Start your app:
   ```bash
   python run.py
   ```

2. Open this diagnostic page:
   ```
   http://127.0.0.1:5000/css-test
   ```

3. You should see an alert telling you if CSS loaded correctly

## Step 2: Clear Cache Properly

### Method 1: Hard Refresh (Recommended)
```
Windows: Ctrl + Shift + R
Or: Ctrl + F5
```

### Method 2: Clear Browser Cache Completely
**Chrome/Edge:**
1. Press `Ctrl + Shift + Delete`
2. Select "All time"
3. Check "Cached images and files"
4. Click "Clear data"

**Firefox:**
1. Press `Ctrl + Shift + Delete`
2. Select "Everything"
3. Check "Cache"
4. Click "Clear Now"

### Method 3: Disable Cache in DevTools
1. Press `F12` to open DevTools
2. Go to Network tab
3. Check "Disable cache"
4. Keep DevTools open
5. Refresh page

## Step 3: Verify CSS File

Check if CSS file is being served:

1. Open: http://127.0.0.1:5000/static/css/style.css?v=2.0
2. You should see CSS code starting with:
   ```css
   :root {
       --oxford-blue: #002147;
   ```

If you see 404 error, the file path is wrong.

## Step 4: Check Browser Console

1. Press `F12` to open DevTools
2. Go to Console tab
3. Look for errors like:
   - "Failed to load resource: style.css"
   - "404 Not Found"
   - "MIME type error"

## Step 5: Verify in DevTools

1. Press `F12`
2. Go to Elements tab
3. Find `<nav class="navbar">`
4. Look at Styles panel on right
5. Check if you see:
   ```css
   .navbar {
       background: var(--oxford-blue) !important;
   }
   ```

6. Check Computed tab
7. Look for `background-color`
8. Should show: `rgb(0, 33, 71)` which is #002147

## Common Issues & Fixes

### Issue 1: CSS File Not Loading

**Symptoms**: 
- Page looks like plain Bootstrap
- No Oxford Blue colors anywhere
- DevTools shows 404 for style.css

**Fix**:
```bash
# Check if file exists
dir static\css\style.css

# If missing, file was deleted
# Restore from backup or recreate
```

### Issue 2: CSS Variables Not Working

**Symptoms**:
- Some colors work, others don't
- Inline styles work but classes don't

**Fix**:
- Old browser version (update browser)
- CSS syntax error (check console)

### Issue 3: Bootstrap Overriding Styles

**Symptoms**:
- Bootstrap blue instead of Oxford Blue
- Some elements styled, others not

**Fix**:
- Added `!important` to critical styles
- Inline backup styles in base.html

### Issue 4: Cache Not Clearing

**Symptoms**:
- Still see old colors after clearing cache
- Changes not reflecting

**Fix**:
1. Close ALL browser windows
2. Reopen browser
3. Try different browser (Firefox, Edge, Chrome)
4. Try incognito/private mode

## Step 6: Manual Verification

Open any page and check these elements:

### Navbar
- Should be: Dark blue (#002147)
- Text: White
- If not: CSS not loading

### Cards
- Headers: Dark blue (#002147)
- Body: White
- Border: Light gray

### Buttons
- Primary: Dark blue (#002147)
- Hover: Lighter blue (#003d82)

## Step 7: Force CSS Reload

I've added cache-busting to base.html:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}?v=2.0">
```

The `?v=2.0` forces browser to reload CSS.

## Step 8: Inline Styles Backup

I've added inline styles to base.html as backup:
```html
<style>
    :root {
        --oxford-blue: #002147;
    }
    .navbar {
        background: #002147 !important;
    }
</style>
```

This ensures navbar is ALWAYS Oxford Blue, even if external CSS fails.

## Step 9: Test Different Pages

Visit these pages and check colors:

1. Home: http://127.0.0.1:5000/
   - Hero section should have gradients
   - Navbar should be Oxford Blue

2. Login: http://127.0.0.1:5000/login
   - Card should have Oxford Blue header

3. Dashboard: http://127.0.0.1:5000/dashboard (after login)
   - Welcome section should be gradient
   - Cards should have Oxford Blue accents

4. CSS Test: http://127.0.0.1:5000/css-test
   - All boxes should be Oxford Blue
   - Alert should say "CSS LOADED CORRECTLY"

## Step 10: Browser-Specific Issues

### Chrome/Edge
- Clear site data: DevTools → Application → Clear storage
- Disable extensions that might interfere

### Firefox
- Clear cache: Ctrl+Shift+Delete
- Disable "Remember history" temporarily

### Safari
- Develop → Empty Caches
- Preferences → Advanced → Show Develop menu

## Step 11: Server-Side Check

Restart Flask app to ensure latest files:

```bash
# Stop app (Ctrl+C)
# Start again
python run.py
```

Check console output for errors.

## Step 12: File Permissions

Ensure CSS file is readable:

```bash
# Windows
icacls static\css\style.css

# Should show read permissions
```

## Expected Results

After following these steps, you should see:

✅ Navbar: Oxford Blue (#002147)
✅ Card headers: Oxford Blue
✅ Primary buttons: Oxford Blue
✅ Welcome sections: Blue gradients
✅ All pages: Consistent theme

## Still Not Working?

If colors still not showing after ALL steps:

### Option 1: Check CSS Content
```bash
# Open CSS file
notepad static\css\style.css

# First lines should be:
# :root {
#     --oxford-blue: #002147;
```

### Option 2: Recreate CSS File

If CSS file is corrupted:

1. Delete: `static\css\style.css`
2. I'll recreate it with correct content

### Option 3: Use Different Browser

Try these browsers in order:
1. Chrome (latest)
2. Firefox (latest)
3. Edge (latest)
4. Brave

### Option 4: Check Flask Static Files

```python
# Test in Python
python -c "from flask import Flask; app = Flask(__name__); print(app.static_folder)"
```

Should output: `static`

## Debug Commands

Run these to diagnose:

```bash
# Check CSS file exists and size
dir static\css\style.css

# Check CSS content
type static\css\style.css | findstr "oxford-blue"

# Should output: --oxford-blue: #002147;
```

## Contact Info

If still not working after all steps:

1. Take screenshot of:
   - Home page
   - CSS test page
   - Browser DevTools Console tab
   - Browser DevTools Network tab (showing style.css)

2. Run diagnostic:
   ```bash
   python test_system.py
   ```

3. Check output of Test 4 (Theme Files)

## Quick Fix Summary

```bash
# 1. Stop app
Ctrl+C

# 2. Start app
python run.py

# 3. Open CSS test
# Go to: http://127.0.0.1:5000/css-test

# 4. Hard refresh
Ctrl + Shift + R

# 5. Check alert message
# Should say "CSS LOADED CORRECTLY"
```

## Success Indicators

You'll know it's working when:

1. CSS test page shows all blue boxes
2. Alert says "CSS LOADED CORRECTLY"
3. Navbar is dark blue (#002147)
4. All pages have consistent Oxford Blue theme
5. No console errors in DevTools

---

**Last Updated**: February 27, 2026
**Status**: Troubleshooting guide complete
