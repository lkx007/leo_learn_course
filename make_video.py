import os
import argparse
import subprocess
import textwrap
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
import numpy as np

# Configuration
FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"  # Alternative macOS Chinese font
FONT_SIZE_TITLE = 60
FONT_SIZE_BODY = 40
FONT_SIZE_CODE = 30
BG_COLOR_NARRATIVE = (255, 250, 240) # FloralWhite
BG_COLOR_CODE = (40, 44, 52)         # Dark for code
TEXT_COLOR_BODY = (0, 0, 0)
TEXT_COLOR_CODE = (200, 200, 200)
VIDEO_SIZE = (1280, 720)
VOICE = "Ting-Ting" # macOS Chinese Voice

class Scene:
    def __init__(self, text, type="narrative", title=None):
        self.text = text
        self.type = type # 'narrative', 'code', 'title'
        self.title = title
        self.code_output = None # New: Capture output for code scenes

class LessonParser:
    @staticmethod
    def parse(file_path):
        scenes = []
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_text = ""
        current_type = "narrative"
        current_title = None
        in_code_block = False
        expecting_output = False
        processing_output_block = False
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith("# "): # Main Title
                if current_text:
                    scenes.append(Scene(current_text, current_type, current_title))
                    current_text = ""
                current_title = stripped.replace("# ", "")
                scenes.append(Scene(current_title, "title", current_title))
                
            elif stripped.startswith("## "): # Section Title
                if current_text:
                    scenes.append(Scene(current_text, current_type, current_title))
                    current_text = ""
                current_title = stripped.replace("## ", "")
                scenes.append(Scene(current_title, "title", current_title))
            
            elif "电脑会输出" in stripped or "Computer outputs" in stripped:
                # Next code block should be treated as output for the previous code scene
                if scenes and scenes[-1].type == 'code':
                    expecting_output = True
                if current_text: # Flush any pending narrative before this line
                     scenes.append(Scene(current_text, "narrative", current_title))
                     current_text = ""

            elif stripped.startswith("```"): # Code Block Marker
                if in_code_block: # End of block
                    in_code_block = False
                    
                    if processing_output_block:
                        # Assign output to previous code scene
                        if scenes and scenes[-1].type == 'code':
                            scenes[-1].code_output = current_text.strip()
                        processing_output_block = False
                    else:
                        # Create new code scene
                        scenes.append(Scene(current_text.strip(), "code", current_title))
                    
                    current_text = ""
                else: # Start of block
                    if current_text:
                        scenes.append(Scene(current_text, "narrative", current_title))
                    current_text = ""
                    
                    in_code_block = True
                    if expecting_output:
                        processing_output_block = True
                        expecting_output = False
                    else:
                        processing_output_block = False
            
            else:
                if in_code_block:
                    current_text += line
                elif stripped: 
                    # Narrative text
                    current_text += line
        
        if current_text:
            scenes.append(Scene(current_text, current_type, current_title))
            
        return scenes

class ArtifactGenerator:
    def __init__(self, work_dir="temp_assets"):
        self.work_dir = work_dir
        if not os.path.exists(self.work_dir):
            os.makedirs(self.work_dir)
            
        # Load Fonts immediately
        try:
            self.font_title = ImageFont.truetype(FONT_PATH, FONT_SIZE_TITLE)
            self.font_body = ImageFont.truetype(FONT_PATH, FONT_SIZE_BODY)
            self.font_code = ImageFont.truetype(FONT_PATH, FONT_SIZE_CODE)
            self.font_ui = ImageFont.truetype(FONT_PATH, 20) # Smaller font for UI
        except OSError:
            print("Warning: Chinese font not found, falling back to default.")
            self.font_title = ImageFont.load_default()
            self.font_body = ImageFont.load_default()
            self.font_code = ImageFont.load_default()
            self.font_ui = ImageFont.load_default()

    def generate_audio(self, text, index):
        filename = os.path.join(self.work_dir, f"{index:03d}.aiff")
        # Clean text for speech
        clean_text = text.replace("---", "").replace("#", "").replace("- ", "").replace("```", "")
        if not clean_text.strip():
             return None # Skip empty
        subprocess.run(['say', '-v', VOICE, '-o', filename, clean_text])
        if not os.path.exists(filename):
            return None
        return filename

    def _draw_thonny_ui(self, draw, code_lines, output_lines, run_active=False):
        # Colors
        COLOR_BG = (230, 230, 230) # Window BG
        COLOR_EDITOR_BG = (255, 255, 255)
        COLOR_SHELL_BG = (250, 250, 250)
        COLOR_TITLE_BAR = (200, 200, 200)
        
        width, height = VIDEO_SIZE
        
        # 1. Background
        draw.rectangle([(0,0), VIDEO_SIZE], fill=COLOR_BG)
        
        # 2. Title Bar
        draw.rectangle([(0,0), (width, 30)], fill=COLOR_TITLE_BAR)
        draw.text((10, 5), "Thonny - <untitled>", font=self.font_ui, fill=(0,0,0))
        
        # 3. Menu Bar (simulated)
        draw.text((10, 35), "File  Edit  View  Run  Tools  Help", font=self.font_ui, fill=(0,0,0))
        
        # 4. Toolbar
        toolbar_y = 60
        # Run Button
        run_color = (0, 200, 0) if not run_active else (0, 255, 0)
        draw.ellipse([(10, toolbar_y), (40, toolbar_y+30)], fill=run_color)
        draw.polygon([(20, toolbar_y+8), (20, toolbar_y+22), (32, toolbar_y+15)], fill='white')
        
        # Stop Button
        draw.ellipse([(50, toolbar_y), (80, toolbar_y+30)], fill=(200, 0, 0))
        draw.rectangle([(60, toolbar_y+10), (70, toolbar_y+20)], fill='white')
        
        # 5. Editor Area (Top Split)
        editor_start_y = 100
        editor_height = int(height * 0.55)
        draw.rectangle([(0, editor_start_y), (width, editor_start_y+editor_height)], fill=COLOR_EDITOR_BG, outline=(200,200,200))
        
        # 6. Shell Area (Bottom Split)
        shell_start_y = editor_start_y + editor_height
        draw.rectangle([(0, shell_start_y), (width, height)], fill=COLOR_SHELL_BG, outline=(200,200,200))
        draw.text((5, shell_start_y + 5), "Shell", font=self.font_ui, fill=(100,100,100))

        # 7. Code Content
        line_height = 35
        for idx, line in enumerate(code_lines):
            draw.text((60, editor_start_y + 10 + idx * line_height), line, font=self.font_code, fill=(0,0,0)) # Line nums could be added
            # Line numbers
            draw.text((10, editor_start_y + 10 + idx * line_height), str(idx+1), font=self.font_code, fill=(200,200,200))

        # 8. Output Content
        for idx, line in enumerate(output_lines):
            draw.text((10, shell_start_y + 30 + idx * line_height), ">>> " + line if idx == 0 else line, font=self.font_code, fill=(0,0,0))

    def _create_image_frame(self, scene, visible_lines, extra_config=None):
        if extra_config is None: extra_config = {}
        
        img = Image.new('RGB', VIDEO_SIZE, color=BG_COLOR_NARRATIVE if scene.type != 'code' else BG_COLOR_CODE)
        draw = ImageDraw.Draw(img)
        
        if scene.type == 'code':
            # Use Thonny UI
            output_visible = extra_config.get('output_visible', [])
            run_active = extra_config.get('run_active', False)
            self._draw_thonny_ui(draw, visible_lines, output_visible, run_active)
            return img

        # Narrative / Title Logic
        margin = 60
        y_cursor = margin
        
        # Draw Title
        if scene.title and scene.type != 'title':
             draw.text((margin, y_cursor), scene.title, font=self.font_title, fill=(100, 100, 100))
             y_cursor += 80

        # Draw Content
        text_color = TEXT_COLOR_BODY
        font = self.font_body
        
        # Center title slides
        if scene.type == 'title':
            total_height = len(visible_lines) * 80
            y_cursor = (VIDEO_SIZE[1] - total_height) / 2
            text_color = (255, 100, 100) 

        for line in visible_lines:
            draw.text((margin, y_cursor), line, font=font, fill=text_color)
            y_cursor += 60
            
        return img

    def generate_dynamic_clip(self, scene, index, audio_clip=None):
        # 1. Prepare Text Lines
        if scene.type == 'code':
            # Don't wrap code lines for now to preserve structure, assume they fit or user formatted them
            wrapped_lines = scene.text.split('\n')
        else:
            max_char = 35 
            wrapped_lines = []
            for line in scene.text.split('\n'):
                 wrapped_lines.extend(textwrap.wrap(line, width=max_char))
        
        # 2. Determine Duration
        audio_dur = audio_clip.duration if audio_clip else 2.0
        final_duration = audio_dur + 0.5 
        
        num_lines = len(wrapped_lines)
        sub_clips = []
        
        if scene.type == 'code':
            # Code Animation Logic: Type Code -> Pause -> Click Run -> Show Output
            
            # Phase 1: Typing Code (Allocated 60% of time or fixed speed)
            # Phase 2: Run (Short click)
            # Phase 3: Output (Remaining time)
            
            output_lines = scene.code_output.split('\n') if scene.code_output else []
            has_output = len(output_lines) > 0
            
            time_typing = final_duration * 0.6
            time_run = 0.5
            time_output = final_duration - time_typing - time_run
            
            # A. Typing Effect
            if num_lines > 0:
                time_per_line = time_typing / num_lines
                start_time = 0
                for i in range(1, num_lines + 1):
                    current_visible = wrapped_lines[:i]
                    img = self._create_image_frame(scene, current_visible, {'output_visible': [], 'run_active': False})
                    dur = time_per_line
                    clip = ImageClip(np.array(img)).with_duration(dur)
                    sub_clips.append(clip)
            
            # B. Run Button Click
            img_run = self._create_image_frame(scene, wrapped_lines, {'output_visible': [], 'run_active': True})
            sub_clips.append(ImageClip(np.array(img_run)).with_duration(time_run))
            
            # C. Output Appearance
            if has_output:
                img_out = self._create_image_frame(scene, wrapped_lines, {'output_visible': output_lines, 'run_active': False})
                # If we want output to appear gradually? For now all at once or simple line by line if long
                sub_clips.append(ImageClip(np.array(img_out)).with_duration(max(0, time_output)))
            else:
                 # Just hold the code view
                 img_hold = self._create_image_frame(scene, wrapped_lines, {'output_visible': [], 'run_active': False})
                 sub_clips.append(ImageClip(np.array(img_hold)).with_duration(max(0, time_output)))

        else:
            # Narrative Animation Logic (Line by line)
            if num_lines == 0:
                 img = self._create_image_frame(scene, [])
                 return ImageClip(np.array(img)).with_duration(final_duration)

            time_per_line = audio_dur / num_lines
            
            for i in range(1, num_lines + 1):
                current_visible = wrapped_lines[:i]
                img = self._create_image_frame(scene, current_visible)
                if i == num_lines:
                    frame_duration = final_duration - (time_per_line * (i-1))
                else:
                    frame_duration = time_per_line
                
                clip = ImageClip(np.array(img)).with_duration(frame_duration)
                sub_clips.append(clip)
            
        # Concatenate
        combined_clip = concatenate_videoclips(sub_clips)
        
        # Attach Audio
        if audio_clip:
            combined_clip = combined_clip.with_audio(audio_clip)
            
        return combined_clip

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to markdown file")
    args = parser.parse_args()
    
    file_path = args.file
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    print("Parsing lesson...")
    scenes = LessonParser.parse(file_path)
    print(f"Found {len(scenes)} scenes.")
    
    generator = ArtifactGenerator()
    clips = []
    
    for i, scene in enumerate(scenes):
        print(f"Processing scene {i+1}/{len(scenes)}...")
        
        # Audio
        speech_text = scene.text
        if scene.type == 'code':
            speech_text = "代码演示 " + scene.title if scene.title else "代码演示"
        
        audio_path = generator.generate_audio(speech_text, i)
        audio_clip = AudioFileClip(audio_path) if audio_path else None
        
        # Clip
        try:
            video_clip = generator.generate_dynamic_clip(scene, i, audio_clip)
            clips.append(video_clip)
        except Exception as e:
            print(f"Error creating clip for scene {i}: {e}")
            import traceback
            traceback.print_exc()
            continue

    print("Assembling video...")
    final_clip = concatenate_videoclips(clips)
    
    output_filename = os.path.splitext(file_path)[0] + ".mp4"
    final_clip.write_videofile(output_filename, fps=24)
    print(f"Video saved to {output_filename}")

if __name__ == "__main__":
    main()
