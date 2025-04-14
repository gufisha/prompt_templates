import json
import os

class PromptTemplateNode:
    @classmethod
    def INPUT_TYPES(cls):
        # Load or fallback
        prompts = cls.load_prompts()
        if prompts:
            cls.prompt_map = {p['header']: p['paragraph'] for p in prompts}
        else:
            cls.prompt_map = {"No prompts available": ""}

        return {
            "required": {
                "prompt_template": (list(cls.prompt_map.keys()),),
                "model_name": ("STRING", {"default": "Esmeralda"}),
            }
        }

    # Two outputs: first is the prompt for encoding, second is the prompt for preview
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("Encoded Prompt", "Preview Prompt")
    FUNCTION = "render_prompt"
    CATEGORY = "Prompt"

    @staticmethod
    def load_prompts():
        base_path = os.path.dirname(__file__)
        json_path = os.path.join(base_path, "prompts.json")
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[PromptTemplateNode] Error loading JSON: {e}")
            return []

    def render_prompt(self, prompt_template, model_name):
        template = self.prompt_map.get(prompt_template, "")
        final_prompt = template.replace("{modelName}", model_name)
        return (final_prompt, final_prompt)


# Register with ComfyUI
NODE_CLASS_MAPPINGS = {
    "PromptTemplateNode": PromptTemplateNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptTemplateNode": "Prompt Templates"
}