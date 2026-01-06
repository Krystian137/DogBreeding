# config/middleware.py
from django.conf import settings
from django.http import FileResponse, Http404
from django.utils._os import safe_join
import os


class ServeMediaMiddleware:
    """Serve media files in production (DEBUG=False)"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only serve media files if DEBUG=False and request starts with MEDIA_URL
        if not settings.DEBUG and request.path.startswith(settings.MEDIA_URL):
            return self.serve_media(request)
        
        response = self.get_response(request)
        return response

    def serve_media(self, request):
        """Serve a media file"""
        # Get relative path
        relative_path = request.path[len(settings.MEDIA_URL):]
        
        # Build full file path
        try:
            file_path = safe_join(settings.MEDIA_ROOT, relative_path)
        except ValueError:
            raise Http404("Invalid path")
        
        # Check if file exists
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise Http404("File not found")
        
        # Serve file
        return FileResponse(open(file_path, 'rb'))