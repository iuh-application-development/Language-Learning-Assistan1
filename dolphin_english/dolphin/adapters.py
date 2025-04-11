from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.account.utils import perform_login
from django.contrib.auth import get_user_model

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Nếu user đã đăng nhập rồi thì bỏ qua
        if request.user.is_authenticated:
            return

        email = sociallogin.user.email
        if email:
            try:
                user = User.objects.get(email=email)
                # Liên kết tài khoản Google với user có sẵn
                sociallogin.connect(request, user)
                raise ImmediateHttpResponse(perform_login(request, user, email_verification='optional'))
            except User.DoesNotExist:
                pass  # để allauth xử lý như thường
