import os
from services.task_router import detect_task
from services.template_service import TemplateService
from services.data_service import fetch_document_data
from app_config import GENERATED_FOLDER


class DocumentService:
    def __init__(self):
        self.template_service = TemplateService()
        self.current_personality = "HR"  # Default personality mode

    def process(self, user_message: str):
        # Step 1: Detect the task and target template
        task_type, template_name, subfolder = detect_task(user_message)

        if not template_name:
            return {
                "type": "text",
                "response": "❌ I couldn't understand that task. Try something like 'Generate invoice' or 'Create offer letter'."
            }

        # Step 2: Check personality match
        if subfolder.upper() != self.current_personality.upper():
            return {
                "type": "switch_prompt",
                "response": f"⚠️ This task looks like a **{subfolder}** task, but you're in **{self.current_personality}** mode.",
                "switch_to": subfolder
            }

        # Step 3: Fetch data from database (static record_id for now)
        record_id = 1  # 🔁 You can update this to be dynamic later
        doc_key = template_name.replace('.docx', '')  # "offer_letter", "invoice", etc.
        data = fetch_document_data(doc_key, record_id)

        if not data:
            return {
                "type": "text",
                "response": f"⚠️ No data found for {task_type} (ID {record_id})."
            }

        # Step 4: Convert DB keys to placeholders like [Candidate Name]
        formatted_data = {
            key.replace("_", " ").title(): str(value) for key, value in data.items()
        }

        # Step 5: Fill template and save to file
        doc = self.template_service.fill_template(template_name, formatted_data, subfolder)
        os.makedirs(GENERATED_FOLDER, exist_ok=True)
        filename = f"{task_type.replace(' ', '_').lower()}_record_{record_id}.docx"
        output_path = os.path.join(GENERATED_FOLDER, filename)
        doc.save(output_path)

        return {
            "type": "document",
            "response": f"✅ {task_type} document generated from database (ID {record_id}).",
            "download_link": f"/download/{filename}"
        }

    def switch_personality(self, new_mode):
        self.current_personality = new_mode.upper() if new_mode else "HR"
