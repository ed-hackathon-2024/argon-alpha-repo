from django.http import JsonResponse

def get_session_data(request):
    data = request.session.get('user_data', {})
    print('session data:', data)
    return JsonResponse(data)