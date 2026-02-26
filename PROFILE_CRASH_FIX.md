# Profile Page Crash Fix

## Issue
The profile page (Performance Analysis) was crashing when displaying test results.

## Root Cause
The score calculation was incorrect. The system uses negative marking:
- **Correct answer**: +4 marks
- **Wrong answer**: -1 mark
- **Unattempted**: 0 marks

This means:
- A test with 9 questions has a **maximum score of 36** (9 × 4)
- But the percentage calculation was treating it as `score / total_questions` instead of `score / max_score`

### Example of the Bug
```
Test with 9 questions, all correct:
- Score: 36 (9 × 4)
- Old calculation: 36 / 9 × 100 = 400% ❌ (WRONG!)
- New calculation: 36 / 36 × 100 = 100% ✅ (CORRECT!)
```

## Files Fixed

### 1. templates/profile.html
**Changed:**
- Score display: `{{ test.score }}/{{ test.total_questions }}` → `{{ test.score }}/{{ test.total_questions * 4 }}`
- Percentage calculation: Added `max_score = test.total_questions * 4`
- Chart data: Updated to use `max_score` instead of `total_questions`

**Before:**
```jinja
<td>{{ test.score }}/{{ test.total_questions }}</td>
<td>
    {% set percentage = ((test.score / test.total_questions * 100) if test.total_questions > 0 else 0) %}
    ...
</td>
```

**After:**
```jinja
<td>{{ test.score }}/{{ test.total_questions * 4 }}</td>
<td>
    {% set max_score = test.total_questions * 4 %}
    {% set percentage = ((test.score / max_score * 100) if max_score > 0 else 0) %}
    ...
</td>
```

### 2. templates/dashboard.html
**Changed:**
- Recent tests score display
- Percentage calculation in test history

**Before:**
```jinja
<div class="score-badge">{{ test.score }}/{{ test.total_questions }}</div>
{% set percentage = ((test.score / test.total_questions * 100) if test.total_questions > 0 else 0) %}
```

**After:**
```jinja
<div class="score-badge">{{ test.score }}/{{ test.total_questions * 4 }}</div>
{% set max_score = test.total_questions * 4 %}
{% set percentage = ((test.score / max_score * 100) if max_score > 0 else 0) %}
```

### 3. templates/test_results.html
**Status:** Already correct ✅
- This file was already using the correct calculation with `max_score`

## Verification

### Test Data
```
Test 1: 11 marks / 44 max (11 questions) = 25.0% ✅
Test 2: 36 marks / 36 max (9 questions) = 100.0% ✅
```

### Before Fix
- Profile page would crash or show 400% for perfect scores
- Dashboard would show incorrect percentages

### After Fix
- Profile page loads correctly
- All percentages are accurate (0-100%)
- Score displays show actual marks vs maximum marks

## Testing Steps

1. Start the application:
   ```bash
   python run.py
   ```

2. Login to the application

3. Navigate to Dashboard - verify recent tests show correct scores

4. Click "Performance Analysis" (Profile page) - should load without crashing

5. Verify:
   - Test history table shows correct scores (e.g., 36/36 instead of 36/9)
   - Percentages are between 0-100%
   - Performance chart displays correctly

## Status
✅ **FIXED** - Profile page now loads correctly with accurate score calculations

## Date
February 26, 2026
