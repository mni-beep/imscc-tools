"""
IMSCC (IMS Common Cartridge) Package Creator for Canvas LMS

This package provides tools to create IMSCC files for importing into Canvas.
"""

from .course import Course
from .wiki_page import WikiPage
from .module import Module
from .resource import FileResource
from .assignment import Assignment, AssignmentGroup, Rubric
from .quiz import (
    Quiz, QuizQuestion,
    MultipleChoiceQuestion, TrueFalseQuestion,
    FillInBlankQuestion, FillInMultipleBlanksQuestion,
    MultipleAnswersQuestion, MultipleDropdownsQuestion,
    MatchingQuestion, NumericalAnswerQuestion,
    FormulaQuestion, EssayQuestion,
    FileUploadQuestion, TextOnlyQuestion
)
from .utils import generate_identifier, extract_imscc

__version__ = "0.1.0"
__all__ = [
    "Course",
    "WikiPage",
    "Module",
    "FileResource",
    "Assignment",
    "AssignmentGroup",
    "Rubric",
    "Quiz",
    "QuizQuestion",
    "MultipleChoiceQuestion",
    "TrueFalseQuestion",
    "FillInBlankQuestion",
    "FillInMultipleBlanksQuestion",
    "MultipleAnswersQuestion",
    "MultipleDropdownsQuestion",
    "MatchingQuestion",
    "NumericalAnswerQuestion",
    "FormulaQuestion",
    "EssayQuestion",
    "FileUploadQuestion",
    "TextOnlyQuestion",
    "generate_identifier",
    "extract_imscc",
]
