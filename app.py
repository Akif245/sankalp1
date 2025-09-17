# from flask import Flask, request, jsonify, send_from_directory
# import os
# import requests
# from dotenv import load_dotenv

# # Load .env file
# load_dotenv()

# app = Flask(__name__, static_folder="static")

# # API configuration - Using OpenRouter as free alternative
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions")

# def call_ai_api(prompt, system_message=None):
#     """Call AI API with the given prompt (using OpenRouter)"""
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json",
#         "HTTP-Referer": "http://localhost:5000",  # Required by OpenRouter
#         "X-Title": "AI Course Generator"  # Required by OpenRouter
#     }
    
#     messages = []
#     if system_message:
#         messages.append({"role": "system", "content": system_message})
#     messages.append({"role": "user", "content": prompt})
    
#     payload = {
#         "model": "deepseek/deepseek-chat",  # Using DeepSeek through OpenRouter
#         "messages": messages,
#         "temperature": 0.7,
#         "max_tokens": 2048
#     }
    
#     try:
#         response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
#         response.raise_for_status()
#         result = response.json()
#         return result['choices'][0]['message']['content']
#     except requests.exceptions.HTTPError as e:
#         if response.status_code == 402:
#             return fallback_response(prompt, system_message)
#         raise Exception(f"API error: {str(e)}")
#     except Exception as e:
#         raise Exception(f"API error: {str(e)}")

# def fallback_response(prompt, system_message=None):
#     """Fallback response when API is not available"""
#     if "course outline" in prompt.lower():
#         topic = prompt.split("topic:")[-1].split(".")[0].strip()
#         return f"""# {topic.title()} Course Outline

# ## Module 1: Introduction to {topic}
# - Basic concepts and terminology
# - Historical background
# - Importance and applications

# ## Module 2: Core Principles
# - Fundamental theories
# - Key methodologies
# - Practical examples

# ## Module 3: Advanced Topics
# - Complex concepts
# - Real-world applications
# - Case studies

# ## Module 4: Practical Implementation
# - Hands-on exercises
# - Project work
# - Best practices

# ## Assessment
# - Quizzes and tests
# - Final project
# - Certification criteria

# *Note: This is a sample outline. For a detailed course, please add credits to your API account.*"""
#     else:
#         return f"I'd be happy to help with that question. However, the AI service requires credits to provide detailed answers. Please add credits to your API account for full functionality. Meanwhile, you might want to research: {prompt}"

# # Serve index.html
# @app.route("/")
# def home():
#     return send_from_directory(".", "index.html")

# # Course generation endpoint
# @app.route("/generate_course", methods=["POST"])
# def generate_course():
#     data = request.get_json()
#     topic = data.get("topic", "")

#     if not topic:
#         return jsonify({"error": "No topic provided"}), 400

#     try:
#         prompt = f"Create a clear, structured study course outline for the topic: {topic}. Keep it simple, organized with bullet points or numbered steps."
#         system_message = "You are an educational content creator. Provide structured, easy-to-follow course outlines."
        
#         response = call_ai_api(prompt, system_message)
#         return jsonify({"course": response.strip()})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # AI Professor Q&A endpoint
# @app.route("/ask_professor", methods=["POST"])
# def ask_professor():
#     data = request.get_json()
#     question = data.get("question", "")

#     if not question:
#         return jsonify({"error": "No question provided"}), 400

#     try:
#         prompt = f"Give a clear, exam-oriented answer to this question: {question}. Keep the explanation structured, educational, and easy for students to understand."
#         system_message = "You are a knowledgeable study professor. Provide clear, educational answers to student questions."
        
#         response = call_ai_api(prompt, system_message)
#         return jsonify({"answer": response.strip()})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, jsonify, send_from_directory
import os
import requests
import json
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = Flask(__name__, static_folder="static")

# API configuration - Using OpenRouter as free alternative
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions")

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

# Serve index.html
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# Course generation endpoint
@app.route("/generate_course", methods=["POST"])
def generate_course():
    data = request.get_json()
    topic = data.get("topic", "")
    student_id = data.get("student_id", "anonymous")  # Simple user tracking

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

# Evaluate assessment endpoint
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
        
        # Update progress
        if 'progress' in student_assessments[student_id]:
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

if __name__ == "__main__":
    app.run(debug=True)