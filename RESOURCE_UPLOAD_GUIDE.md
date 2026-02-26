# Resource Upload Guide - Adding Past Year Papers & Textbooks

## Overview
This guide explains how to add past year question papers and textbooks to your NEET/JEE Learning App.

## Method 1: Manual Upload (Recommended)

### Step 1: Download Resources

#### NEET Past Papers
**Official Source**: https://nta.ac.in
- Go to NTA website
- Navigate to NEET section
- Download question papers from previous years (2024, 2023, 2022, 2021, etc.)

#### JEE Main Past Papers
**Official Source**: https://nta.ac.in
- Go to NTA website
- Navigate to JEE Main section
- Download question papers from previous years

#### JEE Advanced Past Papers
**Official Source**: https://jeeadv.ac.in
- Go to JEE Advanced official website
- Download question papers from previous years

#### NCERT Textbooks
**Official Source**: https://ncert.nic.in/textbook.php
- Download Class 11 & 12 textbooks for:
  - Physics (Part 1 & 2)
  - Chemistry (Part 1 & 2)
  - Biology (Part 1 & 2)
  - Mathematics (Part 1 & 2)

### Step 2: Organize Files

Create a folder structure and rename files for easy identification:

```
Downloads/
├── NEET/
│   ├── neet_2024.pdf
│   ├── neet_2023.pdf
│   ├── neet_2022.pdf
│   └── neet_2021.pdf
│
├── JEE_Main/
│   ├── jee_main_2024.pdf
│   ├── jee_main_2023.pdf
│   └── jee_main_2022.pdf
│
├── JEE_Advanced/
│   ├── jee_advanced_2024.pdf
│   └── jee_advanced_2023.pdf
│
└── NCERT/
    ├── ncert_physics_11.pdf
    ├── ncert_physics_12.pdf
    ├── ncert_chemistry_11.pdf
    ├── ncert_chemistry_12.pdf
    ├── ncert_biology_11.pdf
    ├── ncert_biology_12.pdf
    ├── ncert_math_11.pdf
    └── ncert_math_12.pdf
```

### Step 3: Copy Files to Project

Copy all PDF files to your project's resources folder:

**Windows:**
```cmd
# Navigate to your project
cd C:\Users\a\Desktop\EduMaster

# Copy files (example)
copy "C:\Users\a\Downloads\neet_2024.pdf" "static\resources\"
copy "C:\Users\a\Downloads\jee_main_2024.pdf" "static\resources\"
```

**Or simply:**
1. Open File Explorer
2. Navigate to your Downloads folder
3. Select all PDF files
4. Copy them (Ctrl+C)
5. Navigate to `C:\Users\a\Desktop\EduMaster\static\resources\`
6. Paste them (Ctrl+V)

### Step 4: Update Database

Run the script to add resources to database:

```bash
python add_resources.py
```

**Output:**
```
✓ Added: NEET 2024 Question Paper
✓ Added: NEET 2023 Question Paper
✓ Added: JEE Main 2024 Question Paper
...
============================================================
Resources added successfully!
Total resources added: 18
Total resources in database: 18
============================================================
```

### Step 5: Verify in Application

1. Start your app: `python run.py`
2. Login to your account
3. Go to "Resources" page
4. You should see all uploaded papers and textbooks

## Method 2: Bulk Upload with Custom Script

If you have many files, you can modify the script:

### Step 1: Create a CSV file with resource details

Create `resources_list.csv`:
```csv
title,resource_type,subject,file_path,stream,year
NEET 2024 Question Paper,past_paper,All Subjects,/static/resources/neet_2024.pdf,NEET,2024
NEET 2023 Question Paper,past_paper,All Subjects,/static/resources/neet_2023.pdf,NEET,2023
JEE Main 2024,past_paper,All Subjects,/static/resources/jee_main_2024.pdf,JEE,2024
```

### Step 2: Create import script

```python
import csv
from app import app
from models import db, Resource

with app.app_context():
    with open('resources_list.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            resource = Resource(
                title=row['title'],
                resource_type=row['resource_type'],
                subject=row['subject'],
                file_path=row['file_path'],
                stream=row['stream'],
                year=int(row['year']) if row['year'] else None
            )
            db.session.add(resource)
    db.session.commit()
    print("Resources imported successfully!")
```

## File Naming Convention

### Recommended Format:
- **NEET Papers**: `neet_YYYY.pdf` (e.g., `neet_2024.pdf`)
- **JEE Main**: `jee_main_YYYY.pdf` (e.g., `jee_main_2024.pdf`)
- **JEE Advanced**: `jee_advanced_YYYY.pdf` (e.g., `jee_advanced_2024.pdf`)
- **NCERT Books**: `ncert_subject_class.pdf` (e.g., `ncert_physics_11.pdf`)

### Why This Format?
- Easy to identify
- Sortable by year
- Consistent naming
- No spaces (web-friendly)

## Updating Existing Resources

If you need to update a resource:

### Option 1: Delete and Re-add
```python
from app import app
from models import db, Resource

with app.app_context():
    # Delete old resource
    old_resource = Resource.query.filter_by(title='NEET 2024 Question Paper').first()
    if old_resource:
        db.session.delete(old_resource)
    
    # Add new resource
    new_resource = Resource(
        title='NEET 2024 Question Paper',
        resource_type='past_paper',
        subject='All Subjects',
        file_path='/static/resources/neet_2024_updated.pdf',
        stream='NEET',
        year=2024
    )
    db.session.add(new_resource)
    db.session.commit()
```

### Option 2: Update Existing
```python
from app import app
from models import db, Resource

with app.app_context():
    resource = Resource.query.filter_by(title='NEET 2024 Question Paper').first()
    if resource:
        resource.file_path = '/static/resources/neet_2024_updated.pdf'
        db.session.commit()
```

## Checking Resources in Database

To see what resources are currently in the database:

```python
from app import app
from models import Resource

with app.app_context():
    # Get all resources
    resources = Resource.query.all()
    
    print(f"Total Resources: {len(resources)}\n")
    
    # Group by stream
    neet_resources = Resource.query.filter_by(stream='NEET').all()
    jee_resources = Resource.query.filter_by(stream='JEE').all()
    
    print(f"NEET Resources: {len(neet_resources)}")
    for r in neet_resources:
        print(f"  - {r.title} ({r.year if r.year else 'N/A'})")
    
    print(f"\nJEE Resources: {len(jee_resources)}")
    for r in jee_resources:
        print(f"  - {r.title} ({r.year if r.year else 'N/A'})")
```

## Troubleshooting

### Issue 1: File Not Found Error
**Problem**: PDF shows in database but gives 404 error when downloading

**Solution**: 
- Check file path is correct: `/static/resources/filename.pdf`
- Verify file exists in `static/resources/` folder
- Check file name matches exactly (case-sensitive)

### Issue 2: Large File Size
**Problem**: PDF files are too large (>50MB)

**Solution**:
- Compress PDFs using online tools
- Split large files into smaller parts
- Use PDF optimization tools

### Issue 3: Resources Not Showing
**Problem**: Resources added to database but not showing on page

**Solution**:
- Check stream filter (NEET vs JEE)
- Verify resource_type is correct ('past_paper' or 'textbook')
- Restart Flask application
- Clear browser cache

## Best Practices

### 1. File Organization
- Keep all resources in `static/resources/` folder
- Use subfolders if needed: `static/resources/neet/`, `static/resources/jee/`
- Update file paths in database accordingly

### 2. File Naming
- Use lowercase
- Use underscores instead of spaces
- Include year for past papers
- Be consistent

### 3. Database Management
- Run `add_resources.py` after adding new files
- Keep a backup of your database
- Document what resources you've added

### 4. Legal Compliance
- Only upload official papers from NTA/government websites
- Don't upload copyrighted material without permission
- NCERT books are freely available from official website

## Quick Reference Commands

```bash
# Add resources to database
python add_resources.py

# Check resources in database
python -c "from app import app; from models import Resource; app.app_context().push(); print(f'Total: {Resource.query.count()}')"

# Start application
python run.py

# Initialize database (if needed)
python init_db.py
```

## Example Workflow

1. **Download** PDFs from official websites
2. **Rename** files following naming convention
3. **Copy** files to `static/resources/` folder
4. **Run** `python add_resources.py`
5. **Verify** by visiting Resources page in app
6. **Done!** Resources are now available for download

## Support

If you encounter any issues:
1. Check file paths are correct
2. Verify files exist in resources folder
3. Check database entries
4. Restart Flask application
5. Clear browser cache

## Summary

✅ Download PDFs from official sources
✅ Organize and rename files
✅ Copy to `static/resources/` folder
✅ Run `add_resources.py` script
✅ Verify in application

That's it! Your resources are now available to all users.
