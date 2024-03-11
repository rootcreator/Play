class CloudflareMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Modify response content to replace URLs with Cloudflare CDN URLs
        # You can modify URLs here before the response is returned

        return response
