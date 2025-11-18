# IMSCC Tools

A Python package for creating IMS Common Cartridge (IMSCC) files for importing into Canvas LMS.

## Two Workflows

### 1. Template-Based (Recommended for Course Development)

Work on your course content locally with HTML files and preview in your browser. Links work locally, then auto-convert to Canvas format.

```bash
# Create template
python3 create_template.py my-course

# Edit locally (preview in browser - all links work!)
cd my-course
open wiki_content/welcome.html

# Build IMSCC
python3 ../build_from_template.py .
```

**→ See [TEMPLATE_QUICK_START.md](TEMPLATE_QUICK_START.md) for details**

### 2. Programmatic (For Scripts & Automation)

Use Python to generate courses programmatically.

```python
from imscc import Course

course = Course(title="My Course", course_code="COURSE101")
course.add_page("Welcome", "<h1>Hello World</h1>")
course.export("my_course.imscc")
```

**→ See [QUICKSTART.md](QUICKSTART.md) and [REFERENCE.md](REFERENCE.md) for details**

## Features

- ✅ Create wiki pages with HTML content
- ✅ Organize content into modules
- ✅ **Create assignments with rubrics** ⭐ NEW
- ✅ **Assignment groups for gradebook organization** ⭐ NEW
- ✅ **Support for submission types and grading** ⭐ NEW
- ✅ Attach files and web resources
- ✅ Auto-generate unique identifiers
- ✅ Local development with working preview links
- ✅ Automatic link conversion for Canvas
- ✅ Extract existing IMSCC files as templates
- ✅ No external dependencies (uses Python standard library)

## Installation

```bash
pip install -e .
```

Or use directly without installation (just add the `imscc` directory to your project).

## Quick Start

### Simple Course with Pages

```python
from imscc import Course

course = Course(
    title="Introduction to Python",
    course_code="PYTHON101"
)

course.add_page(
    title="Welcome",
    content="<h1>Welcome!</h1><p>Let's learn Python.</p>"
)

course.export("my_course.imscc")
```

### Course with Modules

```python
from imscc import Course

course = Course(title="Web Development", course_code="WEB101")

# Create pages
intro = course.add_page("Introduction", "<h1>Welcome to Web Dev</h1>")
html = course.add_page("HTML Basics", "<h2>Learn HTML</h2>")
css = course.add_page("CSS Styling", "<h2>Learn CSS</h2>")

# Create module and add pages
module = course.create_module("Week 1: Fundamentals")
module.add_page(intro)
module.add_page(html, indent=1)  # Indent to show hierarchy
module.add_page(css, indent=1)

course.export("web_dev_course.imscc")
```

### Course with Assignments and Rubrics

```python
from imscc import Course, Assignment, Rubric

course = Course(title="Programming 101", course_code="CS101")

# Create assignment groups
homework = course.create_assignment_group("Homework", position=1, group_weight=40.0)
projects = course.create_assignment_group("Projects", position=2, group_weight=60.0)

# Simple assignment
assignment1 = Assignment(
    title="Week 1 Homework",
    description="<p>Complete the exercises.</p>",
    points_possible=100,
    submission_types="online_upload",
    allowed_extensions="py,ipynb",
    grading_type="points",
    workflow_state="published"
)
course.add_assignment(assignment1, homework)

# Assignment with rubric
rubric = Rubric(title="Project Rubric")
rubric.add_criterion(
    description="Code Quality",
    points=50,
    long_description="Code is clean and well-organized",
    ratings=[
        {"description": "Excellent", "points": 50, "long_description": "Perfect code"},
        {"description": "Good", "points": 40, "long_description": "Minor issues"},
        {"description": "Fair", "points": 25, "long_description": "Needs improvement"},
        {"description": "Poor", "points": 0, "long_description": "Poorly written"}
    ]
)
course.add_rubric(rubric)

assignment2 = Assignment(
    title="Final Project",
    description="<p>Build a complete application.</p>",
    points_possible=100,
    submission_types="online_upload",
    rubric_identifierref=rubric.identifier,
    workflow_state="published"
)
course.add_assignment(assignment2, projects)

# Add assignments to a module
module = course.create_module("Week 1")
module.add_assignment(assignment1)

course.export("course_with_assignments.imscc")
```

### Add Files and Resources

```python
from imscc import Course

course = Course(title="Game Development", course_code="GAME101")

# Add individual files
course.add_file("sprites/player.png", "web_resources/sprites/player.png")
course.add_file("sounds/jump.wav", "web_resources/sounds/jump.wav")

# Or add an entire directory
course.add_directory("game_assets", "web_resources")

# Reference files in your page content
page = course.add_page(
    title="Tutorial 1",
    content="""
    <h1>Resources</h1>
    <img src="$IMS-CC-FILEBASE$/web_resources/sprites/player.png" />
    """
)

course.export("game_course.imscc")
```

### Build from Local HTML Files

```python
from imscc import Course
import os

course = Course(title="My Course", course_code="COURSE101")

# Add pages from HTML files in a directory
for filename in os.listdir("content"):
    if filename.endswith(".html"):
        page = course.add_page_from_file(f"content/{filename}")

course.export("from_files.imscc")
```

### Extract Existing IMSCC as Template

```python
from imscc.utils import extract_imscc

# Extract an IMSCC file to examine/modify its structure
extract_imscc("existing_course.imscc", "template_output")

# Now you can:
# 1. Edit HTML files in template_output/wiki_content/
# 2. Add resources to template_output/web_resources/
# 3. Study the structure and recreate with this library
```

## Package Structure

```
imscc-tools/
├── imscc/                 # Main package
│   ├── __init__.py       # Package exports
│   ├── course.py         # Course class
│   ├── wiki_page.py      # WikiPage class
│   ├── module.py         # Module and ModuleItem classes
│   ├── resource.py       # FileResource and FileManager
│   └── utils.py          # Utility functions
├── examples.py           # Usage examples
├── requirements.txt      # Dependencies (none!)
├── setup.py             # Package setup
└── README.md            # This file
```

## API Reference

### Course

Main class for creating IMSCC packages.

```python
course = Course(
    title="Course Title",
    course_code="CODE101",      # Optional
    identifier=None,            # Auto-generated if not provided
    license="private",          # private, public, cc_by, etc.
    default_view="modules"      # modules, wiki, etc.
)

# Add content
page = course.add_page(title, content, workflow_state="active")
page = course.add_page_from_file(filepath, title=None)

# Add modules
module = course.create_module(title, **kwargs)
course.add_module(module)

# Add files
resource = course.add_file(filepath, destination_path=None)
resources = course.add_directory(directory, destination_prefix="web_resources")

# Export
course.export("output.imscc")
```

### WikiPage

Represents a Canvas wiki page.

```python
page = WikiPage(
    title="Page Title",
    content="<p>HTML content</p>",
    identifier=None,           # Auto-generated
    workflow_state="active",   # active, unpublished
    editing_roles="teachers"   # teachers, students
)

# Create from file
page = WikiPage.from_file("path/to/file.html", title=None)

# Get HTML output
html = page.to_html()
```

### Module

Organizes content into modules.

```python
module = Module(
    title="Module Title",
    identifier=None,                    # Auto-generated
    workflow_state="active",
    require_sequential_progress=False,
    locked=False
)

# Add items
module.add_item(title, content_type, identifierref, indent=0)
module.add_page(page, indent=0)  # Helper for WikiPages
```

### Utilities

```python
from imscc.utils import generate_identifier, extract_imscc

# Generate Canvas-style identifier
id = generate_identifier(prefix="g")  # Returns: "gabc123..."

# Extract IMSCC file
extract_imscc("course.imscc", "output_directory")
```

## Examples

Run the included examples:

```bash
python examples.py
```

This will create several example IMSCC files in the `output` directory demonstrating different features.

## File Structure in IMSCC

An IMSCC file is a ZIP archive with this structure:

```
course.imscc (ZIP file)
├── imsmanifest.xml              # Main manifest
├── course_settings/
│   ├── course_settings.xml      # Course metadata
│   ├── module_meta.xml          # Module definitions
│   ├── files_meta.xml           # File metadata
│   ├── context.xml              # Context info
│   └── media_tracks.xml         # Media tracks
├── wiki_content/
│   └── page-name.html           # Wiki page files
└── web_resources/
    └── ...                      # Files and resources
```

## Workflow

### 1. Local Development Workflow

```bash
# 1. Create content directory
mkdir my_course_content
cd my_course_content

# 2. Create HTML files for pages
echo "<h1>Page 1</h1>" > page1.html
echo "<h1>Page 2</h1>" > page2.html

# 3. Add any resources
mkdir resources
# ... add images, files, etc.

# 4. Create Python script to package
```

```python
from imscc import Course
import glob

course = Course(title="My Course", course_code="COURSE")

# Add all HTML files as pages
for html_file in glob.glob("*.html"):
    course.add_page_from_file(html_file)

# Add resources
course.add_directory("resources", "web_resources")

# Export
course.export("my_course.imscc")
```

```bash
# 5. Upload to Canvas
# Import the .imscc file through Canvas course settings
```

### 2. Template-Based Workflow

```python
from imscc.utils import extract_imscc

# Extract existing course as template
extract_imscc("template.imscc", "template")

# Edit files in template/wiki_content/
# Add resources to template/web_resources/

# Rebuild using this library
from imscc import Course

course = Course(title="New Course")
# ... add content based on template structure
course.export("new_course.imscc")
```

## Coming Soon

- 🔲 Assignments
- 🔲 Quizzes
- 🔲 Discussions
- 🔲 External tools (LTI)
- 🔲 Assignment groups
- 🔲 Grading rubrics

## License

MIT License - feel free to use in your projects!

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.
