"""Module class for organizing content in IMSCC packages."""

from typing import Optional, List, Union
from .utils import generate_identifier


class ModuleItem:
    """Represents an item within a module."""
    
    def __init__(
        self,
        title: str,
        content_type: str,
        identifierref: str,
        identifier: Optional[str] = None,
        indent: int = 0,
        workflow_state: str = "active"
    ):
        """
        Create a module item.
        
        Args:
            title: Item title
            content_type: Type of content (WikiPage, Assignment, etc.)
            identifierref: Reference to the actual content resource
            identifier: Unique identifier for this item
            indent: Indentation level (0 = no indent)
            workflow_state: State (active, unpublished, etc.)
        """
        self.identifier = identifier or generate_identifier()
        self.title = title
        self.content_type = content_type
        self.identifierref = identifierref
        self.indent = indent
        self.workflow_state = workflow_state
        self.position = 0  # Set when added to module


class Module:
    """Represents a Canvas module for organizing course content."""
    
    def __init__(
        self,
        title: str,
        identifier: Optional[str] = None,
        workflow_state: str = "active",
        require_sequential_progress: bool = False,
        locked: bool = False
    ):
        """
        Create a new module.
        
        Args:
            title: Module title
            identifier: Unique identifier (auto-generated if not provided)
            workflow_state: State (active, unpublished, etc.)
            require_sequential_progress: Whether items must be completed in order
            locked: Whether module is locked
        """
        self.title = title
        self.identifier = identifier or generate_identifier()
        self.workflow_state = workflow_state
        self.require_sequential_progress = require_sequential_progress
        self.locked = locked
        self.items: List[ModuleItem] = []
        self.position = 0  # Set when added to course
    
    def add_item(
        self,
        title: str,
        content_type: str,
        identifierref: str,
        indent: int = 0
    ) -> "Module":
        """
        Add an item to this module (fluent interface).
        
        Args:
            title: Item title
            content_type: Type (WikiPage, Assignment, etc.)
            identifierref: Reference to the content resource
            indent: Indentation level
        
        Returns:
            Self for chaining
        """
        item = ModuleItem(
            title=title,
            content_type=content_type,
            identifierref=identifierref,
            indent=indent
        )
        item.position = len(self.items) + 1
        self.items.append(item)
        return self
    
    def add_page(self, page, indent: int = 0) -> "Module":
        """
        Add a WikiPage to this module.
        
        Args:
            page: WikiPage instance
            indent: Indentation level
        
        Returns:
            Self for chaining
        """
        return self.add_item(
            title=page.title,
            content_type="WikiPage",
            identifierref=page.identifier,
            indent=indent
        )
    
    def add_assignment(self, assignment, indent: int = 0) -> "Module":
        """
        Add an Assignment to this module.
        
        Args:
            assignment: Assignment instance
            indent: Indentation level
        
        Returns:
            Self for chaining
        """
        return self.add_item(
            title=assignment.title,
            content_type="Assignment",
            identifierref=assignment.identifier,
            indent=indent
        )
    
    def add_quiz(self, quiz, indent: int = 0) -> "Module":
        """
        Add a Quiz to this module.
        
        Args:
            quiz: Quiz instance
            indent: Indentation level
        
        Returns:
            Self for chaining
        """
        return self.add_item(
            title=quiz.title,
            content_type="Quiz",
            identifierref=quiz.identifier,
            indent=indent
        )
