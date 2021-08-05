from rest_framework import routers
from blog import views

router = routers.DefaultRouter()

router.register(r"author", views.AuthorViewset, basename="author")
router.register(r"articel", views.ArticelViewset, basename="articel")
router.register(r"linked_files", views.LinkedFilesViewset, basename="linked_files")
router.register(r"user", views.UserViewset, basename="user")
router.register(r"alohida", views.TopshiriqViewset, basename="alohida")
router.register(r"articel_bay_tag", views.ArticelByTagViewset, basename="articel_bay_tag")
