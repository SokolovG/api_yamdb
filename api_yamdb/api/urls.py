urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('reviews.urls')),
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', TokenObtainView .as_view()),
]
