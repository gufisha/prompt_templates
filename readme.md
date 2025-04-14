# Prompt Templates for ComfyUI

A custom node extension for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) that provides a collection of ready-to-use model prompts for AI image generation.

## Overview

This extension adds a "Prompt Template Formatter" node to ComfyUI that lets you choose from a wide variety of pre-written, professionally crafted prompts for different scenarios, settings, and styles. Each template includes a placeholder for a model name that will be automatically replaced with your chosen name.

The templates cover a broad range of scenarios including:
- Outdoor/environmental scenes
- Fashion and editorial style shots
- Intimate/boudoir settings
- Beach and coastal scenes
- Various outfit styles and poses

## Features

- 40+ professionally written prompt templates
- Customizable model name parameter
- Seamless integration with ComfyUI workflow
- Easy to select through dropdown menu
- Outputs both the encoded prompt (for use in the generation) and a preview prompt

## Installation

1. Clone this repository into your ComfyUI custom_nodes directory:
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/yourusername/prompt_templates.git
```

2. Make sure the `prompts.json` file is in the same directory as the repository root.

3. Restart ComfyUI if it's already running.

## Usage

1. Add the "Prompt Template Formatter" node to your ComfyUI workflow.
2. Select a template from the dropdown menu.
3. Enter a model name in the "Model Name" field (defaults to "Jessica").
4. Connect the "Encoded Prompt" output to your text encoder or other prompt input.
5. The "Preview Prompt" output can be connected to a preview node if you want to see the full text.

## Creating Your Own Templates

You can modify the `prompts.json` file to add your own templates. Each template should follow this format:

```json
{
  "header": "Your Template Name",
  "paragraph": "Your detailed prompt text with {modelName} as a placeholder."
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Created for enhancing the ComfyUI workflow
- Inspired by professional photography and editorial styles