from django.urls import path
from django.conf.urls.static import static
from shop import settings
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home,name="home"),
    path('/<str:category>/', views.home, name='product_list_by_category'),
    path('about-us', views.about_us, name="about-us" ),
    path('news', views.news, name = 'news'),
    path('contact', views.contact),
    path("faq", views.faq),
    path("conf", views.conf),
    path("vacancies", views.vacancies),
    path("reviews", views.review_list, name='review_list'),
    path('reviews/create', views.create_review,name="create_review"),
    path("coupons", views.coupons),
    path("cart/", views.view_cart,name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('create_order/', views.create_order, name='create_order'),
    path('order_list/', views.order_list, name='order_list'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('category-chart/', views.category_chart_view, name='category_chart'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('news_detailed/<int:news_id>/', views.news_detailed, name='news_detailed'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    path('cart/update/<int:cart_product_id>/<str:action>/', views.update_cart, name='update_cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)