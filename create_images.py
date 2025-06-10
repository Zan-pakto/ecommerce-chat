from PIL import Image, ImageDraw, ImageFont
import os
import requests
from io import BytesIO

def create_placeholder():
    # Create a 400x300 placeholder image
    img = Image.new('RGB', (400, 300), color='#f0f0f0')
    draw = ImageDraw.Draw(img)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    text = "No Image Available"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (400 - text_width) // 2
    y = (300 - text_height) // 2
    
    draw.text((x, y), text, fill='#666666', font=font)
    
    # Save the placeholder
    os.makedirs('static/images', exist_ok=True)
    img.save('static/images/placeholder.jpg')

def download_sample_images():
    # Sample product images from Unsplash
    images = {
        'smartphone.jpg': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9',
        'laptop.jpg': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853',
        'book.jpg': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f',
        'tshirt.jpg': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab',
        'coffee-maker.jpg': 'https://images.unsplash.com/photo-1570486916336-1a6d2f7b2c3f'
    }
    
    for filename, url in images.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                # Resize to 400x300 while maintaining aspect ratio
                img.thumbnail((400, 300))
                # Create a new image with white background
                new_img = Image.new('RGB', (400, 300), 'white')
                # Paste the resized image in the center
                offset = ((400 - img.width) // 2, (300 - img.height) // 2)
                new_img.paste(img, offset)
                # Save the image
                new_img.save(f'static/images/{filename}')
                print(f'Downloaded {filename}')
            else:
                print(f'Failed to download {filename}')
        except Exception as e:
            print(f'Error downloading {filename}: {str(e)}')

if __name__ == '__main__':
    create_placeholder()
    download_sample_images() 