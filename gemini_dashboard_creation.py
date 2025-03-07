from PIL import Image
from google import genai
from google.genai import types

from dotenv import load_dotenv
import os


# Initialize Gemini API client using your API key

def generate_html_from_prompt(client,prompt: str, image) -> str:
    """
    Sends the provided prompt and image to the Gemini API to generate a complete HTML dashboard.
    Returns the generated HTML code as a string.
    """
    try:
        print("Starting first API call...")
        response1 = client.models.generate_content(
            model="gemini-2.0-flash-001",
            config=types.GenerateContentConfig(
                system_instruction="You are a highly skilled front-end developer who excels at creating visually appealing, highly responsive, and fully interactive dashboards with a smooth user experience."
            ),
            contents=[image, prompt]
        )
        # Clean up the response text
        html_initial = response1.text.lstrip("```html").rstrip("'''")
        print("First API call completed.")

        # Second call for final HTML adjustments
        print("Starting second API call for HTML refinement...")
        additional_instruction = (
            "Check this HTML file and edit it to produce a dasboard with proper layout, visually appealing charts and small font size matching the provided image. "
            "The dashboard should be in compact form. The charts should strictly be inside container. The legend should always be on top and inside the container"
            "The final output must be a complete HTML file with no extra text or explanations outside the <html> tags."
        )
        response2 = client.models.generate_content(
            model="gemini-2.0-flash-001",
            config=types.GenerateContentConfig(
                system_instruction="You are a highly skilled front-end developer who excels at creating visually appealing, highly responsive, and fully interactive dashboards with a smooth user experience."
            ),
            contents=[image, html_initial + additional_instruction]
        )
        html_final = response2.text.lstrip("```html").rstrip("'''")
        print("Second API call completed.")
        return html_final

    except Exception as e:
        print("Error generating HTML:", e)
        return ""

def main(client,image_path,prompt_path,output_html_path):
    reference_image = Image.open(image_path)
    # Read the prompt from file
    with open(prompt_path, "r", encoding="utf-8") as f:
        user_prompt = f.read().strip()
    # Generate the HTML code using the provided prompt and image
    html_code = generate_html_from_prompt(client,user_prompt, reference_image)
    if html_code:
        output_file = output_html_path
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_code)
        print(f"HTML dashboard successfully saved to {output_file}")
    else:
        print("Failed to generate HTML code.")

if __name__ == "__main__":
    try:
        load_dotenv()  # This automatically reads .env
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        client=genai.Client(api_key=GEMINI_API_KEY)
        
        #Dashboard 1
        # image_path="customer_churn_image.png"
        # prompt_path="customer_churn_insights_prompt.txt"
        # output_html_path="customer_churn_dashboard.html"

        #Dashboard 2
        image_path="cash_flow_forecasting_image.png"
        prompt_path="cash_flow_forecasting_prompt.txt"
        output_html_path="cash_flow_forecasting_dashboard.html"
        # Open the reference image for layout styling
        
        main(client,image_path,prompt_path,output_html_path)
    except Exception as e:
        print("Error reading prompt file:", e)