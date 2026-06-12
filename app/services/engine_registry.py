from app.achievements.achievement_service_engine import AchievementServiceEngine
from app.awards.award_service_engine import AwardServiceEngine
from app.bookmarks.bookmark_engine import BookmarkEngine
from app.certifications.certification_service_engine import CertificationServiceEngine
from app.conferences.conference_service_engine import ConferenceServiceEngine
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
from app.context.context_engine import ContextEngine
from app.decision.decision_engine import DecisionEngine
from app.education.education_service_engine import EducationServiceEngine
from app.emotions.emotion_service_engine import EmotionServiceEngine
from app.experience.experience_service_engine import ExperienceServiceEngine
from app.facial_expressions.facial_expression_service_engine import (
    FacialExpressionServiceEngine,
)
from app.goal_tracker.goal_tracker_engine import GoalTrackerEngine
from app.goals.goal_service_engine import GoalServiceEngine
from app.habits.habit_service_engine import HabitServiceEngine
from app.history.history_engine import HistoryEngine
from app.interests.interest_service_engine import InterestServiceEngine
from app.journals.journal_service_engine import JournalServiceEngine
from app.knowledge.knowledge_engine import KnowledgeEngine
from app.learning.learning_engine import LearningEngine
from app.learning_tracker.learning_tracker_engine import LearningTrackerEngine
from app.licenses.license_service_engine import LicenseServiceEngine
from app.languages.language_service_engine import LanguageServiceEngine
from app.long_term_memory.long_term_memory_engine import LongTermMemoryEngine
from app.memory.memory_engine import MemoryEngine
from app.memberships.membership_service_engine import MembershipServiceEngine
from app.notes.notes_engine import NotesEngine
from app.notifications.notification_engine import NotificationEngine
from app.patents.patent_service_engine import PatentServiceEngine
from app.portfolio.portfolio_service_engine import PortfolioServiceEngine
from app.personality.personality_engine import PersonalityEngine
from app.planning.planning_engine import PlanningEngine
from app.profile.profile_engine import ProfileEngine
from app.publications.publication_service_engine import PublicationServiceEngine
from app.project_memory.project_memory_engine import ProjectMemoryEngine
from app.projects.project_service_engine import ProjectServiceEngine
from app.modules.scheduler.scheduler_engine import SchedulerEngine
from app.recommendations.recommendation_engine import RecommendationEngine
from app.reasoning.reasoning_engine import ReasoningEngine
from app.references.reference_service_engine import ReferenceServiceEngine
from app.research.research_service_engine import ResearchServiceEngine
from app.skills.skill_service_engine import SkillServiceEngine
from app.task_manager.task_manager_engine import TaskManagerEngine
from app.tasks.task_engine import TaskEngine
from app.testimonials.testimonial_service_engine import TestimonialServiceEngine
from app.tools.tool_engine import ToolEngine
from app.user_state.user_state_engine import UserStateEngine
from app.volunteer.volunteer_service_engine import VolunteerServiceEngine
from app.websearch.websearch_engine import WebSearchEngine

presence_engine = PresenceEngine()
achievement_service_engine = AchievementServiceEngine()
award_service_engine = AwardServiceEngine()
habit_engine = HabitEngine()
habit_service_engine = HabitServiceEngine()
journal_service_engine = JournalServiceEngine()
memory_engine = MemoryEngine()
membership_service_engine = MembershipServiceEngine()
context_engine = ContextEngine()
knowledge_engine = KnowledgeEngine()
learning_engine = LearningEngine()
learning_tracker_engine = LearningTrackerEngine()
license_service_engine = LicenseServiceEngine()
language_service_engine = LanguageServiceEngine()
mood_engine = MoodEngine()
notification_engine = NotificationEngine()
patent_service_engine = PatentServiceEngine()
portfolio_service_engine = PortfolioServiceEngine()
notes_engine = NotesEngine()
bookmark_engine = BookmarkEngine()
certification_service_engine = CertificationServiceEngine()
conference_service_engine = ConferenceServiceEngine()
contact_engine = ContactEngine()
course_service_engine = CourseServiceEngine()
education_service_engine = EducationServiceEngine()
emotion_service_engine = EmotionServiceEngine()
facial_expression_service_engine = FacialExpressionServiceEngine()
experience_service_engine = ExperienceServiceEngine()
personality_engine = PersonalityEngine()
goal_engine = GoalEngine()
goal_tracker_engine = GoalTrackerEngine()
goal_service_engine = GoalServiceEngine()
history_engine = HistoryEngine()
interest_service_engine = InterestServiceEngine()
long_term_memory_engine = LongTermMemoryEngine()
user_state_engine = UserStateEngine()
volunteer_service_engine = VolunteerServiceEngine()
project_memory_engine = ProjectMemoryEngine()
project_service_engine = ProjectServiceEngine()
publication_service_engine = PublicationServiceEngine()
recommendation_engine = RecommendationEngine()
reference_service_engine = ReferenceServiceEngine()
research_service_engine = ResearchServiceEngine()
scheduler_engine = SchedulerEngine()
skill_service_engine = SkillServiceEngine()
task_manager_engine = TaskManagerEngine()
task_engine = TaskEngine()
testimonial_service_engine = TestimonialServiceEngine()
conversation_history = ConversationHistory(limit=50)
tool_engine = ToolEngine()
websearch_engine = WebSearchEngine()

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
