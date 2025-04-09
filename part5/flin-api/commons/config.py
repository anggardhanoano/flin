class ConfigKey:
    MOBILE = "mobile_config"
    AI_TUTOR = "ai_tutor_config"
    COMMUNITY = "community_config"
    VOUCHER = "voucher_config"
    REFERRAL = "referral_config"
    COUPON = "coupon_config"
    LANDING_PAGE = "lp_config"
    STUDENT_DATA = "student_data_config"
    EXERCISE = "exercise_config"
    COPILOT = "copilot_config"
    COPILOT_AGENT = "copilot_agent_config"
    COPILOT_TEMPLATE = "copilot_template_config"
    LEARNING_TOOLS = "learning_tools_config"
    STOPWORDS = "stopwords_config"
    TYPESENSE_QUERY_WEIGHT = "typesense_query_weight_config"
    MOBILE_HOME = "mobile_home_config"
    MOBILE_VERSION = "mobile_version_config"
    MOBILE_FEATURE_FLAG = "mobile_feature_flag"


class FEATURE_KEY:
    COPILOT = 'copilot'
    FLASHCARDS = 'flashcard'
    COURSES = "courses"
    BOOKS = "books"
    QUIZ = "quiz"
    COMMUNITIES = "communities"
    CHEATSHEET = "cheatsheet"
    STUDY_PLAN = "study_plan"
    OTHER = "other"

    @classmethod
    def get_all_features(cls):
        return [attr for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")]


class MobileHomeConfig:
    BENTO_MENU = "bento_menu_config"
    PROMO_BANNER = "promo_banner_config"
    HOME_CONTENT = "home_content_config"
