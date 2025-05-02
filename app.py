import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter
import os
from dotenv import load_dotenv
from organizational_rules import rules_text

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found. Please set it in your .env file.")
    st.stop()

llm = ChatOpenAI(
    model="gpt-4", 
    temperature=0.1, 
    api_key=api_key
)

def get_code_fixer_chain():
    prompt = ChatPromptTemplate.from_template("""
You are a cybersecurity expert specialized in secure coding practices across all programming languages. Your task is to analyze the provided code snippet and issue description to identify security vulnerabilities and provide a secure implementation.

CODE SNIPPET:
```
{code}
```

VULNERABILITY TYPE: {vulnerability_type}

ISSUE DESCRIPTION:
{issue_description}

INSTRUCTIONS:
1. Identify the programming language and address the specified security vulnerability in the code
2. Fix the security issue while maintaining the original functionality
3. Return ONLY the fixed code with no explanation, comments, or other text
4. Do not include markdown formatting in your response (no ```code``` blocks)
5. The entire response should be only the fixed code, nothing else

Remember: Your entire response must contain only the fixed code, with absolutely no explanations, introductions, or descriptions before or after.
""")
    
    return prompt | llm | StrOutputParser()

def get_analyze_priority_chain():
    prompt = ChatPromptTemplate.from_template("""
You are a security expert specializing in vulnerability prioritization. Your task is to analyze a vulnerability type and determine how it's prioritized in an organization's documentation.

VULNERABILITY TYPE: {vulnerability_type}

ORGANIZATION'S VULNERABILITY PRIORITY DOCUMENT:
{priority_document}

SYSTEM PRIORITY (Standard industry rating): {system_priority}

INSTRUCTIONS:
1. Carefully review the organization's vulnerability priority document
2. Find where the specified vulnerability type is mentioned in the document
3. Determine the organization's priority level (Critical, High, Medium, or Low) for this vulnerability
4. Extract the rationale for this priority level from the document
5. Compare the organization's priority with the standard industry rating
6. Provide your analysis in the following format:

ORGANIZATIONAL_PRIORITY: [Priority level found in the document (Critical, High, Medium, Low, or Not Found)]
RATIONALE: [The exact rationale text from the document, or "Not specified" if not found]
PRIORITY_COMPARISON: [Higher/Lower/Same compared to system priority, or "Unknown" if not found]

Use only information explicitly stated in the document. If the vulnerability is not found in the document, clearly indicate this.
""")
    
    return prompt | llm | StrOutputParser()

def clean_code_response(response):
    """Remove markdown formatting if present"""
    if "```" in response:
        start_marker = response.find("```")

        first_line_end = response.find("\n", start_marker)

        code_start = first_line_end + 1 if first_line_end > -1 else start_marker + 3

        end_marker = response.rfind("```")

        if end_marker > code_start:
            code = response[code_start:end_marker].strip()
            return code
    
    return response.strip()

def guess_language(code):
    """Attempt to guess the programming language of the code"""
    try:
        lexer = guess_lexer(code)
        return lexer.name.lower()
    except:
        return "text"  # Default fallback

# Define 
#  types by language
VULNERABILITY_TYPES = {
    "General": [
        "Cross-Site Scripting (XSS)",
        "Prototype Pollution",
        "Insecure Direct Object References (IDOR)",
        "SQL Injection",
        "Command Injection",
        "Path Traversal",
        "Remote File Inclusion (RFI)",
        "Cross-Site Request Forgery (CSRF)",
        "Insecure Deserialization",
        "XML External Entity (XXE) Injection",
        "Insecure Randomness",
        "Buffer Overflow",
        "Use After Free",
        "Template Injection",
        "Improper Error Handling"
    ],
}

# Define system priority levels for vulnerabilities (from standard security frameworks)
SYSTEM_PRIORITY_LEVELS = {
    "SQL Injection": "Critical",
    "Cross-Site Scripting (XSS)": "High",
    "Command Injection": "Critical",
    "Path Traversal": "High",
    "Authentication Issues": "Critical",
    "Authorization Issues": "Critical",
    "Insecure Direct Object References (IDOR)": "High",
    "Security Misconfiguration": "Medium",
    "Insecure Deserialization": "High",
    "Prototype Pollution": "High",
    "DOM-based Vulnerabilities": "Medium",
    "NoSQL Injection": "High",
    "Client-side Authorization Checks": "Medium",
    "Weak Password Storage": "High",
    "Server-Side Template Injection": "High",
    "Pickle Deserialization": "High",
    "Remote File Inclusion": "Critical",
    "Local File Inclusion": "High",
    "XML External Entity (XXE) Injection": "High",
    "Improper Authentication": "Critical",
    "Buffer Overflow": "Critical",
    "Memory Leaks": "Medium",
    "Use After Free": "High",
    "Integer Overflow": "Medium",
    "Format String Vulnerabilities": "High",
    "Template Injection": "High",
    "Improper Error Handling": "Medium",
    "Insecure Randomness": "Medium",
}

# Streamlit UI
st.set_page_config(page_title="Secure Code Generator", page_icon="🔒", layout="wide")

st.title("Secure Code Generator")
st.markdown("""
This application automatically fixes security vulnerabilities in your code.
Just paste your code, select the vulnerability type (if known), and describe the security issue.
""")

st.subheader("Enter your code:")
code_input = st.text_area("", height=250, placeholder="Paste your code here...")

# Try to guess the language for better vulnerability selection
guessed_language = "General"
if code_input:
    detected_lang = guess_language(code_input)
    if "javascript" in detected_lang or "js" in detected_lang:
        guessed_language = "JavaScript"
    elif "python" in detected_lang:
        guessed_language = "Python"
    elif "php" in detected_lang:
        guessed_language = "PHP"
    elif "java" in detected_lang:
        guessed_language = "Java"
    elif "c++" in detected_lang or "cpp" in detected_lang or "c" == detected_lang:
        guessed_language = "C/C++"
    elif "go" in detected_lang:
        guessed_language = "Go"

# Vulnerability selection
st.subheader("Security Issue Information:")
col1, col2 = st.columns([1, 1])

with col1:
    # Common vulnerabilities + language-specific ones if we detect the language
    vulnerability_options = VULNERABILITY_TYPES["General"].copy()
    if guessed_language in VULNERABILITY_TYPES and guessed_language != "General":
        vulnerability_options.extend(VULNERABILITY_TYPES[guessed_language])
    
    selected_vulnerability = st.selectbox(
        "Select Vulnerability Type (if known):",
        vulnerability_options
    )

    # Show system priority level if a specific vulnerability is selected
    if selected_vulnerability != "Select vulnerability type (optional)" and selected_vulnerability != "Other (describe below)":
        priority = SYSTEM_PRIORITY_LEVELS.get(selected_vulnerability, "Unknown")
        priority_color = {
            "Critical": "red",
            "High": "orange",
            "Medium": "blue",
            "Low": "green",
            "Unknown": "gray"
        }.get(priority, "gray")
        
        st.markdown(f"<div style='background-color: {priority_color}; padding: 5px 10px; border-radius: 5px; color: white; display: inline-block; margin-top: 5px;'>System Priority: {priority}</div>", unsafe_allow_html=True)

with col2:
    issue_description = st.text_area(
        "Describe the security issue or concern:", 
        height=100,
        placeholder="Example: I think this code might be vulnerable to SQL injection, or I'm concerned about user input validation..."
    )

# Prepare the vulnerability type for the prompt
vulnerability_type = ""
if selected_vulnerability and selected_vulnerability != "Select vulnerability type (optional)":
    vulnerability_type = selected_vulnerability
    if selected_vulnerability == "Other (describe below)":
        vulnerability_type = "Custom vulnerability (see description)"

# Generate button
if st.button("Generate Secure Code"):
    if not code_input:
        st.error("Please enter code to analyze.")
    elif not issue_description and (not vulnerability_type or vulnerability_type == "Custom vulnerability (see description)"):
        st.error("Please either select a vulnerability type or provide a description of the security issue.")
    else:
        with st.spinner("Generating secure code..."):
            # Create the LangChain chain
            code_fixer_chain = get_code_fixer_chain()
            
            # Process the inputs
            fixed_code = code_fixer_chain.invoke({
                "code": code_input,
                "vulnerability_type": vulnerability_type,
                "issue_description": issue_description
            })
            
            # Clean the response if needed
            fixed_code = clean_code_response(fixed_code)
            
            # Try to guess the language for syntax highlighting
            guessed_language_for_display = guess_language(code_input)
            
            # Display the fixed code
            st.subheader("Secure Code")
            st.code(fixed_code, language=guessed_language_for_display)
            
            # Add a button to copy the fixed code
            file_extension = {
                "python": "py",
                "javascript": "js",
                "java": "java",
                "cpp": "cpp",
                "c++": "cpp",
                "c": "c",
                "csharp": "cs",
                "c#": "cs",
                "php": "php",
                "ruby": "rb",
                "go": "go",
                "sql": "sql",
                "typescript": "ts"
            }.get(guessed_language_for_display, "txt")
            
            st.download_button(
                label="Download Secure Code",
                data=fixed_code,
                file_name=f"secure_code.{file_extension}",
                mime="text/plain"
            )

if st.button("Analyze priority"):
    with st.spinner("Analyzing priority.."):
        analyze_priority_chain = get_analyze_priority_chain()
        priority = SYSTEM_PRIORITY_LEVELS.get(selected_vulnerability, "Unknown")
        priority_document = rules_text()
        analysis = analyze_priority_chain.invoke({
            "vulnerability_type": vulnerability_type,
            "priority_document": priority_document,
            "system_priority": priority
        })
        st.markdown(analysis)

# Footer
st.markdown("---")
st.markdown("Created for secure code generation. Not a substitute for professional security review.")