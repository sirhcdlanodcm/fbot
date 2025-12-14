"""Google Gemini provider implementation."""

import google.generativeai as genai
import logging

from bot.services.llm_provider import LLMProvider
from config import load_config

logger = logging.getLogger(__name__)


class GeminiProvider(LLMProvider):
    """Google Gemini API provider."""
    
    def __init__(self, model: str = None, api_key: str = None):
        """
        Initialize Gemini provider.
        
        :param model: Model name (defaults to 'gemini-pro')
        :param api_key: API key (from GEMINI_API_KEY env var or config)
        """
        logger.info("Initializing GeminiProvider")
        config = load_config()
        self.api_key = api_key or config.gemini_api_key
        if not self.api_key:
            error_msg = "GEMINI_API_KEY environment variable is not set (required for Gemini provider)"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        self.model = model or config.gemini_model
        logger.info(f"GeminiProvider initialized - model: {self.model}, API key present: {bool(self.api_key)}")
        genai.configure(api_key=self.api_key)
        
        # List available models for debugging
        try:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            logger.info(f"Available Gemini models: {available_models}")
        except Exception as e:
            logger.warning(f"Could not list available models: {e}")
        
        self.client = genai.GenerativeModel(self.model)
        logger.debug("Gemini GenerativeModel created")
    
    def generate_response(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
        conversation_history: str = ""
    ) -> str:
        """Generate response using Google Gemini."""
        logger.info(f"GeminiProvider.generate_response called - system_prompt length: {len(system_prompt)}, user_message: {user_message[:50]}..., history length: {len(conversation_history)}")
        try:
            # Configure generation parameters
            # Map finish reasons: 0=STOP, 1=MAX_TOKENS, 2=SAFETY, 3=RECITATION, 4=OTHER
            generation_config = {
                'temperature': temperature,
                'max_output_tokens': max_tokens,
            }
            
            # Configure safety settings to be more permissive for Discord bot
            # Use integer values: BLOCK_NONE = 1 (most permissive that's supported)
            # Note: The API may still apply some safety filtering, but this should minimize it
            safety_settings = [
                {
                    'category': genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    'threshold': 1  # BLOCK_NONE
                },
                {
                    'category': genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    'threshold': 1  # BLOCK_NONE
                },
                {
                    'category': genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    'threshold': 1  # BLOCK_NONE
                },
                {
                    'category': genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    'threshold': 1  # BLOCK_NONE
                },
            ]
            logger.info("Using permissive safety settings (BLOCK_NONE=1) for Discord bot")
            
            logger.debug(f"Generation config: temperature={temperature}, max_output_tokens={max_tokens}")
            logger.debug(f"Safety settings: {safety_settings}")
            
            # Build the full prompt with conversation history
            # If we have history, prepend it to the user message with context
            if conversation_history:
                context_prompt = f"{conversation_history}\n\nCurrent message:\n{user_message}"
                logger.info(f"Including conversation history ({len(conversation_history)} chars) in prompt")
                logger.info(f"=== FULL PROMPT BEING SENT TO GEMINI ===\n{context_prompt}\n=== END PROMPT ===")
            else:
                context_prompt = user_message
                logger.warning("No conversation history provided - this might be a problem!")
                logger.info(f"=== FULL PROMPT BEING SENT TO GEMINI ===\n{context_prompt}\n=== END PROMPT ===")
            
            # Gemini supports system instructions in newer models
            # For older models, we combine them into the prompt
            # Try using system_instruction if available, otherwise combine
            try:
                # Newer API: use system_instruction parameter
                logger.info("Attempting to use system_instruction parameter (newer API)")
                logger.info(f"=== SYSTEM INSTRUCTION ===\n{system_prompt[:500]}...\n=== END SYSTEM INSTRUCTION ===")
                logger.info(f"=== USER MESSAGE WITH HISTORY ===\n{context_prompt}\n=== END USER MESSAGE ===")
                response = self.client.generate_content(
                    context_prompt,
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                    system_instruction=system_prompt
                )
                logger.info("Successfully used system_instruction parameter")
            except (TypeError, AttributeError) as e:
                # Fallback: combine into single prompt for older API versions
                logger.warning(f"system_instruction not supported, falling back to combined prompt: {e}")
                full_prompt = f"{system_prompt}\n\n{conversation_history}\n\nUser: {user_message}\nAssistant:" if conversation_history else f"{system_prompt}\n\nUser: {user_message}\nAssistant:"
                logger.info(f"Using combined prompt (length: {len(full_prompt)})")
                logger.info(f"=== FULL COMBINED PROMPT ===\n{full_prompt}\n=== END PROMPT ===")
                response = self.client.generate_content(
                    full_prompt,
                    generation_config=generation_config,
                    safety_settings=safety_settings
                )
                logger.info("Successfully generated content with combined prompt")
            
            # Extract response text - handle different response formats
            logger.debug(f"Response object type: {type(response)}")
            logger.debug(f"Response object attributes: {dir(response)}")
            
            # Check for blocking or safety issues first
            if hasattr(response, 'prompt_feedback'):
                prompt_feedback = response.prompt_feedback
                logger.info(f"Prompt feedback: {prompt_feedback}")
                if hasattr(prompt_feedback, 'block_reason') and prompt_feedback.block_reason:
                    logger.error(f"Prompt was blocked! Reason: {prompt_feedback.block_reason}")
                    raise ValueError(f"Gemini blocked the prompt: {prompt_feedback.block_reason}")
            
            # Extract text from response - check all candidates
            logger.debug(f"Response has {len(response.candidates) if hasattr(response, 'candidates') else 0} candidates")
            
            # Log full response object structure for debugging
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                logger.debug(f"Candidate finish_reason: {getattr(candidate, 'finish_reason', 'N/A')}")
                logger.debug(f"Candidate content type: {type(getattr(candidate, 'content', None))}")
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    logger.debug(f"Number of content parts: {len(candidate.content.parts)}")
                    for i, part in enumerate(candidate.content.parts):
                        logger.debug(f"Part {i}: type={type(part)}, has text={hasattr(part, 'text')}")
                        if hasattr(part, 'text'):
                            logger.debug(f"Part {i} text length: {len(part.text)}")
            
            # Try to extract response - check multiple methods
            response_text = None
            
            # Method 1: Try response.text (standard method)
            try:
                response_text = response.text
                logger.debug("Extracted response using response.text")
            except AttributeError:
                logger.debug("response.text not available")
            
            # Method 2: If that didn't work or seems incomplete, try extracting from candidates directly
            if not response_text or (hasattr(response, 'candidates') and response.candidates):
                if hasattr(response, 'candidates') and response.candidates:
                    candidate = response.candidates[0]
                    logger.debug(f"Candidate attributes: {dir(candidate)}")
                    
                    # Check if candidate has content with parts
                    if hasattr(candidate, 'content'):
                        if hasattr(candidate.content, 'parts'):
                            # Extract from all parts (this might have more content than response.text)
                            all_parts = []
                            for i, part in enumerate(candidate.content.parts):
                                if hasattr(part, 'text'):
                                    part_text = part.text
                                    all_parts.append(part_text)
                                    logger.debug(f"Part {i} text: {repr(part_text[:50])}... (length: {len(part_text)})")
                                else:
                                    all_parts.append(str(part))
                            
                            parts_text = ''.join(all_parts)
                            logger.debug(f"Extracted from {len(all_parts)} parts, total length: {len(parts_text)}")
                            
                            # Use parts text if it's longer than response.text (might have more content)
                            if not response_text or len(parts_text) > len(response_text):
                                response_text = parts_text
                                logger.info(f"Using parts extraction (longer: {len(parts_text)} vs {len(response_text) if response_text else 0})")
                        else:
                            if not response_text:
                                response_text = str(candidate.content)
                    else:
                        if not response_text:
                            response_text = str(candidate)
            
            # Fallback if still nothing
            if not response_text:
                response_text = str(response)
                logger.warning("Using str(response) as fallback")
            
            logger.info(f"Gemini API returned response (length: {len(response_text)} chars)")
            logger.info(f"Full response text (repr): {repr(response_text)}")  # Use repr to see exact content
            logger.debug(f"Full response text (first 200 chars): {response_text[:200]}")
            
            # Check if response was incomplete
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'finish_reason'):
                    finish_reason = candidate.finish_reason
                    # Map finish reason codes to names
                    finish_reason_map = {
                        0: 'STOP',
                        1: 'MAX_TOKENS',
                        2: 'SAFETY',
                        3: 'RECITATION',
                        4: 'OTHER'
                    }
                    finish_reason_name = finish_reason_map.get(finish_reason, f'UNKNOWN({finish_reason})')
                    logger.info(f"Finish reason: {finish_reason} ({finish_reason_name})")
                    
                    if finish_reason == 0:  # 0 = STOP (normal completion)
                        logger.info(f"Response completed normally (STOP)")
                    elif finish_reason == 1:  # MAX_TOKENS
                        logger.warning(f"Response hit max_output_tokens limit ({max_tokens}). Response may be truncated.")
                    elif finish_reason == 2:  # SAFETY
                        logger.error("Response was blocked by safety filters!")
                        if hasattr(candidate, 'safety_ratings'):
                            safety_ratings = candidate.safety_ratings
                            logger.error(f"Safety ratings: {safety_ratings}")
                            for rating in safety_ratings:
                                logger.error(f"  - {getattr(rating, 'category', 'unknown')}: blocked={getattr(rating, 'blocked', False)}, probability={getattr(rating, 'probability', 'unknown')}")
                        # Check if we can get the partial response that was generated before blocking
                        if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                            partial_texts = []
                            for part in candidate.content.parts:
                                if hasattr(part, 'text'):
                                    partial_texts.append(part.text)
                            if partial_texts:
                                logger.warning(f"Partial response before safety block: {''.join(partial_texts)}")
                    elif finish_reason == 1:  # MAX_TOKENS
                            logger.warning(f"Response hit max_output_tokens limit ({max_tokens})")
                    
                if hasattr(candidate, 'safety_ratings'):
                    safety_ratings = candidate.safety_ratings
                    logger.info(f"Safety ratings: {safety_ratings}")
                    # Check if any safety rating blocked the response
                    for rating in safety_ratings:
                        if hasattr(rating, 'blocked') and rating.blocked:
                            logger.error(f"Content blocked by {rating.category}: {rating.probability}")
            
            return response_text
        
        except Exception as e:
            logger.error(f"Gemini API error: {e}", exc_info=True)
            raise
    
    def get_model_name(self) -> str:
        """Get the model name."""
        return self.model

