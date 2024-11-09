class SetSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Initialize session data if not already set
        if 'user_data' not in request.session:
            request.session['user_data'] = {
                'name': 'random_name',
                'financial goal': '',
                'motivational_message': '',
                'insights': ''
            }

        # Proceed to the next middleware or view
        response = self.get_response(request)
        return response