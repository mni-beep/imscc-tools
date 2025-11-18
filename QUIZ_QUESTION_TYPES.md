# Canvas Quiz Question Types - Complete Implementation

This document describes all 11 Canvas quiz question types now supported by imscc-tools.

## Implemented Question Types

### 1. Multiple Choice Question
**Class:** `MultipleChoiceQuestion`

Students select **one** correct answer from multiple options.

```python
MultipleChoiceQuestion(
    question_text="<p>What is the capital of France?</p>",
    answers=[
        {"text": "London", "correct": False},
        {"text": "Paris", "correct": True},
        {"text": "Berlin", "correct": False},
        {"text": "Madrid", "correct": False}
    ],
    points_possible=1.0
)
```

### 2. True/False Question
**Class:** `TrueFalseQuestion`

Simple true or false question.

```python
TrueFalseQuestion(
    question_text="<p>Python is a compiled language.</p>",
    correct_answer=False,
    points_possible=1.0
)
```

### 3. Fill in the Blank
**Class:** `FillInBlankQuestion`

Students type a short answer that matches exactly (or one of several acceptable answers).

```python
FillInBlankQuestion(
    question_text="<p>The chemical symbol for water is ___.</p>",
    answers=["H2O", "h2o"],  # Multiple acceptable answers
    points_possible=1.0
)
```

### 4. Fill in Multiple Blanks
**Class:** `FillInMultipleBlanksQuestion`

Multiple fill-in-the-blank responses within the same question. Use `[variable_name]` syntax in the question text.

```python
FillInMultipleBlanksQuestion(
    question_text="<p>The primary colors are [color1], [color2], and [color3].</p>",
    blanks={
        "color1": ["red", "Red"],
        "color2": ["blue", "Blue"],
        "color3": ["yellow", "Yellow"]
    },
    points_possible=3.0
)
```

### 5. Multiple Answers
**Class:** `MultipleAnswersQuestion`

Students can select **multiple** correct answers (checkboxes instead of radio buttons).

```python
MultipleAnswersQuestion(
    question_text="<p>Which of the following are programming languages? (Select all that apply)</p>",
    answers=[
        {"text": "Python", "correct": True},
        {"text": "HTML", "correct": False},
        {"text": "Java", "correct": True},
        {"text": "CSS", "correct": False},
        {"text": "JavaScript", "correct": True}
    ],
    points_possible=2.0
)
```

### 6. Multiple Dropdowns
**Class:** `MultipleDropdownsQuestion`

Multiple dropdown selections embedded within the question text. Use `[variable_name]` syntax.

```python
MultipleDropdownsQuestion(
    question_text="<p>In the equation E = mc[exponent], energy equals [particle] times the speed of [wave] squared.</p>",
    dropdowns={
        "exponent": [
            {"text": "1", "correct": False},
            {"text": "2", "correct": True},
            {"text": "3", "correct": False}
        ],
        "particle": [
            {"text": "mass", "correct": True},
            {"text": "velocity", "correct": False}
        ],
        "wave": [
            {"text": "sound", "correct": False},
            {"text": "light", "correct": True}
        ]
    },
    points_possible=3.0
)
```

### 7. Matching Question
**Class:** `MatchingQuestion`

Students match items from the left column to items in the right column.

```python
MatchingQuestion(
    question_text="<p>Match each data structure with its description:</p>",
    matches=[
        {"prompt": "Stack", "answer": "Last In, First Out (LIFO)"},
        {"prompt": "Queue", "answer": "First In, First Out (FIFO)"},
        {"prompt": "Hash Table", "answer": "Key-value pairs with O(1) lookup"}
    ],
    distractors=["Linked list with circular references"],  # Extra wrong answers
    points_possible=3.0
)
```

### 8. Numerical Answer
**Class:** `NumericalAnswerQuestion`

Students enter a numerical value. Supports exact answers with margin of error or answer ranges.

```python
# Exact answer with margin
NumericalAnswerQuestion(
    question_text="<p>What is the value of π (pi) to two decimal places?</p>",
    exact_answer=3.14,
    margin=0.01,  # Accept 3.13 to 3.15
    points_possible=1.0
)

# Answer range
NumericalAnswerQuestion(
    question_text="<p>How many days are in a year?</p>",
    answer_range=(365, 366),  # Accept 365 or 366
    points_possible=1.0
)
```

### 9. Formula Question (Calculated)
**Class:** `FormulaQuestion`

Answer is calculated from variables with random values. Canvas generates different versions for each student.

```python
FormulaQuestion(
    question_text="<p>A rectangle has length [length] meters and width [width] meters. What is its area?</p>",
    formula="[length] * [width]",
    variables={
        "length": (5.0, 15.0),  # Random value between 5 and 15
        "width": (3.0, 10.0)    # Random value between 3 and 10
    },
    tolerance=0.1,
    points_possible=2.0
)
```

### 10. Essay Question
**Class:** `EssayQuestion`

Students write a long-form text response. Requires manual grading.

```python
EssayQuestion(
    question_text="""<p>In 200-300 words, explain the difference between 
    compiled and interpreted programming languages. Include at least two 
    examples of each.</p>""",
    points_possible=10.0
)
```

### 11. File Upload Question
**Class:** `FileUploadQuestion`

Students upload a file as their answer. Requires manual grading.

```python
FileUploadQuestion(
    question_text="<p>Upload a Python script that prints 'Hello, World!' to the console.</p>",
    points_possible=5.0
)
```

### Bonus: Text Only (Informational)
**Class:** `TextOnlyQuestion`

Displays information without requiring an answer. Worth 0 points.

```python
TextOnlyQuestion(
    question_text="""<h3>Important Notice</h3>
    <p>The following questions are bonus questions.</p>
    <p>Good luck!</p>"""
)
```

## Complete Example

See `all_question_types_demo.py` for a comprehensive example showing all question types in a single quiz.

```bash
python3 all_question_types_demo.py
```

This creates `all-question-types.imscc` with 12 questions (one of each type) totaling 32 points.

## Technical Details

### QTI 1.2 Format
All questions are exported in QTI 1.2 (IMS Question & Test Interoperability) format, which is the standard used by Canvas LMS.

### Question Structure
Each question generates:
- **Item metadata** with question type and points
- **Presentation section** with question text and response fields
- **Response processing** with correct answer conditions and scoring

### Response Types
Different question types use different QTI response types:
- `response_lid` - Multiple choice, Multiple answers, Multiple dropdowns
- `response_str` - Fill in blank, Essay, File upload, Numerical
- `response_grp` - Matching questions

### Constructor Pattern
All question classes follow this pattern:
```python
def __init__(
    self, 
    question_text: str,           # HTML supported
    # ... type-specific parameters ...
    points_possible: float = 1.0,
    identifier: Optional[str] = None  # Auto-generated if not provided
):
```

## Quiz Settings

Quizzes support comprehensive Canvas settings:

```python
Quiz(
    title="My Quiz",
    description="<p>Quiz description</p>",
    quiz_type="assignment",  # or "practice_quiz", "graded_survey", "survey"
    points_possible=None,  # Auto-calculated from questions
    allowed_attempts=1,
    scoring_policy="keep_highest",  # or "keep_latest", "keep_average"
    shuffle_questions=False,
    shuffle_answers=False,
    show_correct_answers=True,
    one_question_at_a_time=False,
    cant_go_back=False,
    time_limit=None  # Minutes, or None for unlimited
)
```

## Files Updated

- `imscc/quiz.py` - All 11 question type classes
- `imscc/__init__.py` - Export all question types
- `all_question_types_demo.py` - Comprehensive demo
- `comprehensive_demo.py` - Full course with quizzes
- `quiz_types_reference.py` - Quiz configuration examples

## Testing

All question types have been tested and successfully export to valid IMSCC packages that can be imported into Canvas LMS.

```bash
# Test all question types
python3 all_question_types_demo.py

# Test comprehensive course
python3 comprehensive_demo.py

# Test quiz configurations
python3 quiz_types_reference.py
```
