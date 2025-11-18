"""Assignment classes for Canvas assignments, groups, and rubrics."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from .utils import generate_identifier, slugify


class Assignment:
    """Represents a Canvas assignment."""
    
    def __init__(
        self,
        title: str,
        description: str = "",
        points_possible: float = 0.0,
        submission_types: str = "none",
        identifier: Optional[str] = None,
        assignment_group_identifierref: Optional[str] = None,
        workflow_state: str = "published",
        grading_type: str = "points",
        allowed_extensions: str = "",
        due_at: Optional[str] = None,
        unlock_at: Optional[str] = None,
        lock_at: Optional[str] = None,
        position: int = 1,
        rubric: Optional['Rubric'] = None,
        **kwargs
    ):
        """
        Create a new assignment.
        
        Args:
            title: Assignment title
            description: HTML description/instructions
            points_possible: Maximum points for the assignment
            submission_types: Comma-separated list of submission types
                (none, online_upload, online_text_entry, online_url, etc.)
            identifier: Unique identifier (auto-generated if not provided)
            assignment_group_identifierref: Assignment group identifier
            workflow_state: published or unpublished
            grading_type: points, percent, letter_grade, gpa_scale, pass_fail, not_graded
            allowed_extensions: Comma-separated file extensions for uploads (e.g., "pdf,doc,docx")
            due_at: Due date in ISO format or datetime object
            unlock_at: Unlock date in ISO format or datetime object
            lock_at: Lock date in ISO format or datetime object
            position: Position in assignment list
            rubric: Optional Rubric object
            **kwargs: Additional Canvas assignment properties
        """
        self.title = title
        self.description = description
        self.points_possible = points_possible
        self.submission_types = submission_types
        self.identifier = identifier or generate_identifier()
        self.assignment_group_identifierref = assignment_group_identifierref
        self.workflow_state = workflow_state
        self.grading_type = grading_type
        self.allowed_extensions = allowed_extensions
        self.due_at = self._format_date(due_at) if due_at else ""
        self.unlock_at = self._format_date(unlock_at) if unlock_at else ""
        self.lock_at = self._format_date(lock_at) if lock_at else ""
        self.position = position
        self.rubric = rubric
        
        # Default values for other Canvas properties
        self.module_locked = kwargs.get('module_locked', False)
        self.all_day = kwargs.get('all_day', False)
        self.turnitin_enabled = kwargs.get('turnitin_enabled', False)
        self.vericite_enabled = kwargs.get('vericite_enabled', False)
        self.peer_reviews = kwargs.get('peer_reviews', False)
        self.automatic_peer_reviews = kwargs.get('automatic_peer_reviews', False)
        self.anonymous_peer_reviews = kwargs.get('anonymous_peer_reviews', False)
        self.peer_review_count = kwargs.get('peer_review_count', 0)
        self.grade_group_students_individually = kwargs.get('grade_group_students_individually', False)
        self.freeze_on_copy = kwargs.get('freeze_on_copy', False)
        self.omit_from_final_grade = kwargs.get('omit_from_final_grade', False)
        self.hide_in_gradebook = kwargs.get('hide_in_gradebook', False)
        self.has_group_category = kwargs.get('has_group_category', False)
        self.intra_group_peer_reviews = kwargs.get('intra_group_peer_reviews', False)
        self.only_visible_to_overrides = kwargs.get('only_visible_to_overrides', False)
        self.post_to_sis = kwargs.get('post_to_sis', False)
        self.moderated_grading = kwargs.get('moderated_grading', False)
        self.grader_count = kwargs.get('grader_count', 0)
        self.grader_comments_visible_to_graders = kwargs.get('grader_comments_visible_to_graders', True)
        self.anonymous_grading = kwargs.get('anonymous_grading', False)
        self.graders_anonymous_to_graders = kwargs.get('graders_anonymous_to_graders', False)
        self.grader_names_visible_to_final_grader = kwargs.get('grader_names_visible_to_final_grader', True)
        self.anonymous_instructor_annotations = kwargs.get('anonymous_instructor_annotations', False)
        self.post_manually = kwargs.get('post_manually', False)
        
    def _format_date(self, date: Any) -> str:
        """Convert date to ISO format string."""
        if isinstance(date, datetime):
            return date.isoformat()
        elif isinstance(date, str):
            return date
        return ""
    
    @property
    def slug(self) -> str:
        """Generate a slug from the title."""
        return slugify(self.title)
    
    def attach_rubric(self, rubric: 'Rubric') -> 'Assignment':
        """Attach a rubric to this assignment.
        
        Args:
            rubric: The Rubric to attach
            
        Returns:
            Self for method chaining
        """
        self.rubric = rubric
        return self
    
    def to_xml(self) -> str:
        """
        Generate XML string for assignment_settings.xml.
        
        Returns:
            Formatted XML string
        """
        assignment = Element(
            'assignment',
            identifier=self.identifier,
            xmlns="http://canvas.instructure.com/xsd/cccv1p0",
            attrib={
                'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
                'xsi:schemaLocation': "http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd"
            }
        )
        
        # Add elements in the order they appear in Canvas exports
        SubElement(assignment, 'title').text = self.title
        
        # Add dates
        SubElement(assignment, 'due_at').text = self.due_at
        SubElement(assignment, 'lock_at').text = self.lock_at
        SubElement(assignment, 'unlock_at').text = self.unlock_at
        
        SubElement(assignment, 'module_locked').text = str(self.module_locked).lower()
        
        # Assignment group reference
        if self.assignment_group_identifierref:
            SubElement(assignment, 'assignment_group_identifierref').text = self.assignment_group_identifierref
        
        SubElement(assignment, 'workflow_state').text = self.workflow_state
        
        # Rubric references if rubric is attached
        if self.rubric:
            SubElement(assignment, 'rubric_identifierref').text = self.rubric.identifier
            SubElement(assignment, 'rubric_use_for_grading').text = str(self.rubric.use_for_grading).lower()
            SubElement(assignment, 'rubric_hide_points').text = str(self.rubric.hide_points).lower()
            SubElement(assignment, 'rubric_hide_outcome_results').text = str(self.rubric.hide_outcome_results).lower()
            SubElement(assignment, 'rubric_hide_score_total').text = str(self.rubric.hide_score_total).lower()
        
        # Assignment overrides (empty for now)
        SubElement(assignment, 'assignment_overrides')
        
        # Allowed extensions for file uploads
        SubElement(assignment, 'allowed_extensions').text = self.allowed_extensions
        
        SubElement(assignment, 'has_group_category').text = str(self.has_group_category).lower()
        SubElement(assignment, 'points_possible').text = str(self.points_possible)
        SubElement(assignment, 'grading_type').text = self.grading_type
        SubElement(assignment, 'all_day').text = str(self.all_day).lower()
        SubElement(assignment, 'submission_types').text = self.submission_types
        SubElement(assignment, 'position').text = str(self.position)
        
        # Plagiarism detection
        SubElement(assignment, 'turnitin_enabled').text = str(self.turnitin_enabled).lower()
        SubElement(assignment, 'vericite_enabled').text = str(self.vericite_enabled).lower()
        
        # Peer reviews
        SubElement(assignment, 'peer_review_count').text = str(self.peer_review_count)
        SubElement(assignment, 'peer_reviews').text = str(self.peer_reviews).lower()
        SubElement(assignment, 'automatic_peer_reviews').text = str(self.automatic_peer_reviews).lower()
        SubElement(assignment, 'anonymous_peer_reviews').text = str(self.anonymous_peer_reviews).lower()
        
        # Other settings
        SubElement(assignment, 'grade_group_students_individually').text = str(self.grade_group_students_individually).lower()
        SubElement(assignment, 'freeze_on_copy').text = str(self.freeze_on_copy).lower()
        SubElement(assignment, 'omit_from_final_grade').text = str(self.omit_from_final_grade).lower()
        SubElement(assignment, 'hide_in_gradebook').text = str(self.hide_in_gradebook).lower()
        SubElement(assignment, 'intra_group_peer_reviews').text = str(self.intra_group_peer_reviews).lower()
        SubElement(assignment, 'only_visible_to_overrides').text = str(self.only_visible_to_overrides).lower()
        SubElement(assignment, 'post_to_sis').text = str(self.post_to_sis).lower()
        
        # Moderated grading
        SubElement(assignment, 'moderated_grading').text = str(self.moderated_grading).lower()
        SubElement(assignment, 'grader_count').text = str(self.grader_count)
        SubElement(assignment, 'grader_comments_visible_to_graders').text = str(self.grader_comments_visible_to_graders).lower()
        SubElement(assignment, 'anonymous_grading').text = str(self.anonymous_grading).lower()
        SubElement(assignment, 'graders_anonymous_to_graders').text = str(self.graders_anonymous_to_graders).lower()
        SubElement(assignment, 'grader_names_visible_to_final_grader').text = str(self.grader_names_visible_to_final_grader).lower()
        SubElement(assignment, 'anonymous_instructor_annotations').text = str(self.anonymous_instructor_annotations).lower()
        
        # Post policy
        post_policy = SubElement(assignment, 'post_policy')
        SubElement(post_policy, 'post_manually').text = str(self.post_manually).lower()
        
        # Convert to formatted string
        rough_string = tostring(assignment, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding='UTF-8').decode('utf-8')
    
    def get_html_content(self) -> str:
        """
        Generate HTML content for the assignment description file.
        
        Returns:
            HTML string
        """
        return f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>Assignment: {self.title}</title>
</head>
<body>
{self.description}
</body>
</html>"""


class AssignmentGroup:
    """Represents a Canvas assignment group."""
    
    def __init__(
        self,
        title: str,
        position: int = 1,
        group_weight: float = 0.0,
        identifier: Optional[str] = None
    ):
        """
        Create an assignment group.
        
        Args:
            title: Group title
            position: Position in group list
            group_weight: Weight for weighted grading (0-100)
            identifier: Unique identifier (auto-generated if not provided)
        """
        self.title = title
        self.position = position
        self.group_weight = group_weight
        self.identifier = identifier or generate_identifier()
    
    def to_xml(self) -> Element:
        """Generate XML element for assignment group."""
        group = Element('assignmentGroup', identifier=self.identifier)
        SubElement(group, 'title').text = self.title
        SubElement(group, 'position').text = str(self.position)
        SubElement(group, 'group_weight').text = str(self.group_weight)
        return group


class Rubric:
    """Represents a Canvas rubric."""
    
    def __init__(
        self,
        title: str,
        criteria: Optional[List[Dict[str, Any]]] = None,
        identifier: Optional[str] = None,
        points_possible: Optional[float] = None,
        read_only: bool = False,
        reusable: bool = False,
        public: bool = False,
        hide_score_total: bool = False,
        free_form_criterion_comments: bool = False,
        use_for_grading: bool = True,
        hide_points: bool = False,
        hide_outcome_results: bool = False
    ):
        """
        Create a rubric.
        
        Args:
            title: Rubric title
            criteria: List of criterion dictionaries
            identifier: Unique identifier (auto-generated if not provided)
            points_possible: Total points (calculated from criteria if not provided)
            read_only: Whether rubric is read-only
            reusable: Whether rubric can be reused
            public: Whether rubric is public
            hide_score_total: Hide the score total
            free_form_criterion_comments: Allow free-form comments
            use_for_grading: Use rubric for grading
            hide_points: Hide points from students
            hide_outcome_results: Hide outcome results
        """
        self.title = title
        self.criteria = criteria or []
        self.identifier = identifier or generate_identifier()
        self.read_only = read_only
        self.reusable = reusable
        self.public = public
        self.hide_score_total = hide_score_total
        self.free_form_criterion_comments = free_form_criterion_comments
        self.use_for_grading = use_for_grading
        self.hide_points = hide_points
        self.hide_outcome_results = hide_outcome_results
        
        # Calculate total points if not provided
        if points_possible is None:
            self.points_possible = sum(c.get('points', 0) for c in self.criteria)
        else:
            self.points_possible = points_possible
    
    def add_criterion(
        self,
        description: str,
        points: float,
        long_description: str = "",
        ratings: Optional[List[Dict[str, Any]]] = None,
        criterion_id: Optional[str] = None
    ) -> 'Rubric':
        """
        Add a criterion to the rubric.
        
        Args:
            description: Short description
            points: Maximum points for this criterion
            long_description: Detailed description
            ratings: List of rating dictionaries with description, points, long_description
            criterion_id: Optional criterion ID (auto-generated if not provided)
        
        Returns:
            Self for chaining
        """
        if criterion_id is None:
            criterion_id = f"_{len(self.criteria) + 1000}"
        
        criterion = {
            'criterion_id': criterion_id,
            'description': description,
            'points': points,
            'long_description': long_description,
            'ratings': ratings or []
        }
        
        self.criteria.append(criterion)
        self.points_possible = sum(c.get('points', 0) for c in self.criteria)
        return self
    
    def to_xml(self) -> Element:
        """Generate XML element for rubric."""
        rubric = Element('rubric', identifier=self.identifier)
        
        SubElement(rubric, 'read_only').text = str(self.read_only).lower()
        SubElement(rubric, 'title').text = self.title
        SubElement(rubric, 'reusable').text = str(self.reusable).lower()
        SubElement(rubric, 'public').text = str(self.public).lower()
        SubElement(rubric, 'points_possible').text = str(self.points_possible)
        SubElement(rubric, 'hide_score_total').text = str(self.hide_score_total).lower()
        SubElement(rubric, 'free_form_criterion_comments').text = str(self.free_form_criterion_comments).lower()
        
        # Add criteria
        criteria_elem = SubElement(rubric, 'criteria')
        for criterion in self.criteria:
            criterion_elem = SubElement(criteria_elem, 'criterion')
            SubElement(criterion_elem, 'criterion_id').text = criterion['criterion_id']
            SubElement(criterion_elem, 'points').text = str(criterion['points'])
            SubElement(criterion_elem, 'description').text = criterion['description']
            SubElement(criterion_elem, 'long_description').text = criterion.get('long_description', '')
            
            # Add ratings
            ratings_elem = SubElement(criterion_elem, 'ratings')
            for rating in criterion.get('ratings', []):
                rating_elem = SubElement(ratings_elem, 'rating')
                SubElement(rating_elem, 'description').text = rating.get('description', '')
                SubElement(rating_elem, 'points').text = str(rating.get('points', 0))
                SubElement(rating_elem, 'criterion_id').text = criterion['criterion_id']
                SubElement(rating_elem, 'long_description').text = rating.get('long_description', '')
                SubElement(rating_elem, 'id').text = rating.get('id', 'blank')
        
        return rubric
