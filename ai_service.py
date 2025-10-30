import asyncio
from typing import Optional
import openai

class AIService:
    def __init__(self, api_key: Optional[str]):
        self.api_key = api_key
        self.client = None
        if api_key:
            self.client = openai.OpenAI(api_key=api_key)
    
    async def analyze_script(self, script: str) -> dict:
        if not self.client:
            return {
                'safe': True,
                'analysis': 'AI analysis not available (no API key)',
                'confidence': 0
            }
        
        try:
            prompt = f"""Analyze this Lua/Roblox script for safety and malicious behavior.
Look for:
- Malicious functions (getfenv, setfenv, loadstring abuse)
- Data stealing attempts
- Keylogging or input monitoring
- Unauthorized API calls
- Obfuscated or suspicious code patterns

Script to analyze:
{script[:2000]}

Provide a brief safety analysis (2-3 sentences) and rate it as 'safe', 'suspicious', or 'dangerous'."""

            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert analyzing Lua scripts for safety."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content or ""
            
            safety_level = 'safe'
            if analysis_text and ('dangerous' in analysis_text.lower() or 'malicious' in analysis_text.lower()):
                safety_level = 'dangerous'
            elif analysis_text and ('suspicious' in analysis_text.lower() or 'caution' in analysis_text.lower()):
                safety_level = 'suspicious'
            
            return {
                'safe': safety_level == 'safe',
                'analysis': analysis_text,
                'confidence': 85,
                'level': safety_level
            }
        except Exception as e:
            return {
                'safe': True,
                'analysis': f'AI analysis failed: {str(e)}',
                'confidence': 0
            }
    
    async def get_helpful_error_message(self, error: str, link: str) -> str:
        if not self.client:
            return "Try checking if the link is from a supported service."
        
        try:
            prompt = f"""A user tried to bypass this link: {link}
But got this error: {error}

Provide a brief, helpful suggestion (1-2 sentences) on what might be wrong and how to fix it."""

            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant providing troubleshooting advice for link bypass errors."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.5
            )
            
            return response.choices[0].message.content or "Try checking if the link is valid and from a supported service."
        except:
            return "Try checking if the link is valid and from a supported service."
    
    async def summarize_script(self, script: str, max_length: int = 500) -> str:
        if not self.client:
            return script[:max_length]
        
        if len(script) <= max_length:
            return script
        
        try:
            prompt = f"""Summarize what this Roblox/Lua script does in a concise way (under 200 characters):

{script[:1000]}"""

            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a code analyzer that summarizes scripts concisely."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.3
            )
            
            return response.choices[0].message.content or script[:max_length]
        except:
            return script[:max_length]
