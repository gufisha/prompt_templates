import json
import os

class PromptTemplateNode:
    # Use a flat map: { "Filename: Header": "Paragraph" }
    prompt_map = {}

    @classmethod
    def INPUT_TYPES(cls):
        cls.load_prompts_from_directory() # Load or reload prompts

        prompt_keys = sorted(list(cls.prompt_map.keys())) # Sort keys alphabetically
        if not prompt_keys:
            prompt_keys = ["No prompts found"]

        return {
            "required": {
                 "model_name": ("STRING", {"default": "Esmeralda"}),
                 # Single dropdown with formatted keys
                 "prompt_template_key": (prompt_keys,),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("Encoded Prompt", "Preview Prompt")
    FUNCTION = "render_prompt"
    CATEGORY = "Prompt"

    @classmethod
    def load_prompts_from_directory(cls):
        # Reset the map
        cls.prompt_map = {}

        base_path = os.path.dirname(__file__)
        prompts_dir = os.path.join(base_path, "prompts")

        if not os.path.isdir(prompts_dir):
            print(f"[PromptTemplateNode] Prompts directory not found: {prompts_dir}")
            return

        try:
            for filename in os.listdir(prompts_dir):
                if filename.endswith(".json"):
                    # Use filename without extension as the prefix
                    category_name = os.path.splitext(filename)[0]
                    file_path = os.path.join(prompts_dir, filename)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            prompts_in_file = json.load(f)
                            if isinstance(prompts_in_file, list):
                                for prompt_data in prompts_in_file:
                                    if isinstance(prompt_data, dict) and 'header' in prompt_data and 'paragraph' in prompt_data:
                                        header = prompt_data['header']
                                        paragraph = prompt_data['paragraph']
                                        # Create the formatted key "Filename: Header"
                                        map_key = f"{category_name}: {header}"
                                        cls.prompt_map[map_key] = paragraph
                                    else:
                                         print(f"[PromptTemplateNode] Skipping invalid prompt entry in {filename}: {prompt_data}")
                            else:
                                print(f"[PromptTemplateNode] Invalid format in {filename}, expected a list of prompts.")
                    except json.JSONDecodeError as e:
                        print(f"[PromptTemplateNode] Error decoding JSON from {filename}: {e}")
                    except Exception as e:
                        print(f"[PromptTemplateNode] Error reading file {filename}: {e}")
        except Exception as e:
            print(f"[PromptTemplateNode] Error listing prompts directory {prompts_dir}: {e}")


    def render_prompt(self, model_name, prompt_template_key):
        # Look up the template using the combined key
        template = self.prompt_map.get(prompt_template_key, "")

        if not template:
             print(f"[PromptTemplateNode] Warning: Prompt template not found for key '{prompt_template_key}'")
             return ("", f"Prompt not found for: {prompt_template_key}")

        final_prompt = template.replace("{modelName}", model_name)
        return (final_prompt, final_prompt)


# Register with ComfyUI
NODE_CLASS_MAPPINGS = {
    "PromptTemplateNode": PromptTemplateNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptTemplateNode": "Prompt Templates"
}