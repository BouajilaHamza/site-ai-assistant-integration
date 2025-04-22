from comet_ml import start
from backend.core.config import settings

def get_experiment():
    """
    Initialize and return a Comet ML experiment using settings from config.
    """
    experiment = start(
        api_key=settings.COMET_ML_API_KEY,
        project_name=settings.COMET_ML_PROJECT_NAME,
        workspace=settings.COMET_ML_WORKSPACE,
    )
    return experiment
