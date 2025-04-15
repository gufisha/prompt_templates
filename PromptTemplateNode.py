import json
import os
from collections import defaultdict

class PromptTemplateNode:
    # Store nested data: { "category": { "header": "paragraph" } }
    prompt_data = defaultdict(dict)
    # Store list of categories ["cat1", "cat2"]
    categories = []
    # Store list of unique headers ["header1", "header2"]
    all_headers = set()


    @classmethod
    def INPUT_TYPES(cls):
        cls.load_prompts_from_directory() # Load or reload prompts

        # Fallbacks if loading fails or directory is empty
        categories_list = cls.categories if cls.categories else ["No categories found"]
        headers_list = sorted(list(cls.all_headers)) if cls.all_headers else ["No prompts found"]

        return {
            "required": {
                 "model_name": ("STRING", {"default": "Esmeralda"}),
                 "prompt_category": (categories_list,),
                 "prompt_header": (headers_list,),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("Encoded Prompt", "Preview Prompt")
    FUNCTION = "render_prompt"
    CATEGORY = "Prompt"

    @classmethod
    def load_prompts_from_directory(cls):
        # Reset class variables
        cls.prompt_data = defaultdict(dict)
        cls.categories = []
        cls.all_headers = set()

        base_path = os.path.dirname(__file__)
        prompts_dir = os.path.join(base_path, "prompts")

        if not os.path.isdir(prompts_dir):
            print(f"[PromptTemplateNode] Prompts directory not found: {prompts_dir}")
            return

        found_files = False
        try:
            for filename in os.listdir(prompts_dir):
                if filename.endswith(".json"):
                    found_files = True
                    category_name = os.path.splitext(filename)[0] # Use original filename as key
                    cls.categories.append(category_name)
                    file_path = os.path.join(prompts_dir, filename)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            prompts_in_file = json.load(f)
                            if isinstance(prompts_in_file, list):
                                for prompt_data in prompts_in_file:
                                    if isinstance(prompt_data, dict) and 'header' in prompt_data and 'paragraph' in prompt_data:
                                        header = prompt_data['header']
                                        paragraph = prompt_data['paragraph']
                                        cls.prompt_data[category_name][header] = paragraph
                                        cls.all_headers.add(header) # Add header to the set of all unique headers
                                    else:
                                         print(f"[PromptTemplateNode] Skipping invalid prompt entry in {filename}: {prompt_data}")
                            else:
                                print(f"[PromptTemplateNode] Invalid format in {filename}, expected a list of prompts.")
                    except json.JSONDecodeError as e:
                        print(f"[PromptTemplateNode] Error decoding JSON from {filename}: {e}")
                    except Exception as e:
                        print(f"[PromptTemplateNode] Error reading file {filename}: {e}")

            if found_files:
                 cls.categories.sort() # Sort categories alphabetically

        except Exception as e:
            print(f"[PromptTemplateNode] Error listing prompts directory {prompts_dir}: {e}")


    def render_prompt(self, model_name, prompt_category, prompt_header):
        # Look up the paragraph using both category and header
        template = self.prompt_data.get(prompt_category, {}).get(prompt_header, "")

        if not template:
             print(f"[PromptTemplateNode] Warning: Prompt template not found for category '{prompt_category}' and header '{prompt_header}'")
             # Return empty strings or a default message if the combo isn't found
             return ("", f"Prompt not found for: {prompt_category} / {prompt_header}")

        final_prompt = template.replace("{modelName}", model_name)
        return (final_prompt, final_prompt)


# Register with ComfyUI
NODE_CLASS_MAPPINGS = {
    "PromptTemplateNode": PromptTemplateNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptTemplateNode": "Prompt Templates"
}