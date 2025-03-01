import json
from celery import shared_task
from .models import Category


@shared_task
def process_category_json(file_path):
    """Processes the uploaded JSON file and adds categories in the database."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        categories = data.get('categories', [])

        for item in categories:
            Category.objects.update_or_create(
                name=item.get('category_name'),
                defaults={
                    'description': item.get('description', ''),
                }
            )

        return f"Processed {len(categories)} categories successfully."

    except Exception as e:
        return f"Error processing file: {str(e)}"
