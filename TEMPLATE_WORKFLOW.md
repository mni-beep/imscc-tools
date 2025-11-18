# Template Workflow Guide

This guide shows how to use the template workflow to create Canvas courses locally with quizzes, assignments, and rubrics.

## Quick Start

### 1. Create a New Template

```bash
python3 create_template.py my-course
cd my-course
```

This creates a folder structure with examples:
```
my-course/
├── wiki_content/          # HTML pages
│   ├── welcome.html
│   ├── lesson-1.html
│   └── lesson-2.html
├── web_resources/         # Files (PDFs, images, etc.)
│   ├── syllabus.txt
│   └── week1-reading.txt
├── quizzes/              # Quiz definitions (JSON)
│   └── week-1-quiz.json
├── assignments/          # Assignment definitions (JSON)
│   └── week-1-homework.json
├── rubrics/              # Rubrics (JSON)
│   └── homework-rubric.json
├── course.json           # Course metadata
├── modules.json          # Module organization
└── README.md
```

### 2. Edit Your Content

**Pages**: Edit HTML files in `wiki_content/`
- Add metadata with `<!-- CANVAS_META -->` comments
- Link to files: `<a href="../web_resources/file.pdf">File</a>`
- Link to pages: `<a href="lesson-1.html">Lesson 1</a>`

**Files**: Add PDFs, images, etc. to `web_resources/`

**Quizzes**: Create/edit JSON files in `quizzes/`

**Assignments**: Create/edit JSON files in `assignments/`

**Rubrics**: Create/edit JSON files in `rubrics/`

### 3. Build IMSCC

```bash
python3 ../build_from_template.py .
```

This creates `COURSECODE.imscc` ready for Canvas import.

### 4. Import to Canvas

1. Go to your Canvas course
2. Settings → Import Course Content
3. Choose "Common Cartridge 1.x Package"
4. Upload the `.imscc` file
5. Import!

## Quiz Format

Create quizzes as JSON files in `quizzes/`:

```json
{
  "title": "Week 1 Quiz",
  "description": "<p>Test your knowledge</p>",
  "settings": {
    "quiz_type": "assignment",
    "allowed_attempts": 2,
    "time_limit": 20,
    "shuffle_questions": true,
    "shuffle_answers": true,
    "show_correct_answers": true,
    "one_question_at_a_time": false,
    "cant_go_back": false
  },
  "questions": [
    {
      "type": "multiple_choice",
      "text": "<p>What is 2 + 2?</p>",
      "answers": [
        {"text": "3", "correct": false},
        {"text": "4", "correct": true},
        {"text": "5", "correct": false}
      ],
      "points": 1.0
    },
    {
      "type": "true_false",
      "text": "<p>Python is compiled.</p>",
      "correct_answer": false,
      "points": 1.0
    },
    {
      "type": "fill_in_blank",
      "text": "<p>H2O is ___.</p>",
      "answers": ["water", "Water"],
      "points": 1.0
    }
  ]
}
```

### Supported Question Types

1. **multiple_choice** - One correct answer
2. **true_false** - True or false
3. **fill_in_blank** - Short text answer
4. **fill_in_multiple_blanks** - Multiple blanks with `[var1]`, `[var2]` syntax
5. **multiple_answers** - Select all that apply
6. **multiple_dropdowns** - Dropdowns embedded in text
7. **matching** - Match left to right columns
8. **numerical_answer** - Numeric with tolerance/range
9. **formula_question** - Calculated with variables
10. **essay_question** - Long-form text (manual grading)
11. **file_upload_question** - File upload (manual grading)
12. **text_only_question** - Informational (0 points)

See `quizzes/week-1-quiz.json` in your template for examples.

## Assignment Format

Create assignments as JSON files in `assignments/`:

```json
{
  "title": "Week 1 Homework",
  "description": "<p>Complete the exercises</p>",
  "points_possible": 100,
  "submission_types": ["online_upload"],
  "allowed_extensions": [".pdf", ".doc", ".docx"],
  "grading_type": "points",
  "assignment_group": "Homework",
  "rubric": "homework-rubric",
  "due_at": "2025-12-31T23:59:59Z"
}
```

### Assignment Properties

- **title**: Assignment name (required)
- **description**: HTML description
- **points_possible**: Total points (default: 100)
- **submission_types**: Array of submission types:
  - `"online_upload"` - File upload
  - `"online_text_entry"` - Text box
  - `"online_url"` - URL submission
  - `"none"` - No submission
- **allowed_extensions**: Array like `[".pdf", ".doc"]`
- **grading_type**: `"points"`, `"letter_grade"`, `"gpa_scale"`, `"percent"`, `"pass_fail"`, `"not_graded"`
- **assignment_group**: Name of assignment group (auto-created)
- **rubric**: Rubric ID (filename without `.csv`)
- **due_at**: ISO 8601 date/time

## Rubric Format

Create rubrics as JSON files in `rubrics/`:

```json
{
  "title": "Assignment Rubric",
  "criteria": [
    {
      "description": "Completeness",
      "long_description": "All required exercises are completed",
      "points": 30,
      "ratings": [
        {
          "description": "Excellent",
          "long_description": "All exercises completed with thorough work",
          "points": 30
        },
        {
          "description": "Good",
          "long_description": "Most exercises completed adequately",
          "points": 20
        },
        {
          "description": "Needs Work",
          "long_description": "Several exercises incomplete or missing",
          "points": 10
        }
      ]
    },
    {
      "description": "Correctness",
      "long_description": "Solutions are correct and accurate",
      "points": 40,
      "ratings": [
        {
          "description": "Excellent",
          "long_description": "All solutions correct with proper methodology",
          "points": 40
        },
        {
          "description": "Good",
          "long_description": "Most solutions correct with minor errors",
          "points": 30
        },
        {
          "description": "Needs Work",
          "long_description": "Multiple incorrect solutions or major errors",
          "points": 15
        }
      ]
    }
  ]
}
```

### Rubric Structure

- **title**: Rubric name (optional, defaults to filename)
- **criteria**: Array of criterion objects
  - **description**: Criterion name (e.g., "Quality", "Completeness")
  - **long_description**: Detailed explanation of the criterion
  - **points**: Maximum points for this criterion
  - **ratings**: Array of rating levels from best to worst
    - **description**: Rating name (e.g., "Excellent", "Good", "Poor")
    - **long_description**: Detailed explanation of what earns this rating
    - **points**: Points awarded for this rating level

## Module Organization

Edit `modules.json` to organize content with unified ordering:

```json
{
  "modules": [
    {
      "title": "Week 1: Introduction",
      "items": [
        {"type": "page", "id": "welcome"},
        {"type": "page", "id": "lesson-1"},
        {"type": "assignment", "id": "week-1-homework"},
        {"type": "quiz", "id": "week-1-quiz"}
      ]
    },
    {
      "title": "Week 2: Advanced Topics",
      "items": [
        {"type": "page", "id": "lesson-2"},
        {"type": "quiz", "id": "week-2-quiz"}
      ]
    }
  ]
}
```

### Item Types

- **page**: HTML page (id = filename without `.html`)
- **quiz**: Quiz (id = filename without `.json`)
- **assignment**: Assignment (id = filename without `.json`)

IDs must match the filenames in their respective folders.

## Page Metadata

Add metadata to HTML pages using HTML comments:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Welcome</title>
</head>
<body>
<!-- CANVAS_META
title: Welcome to the Course
home: true
-->

<h1>Welcome!</h1>
<p>This is the course home page.</p>

</body>
</html>
```

### Supported Metadata

- **title**: Page title (defaults to filename)
- **home**: Set to `true` to make this the course home page

## Course Configuration

Edit `course.json` to set course properties:

```json
{
  "title": "My Canvas Course",
  "course_code": "COURSE101",
  "default_view": "wiki",
  "description": "Course description here"
}
```

## Tips & Tricks

### Local Preview
All links work locally! Open any HTML page in your browser to preview.

### Link Conversion
The build script automatically converts:
- `../web_resources/file.pdf` → `$IMS-CC-FILEBASE$/web_resources/file.pdf`
- `lesson-1.html` → `$CANVAS_OBJECT_REFERENCE$/pages/lesson-1`

### Question Text with HTML
All question text fields support HTML:
```json
{
  "text": "<p>Question text with <strong>bold</strong> and <em>italics</em></p><ul><li>List item</li></ul>"
}
```

### Multiple Blanks Example
```json
{
  "type": "fill_in_multiple_blanks",
  "text": "<p>The primary colors are [color1], [color2], and [color3].</p>",
  "blanks": {
    "color1": ["red", "Red"],
    "color2": ["blue", "Blue"],
    "color3": ["yellow", "Yellow"]
  },
  "points": 3.0
}
```

### Matching Question Example
```json
{
  "type": "matching",
  "text": "<p>Match data structures:</p>",
  "matches": [
    {"prompt": "Stack", "answer": "LIFO"},
    {"prompt": "Queue", "answer": "FIFO"},
    {"prompt": "Hash", "answer": "O(1) lookup"}
  ],
  "distractors": ["O(n) lookup"],
  "points": 3.0
}
```

### Formula Question Example
```json
{
  "type": "formula_question",
  "text": "<p>Rectangle with length [len] and width [width], what is area?</p>",
  "formula": "[len] * [width]",
  "variables": {
    "len": [5.0, 15.0],
    "width": [3.0, 10.0]
  },
  "tolerance": 0.1,
  "points": 2.0
}
```

## Example Workflow

```bash
# Create template
python3 create_template.py biology-101
cd biology-101

# Edit content
# ... edit HTML pages, add quizzes, assignments, etc. ...

# Build IMSCC
python3 ../build_from_template.py .

# Import BIOLOGY101.imscc into Canvas
```

## Backwards Compatibility

The old `modules.json` format still works:

```json
{
  "modules": [
    {
      "title": "Week 1",
      "pages": ["welcome", "lesson-1"]
    }
  ]
}
```

This automatically converts to the new format internally.
