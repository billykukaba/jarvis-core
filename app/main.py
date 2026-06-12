import logging

from fastapi import FastAPI

from app.brain.router import router as brain_router
from app.chat.router import router as chat_router
from app.api.memory import router as memory_router
from app.habits.router import habits_router
from app.api.mood import router as mood_router
from app.api.presence import router as presence_router
from app.api.proactive import router as proactive_router
from app.achievements.router import achievements_router
from app.awards.router import awards_router
from app.bookmarks.router import bookmarks_router
from app.certifications.router import certifications_router
from app.conferences.router import conferences_router
from app.contacts.router import contacts_router
from app.courses.router import courses_router
from app.context.router import router as context_router
from app.decision.router import router as decision_router
from app.education.router import education_router
from app.emotions.router import emotions_router
from app.experience.router import experience_router
from app.facial_expressions.router import facial_expressions_router
from app.goals.router import goals_router
from app.history.router import router as history_router
from app.interests.router import interests_router
from app.journals.router import journals_router
from app.knowledge.router import router as knowledge_router
from app.learning_tracker.router import router as learning_tracker_router
from app.languages.router import languages_router
from app.licenses.router import licenses_router
from app.long_term_memory.router import router as long_term_memory_router
from app.memberships.router import memberships_router
from app.notifications.router import router as notifications_router
from app.notes.router import router as notes_router
from app.patents.router import patents_router
from app.portfolio.router import portfolio_router
from app.personality.router import router as personality_router
from app.planning.router import router as planning_router
from app.profile.router import router as profile_router
from app.publications.router import publications_router
from app.projects.router import projects_router
from app.modules.scheduler.router import router as scheduler_router
from app.recommendations.router import router as recommendations_router
from app.reasoning.router import router as reasoning_router
from app.references.router import references_router
from app.research.router import research_router
from app.skills.router import skills_router
from app.tasks.router import tasks_router
from app.testimonials.router import testimonials_router
from app.tools.router import router as tools_router
from app.user_state.router import router as user_state_router
from app.volunteer.router import volunteer_router
from app.websearch.router import router as websearch_router

logging.basicConfig(level=logging.DEBUG)


def create_app() -> FastAPI:
    app = FastAPI(
        title="JARVIS CORE",
        version="0.1",
    )

    @app.get("/")
    async def root() -> dict[str, str]:
        return {
            "name": "JARVIS CORE",
            "version": "0.1",
        }

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {
            "status": "online",
        }

    app.include_router(presence_router)
    app.include_router(habits_router)
    app.include_router(memory_router)
    app.include_router(context_router)
    app.include_router(history_router)
    app.include_router(interests_router)
    app.include_router(portfolio_router)
    app.include_router(journals_router)
    app.include_router(achievements_router)
    app.include_router(awards_router)
    app.include_router(long_term_memory_router)
    app.include_router(memberships_router)
    app.include_router(knowledge_router)
    app.include_router(learning_tracker_router)
    app.include_router(languages_router)
    app.include_router(licenses_router)
    app.include_router(mood_router)
    app.include_router(notifications_router)
    app.include_router(notes_router)
    app.include_router(bookmarks_router)
    app.include_router(contacts_router)
    app.include_router(courses_router)
    app.include_router(education_router)
    app.include_router(emotions_router)
    app.include_router(facial_expressions_router)
    app.include_router(experience_router)
    app.include_router(certifications_router)
    app.include_router(conferences_router)
    app.include_router(personality_router)
    app.include_router(goals_router)
    app.include_router(proactive_router)
    app.include_router(chat_router)
    app.include_router(profile_router)
    app.include_router(publications_router)
    app.include_router(patents_router)
    app.include_router(projects_router)
    app.include_router(recommendations_router)
    app.include_router(references_router)
    app.include_router(research_router)
    app.include_router(scheduler_router)
    app.include_router(skills_router)
    app.include_router(reasoning_router)
    app.include_router(tasks_router)
    app.include_router(testimonials_router)
    app.include_router(planning_router)
    app.include_router(tools_router)
    app.include_router(user_state_router)
    app.include_router(volunteer_router)
    app.include_router(websearch_router)
    app.include_router(decision_router)
    app.include_router(brain_router)

    return app


app = create_app()
