import os
import google.generativeai as genai
import gradio as gr
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# --- API Keys ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Gemini API key
HF_TOKEN = os.getenv("HF_API_KEY")  # Hugging Face token

# --- Meme Generation Logic ---
def generate_meme_image(prompt):
    """Get image from Stable Diffusion via Hugging Face"""
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    payload = {
        "inputs": f"A meme template about {prompt}. Simple, bold visuals with space for text.",
        "parameters": {"width": 1024, "height": 1024}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        image = Image.open(BytesIO(response.content))
        return image
    except:
        return Image.new("RGB", (1024, 1024), color="white") 

def generate_meme_text(topic):
    """Get captions from Gemini"""
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""Create a funny meme about {topic}. Provide:
    - Top text (short, bold)
    - Bottom text (punchline)
    - 3 hashtags
    Format: TOP_TEXT|BOTTOM_TEXT|HASHTAGS"""
    
    try:
        response = model.generate_content(prompt)
        parts = response.text.split("|")
        return {
            "top": parts[0].strip(),
            "bottom": parts[1].strip(),
            "hashtags": parts[2].strip()
        }
    except:
        return {"top": "MEME FAILED", "bottom": "TRY AGAIN", "hashtags": "#oops"}

def create_meme(topic):
    """Combine image and text"""
    if not topic.strip():
        return None, "Enter a topic!"
    
    # Get assets
    image = generate_meme_image(topic)
    text = generate_meme_text(topic)
    
    # Add text overlay
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 60) if os.path.exists("arial.ttf") else ImageFont.load_default()
    
    draw.text((50, 50), text["top"], fill="white", stroke_fill="black", stroke_width=2, font=font)
    draw.text((50, 900), text["bottom"], fill="white", stroke_fill="black", stroke_width=2, font=font)
    
    caption = f"{text['top']}\n{text['bottom']}\n\n{text['hashtags']}"
    return image, caption

# --- Professional Gradio UI ---
custom_theme = gr.themes.Default(
    primary_hue="emerald",
    secondary_hue="gray",
    font=gr.themes.GoogleFont("Poppins"),
).set(
    button_primary_background_fill="*primary_500",
    button_primary_background_fill_hover="*primary_400",
    button_primary_text_color="white",
    slider_color="*primary_500"
)

css = """
#title {text-align: center; margin: 1em auto}
#subtitle {text-align: center; margin-bottom: 2em}
.example-image {border-radius: 12px; cursor: pointer}
footer {visibility: hidden !important}
.output-image {border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.1)}
"""

with gr.Blocks(theme=custom_theme, css=css) as demo:
    # Hero Section
    gr.Markdown("""# MemeForge""", elem_id="title")
    gr.Markdown("""Intelligent Visual Content Generation System (Gemini + Stable Diffusion )""", elem_id="subtitle")
    
    with gr.Row(variant="panel"):
        with gr.Column(scale=3):
            # Input Section
            with gr.Group():
                input_topic = gr.Textbox(
                    label="✨ Enter Your Meme Topic",
                    placeholder="e.g., 'AI taking over jobs', 'Python vs Excel'...",
                    lines=2,
                    max_lines=3
                )
                generate_btn = gr.Button(
                    "Generate Meme 🚀",
                    scale=1,
                    variant="primary"
                )
            
            output_caption = gr.Textbox(
                label="Caption & Hashtags",
                interactive=False,
                lines=3
            )
            
            # Style Options
            with gr.Accordion("🎨 Advanced Options", open=False):
                with gr.Row():
                    style_choice = gr.Dropdown(
                        ["Modern", "Classic", "Dark Humor", "Wholesome"],
                        value="Modern",
                        label="Meme Style"
                    )
                    font_choice = gr.Dropdown(
                        ["Impact", "Arial", "Comic Sans", "Roboto"],
                        value="Impact",
                        label="Font Style"
                    )
                
                intensity = gr.Slider(1, 5, value=3, label="Humor Intensity")

        # Output Section
        with gr.Column(scale=4):
            output_image = gr.Image(
                label="Generated Meme",
                elem_classes="output-image",
                height=500
            )
            with gr.Row():
                download_btn = gr.Button("📥 Download Meme", scale=0)
                share_btn = gr.Button("📤 Share to Social", scale=0)
            

    # Example Gallery
    with gr.Column(variant="panel"):
        gr.Markdown("## 🎭 Popular Examples")
        with gr.Row():
            gr.Examples(
                examples=[
                    ["tech support hell", "examples/tech_meme.png"],
                    ["Python vs Excel", "examples/python_excel.png"],
                    ["zoom fatigue", "examples/zoom_meme.png"]
                ],
                inputs=[input_topic],
                examples_per_page=3,
                label="Click an example to start →"
            )

    # Loading Animation
    generate_btn.click(
        fn=lambda: gr.Textbox(interactive=False),
        outputs=[input_topic]
    ).then(
        fn=create_meme,
        inputs=input_topic,
        outputs=[output_image, output_caption],
        preprocess=False
    ).then(
        fn=lambda: gr.Textbox(interactive=True),
        outputs=[input_topic]
    )

    # Interactive Events
    share_btn.click(
        fn=lambda: gr.Info("Sharing feature coming soon!"),
        queue=False
    )

if __name__ == "__main__":
    demo.launch(
        server_port=7860,
        show_api=False,
        share=True
    )