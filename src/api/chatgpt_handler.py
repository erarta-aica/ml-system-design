import openai
import base64

async def process_image_with_gpt4(image_file):
    # Конвертация изображения в base64
    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    
    response = await openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Estimate calories in this food image"
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{image_base64}"
                    }
                ]
            }
        ]
    )
    
    return response.choices[0].message.content 