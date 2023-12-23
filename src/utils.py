import pathlib

from jinja2 import Template

from src.constants import TEMPLATE_PATHS, EMAIL_SUBJECTS, EMAIL_TEXT


PARENT_PATH = parenth_path = pathlib.Path(__file__).parent.resolve()


def get_template_path(email_type: str) -> str:
    if email_type in TEMPLATE_PATHS:
        return '{parent_path}/{template_path}'.format(
            parent_path=PARENT_PATH,
            template_path=TEMPLATE_PATHS.get(email_type),
        )
    raise ValueError('Invalid email type')


def get_email_subject(email_type: str) -> str:
    if email_type in EMAIL_SUBJECTS:
        return EMAIL_SUBJECTS.get(email_type)
    raise ValueError('Invalid email type')


def build_html(email_type: str, action_url: str, replacements: dict) -> str:
    template_path: str = get_template_path(email_type)
    try:
        with open(template_path) as template_file:
            return Template(template_file.read()).render(
                action_url=action_url,
                **replacements,
            )
    except Exception as e:
        raise e
    

def build_text(email_type: str) -> str:
    if email_type in EMAIL_TEXT:
        return EMAIL_TEXT.get(email_type)
    raise ValueError('Invalid email type')


def convert_input(event):
    return {
        "email_type": event["email_type"],
        "action_url": event["action_url"],
        "replacements": event["replacements"],
    }
