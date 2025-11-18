# My Canvas Course

This is a **comprehensive Canvas course template** created with the IMSCC tools, demonstrating all available features.

## 🎯 Template Files

All example files are tagged with `_TEMPLATE` in their filenames for easy identification and removal:

- **Pages:** `welcome_TEMPLATE.html`, `lesson-1_TEMPLATE.html`, `lesson-2_TEMPLATE.html`
- **Files:** `syllabus_TEMPLATE.txt`, `week1-reading_TEMPLATE.txt`, `resources_TEMPLATE.txt`
- **Quiz:** `comprehensive-quiz_TEMPLATE.json` (demonstrates all 12 question types)
- **Assignment:** `comprehensive-assignment_TEMPLATE.json` (with rubric integration)
- **Rubric:** `comprehensive-rubric_TEMPLATE.json` (5 criteria with detailed rating descriptions)

**To remove templates:** Delete all files containing `_TEMPLATE` when you're ready to add your own content.

## 📁 Folder Structure

```
ICTSAS305/
├── wiki_content/                            # HTML pages for your course
│   ├── welcome_TEMPLATE.html                # Home page example
│   ├── lesson-1_TEMPLATE.html               # Lesson page with file links
│   └── lesson-2_TEMPLATE.html               # Lesson page with navigation
├── web_resources/                           # Files (PDFs, images, documents)
│   ├── syllabus_TEMPLATE.txt                # Example syllabus
│   ├── week1-reading_TEMPLATE.txt           # Example reading material
│   └── resources_TEMPLATE.txt               # Example resources
├── quizzes/                                 # Quiz definitions (JSON)
│   └── comprehensive-quiz_TEMPLATE.json     # All 12 question types!
├── assignments/                             # Assignment definitions (JSON)
│   └── comprehensive-assignment_TEMPLATE.json
├── rubrics/                                 # Rubrics (JSON format)
│   └── comprehensive-rubric_TEMPLATE.json   # 5 criteria, 5 ratings each
├── course.json                              # Course metadata
├── modules.json                             # Module organization
└── README.md                                # This file
```

## 🚀 Working Locally

1. **Edit pages**: Open HTML files in `wiki_content/` with your favorite editor
2. **Preview**: Open HTML files directly in your browser - all links work locally!
3. **Add files**: Place PDFs, images, etc. in `web_resources/`
4. **Create content**: Add quizzes, assignments, and rubrics as JSON files
5. **Organize**: Update `modules.json` to organize all content into modules

## 📄 Page Metadata

Each page can have metadata in HTML comments at the top:

```html
<!-- CANVAS_META
title: My Page Title
home: true
-->
```

Supported metadata:
- `title`: Page title (defaults to filename)
- `home`: Set to `true` to make this the course home page

## 🔗 Linking

### Link to files:
```html
<a href="../web_resources/syllabus.txt">Syllabus</a>
```

### Link to other pages:
```html
<a href="lesson-1.html">Go to Lesson 1</a>
```

These links work locally for preview. When you export to IMSCC, they're automatically
converted to Canvas format.

## Export to IMSCC

When ready to upload to Canvas:

```bash
python3 build_from_template.py ICTSAS305
```

This will create `COURSE101.imscc` that you can import into Canvas.

## 📊 Quizzes

Create quiz files in `quizzes/` using JSON format. The template includes a comprehensive example with **all 12 question types**:

### Question Types Supported:
1. **`multiple_choice`** - One correct answer from multiple options
2. **`true_false`** - Simple true or false question
3. **`fill_in_blank`** - Short text answer (exact match)
4. **`fill_in_multiple_blanks`** - Multiple blanks with different answers
5. **`multiple_answers`** - Select all correct answers (checkboxes)
6. **`multiple_dropdowns`** - Multiple dropdown menus in text
7. **`matching`** - Match items between two columns
8. **`numerical_answer`** - Numeric answer with tolerance/range
9. **`formula_question`** - Calculated question with variables
10. **`essay_question`** - Long-form text response (manual grading)
11. **`file_upload_question`** - File submission (manual grading)
12. **`text_only_question`** - Informational text (0 points)

See `comprehensive-quiz_TEMPLATE.json` for examples of each type!

### Quiz Settings:
```json
{
  "title": "My Quiz",
  "description": "<p>Quiz description</p>",
  "settings": {
    "quiz_type": "assignment",
    "allowed_attempts": 2,
    "time_limit": 30,
    "shuffle_questions": true,
    "shuffle_answers": true,
    "show_correct_answers": true,
    "one_question_at_a_time": false,
    "cant_go_back": false,
    "scoring_policy": "keep_highest"
  },
  "questions": [...]
}
```

## 📋 Assignments

Create assignment files in `assignments/` using JSON format:

```json
{
  "title": "Assignment Title",
  "description": "<p>Assignment instructions</p>",
  "points_possible": 100,
  "submission_types": ["online_upload", "online_text_entry"],
  "allowed_extensions": [".pdf", ".doc", ".docx"],
  "grading_type": "points",
  "assignment_group": "Assignments",
  "rubric": "rubric-filename"
}
```

**Submission Types:** `online_upload`, `online_text_entry`, `online_url`, `media_recording`

## 📏 Rubrics

Create rubrics in `rubrics/` as JSON files. The template includes a detailed example with 5 criteria and 5 rating levels each:

```json
{
  "title": "Rubric Title",
  "criteria": [
    {
      "description": "Criterion Name",
      "long_description": "Detailed description of what this criterion evaluates",
      "points": 25,
      "ratings": [
        {
          "description": "Exemplary",
          "long_description": "Detailed description of exemplary performance",
          "points": 25
        },
        {
          "description": "Proficient",
          "long_description": "Detailed description of proficient performance",
          "points": 20
        }
      ]
    }
  ]
}
```

**Note:** Both criteria and ratings support `long_description` for detailed feedback guidance.

## 📚 Module Organization

Edit `modules.json` to organize all content types into modules:

```json
{
  "modules": [
    {
      "title": "Week 1",
      "items": [
        {"type": "page", "id": "welcome"},
        {"type": "page", "id": "lesson-1"},
        {"type": "quiz", "id": "week-1-quiz"},
        {"type": "assignment", "id": "homework-1"}
      ]
    }
  ]
}
```

**Content Types:** `page`, `quiz`, `assignment`  
**IDs:** Match filenames without extensions (e.g., `welcome_TEMPLATE.html` → `"id": "welcome_TEMPLATE"`)

## 🔨 Export to IMSCC

When ready to upload to Canvas:

```bash
python3 build_from_template.py ICTSAS305
```

This will create `COURSE101.imscc` that you can import into Canvas.

## 💡 Tips

1. **Preview locally**: All links work in your browser before exporting
2. **Easy cleanup**: Delete all `_TEMPLATE` files when ready to add your content
3. **Reference examples**: Keep template files while learning the system
4. **Comprehensive examples**: Check the quiz file to see all 12 question types in action
5. **Rubric details**: Use `long_description` fields for clear grading criteria
