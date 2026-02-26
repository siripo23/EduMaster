# Testing Guide for Enhanced Test System

## Current Status
✅ Flask app is running successfully on http://127.0.0.1:5000
✅ Database has 17 sample questions (NEET and JEE)
✅ All new routes are implemented and working
✅ Enhanced test interface with security features is ready

## Features to Test

### 1. Test Start Page (`/test/start/<test_type>`)
**What to test:**
- Navigate to dashboard after login
- Click on any test type card (Adaptive, Full Mock, Subject-wise)
- Verify the test instructions page loads
- Check that test details are displayed (questions count, duration)
- Verify the "I agree" checkbox works
- Click "Start Test" button

**Expected behavior:**
- Instructions page shows test rules
- Timer duration is displayed correctly
- Checkbox must be checked before starting
- Redirects to actual test page after clicking Start

### 2. Enhanced Test Interface (`/test/take/<test_type>`)
**What to test:**
- Timer countdown (should auto-submit when reaches 0)
- Question navigation (click on question numbers)
- Answer selection (radio buttons)
- Mark for review functionality
- Fullscreen enforcement
- Tab switching detection
- Copy/paste prevention
- Dev tools detection

**Expected behavior:**
- Timer counts down from specified duration
- Can navigate between questions
- Selected answers are highlighted
- Marked questions show different color
- Fullscreen mode is enforced
- Warning on first tab switch, auto-submit on second
- Cannot copy/paste in test area
- Warning if dev tools are opened

### 3. Test Submission and Results
**What to test:**
- Submit test manually
- Auto-submit when timer expires
- Auto-submit on security violations
- View results page

**Expected behavior:**
- Shows correct/wrong/unattempted breakdown
- Displays negative marking calculation (+4 correct, -1 wrong)
- Shows final score and percentage
- Displays subject-wise performance

### 4. Test Types Available

#### Initial Test
- **Route:** `/test/start/initial`
- **Questions:** 25
- **Duration:** 60 minutes
- **Purpose:** Level detection for new users

#### Adaptive Test
- **Route:** `/test/start/adaptive`
- **Questions:** 30
- **Duration:** 90 minutes
- **Purpose:** AI-generated based on weak areas

#### Full Mock Test
- **Route:** `/test/start/full_paper`
- **Questions:** 180 (NEET: 45 Physics, 45 Chemistry, 90 Biology | JEE: 60 each)
- **Duration:** 180 minutes
- **Purpose:** Complete exam simulation

#### Subject-wise Tests
- **Physics:** `/test/start/subject_Physics`
- **Chemistry:** `/test/start/subject_Chemistry`
- **Biology/Mathematics:** `/test/start/subject_Biology` or `/test/start/subject_Mathematics`
- **Questions:** 30 each
- **Duration:** 45 minutes

## Security Features Implemented

### 1. Fullscreen Enforcement
- Test automatically enters fullscreen mode
- Exiting fullscreen triggers warning and auto-submit

### 2. Tab Switching Detection
- First switch: Warning message
- Second switch: Auto-submit test

### 3. Copy/Paste Prevention
- Copy, cut, paste disabled in test area
- Right-click context menu disabled

### 4. Dev Tools Detection
- Detects if browser dev tools are opened
- Shows warning message

### 5. Auto-save
- Answers saved every 30 seconds
- Prevents data loss

## Testing Checklist

- [ ] Login to the application
- [ ] Navigate to dashboard
- [ ] Verify all test type cards are visible
- [ ] Click on "Adaptive Test" card
- [ ] Verify test start page loads with instructions
- [ ] Check the "I agree" checkbox
- [ ] Click "Start Test" button
- [ ] Verify test interface loads in fullscreen
- [ ] Check timer is counting down
- [ ] Answer a few questions
- [ ] Try to switch tabs (should show warning)
- [ ] Try to exit fullscreen (should show warning)
- [ ] Navigate between questions using question palette
- [ ] Mark a question for review
- [ ] Submit the test
- [ ] Verify results page shows:
  - Correct answers count
  - Wrong answers count
  - Unattempted questions count
  - Final score with negative marking
  - Percentage
- [ ] Return to dashboard
- [ ] Try subject-wise test (Physics/Chemistry/Biology or Mathematics)
- [ ] Verify resources page works

## Known Limitations

1. **Sample Data:** Only 17 questions available, so full mock tests may not have enough questions
2. **Resources:** PDF files are placeholders, actual files need to be added
3. **Email/SMS:** Password reset currently shows token in flash message (needs email integration)

## Next Steps

1. Add more questions to database (at least 200+ per subject)
2. Collect actual past year papers and textbooks
3. Implement email/SMS for password reset
4. Add topic-wise test functionality
5. Implement performance analytics graphs
6. Add question bookmarking feature
7. Create practice mode (without timer/negative marking)

## Troubleshooting

### If test page doesn't load:
- Check browser console for JavaScript errors
- Verify Flask app is running
- Check if questions exist in database

### If timer doesn't work:
- Check browser console for errors
- Verify JavaScript file is loaded
- Check if duration is passed correctly

### If fullscreen doesn't work:
- Some browsers block fullscreen API
- Try different browser (Chrome/Firefox recommended)
- Check browser permissions

### If answers aren't saved:
- Check browser console for AJAX errors
- Verify session is active
- Check Flask logs for errors

## Support

For issues or questions, check:
1. Flask app logs (in terminal where `python run.py` is running)
2. Browser console (F12 → Console tab)
3. Network tab (F12 → Network tab) for failed requests
