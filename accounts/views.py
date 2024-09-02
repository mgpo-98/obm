# accounts/views.py
from django.http import JsonResponse
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from .models import EmailVerification
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail

def check_nickname(request):
    nickname = request.GET.get('nickname', None)
    data = {
        'is_taken': CustomUser.objects.filter(nickname__iexact=nickname).exists()
    }
    return JsonResponse(data)

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        email_local = request.POST.get('email_local')
        email_domain = request.POST.get('email_domain')
        email = f"{email_local}@{email_domain}"
        verification_code = request.POST.get('email_verification_code')
        
        try:
            verification = EmailVerification.objects.get(email=email)
            if not verification.is_code_valid(verification_code):
                return render(request, 'signup.html', {'error': 'Invalid verification code.'})
        except EmailVerification.DoesNotExist:
            return render(request, 'signup.html', {'error': 'Verification code does not exist.'})
        
        # 여기서 회원가입 처리
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = email
            user.save()
            return redirect('accounts:signup')
        
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def send_verification_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = get_random_string(length=6, allowed_chars='0123456789')
        EmailVerification.objects.update_or_create(email=email, defaults={'code': code})
        
        # 여기에 이메일 전송 로직 추가 (생략)
        send_mail(
            '이미지방 메일 인증번호', # 이메일 제목
            f'코드를 입력창에 입력하세요 {code}', # 이메일 내용 (본문)
            'jsy776@gmail.com', # 발신자 이메일
            [email], # 수신자 이메일 리스트
            fail_silently=False,
        )
        print(send_mail)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
