import toml
from pathlib import Path
from typing import Dict, Iterable, Optional


class ApplicationSchema:

    @classmethod
    def get_schema(cls) -> Dict:
        _application_schema_path = Path(__file__).parent.parent / "application_schema.toml"
        return toml.load(_application_schema_path)

    @classmethod
    def get_selections(cls) -> Dict:
        return ApplicationSchema.get_schema()['selections']

    @classmethod
    def get_questions_and_aliases(cls) -> Dict[str, Optional[str]]:
        questions = ApplicationSchema.get_schema()['survey_questions']
        questions_and_aliases = {
            question: None
            for question in questions['no_alias']
        }
        questions_and_aliases.update(questions['with_alias'])
        return questions_and_aliases

    @classmethod
    def get_locations_and_genders(cls) -> Iterable:
        sel = ApplicationSchema.get_selections()
        return sel['location'] + sel['gender']
