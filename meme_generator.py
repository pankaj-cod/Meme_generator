"""
Meme generation module
"""
from PIL import Image, ImageDraw, ImageFont
import os
import random

class MemeGenerator:
    def __init__(self):
        """Initialize meme generator with emotion-based templates"""
        self.meme_texts = {
            'happy': [
                ("WHEN YOU FINALLY", "UNDERSTAND THE CODE"),
                ("SUCCESS!", "THAT FEELING WHEN IT WORKS"),
                ("ME AFTER", "FIXING THAT BUG"),
                ("HAPPINESS IS", "CODE THAT COMPILES"),
            ],
            'sad': [
                ("WHEN YOUR CODE", "DOESN'T WORK"),
                ("ME AFTER", "DEBUGGING FOR 3 HOURS"),
                ("THAT MOMENT WHEN", "YOU REALIZE IT'S A TYPO"),
                ("PRODUCTION IS DOWN", "AND IT'S FRIDAY"),
            ],
            'angry': [
                ("WHEN SOMEONE", "BREAKS THE BUILD"),
                ("WHO PUSHED TO", "MAIN WITHOUT TESTING"),
                ("WHEN THE CLIENT SAYS", "JUST A SMALL CHANGE"),
                ("ME AFTER READING", "LEGACY CODE"),
            ],
            'surprise': [
                ("WAIT, IT ACTUALLY", "WORKED?!"),
                ("WHEN THE CODE WORKS", "ON THE FIRST TRY"),
                ("DID I JUST", "FIX IT?"),
                ("PLOT TWIST:", "NO ERRORS"),
            ],
            'fear': [
                ("WHEN YOU SEE", "PRODUCTION ERRORS"),
                ("OH NO", "I FORGOT TO COMMIT"),
                ("WHEN YOU REALIZE", "YOU'RE IN PROD"),
                ("THAT FEELING WHEN", "THE DEMO IS IN 5 MINUTES"),
            ],
            'disgust': [
                ("WHEN I SEE", "SPAGHETTI CODE"),
                ("THIS CODE IS", "DISGUSTING"),
                ("WHO WROTE", "THIS MESS?"),
                ("WHEN THERE ARE", "NO COMMENTS"),
            ],
            'neutral': [
                ("JUST ANOTHER", "DAY OF CODING"),
                ("KEEPING CALM", "AND CODING ON"),
                ("NEUTRAL MODE:", "ACTIVATED"),
                ("JUST VIBING", "WITH THE CODE"),
            ]
        }
    
    def generate_meme(self, image_path, emotion, output_path):
        """
        Generate a meme based on the detected emotion
        
        Args:
            image_path: Path to the input image
            emotion: Detected emotion
            output_path: Path to save the generated meme
            
        Returns:
            str: Path to the generated meme
        """
        try:
            # Open the image
            img = Image.open(image_path)
            
            # Resize if too large
            max_size = 800
            if img.width > max_size or img.height > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Create a new image with space for text
            meme_height = img.height + 200  # Extra space for text
            meme_img = Image.new('RGB', (img.width, meme_height), color='white')
            
            # Paste the original image
            meme_img.paste(img, (0, 100))
            
            # Get random meme text for the emotion
            texts = self.meme_texts.get(emotion, self.meme_texts['neutral'])
            top_text, bottom_text = random.choice(texts)
            
            # Draw text
            draw = ImageDraw.Draw(meme_img)
            
            # Try to use a bold font, fallback to default if not available
            try:
                font_size = 40
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
                small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
            except:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Draw top text
            self._draw_text_with_outline(draw, top_text, (img.width // 2, 50), font)
            
            # Draw bottom text
            self._draw_text_with_outline(draw, bottom_text, (img.width // 2, meme_height - 50), font)
            
            # Draw emotion label
            emotion_text = f"Detected: {emotion.upper()}"
            self._draw_text_with_outline(draw, emotion_text, (img.width // 2, meme_height - 100), small_font, fill='yellow')
            
            # Save the meme
            meme_img.save(output_path, quality=95)
            
            return output_path
            
        except Exception as e:
            print(f"Error generating meme: {str(e)}")
            return None
    
    def _draw_text_with_outline(self, draw, text, position, font, fill='white', outline='black'):
        """
        Draw text with an outline for better visibility
        
        Args:
            draw: ImageDraw object
            text: Text to draw
            position: (x, y) position
            font: Font to use
            fill: Fill color
            outline: Outline color
        """
        x, y = position
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text
        x = x - text_width // 2
        y = y - text_height // 2
        
        # Draw outline
        outline_range = 2
        for adj_x in range(-outline_range, outline_range + 1):
            for adj_y in range(-outline_range, outline_range + 1):
                draw.text((x + adj_x, y + adj_y), text, font=font, fill=outline)
        
        # Draw main text
        draw.text((x, y), text, font=font, fill=fill)
    
    def get_meme_preview_text(self, emotion):
        """
        Get a preview of what meme text will be used
        
        Args:
            emotion: The emotion to get preview for
            
        Returns:
            tuple: (top_text, bottom_text)
        """
        texts = self.meme_texts.get(emotion, self.meme_texts['neutral'])
        return random.choice(texts)
