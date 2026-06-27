from app.achievements.achievement_service_engine import AchievementServiceEngine
from app.autonomous_action_engine.autonomous_action_engine_engine import (
    AutonomousActionEngine,
)
from app.autonomous_research_engine.autonomous_research_engine_engine import (
    AutonomousResearchEngine,
)
from app.activity_recognition_agent.activity_recognition_agent_engine import (
    ActivityRecognitionAgentEngine,
)
from app.avatar_animations.avatar_animation_service_engine import (
    AvatarAnimationServiceEngine,
)
from app.awards.award_service_engine import AwardServiceEngine
from app.bookmarks.bookmark_engine import BookmarkEngine
from app.browser_agent.browser_agent_engine import BrowserAgentEngine
from app.certifications.certification_service_engine import CertificationServiceEngine
from app.conferences.conference_service_engine import ConferenceServiceEngine
from app.conversation_manager.conversation_manager_engine import (
    ConversationManagerEngine,
)
from app.conversation_intelligence.conversation_intelligence_engine import (
    ConversationIntelligenceEngine,
)
from app.cognitive_growth_tracker.cognitive_growth_tracker_engine import (
    CognitiveGrowthTrackerEngine,
)
from app.contacts.contact_engine import ContactEngine
from app.courses.course_service_engine import CourseServiceEngine
from app.brain.brain_engine import BrainEngine
from app.chat.chat_engine import ChatEngine
from app.chat.conversation_history import ConversationHistory
from app.consciousness.goal_engine import GoalEngine
from app.consciousness.habit_engine import HabitEngine
from app.consciousness.mood_engine import MoodEngine
from app.consciousness.presence_engine import PresenceEngine
from app.consciousness.proactive_engine import ProactiveEngine
from app.context_fusion_engine.context_fusion_engine_engine import ContextFusionEngine
from app.context.context_engine import ContextEngine
from app.decision.decision_engine import DecisionEngine
from app.docx_reader_agent.docx_reader_agent_engine import DOCXReaderAgentEngine
from app.education.education_service_engine import EducationServiceEngine
from app.emotions.emotion_service_engine import EmotionServiceEngine
from app.emotional_intelligence_tracker.emotional_intelligence_tracker_engine import (
    EmotionalIntelligenceTrackerEngine,
)
from app.emotion_recognition_agent.emotion_recognition_agent_engine import (
    EmotionRecognitionAgentEngine,
)
from app.experience.experience_service_engine import ExperienceServiceEngine
from app.file_knowledge_extraction_agent.file_knowledge_extraction_agent_engine import (
    FileKnowledgeExtractionAgentEngine,
)
from app.face_recognition_agent.face_recognition_agent_engine import (
    FaceRecognitionAgentEngine,
)
from app.facial_expressions.facial_expression_service_engine import (
    FacialExpressionServiceEngine,
)
from app.goal_tracker.goal_tracker_engine import GoalTrackerEngine
from app.goals.goal_service_engine import GoalServiceEngine
from app.goal_execution_agent.goal_execution_agent_engine import GoalExecutionAgentEngine
from app.habits.habit_service_engine import HabitServiceEngine
from app.history.history_engine import HistoryEngine
from app.image_understanding_agent.image_understanding_agent_engine import (
    ImageUnderstandingAgentEngine,
)
from app.interests.interest_service_engine import InterestServiceEngine
from app.intelligence_quotient_tracker.intelligence_quotient_tracker_engine import (
    IntelligenceQuotientTrackerEngine,
)
from app.journals.journal_service_engine import JournalServiceEngine
from app.knowledge.knowledge_engine import KnowledgeEngine
from app.knowledge_gap_detector.knowledge_gap_detector_engine import (
    KnowledgeGapDetectorEngine,
)
from app.learning.learning_engine import LearningEngine
from app.learning_tracker.learning_tracker_engine import LearningTrackerEngine
from app.learning_planner.learning_planner_engine import LearningPlannerEngine
from app.licenses.license_service_engine import LicenseServiceEngine
from app.languages.language_service_engine import LanguageServiceEngine
from app.long_term_memory.long_term_memory_engine import LongTermMemoryEngine
from app.memory.memory_engine import MemoryEngine
from app.memberships.membership_service_engine import MembershipServiceEngine
from app.multi_agent_coordinator.multi_agent_coordinator_engine import (
    MultiAgentCoordinatorEngine,
)
from app.notes.notes_engine import NotesEngine
from app.ocr_agent.ocr_agent_engine import OCRAgentEngine
from app.object_detection_agent.object_detection_agent_engine import (
    ObjectDetectionAgentEngine,
)
from app.object_tracking_agent.object_tracking_agent_engine import (
    ObjectTrackingAgentEngine,
)
from app.news_monitoring_agent.news_monitoring_agent_engine import (
    NewsMonitoringAgentEngine,
)
from app.notifications.notification_engine import NotificationEngine
from app.pdf_reader_agent.pdf_reader_agent_engine import PDFReaderAgentEngine
from app.patents.patent_service_engine import PatentServiceEngine
from app.portfolio.portfolio_service_engine import PortfolioServiceEngine
from app.personal_knowledge_base_agent.personal_knowledge_base_agent_engine import (
    PersonalKnowledgeBaseAgentEngine,
)
from app.personality.personality_engine import PersonalityEngine
from app.planning.planning_engine import PlanningEngine
from app.pose_estimation_agent.pose_estimation_agent_engine import (
    PoseEstimationAgentEngine,
)
from app.profile.profile_engine import ProfileEngine
from app.publications.publication_service_engine import PublicationServiceEngine
from app.project_memory.project_memory_engine import ProjectMemoryEngine
from app.projects.project_service_engine import ProjectServiceEngine
from app.project_manager_agent.project_manager_agent_engine import (
    ProjectManagerAgentEngine,
)
from app.camera_analysis_agent.camera_analysis_agent_engine import (
    CameraAnalysisAgentEngine,
)
from app.scene_understanding_agent.scene_understanding_agent_engine import (
    SceneUnderstandingAgentEngine,
)
from app.modules.scheduler.scheduler_engine import SchedulerEngine
from app.screen_analysis_agent.screen_analysis_agent_engine import (
    ScreenAnalysisAgentEngine,
)
from app.recommendations.recommendation_engine import RecommendationEngine
from app.reasoning.reasoning_engine import ReasoningEngine
from app.relationship_engine.relationship_engine_engine import RelationshipEngine
from app.reflection_engine.reflection_engine import ReflectionEngine
from app.references.reference_service_engine import ReferenceServiceEngine
from app.research.research_service_engine import ResearchServiceEngine
from app.research_agent.research_agent_engine import ResearchAgentEngine
from app.self_correction_engine.self_correction_engine_engine import (
    SelfCorrectionEngine,
)
from app.self_optimization_engine.self_optimization_engine_engine import (
    SelfOptimizationEngine,
)
from app.self_improvement_engine.self_improvement_engine_engine import (
    SelfImprovementEngine,
)
from app.self_monitoring_engine.self_monitoring_engine_engine import (
    SelfMonitoringEngine,
)
from app.self_evaluation_engine.self_evaluation_engine import SelfEvaluationEngine
from app.skills.skill_service_engine import SkillServiceEngine
from app.spreadsheet_reader_agent.spreadsheet_reader_agent_engine import (
    SpreadsheetReaderAgentEngine,
)
from app.speech_to_text_agent.speech_to_text_agent_engine import SpeechToTextAgentEngine
from app.text_to_speech_agent.text_to_speech_agent_engine import TextToSpeechAgentEngine
from app.skill_evolution_engine.skill_evolution_engine import SkillEvolutionEngine
from app.task_manager.task_manager_engine import TaskManagerEngine
from app.tasks.task_engine import TaskEngine
from app.testimonials.testimonial_service_engine import TestimonialServiceEngine
from app.tools.tool_engine import ToolEngine
from app.user_timeline_engine.user_timeline_engine_engine import UserTimelineEngine
from app.user_state.user_state_engine import UserStateEngine
from app.volunteer.volunteer_service_engine import VolunteerServiceEngine
from app.vision_agent.vision_agent_engine import VisionAgentEngine
from app.voice_emotion_mappings.voice_emotion_mapping_engine import (
    VoiceEmotionMappingEngine,
)
from app.voice_personalities.voice_personality_engine import VoicePersonalityEngine
from app.website_automation_agent.website_automation_agent_engine import (
    WebsiteAutomationAgentEngine,
)
from app.websearch.websearch_engine import WebSearchEngine
from app.workflow_engine.workflow_engine import WorkflowEngine

presence_engine = PresenceEngine()
achievement_service_engine = AchievementServiceEngine()
activity_recognition_agent_engine = ActivityRecognitionAgentEngine()
autonomous_action_engine = AutonomousActionEngine()
autonomous_research_engine = AutonomousResearchEngine()
avatar_animation_service_engine = AvatarAnimationServiceEngine()
award_service_engine = AwardServiceEngine()
habit_engine = HabitEngine()
habit_service_engine = HabitServiceEngine()
journal_service_engine = JournalServiceEngine()
memory_engine = MemoryEngine()
membership_service_engine = MembershipServiceEngine()
multi_agent_coordinator_engine = MultiAgentCoordinatorEngine()
context_engine = ContextEngine()
context_fusion_engine = ContextFusionEngine()
knowledge_engine = KnowledgeEngine()
knowledge_gap_detector_engine = KnowledgeGapDetectorEngine()
learning_engine = LearningEngine()
learning_tracker_engine = LearningTrackerEngine()
learning_planner_engine = LearningPlannerEngine()
license_service_engine = LicenseServiceEngine()
language_service_engine = LanguageServiceEngine()
mood_engine = MoodEngine()
notification_engine = NotificationEngine()
news_monitoring_agent_engine = NewsMonitoringAgentEngine()
patent_service_engine = PatentServiceEngine()
pdf_reader_agent_engine = PDFReaderAgentEngine()
docx_reader_agent_engine = DOCXReaderAgentEngine()
portfolio_service_engine = PortfolioServiceEngine()
pose_estimation_agent_engine = PoseEstimationAgentEngine()
notes_engine = NotesEngine()
ocr_agent_engine = OCRAgentEngine()
object_detection_agent_engine = ObjectDetectionAgentEngine()
object_tracking_agent_engine = ObjectTrackingAgentEngine()
bookmark_engine = BookmarkEngine()
browser_agent_engine = BrowserAgentEngine()
certification_service_engine = CertificationServiceEngine()
conference_service_engine = ConferenceServiceEngine()
conversation_manager_engine = ConversationManagerEngine()
conversation_intelligence_engine = ConversationIntelligenceEngine()
cognitive_growth_tracker_engine = CognitiveGrowthTrackerEngine()
contact_engine = ContactEngine()
course_service_engine = CourseServiceEngine()
education_service_engine = EducationServiceEngine()
emotion_service_engine = EmotionServiceEngine()
emotional_intelligence_tracker_engine = EmotionalIntelligenceTrackerEngine()
emotion_recognition_agent_engine = EmotionRecognitionAgentEngine()
face_recognition_agent_engine = FaceRecognitionAgentEngine()
file_knowledge_extraction_agent_engine = FileKnowledgeExtractionAgentEngine()
facial_expression_service_engine = FacialExpressionServiceEngine()
experience_service_engine = ExperienceServiceEngine()
personality_engine = PersonalityEngine()
personal_knowledge_base_agent_engine = PersonalKnowledgeBaseAgentEngine()
goal_engine = GoalEngine()
goal_tracker_engine = GoalTrackerEngine()
goal_service_engine = GoalServiceEngine()
goal_execution_agent_engine = GoalExecutionAgentEngine()
history_engine = HistoryEngine()
image_understanding_agent_engine = ImageUnderstandingAgentEngine()
interest_service_engine = InterestServiceEngine()
intelligence_quotient_tracker_engine = IntelligenceQuotientTrackerEngine()
long_term_memory_engine = LongTermMemoryEngine()
user_state_engine = UserStateEngine()
user_timeline_engine = UserTimelineEngine()
volunteer_service_engine = VolunteerServiceEngine()
vision_agent_engine = VisionAgentEngine()
voice_personality_engine = VoicePersonalityEngine()
voice_emotion_mapping_engine = VoiceEmotionMappingEngine()
project_memory_engine = ProjectMemoryEngine()
project_service_engine = ProjectServiceEngine()
project_manager_agent_engine = ProjectManagerAgentEngine()
publication_service_engine = PublicationServiceEngine()
recommendation_engine = RecommendationEngine()
reference_service_engine = ReferenceServiceEngine()
research_service_engine = ResearchServiceEngine()
research_agent_engine = ResearchAgentEngine()
self_evaluation_engine = SelfEvaluationEngine()
self_improvement_engine = SelfImprovementEngine()
self_optimization_engine = SelfOptimizationEngine()
self_correction_engine = SelfCorrectionEngine()
self_monitoring_engine = SelfMonitoringEngine()
camera_analysis_agent_engine = CameraAnalysisAgentEngine()
scene_understanding_agent_engine = SceneUnderstandingAgentEngine()
scheduler_engine = SchedulerEngine()
screen_analysis_agent_engine = ScreenAnalysisAgentEngine()
skill_service_engine = SkillServiceEngine()
speech_to_text_agent_engine = SpeechToTextAgentEngine()
spreadsheet_reader_agent_engine = SpreadsheetReaderAgentEngine()
text_to_speech_agent_engine = TextToSpeechAgentEngine()
skill_evolution_engine = SkillEvolutionEngine()
task_manager_engine = TaskManagerEngine()
task_engine = TaskEngine()
testimonial_service_engine = TestimonialServiceEngine()
conversation_history = ConversationHistory(limit=50)
tool_engine = ToolEngine()
websearch_engine = WebSearchEngine()
website_automation_agent_engine = WebsiteAutomationAgentEngine()
workflow_engine = WorkflowEngine()

proactive_engine = ProactiveEngine(
    habit_engine=habit_engine,
    memory_engine=memory_engine,
    mood_engine=mood_engine,
    goal_engine=goal_engine,
)

chat_engine = ChatEngine(
    memory_engine=memory_engine,
    mood_engine=mood_engine,
    goal_engine=goal_engine,
    habit_engine=habit_engine,
    conversation_history=conversation_history,
)

profile_engine = ProfileEngine(
    memory_engine=memory_engine,
    knowledge_engine=knowledge_engine,
    goal_engine=goal_engine,
    conversation_history=conversation_history,
)

reasoning_engine = ReasoningEngine(
    profile_engine=profile_engine,
    knowledge_engine=knowledge_engine,
    goal_engine=goal_engine,
)
reflection_engine = ReflectionEngine()
relationship_engine = RelationshipEngine()

planning_engine = PlanningEngine(
    profile_engine=profile_engine,
    reasoning_engine=reasoning_engine,
    goal_engine=goal_engine,
)

decision_engine = DecisionEngine(
    profile_engine=profile_engine,
    goal_engine=goal_engine,
    knowledge_engine=knowledge_engine,
    learning_engine=learning_engine,
    mood_engine=mood_engine,
)

brain_engine = BrainEngine(
    memory_engine=memory_engine,
    knowledge_engine=knowledge_engine,
    learning_engine=learning_engine,
    goal_engine=goal_engine,
    mood_engine=mood_engine,
    profile_engine=profile_engine,
    reasoning_engine=reasoning_engine,
    planning_engine=planning_engine,
    decision_engine=decision_engine,
    websearch_engine=websearch_engine,
)
