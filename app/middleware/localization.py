import os
import aiofiles
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from babel.support import Translations


class DynamicLocalizationMiddleware(BaseHTTPMiddleware):
    """
    Dynamic Localization Middleware with Asynchronous Loading and Caching.
    """
    def __init__(self, app: FastAPI, default_language: str = "en", supported_languages=None):
        super().__init__(app)
        self.default_language = default_language
        self.supported_languages = supported_languages or ["en"]
        self.locales_dir = os.path.join(os.getcwd(), "locales")
        self.translations_cache = {}

    def detect_language(self, request: Request) -> str:
        # Check for language in query params or headers
        lang = request.query_params.get("lang")
        if lang and lang in self.supported_languages:
            return lang

        accept_language = request.headers.get("accept-language", "")
        if accept_language:
            for lang in accept_language.split(","):
                lang_code = lang.split(";")[0].strip()
                if lang_code in self.supported_languages:
                    return lang_code

        return self.default_language

    async def load_translations(self, language: str, module: str) -> Translations:
        # Check if translations are already cached
        cache_key = (language, module)
        if cache_key in self.translations_cache:
            return self.translations_cache[cache_key]

        # Load the .mo file for the specific module and language
        locale_path = os.path.join(self.locales_dir, language, module, "LC_MESSAGES", "messages.mo")
        if os.path.exists(locale_path):
            # Asynchronous loading of translation files (if needed)
            async with aiofiles.open(locale_path, 'rb') as f:
                # Here, we should probably parse the .mo file asynchronously if necessary
                # But for simplicity, we'll load it synchronously via babel's Translations.load
                translations = Translations.load(dirname=os.path.join(self.locales_dir, language, module))
        else:
            # Fallback to default language
            translations = Translations.load(dirname=os.path.join(self.locales_dir, self.default_language, module))

        # Cache the translations for future use
        self.translations_cache[cache_key] = translations
        return translations

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        # Detect language
        language = self.detect_language(request)

        # Attach a translation loader for the request
        def get_translations(module: str) -> Translations:
            return self.load_translations(language, module)

        request.state.language = language
        request.state.get_translations = get_translations

        # Continue processing the request
        response = await call_next(request)
        return response
