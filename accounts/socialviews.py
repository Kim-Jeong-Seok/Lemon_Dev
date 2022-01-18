from allauth.socialaccount.providers.kakao import views as kakao_view
from mysettings import SECRET_KEY,KAKAO_KEY
from django.views import View


#
# def kakao_login(request):
#     app_rest_api_key = os.environ.get("f7392204050136e895a59bbdcb9090db")
#     redirect_uri = main_domain + "accounts/kakao/login/callback"
#     return redirect(
#         f"https://kauth.kakao.com/oauth/authorize?client_id={'f7392204050136e895a59bbdcb9090db'}&redirect_uri={'http://127.0.0.1:8000/'}&response_type=code"
#     )


class KakaoSignInView(View):
    def get(self, request):
        client_id = KAKAO_KEY['KAKAO_KEY']
        redirect_uri = "http://127.0.0.1:8000/account/kakao/login/callback/"
        #redirect_uri = "https://192.168.0.26:8000/account/kakao/login/callback/"
        kakao_auth_api = 'http://kauth.kakao.com/pauth/author?response_type=code '
        return redirect(
                f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={'http://127.0.0.1:8000/signup2'}&response_type=code"
            )

class KakaoSignInCallbackView(View):
    def get(self, request):
        try:
            code            = request.GET.get("code")
            client_id       = KAKAO_KEY['KAKAO_KEY']
            redirect_uri    = "http://127.0.0.1:8000account/kakao/login/callback/"
            #redirect_uri = "https://192.168.0.26:8000/account/kakao/login/callback/"
            token_request   = requests.get(
                f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={'http://127.0.0.1:8000/signup2'}&code={code}"
            )
            token_json      = token_request.json()
            #print(token_json)

            error           = token_json.get("error", None)

            if error is not None:
                return JsonResponse({"message":"INVALD_CODE"}, status=400)

            access_token    = token_json.get("access_token")

            profile_request     = requests.get(
                "https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"},
            )

            profile_json        = profile_request.json()
            kakao_account       = profile_json.get("kakao_account")
            email               = kakao_account.get("email", None)
            kakao_id            = profile_json.get("id")
            profileImageUR      = profile_json.get("profile_image")
            nickName            = profile_json.get("nickname")


        except KeyError:
            return JsonResponse({"message":"INVALID_TOKEN"}, status=400)

        except access_token.DoesNotExist:
            return JsonResponse({"message":"INVALID_TOKEN"}, status=400)
        if member.objects.filter(social_account = kakao_id).exists():
            kakao_user    = member.objects.get(social_account = kakao_id)
            token   = jwt.encode({"email":email}, SECRET['SECRET_KEY'], algorithm="HS256")
            token   = token.decode("utf-8")

            print("success")

            return JsonResponse({"token" : token}, status=200)


        else:
            member(social_account = kakao_id,
                email    = email,
            ).save()
            token = jwt.encode({"email" : email}, SECRET['SECRET_KEY'], algorithm = "HS256")
            token = token.decode("utf-8")
            return JsonResponse({"token" : token}, status = 200)
