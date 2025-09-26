# # from flask import Flask, request, jsonify, send_from_directory
# # import os
# # import requests
# # import json
# # from dotenv import load_dotenv

# # # Load .env file
# # load_dotenv()

# # app = Flask(__name__, static_folder="static")

# # # API configuration - Using OpenRouter as free alternative
# # OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# # OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions")

# # # In-memory storage for assessments (replace with database in production)
# # student_assessments = {}

# # def call_ai_api(prompt, system_message=None):
# #     """Call AI API with the given prompt (using OpenRouter)"""
# #     headers = {
# #         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
# #         "Content-Type": "application/json",
# #         "HTTP-Referer": "http://localhost:5000",
# #         "X-Title": "AI Course Generator"
# #     }
    
# #     messages = []
# #     if system_message:
# #         messages.append({"role": "system", "content": system_message})
# #     messages.append({"role": "user", "content": prompt})
    
# #     payload = {
# #         "model": "deepseek/deepseek-chat",
# #         "messages": messages,
# #         "temperature": 0.7,
# #         "max_tokens": 2048
# #     }
    
# #     try:
# #         response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
# #         response.raise_for_status()
# #         result = response.json()
# #         return result['choices'][0]['message']['content']
# #     except Exception as e:
# #         return f"AI API temporarily unavailable. Error: {str(e)}"

# # # Serve index.html
# # @app.route("/")
# # def home():
# #     return send_from_directory(".", "index.html")

# # # Course generation endpoint
# # @app.route("/generate_course", methods=["POST"])
# # def generate_course():
# #     data = request.get_json()
# #     topic = data.get("topic", "")
# #     student_id = data.get("student_id", "anonymous")

# #     if not topic:
# #         return jsonify({"error": "No topic provided"}), 400

# #     try:
# #         prompt = f"Create a clear, structured study course outline for the topic: {topic}. Include 3-5 practical assessment projects at the end. Keep it organized with modules and bullet points."
# #         system_message = "You are an educational content creator. Provide structured course outlines with practical assessments."
        
# #         response = call_ai_api(prompt, system_message)
        
# #         # Store course in memory (replace with database)
# #         if student_id not in student_assessments:
# #             student_assessments[student_id] = {}
# #         student_assessments[student_id]['course'] = response
# #         student_assessments[student_id]['progress'] = {"completed": [], "in_progress": []}
        
# #         return jsonify({"course": response.strip()})
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# # # AI Professor Q&A endpoint
# # @app.route("/ask_professor", methods=["POST"])
# # def ask_professor():
# #     data = request.get_json()
# #     question = data.get("question", "")
# #     student_id = data.get("student_id", "anonymous")

# #     if not question:
# #         return jsonify({"error": "No question provided"}), 400

# #     try:
# #         prompt = f"Give a clear, exam-oriented answer to this question: {question}. Keep the explanation structured, educational, and easy for students to understand."
# #         system_message = "You are a knowledgeable study professor. Provide clear, educational answers to student questions."
        
# #         response = call_ai_api(prompt, system_message)
# #         return jsonify({"answer": response.strip()})
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# # # Generate assessment endpoint
# # @app.route("/generate_assessment", methods=["POST"])
# # def generate_assessment():
# #     data = request.get_json()
# #     topic = data.get("topic", "")
# #     module_name = data.get("module", "")
# #     student_id = data.get("student_id", "anonymous")

# #     if not topic or not module_name:
# #         return jsonify({"error": "Topic and module name required"}), 400

# #     try:
# #         prompt = f"""
# #         Create a practical hands-on assessment project for the module: {module_name} in the topic: {topic}.
        
# #         Include:
# #         1. Project title and description
# #         2. Clear objectives and requirements
# #         3. Step-by-step instructions
# #         4. Expected deliverables
# #         5. Evaluation criteria
        
# #         Make it practical and suitable for students to actually build.
# #         """
# #         system_message = "You are an educational assessment designer. Create practical, hands-on projects that test real skills."
        
# #         response = call_ai_api(prompt, system_message)
        
# #         # Store assessment
# #         if student_id not in student_assessments:
# #             student_assessments[student_id] = {}
# #         if 'assessments' not in student_assessments[student_id]:
# #             student_assessments[student_id]['assessments'] = {}
        
# #         student_assessments[student_id]['assessments'][module_name] = {
# #             "assessment": response,
# #             "status": "assigned",
# #             "submission": None,
# #             "feedback": None
# #         }
        
# #         return jsonify({"assessment": response.strip()})
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# # # Submit assessment endpoint
# # @app.route("/submit_assessment", methods=["POST"])
# # def submit_assessment():
# #     data = request.get_json()
# #     module_name = data.get("module", "")
# #     submission = data.get("submission", "")
# #     student_id = data.get("student_id", "anonymous")

# #     if not module_name or not submission:
# #         return jsonify({"error": "Module name and submission required"}), 400

# #     try:
# #         # Store submission
# #         if (student_id in student_assessments and 
# #             'assessments' in student_assessments[student_id] and 
# #             module_name in student_assessments[student_id]['assessments']):
            
# #             student_assessments[student_id]['assessments'][module_name]['submission'] = submission
# #             student_assessments[student_id]['assessments'][module_name]['status'] = "submitted"
            
# #             return jsonify({"message": "Assessment submitted successfully!", "status": "submitted"})
# #         else:
# #             return jsonify({"error": "Assessment not found"}), 404
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# # # Evaluate assessment endpoint
# # @app.route("/evaluate_assessment", methods=["POST"])
# # def evaluate_assessment():
# #     data = request.get_json()
# #     module_name = data.get("module", "")
# #     student_id = data.get("student_id", "anonymous")

# #     if not module_name:
# #         return jsonify({"error": "Module name required"}), 400

# #     try:
# #         if (student_id not in student_assessments or 
# #             'assessments' not in student_assessments[student_id] or 
# #             module_name not in student_assessments[student_id]['assessments'] or
# #             not student_assessments[student_id]['assessments'][module_name]['submission']):
            
# #             return jsonify({"error": "Submission not found"}), 404

# #         submission = student_assessments[student_id]['assessments'][module_name]['submission']
# #         assessment = student_assessments[student_id]['assessments'][module_name]['assessment']
        
# #         prompt = f"""
# #         As an expert professor, evaluate this student's assessment submission.
        
# #         ASSESSMENT BRIEF:
# #         {assessment}
        
# #         STUDENT'S SUBMISSION:
# #         {submission}
        
# #         Provide:
# #         1. Overall score (0-100)
# #         2. Strengths and what was done well
# #         3. Areas for improvement
# #         4. Specific feedback and suggestions
# #         5. Encouraging closing remarks
        
# #         Be constructive, educational, and supportive.
# #         """
# #         system_message = "You are a supportive professor evaluating student work. Provide constructive feedback that helps students learn and improve."
        
# #         feedback = call_ai_api(prompt, system_message)
        
# #         # Store feedback
# #         student_assessments[student_id]['assessments'][module_name]['feedback'] = feedback
# #         student_assessments[student_id]['assessments'][module_name]['status'] = "evaluated"
        
# #         # Update progress
# #         if 'progress' in student_assessments[student_id]:
# #             if module_name not in student_assessments[student_id]['progress']['completed']:
# #                 student_assessments[student_id]['progress']['completed'].append(module_name)
        
# #         return jsonify({"feedback": feedback.strip(), "status": "evaluated"})
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# # # Get progress endpoint
# # @app.route("/get_progress", methods=["POST"])
# # def get_progress():
# #     data = request.get_json()
# #     student_id = data.get("student_id", "anonymous")

# #     try:
# #         if student_id in student_assessments:
# #             progress = student_assessments[student_id].get('progress', {})
# #             assessments = student_assessments[student_id].get('assessments', {})
# #             return jsonify({"progress": progress, "assessments": assessments})
# #         else:
# #             return jsonify({"progress": {"completed": [], "in_progress": []}, "assessments": {}})
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# # # Explain concept endpoint
# # @app.route("/explain_concept", methods=["POST"])
# # def explain_concept():
# #     data = request.get_json()
# #     topic = data.get("topic", "")

# #     if not topic:
# #         return jsonify({"error": "No topic provided"}), 400

# #     try:
# #         prompt = f"Explain the core concepts of {topic} in a simple, engaging way suitable for students. Break it down into fundamental principles and provide clear examples."
# #         system_message = "You are an engaging professor who explains concepts clearly with practical examples. Use analogies and simple language."
        
# #         response = call_ai_api(prompt, system_message)
# #         return jsonify({"explanation": response.strip()})
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# # # Give example endpoint
# # @app.route("/give_example", methods=["POST"])
# # def give_example():
# #     data = request.get_json()
# #     topic = data.get("topic", "")

# #     if not topic:
# #         return jsonify({"error": "No topic provided"}), 400

# #     try:
# #         prompt = f"Provide a practical, real-world example of {topic}. Make it engaging and educational, showing how this concept applies in practice."
# #         system_message = "You are a professor who provides excellent real-world examples that help students understand abstract concepts."
        
# #         response = call_ai_api(prompt, system_message)
# #         return jsonify({"example": response.strip()})
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# # # Summarize topic endpoint
# # @app.route("/summarize_topic", methods=["POST"])
# # def summarize_topic():
# #     data = request.get_json()
# #     topic = data.get("topic", "")

# #     if not topic:
# #         return jsonify({"error": "No topic provided"}), 400

# #     try:
# #         prompt = f"Create a concise but comprehensive summary of {topic}. Highlight the key points, main concepts, and most important takeaways for students."
# #         system_message = "You are a professor who creates excellent summaries that help students review and remember key information."
        
# #         response = call_ai_api(prompt, system_message)
# #         return jsonify({"summary": response.strip()})
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# # # Interactive video lessons endpoint (simulated)
# # @app.route("/get_video_lesson", methods=["POST"])
# # def get_video_lesson():
# #     data = request.get_json()
# #     topic = data.get("topic", "")
# #     module = data.get("module", "")

# #     if not topic:
# #         return jsonify({"error": "No topic provided"}), 400

# #     try:
# #         # In a real implementation, you would have actual video URLs
# #         # For now, we'll generate a simulated lesson script
# #         prompt = f"Create an interactive video lesson script for {module} in the course about {topic}. Include explanations, examples, and engaging questions for students."
# #         system_message = "You are a video lesson creator who makes engaging educational content with clear explanations and interactive elements."
        
# #         response = call_ai_api(prompt, system_message)
        
# #         # Simulate a video response (in a real app, you'd return actual video URLs)
# #         return jsonify({
# #             "lesson_script": response.strip(),
# #             "video_url": f"/static/videos/{topic}_{module}.mp4",  # This would be a real URL
# #             "duration": "15:30",
# #             "title": f"Interactive Lesson: {module}"
# #         })
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# # if __name__ == "__main__":      
# #     app.run(debug=True)



# from flask import Flask, request, jsonify, send_from_directory
# import os
# import requests
# import json
# from dotenv import load_dotenv
# from urllib.parse import quote

# # Load .env file
# load_dotenv()

# app = Flask(__name__, static_folder="static")

# # API configuration - Using OpenRouter as free alternative
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions")
# YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# # In-memory storage for assessments (replace with database in production)
# student_assessments = {}

# def call_ai_api(prompt, system_message=None):
#     """Call AI API with the given prompt (using OpenRouter)"""
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json",
#         "HTTP-Referer": "http://localhost:5000",
#         "X-Title": "AI Course Generator"
#     }
    
#     messages = []
#     if system_message:
#         messages.append({"role": "system", "content": system_message})
#     messages.append({"role": "user", "content": prompt})
    
#     payload = {
#         "model": "deepseek/deepseek-chat",
#         "messages": messages,
#         "temperature": 0.7,
#         "max_tokens": 2048
#     }
    
#     try:
#         response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
#         response.raise_for_status()
#         result = response.json()
#         return result['choices'][0]['message']['content']
#     except Exception as e:
#         return f"AI API temporarily unavailable. Error: {str(e)}"

# def search_youtube_videos(query, max_results=5):
#     """Search for educational videos on YouTube"""
#     if not YOUTUBE_API_KEY:
#         return {"error": "YouTube API key not configured"}
    
#     try:
#         # Format the query to focus on educational content
#         formatted_query = f"{query} tutorial lecture course education"
#         url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={max_results}&q={quote(formatted_query)}&type=video&key={YOUTUBE_API_KEY}"
        
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
        
#         videos = []
#         for item in data.get('items', []):
#             video_id = item['id']['videoId']
#             title = item['snippet']['title']
#             channel = item['snippet']['channelTitle']
#             description = item['snippet']['description']
#             thumbnail = item['snippet']['thumbnails']['high']['url']
            
#             videos.append({
#                 'video_id': video_id,
#                 'title': title,
#                 'channel': channel,
#                 'description': description,
#                 'thumbnail': thumbnail,
#                 'embed_url': f"https://www.youtube.com/embed/{video_id}"
#             })
        
#         return videos
#     except Exception as e:
#         return {"error": f"YouTube API error: {str(e)}"}

# # Serve index.html
# @app.route("/")
# def home():
#     return send_from_directory(".", "index.html")

# # Course generation endpoint
# @app.route("/generate_course", methods=["POST"])
# def generate_course():
#     data = request.get_json()
#     topic = data.get("topic", "")
#     student_id = data.get("student_id", "anonymous")

#     if not topic:
#         return jsonify({"error": "No topic provided"}), 400

#     try:
#         prompt = f"Create a clear, structured study course outline for the topic: {topic}. Include 3-5 practical assessment projects at the end. Keep it organized with modules and bullet points."
#         system_message = "You are an educational content creator. Provide structured course outlines with practical assessments."
        
#         response = call_ai_api(prompt, system_message)
        
#         # Store course in memory (replace with database)
#         if student_id not in student_assessments:
#             student_assessments[student_id] = {}
#         student_assessments[student_id]['course'] = response
#         student_assessments[student_id]['progress'] = {"completed": [], "in_progress": []}
        
#         return jsonify({"course": response.strip()})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # AI Professor Q&A endpoint
# @app.route("/ask_professor", methods=["POST"])
# def ask_professor():
#     data = request.get_json()
#     question = data.get("question", "")
#     student_id = data.get("student_id", "anonymous")

#     if not question:
#         return jsonify({"error": "No question provided"}), 400

#     try:
#         prompt = f"Give a clear, exam-oriented answer to this question: {question}. Keep the explanation structured, educational, and easy for students to understand."
#         system_message = "You are a knowledgeable study professor. Provide clear, educational answers to student questions."
        
#         response = call_ai_api(prompt, system_message)
#         return jsonify({"answer": response.strip()})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Generate assessment endpoint
# @app.route("/generate_assessment", methods=["POST"])
# def generate_assessment():
#     data = request.get_json()
#     topic = data.get("topic", "")
#     module_name = data.get("module", "")
#     student_id = data.get("student_id", "anonymous")

#     if not topic or not module_name:
#         return jsonify({"error": "Topic and module name required"}), 400

#     try:
#         prompt = f"""
#         Create a practical hands-on assessment project for the module: {module_name} in the topic: {topic}.
        
#         Include:
#         1. Project title and description
#         2. Clear objectives and requirements
#         3. Step-by-step instructions
#         4. Expected deliverables
#         5. Evaluation criteria
        
#         Make it practical and suitable for students to actually build.
#         """
#         system_message = "You are an educational assessment designer. Create practical, hands-on projects that test real skills."
        
#         response = call_ai_api(prompt, system_message)
        
#         # Store assessment
#         if student_id not in student_assessments:
#             student_assessments[student_id] = {}
#         if 'assessments' not in student_assessments[student_id]:
#             student_assessments[student_id]['assessments'] = {}
        
#         student_assessments[student_id]['assessments'][module_name] = {
#             "assessment": response,
#             "status": "assigned",
#             "submission": None,
#             "feedback": None
#         }
        
#         return jsonify({"assessment": response.strip()})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Submit assessment endpoint
# @app.route("/submit_assessment", methods=["POST"])
# def submit_assessment():
#     data = request.get_json()
#     module_name = data.get("module", "")
#     submission = data.get("submission", "")
#     student_id = data.get("student_id", "anonymous")

#     if not module_name or not submission:
#         return jsonify({"error": "Module name and submission required"}), 400

#     try:
#         # Store submission
#         if (student_id in student_assessments and 
#             'assessments' in student_assessments[student_id] and 
#             module_name in student_assessments[student_id]['assessments']):
            
#             student_assessments[student_id]['assessments'][module_name]['submission'] = submission
#             student_assessments[student_id]['assessments'][module_name]['status'] = "submitted"
            
#             return jsonify({"message": "Assessment submitted successfully!", "status": "submitted"})
#         else:
#             return jsonify({"error": "Assessment not found"}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Evaluate assessment endpoint
# @app.route("/evaluate_assessment", methods=["POST"])
# def evaluate_assessment():
#     data = request.get_json()
#     module_name = data.get("module", "")
#     student_id = data.get("student_id", "anonymous")

#     if not module_name:
#         return jsonify({"error": "Module name required"}), 400

#     try:
#         if (student_id not in student_assessments or 
#             'assessments' not in student_assessments[student_id] or 
#             module_name not in student_assessments[student_id]['assessments'] or
#             not student_assessments[student_id]['assessments'][module_name]['submission']):
            
#             return jsonify({"error": "Submission not found"}), 404

#         submission = student_assessments[student_id]['assessments'][module_name]['submission']
#         assessment = student_assessments[student_id]['assessments'][module_name]['assessment']
        
#         prompt = f"""
#         As an expert professor, evaluate this student's assessment submission.
        
#         ASSESSMENT BRIEF:
#         {assessment}
        
#         STUDENT'S SUBMISSION:
#         {submission}
        
#         Provide:
#         1. Overall score (0-100)
#         2. Strengths and what was done well
#         3. Areas for improvement
#         4. Specific feedback and suggestions
#         5. Encouraging closing remarks
        
#         Be constructive, educational, and supportive.
#         """
#         system_message = "You are a supportive professor evaluating student work. Provide constructive feedback that helps students learn and improve."
        
#         feedback = call_ai_api(prompt, system_message)
        
#         # Store feedback
#         student_assessments[student_id]['assessments'][module_name]['feedback'] = feedback
#         student_assessments[student_id]['assessments'][module_name]['status'] = "evaluated"
        
#         # Update progress
#         if 'progress' in student_assessments[student_id]:
#             if module_name not in student_assessments[student_id]['progress']['completed']:
#                 student_assessments[student_id]['progress']['completed'].append(module_name)
        
#         return jsonify({"feedback": feedback.strip(), "status": "evaluated"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Get progress endpoint
# @app.route("/get_progress", methods=["POST"])
# def get_progress():
#     data = request.get_json()
#     student_id = data.get("student_id", "anonymous")

#     try:
#         if student_id in student_assessments:
#             progress = student_assessments[student_id].get('progress', {})
#             assessments = student_assessments[student_id].get('assessments', {})
#             return jsonify({"progress": progress, "assessments": assessments})
#         else:
#             return jsonify({"progress": {"completed": [], "in_progress": []}, "assessments": {}})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Explain concept endpoint
# @app.route("/explain_concept", methods=["POST"])
# def explain_concept():
#     data = request.get_json()
#     topic = data.get("topic", "")

#     if not topic:
#         return jsonify({"error": "No topic provided"}), 400

#     try:
#         prompt = f"Explain the core concepts of {topic} in a simple, engaging way suitable for students. Break it down into fundamental principles and provide clear examples."
#         system_message = "You are an engaging professor who explains concepts clearly with practical examples. Use analogies and simple language."
        
#         response = call_ai_api(prompt, system_message)
#         return jsonify({"explanation": response.strip()})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Give example endpoint
# @app.route("/give_example", methods=["POST"])
# def give_example():
#     data = request.get_json()
#     topic = data.get("topic", "")

#     if not topic:
#         return jsonify({"error": "No topic provided"}), 400

#     try:
#         prompt = f"Provide a practical, real-world example of {topic}. Make it engaging and educational, showing how this concept applies in practice."
#         system_message = "You are a professor who provides excellent real-world examples that help students understand abstract concepts."
        
#         response = call_ai_api(prompt, system_message)
#         return jsonify({"example": response.strip()})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Summarize topic endpoint
# @app.route("/summarize_topic", methods=["POST"])
# def summarize_topic():
#     data = request.get_json()
#     topic = data.get("topic", "")

#     if not topic:
#         return jsonify({"error": "No topic provided"}), 400

#     try:
#         prompt = f"Create a concise but comprehensive summary of {topic}. Highlight the key points, main concepts, and most important takeaways for students."
#         system_message = "You are a professor who creates excellent summaries that help students review and remember key information."
        
#         response = call_ai_api(prompt, system_message)
#         return jsonify({"summary": response.strip()})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Get video lectures from YouTube
# @app.route("/get_video_lectures", methods=["POST"])
# def get_video_lectures():
#     data = request.get_json()
#     topic = data.get("topic", "")
#     module = data.get("module", "")

#     if not topic:
#         return jsonify({"error": "No topic provided"}), 400

#     try:
#         # Search for videos based on the topic and module
#         search_query = f"{topic} {module}" if module else topic
#         videos = search_youtube_videos(search_query)
        
#         if "error" in videos:
#             return jsonify({"error": videos["error"]}), 500
            
#         return jsonify({
#             "videos": videos,
#             "topic": topic,
#             "module": module
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":      
#     app.run(debug=True)

from flask import Flask, request, jsonify, send_from_directory
import os
import requests
import json
from dotenv import load_dotenv
from urllib.parse import quote

# Load .env file
load_dotenv()

app = Flask(__name__, static_folder="static")

# API configuration - Using OpenRouter as free alternative
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# In-memory storage for assessments (replace with database in production)
student_assessments = {}

def call_ai_api(prompt, system_message=None):
    """Call AI API with the given prompt (using OpenRouter)"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "AI Course Generator"
    }
    
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2048
    }
    
    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"AI API temporarily unavailable. Error: {str(e)}"


def search_youtube_videos(query, max_results=5):
    """Search for educational videos on YouTube with better query formatting"""
    if not YOUTUBE_API_KEY:
        return {"error": "YouTube API key not configured"}
    
    try:
        # Better query formatting for educational content
        formatted_query = f"{query} tutorial course education learn how to"
        
        # YouTube API endpoint
        url = f"https://www.googleapis.com/youtube/v3/search"
        params = {
            'part': 'snippet',
            'maxResults': max_results,
            'q': formatted_query,
            'type': 'video',
            'key': YOUTUBE_API_KEY,
            'relevanceLanguage': 'en',
            'videoDuration': 'medium',  # Prefer medium-length videos (4-20 minutes)
            'videoEmbeddable': 'true'   # Only embeddable videos
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        videos = []
        for item in data.get('items', []):
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            channel = item['snippet']['channelTitle']
            description = item['snippet']['description']
            thumbnail = item['snippet']['thumbnails']['high']['url']
            
            videos.append({
                'video_id': video_id,
                'title': title,
                'channel': channel,
                'description': description,
                'thumbnail': thumbnail,
                'embed_url': f"https://www.youtube.com/embed/{video_id}",
                'watch_url': f"https://www.youtube.com/watch?v={video_id}"
            })
        
        return videos
    except Exception as e:
        print(f"YouTube API error: {str(e)}")
        return {"error": f"YouTube API temporarily unavailable: {str(e)}"}

# def search_youtube_videos(query, max_results=5):
#     """Search for educational videos on YouTube"""
#     if not YOUTUBE_API_KEY:
#         return {"error": "YouTube API key not configured"}
    
#     try:
#         # Format the query to focus on educational content
#         formatted_query = f"{query} tutorial lecture course education"
#         url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={max_results}&q={quote(formatted_query)}&type=video&key={YOUTUBE_API_KEY}"
        
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
        
#         videos = []
#         for item in data.get('items', []):
#             video_id = item['id']['videoId']
#             title = item['snippet']['title']
#             channel = item['snippet']['channelTitle']
#             description = item['snippet']['description']
#             thumbnail = item['snippet']['thumbnails']['high']['url']
            
#             videos.append({
#                 'video_id': video_id,
#                 'title': title,
#                 'channel': channel,
#                 'description': description,
#                 'thumbnail': thumbnail,
#                 'embed_url': f"https://www.youtube.com/embed/{video_id}"
#             })
        
#         return videos
#     except Exception as e:
#         return {"error": f"YouTube API error: {str(e)}"}

# Serve index.html
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# Course generation endpoint
@app.route("/generate_course", methods=["POST"])
def generate_course():
    data = request.get_json()
    topic = data.get("topic", "")
    student_id = data.get("student_id", "anonymous")

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    try:
        prompt = f"Create a clear, structured study course outline for the topic: {topic}. Include 3-5 practical assessment projects at the end. Keep it organized with modules and bullet points."
        system_message = "You are an educational content creator. Provide structured course outlines with practical assessments."
        
        response = call_ai_api(prompt, system_message)
        
        # Store course in memory (replace with database)
        if student_id not in student_assessments:
            student_assessments[student_id] = {}
        student_assessments[student_id]['course'] = response
        student_assessments[student_id]['progress'] = {"completed": [], "in_progress": []}
        
        return jsonify({"course": response.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# AI Professor Q&A endpoint
@app.route("/ask_professor", methods=["POST"])
def ask_professor():
    data = request.get_json()
    question = data.get("question", "")
    student_id = data.get("student_id", "anonymous")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        prompt = f"Give a clear, exam-oriented answer to this question: {question}. Keep the explanation structured, educational, and easy for students to understand."
        system_message = "You are a knowledgeable study professor. Provide clear, educational answers to student questions."
        
        response = call_ai_api(prompt, system_message)
        return jsonify({"answer": response.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Generate assessment endpoint
@app.route("/generate_assessment", methods=["POST"])
def generate_assessment():
    data = request.get_json()
    topic = data.get("topic", "")
    module_name = data.get("module", "")
    student_id = data.get("student_id", "anonymous")

    if not topic or not module_name:
        return jsonify({"error": "Topic and module name required"}), 400

    try:
        prompt = f"""
        Create a practical hands-on assessment project for the module: {module_name} in the topic: {topic}.
        
        Include:
        1. Project title and description
        2. Clear objectives and requirements
        3. Step-by-step instructions
        4. Expected deliverables
        5. Evaluation criteria
        
        Make it practical and suitable for students to actually build.
        """
        system_message = "You are an educational assessment designer. Create practical, hands-on projects that test real skills."
        
        response = call_ai_api(prompt, system_message)
        
        # Store assessment
        if student_id not in student_assessments:
            student_assessments[student_id] = {}
        if 'assessments' not in student_assessments[student_id]:
            student_assessments[student_id]['assessments'] = {}
        
        student_assessments[student_id]['assessments'][module_name] = {
            "assessment": response,
            "status": "assigned",
            "submission": None,
            "feedback": None
        }
        
        return jsonify({"assessment": response.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Submit assessment endpoint
@app.route("/submit_assessment", methods=["POST"])
def submit_assessment():
    data = request.get_json()
    module_name = data.get("module", "")
    submission = data.get("submission", "")
    student_id = data.get("student_id", "anonymous")

    if not module_name or not submission:
        return jsonify({"error": "Module name and submission required"}), 400

    try:
        # Store submission
        if (student_id in student_assessments and 
            'assessments' in student_assessments[student_id] and 
            module_name in student_assessments[student_id]['assessments']):
            
            student_assessments[student_id]['assessments'][module_name]['submission'] = submission
            student_assessments[student_id]['assessments'][module_name]['status'] = "submitted"
            
            return jsonify({"message": "Assessment submitted successfully!", "status": "submitted"})
        else:
            return jsonify({"error": "Assessment not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Evaluate assessment endpoint (FIXED VERSION)
@app.route("/evaluate_assessment", methods=["POST"])
def evaluate_assessment():
    data = request.get_json()
    module_name = data.get("module", "")
    student_id = data.get("student_id", "anonymous")

    if not module_name:
        return jsonify({"error": "Module name required"}), 400

    try:
        if (student_id not in student_assessments or 
            'assessments' not in student_assessments[student_id] or 
            module_name not in student_assessments[student_id]['assessments'] or
            not student_assessments[student_id]['assessments'][module_name]['submission']):
            
            return jsonify({"error": "Submission not found"}), 404

        submission = student_assessments[student_id]['assessments'][module_name]['submission']
        assessment = student_assessments[student_id]['assessments'][module_name]['assessment']
        
        prompt = f"""
        As an expert professor, evaluate this student's assessment submission.
        
        ASSESSMENT BRIEF:
        {assessment}
        
        STUDENT'S SUBMISSION:
        {submission}
        
        Provide:
        1. Overall score (0-100)
        2. Strengths and what was done well
        3. Areas for improvement
        4. Specific feedback and suggestions
        5. Encouraging closing remarks
        
        Be constructive, educational, and supportive.
        """
        system_message = "You are a supportive professor evaluating student work. Provide constructive feedback that helps students learn and improve."
        
        feedback = call_ai_api(prompt, system_message)
        
        # Store feedback
        student_assessments[student_id]['assessments'][module_name]['feedback'] = feedback
        student_assessments[student_id]['assessments'][module_name]['status'] = "evaluated"
        
        # FIXED: Update progress - Ensure progress structure exists
        if student_id not in student_assessments:
            student_assessments[student_id] = {}
        
        if 'progress' not in student_assessments[student_id]:
            student_assessments[student_id]['progress'] = {"completed": [], "in_progress": []}
        
        # Add module to completed list if not already there
        if module_name not in student_assessments[student_id]['progress']['completed']:
            student_assessments[student_id]['progress']['completed'].append(module_name)
        
        return jsonify({"feedback": feedback.strip(), "status": "evaluated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get progress endpoint
@app.route("/get_progress", methods=["POST"])
def get_progress():
    data = request.get_json()
    student_id = data.get("student_id", "anonymous")

    try:
        if student_id in student_assessments:
            progress = student_assessments[student_id].get('progress', {})
            assessments = student_assessments[student_id].get('assessments', {})
            return jsonify({"progress": progress, "assessments": assessments})
        else:
            return jsonify({"progress": {"completed": [], "in_progress": []}, "assessments": {}})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Explain concept endpoint
@app.route("/explain_concept", methods=["POST"])
def explain_concept():
    data = request.get_json()
    topic = data.get("topic", "")

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    try:
        prompt = f"Explain the core concepts of {topic} in a simple, engaging way suitable for students. Break it down into fundamental principles and provide clear examples."
        system_message = "You are an engaging professor who explains concepts clearly with practical examples. Use analogies and simple language."
        
        response = call_ai_api(prompt, system_message)
        return jsonify({"explanation": response.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Give example endpoint
@app.route("/give_example", methods=["POST"])
def give_example():
    data = request.get_json()
    topic = data.get("topic", "")

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    try:
        prompt = f"Provide a practical, real-world example of {topic}. Make it engaging and educational, showing how this concept applies in practice."
        system_message = "You are a professor who provides excellent real-world examples that help students understand abstract concepts."
        
        response = call_ai_api(prompt, system_message)
        return jsonify({"example": response.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Summarize topic endpoint
@app.route("/summarize_topic", methods=["POST"])
def summarize_topic():
    data = request.get_json()
    topic = data.get("topic", "")

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    try:
        prompt = f"Create a concise but comprehensive summary of {topic}. Highlight the key points, main concepts, and most important takeaways for students."
        system_message = "You are a professor who creates excellent summaries that help students review and remember key information."
        
        response = call_ai_api(prompt, system_message)
        return jsonify({"summary": response.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get video lectures from YouTube
@app.route("/get_video_lectures", methods=["POST"])
def get_video_lectures():
    data = request.get_json()
    topic = data.get("topic", "")
    module = data.get("module", "")

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    try:
        # Search for videos based on the topic and module
        search_query = f"{topic} {module}" if module else topic
        videos = search_youtube_videos(search_query)
        
        if "error" in videos:
            return jsonify({"error": videos["error"]}), 500
            
        return jsonify({
            "videos": videos,
            "topic": topic,
            "module": module
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":      
    app.run(debug=True)