# Template-Based Workflow Summary

## Two Scripts for Local Course Development

### 1. `create_template.py` - Create New Course Template

**Purpose:** Generate a complete course folder structure with example content.

**Usage:**
```bash
python3 create_template.py my-course-name
```

**Creates:**
```
my-course-name/
├── wiki_content/          # HTML pages (editable locally)
│   ├── welcome.html       # Home page with file & page links
│   ├── lesson-1.html      # Example lesson
│   └── lesson-2.html      # Example lesson
├── web_resources/         # Files (PDFs, images, etc.)
│   ├── syllabus.txt
│   ├── week1-reading.txt
│   └── resources.txt
├── course.json           # Course metadata (title, code, etc.)
├── modules.json          # Module organization
└── README.md            # Instructions
```

**Key Features:**
- All links work locally for preview in browser
- No server needed
- Example content shows best practices

---

### 2. `build_from_template.py` - Convert to IMSCC

**Purpose:** Convert local template folder to Canvas IMSCC file.

**Usage:**
```bash
# From within course folder
cd my-course-name
python3 ../build_from_template.py .

# Or from outside
python3 build_from_template.py my-course-name

# Custom output name
python3 build_from_template.py my-course-name -o course-v2.imscc
```

**What it does:**
1. ✅ Reads `course.json` for course metadata (or uses defaults)
2. ✅ Reads `modules.json` for module organization
3. ✅ Parses HTML files for `<!-- CANVAS_META -->` metadata
4. ✅ Converts local links to Canvas tokens:
   - `../web_resources/file.txt` → `$IMS-CC-FILEBASE$/web_resources/file.txt`
   - `lesson-1.html` → `$CANVAS_OBJECT_REFERENCE$/pages/lesson-1`
5. ✅ Copies all files from `web_resources/`
6. ✅ Generates complete IMSCC ready for Canvas import

---

## Complete Workflow

```bash
# 1. CREATE TEMPLATE
python3 create_template.py biology-101

# 2. WORK LOCALLY
cd biology-101

# Edit pages
vim wiki_content/welcome.html
vim wiki_content/lesson-1.html

# Add files
cp ~/syllabus.pdf web_resources/
cp ~/readings.pdf web_resources/

# Preview in browser (all links work!)
open wiki_content/welcome.html

# Configure course
vim course.json      # Set title, course code
vim modules.json     # Organize pages into modules

# 3. BUILD IMSCC
python3 ../build_from_template.py .

# 4. IMPORT TO CANVAS
# Upload biology-101.imscc via Canvas → Settings → Import Course Content
```

---

## Page Metadata Format

Add metadata using HTML comments at the top of each page:

```html
<!DOCTYPE html>
<html>
<body>
<!-- CANVAS_META
title: Welcome to Biology 101
home: true
-->

<h1>Welcome!</h1>
<p><a href="../web_resources/syllabus.pdf">Download Syllabus</a></p>
<p><a href="lesson-1.html">Start Lesson 1</a></p>

</body>
</html>
```

**Metadata fields:**
- `title`: Page title in Canvas (defaults to filename if omitted)
- `home`: Set to `true` to make this the course home page

---

## Link Formats

### Files (PDFs, images, documents)

**Local (for preview):**
```html
<a href="../web_resources/syllabus.pdf">Syllabus</a>
<img src="../web_resources/diagram.png" />
```

**Auto-converted to Canvas format:**
```html
<a href="$IMS-CC-FILEBASE$/web_resources/syllabus.pdf">Syllabus</a>
<img src="$IMS-CC-FILEBASE$/web_resources/diagram.png" />
```

### Pages (other wiki pages)

**Local (for preview):**
```html
<a href="lesson-1.html">Go to Lesson 1</a>
<a href="welcome.html">Back to Home</a>
```

**Auto-converted to Canvas format:**
```html
<a href="$CANVAS_OBJECT_REFERENCE$/pages/lesson-1">Go to Lesson 1</a>
<a href="$CANVAS_OBJECT_REFERENCE$/pages/welcome">Back to Home</a>
```

---

## Module Organization

Edit `modules.json` to organize pages:

```json
{
  "modules": [
    {
      "title": "Week 1: Getting Started",
      "pages": ["welcome", "lesson-1"]
    },
    {
      "title": "Week 2: Core Concepts",
      "pages": ["lesson-2", "practice"]
    }
  ]
}
```

- Page names = filename without `.html`
- Pages appear in order listed
- Optional: leave empty `[]` for no modules

---

## Course Configuration

Edit `course.json`:

```json
{
  "title": "Introduction to Biology",
  "course_code": "BIO101",
  "default_view": "wiki",
  "description": "An introductory biology course"
}
```

**If `course.json` is missing:** Sensible defaults are used based on folder name.

---

## Example: Quick Start

```bash
# Create template
python3 create_template.py test-course

# Examine the example
cd test-course
open wiki_content/welcome.html  # Preview in browser - click the links!

# Build IMSCC
python3 ../build_from_template.py .

# Result: COURSE101.imscc ready for Canvas import
```

---

## Benefits of This Workflow

✅ **Local Preview** - Open HTML files directly in browser, all links work  
✅ **No Dependencies** - Just HTML, no special tools needed to edit  
✅ **Version Control** - Track changes with Git  
✅ **Team Collaboration** - Multiple people can work on same course  
✅ **File Organization** - Organize files in subdirectories  
✅ **Automatic Conversion** - Links automatically converted to Canvas format  
✅ **Reusable** - Edit locally, rebuild IMSCC, re-import to Canvas  

---

## For More Details

- **TEMPLATE_WORKFLOW.md** - Complete workflow guide with examples
- **README.md** - General IMSCC tools documentation
- **REFERENCE.md** - Python API reference for programmatic use

---

## Demo Course

A demo course template has been created at `demo-course/`:

```bash
cd demo-course
open wiki_content/welcome.html  # Preview in browser
python3 ../build_from_template.py .  # Build IMSCC
```
