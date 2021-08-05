from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from rest_framework import viewsets


class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    # def list(self, request, *args, **kwargs):
    #     serializers = self.get_serializer(self.queryset, many=True)
    #     authors = []
    #     for i in serializers.data:
    #         articels = Articel.objects.filter(author = i["id"])
    #         o = []
    #         s, m = 0, "maqola"
    #         for item in articels:
    #             s += 1
    #             cud = m + str(s)
    #             f = {
    #                 cud: item.name
    #             }
    #             o.append(f)
    #         d = {
    #             "id" : i["id"],
    #             "level": i["level"],
    #             "user": i["user"],
    #             "faculty" : i["faculty"],
    #             "cafedra" : i["cafedra"],
    #             "row_date" : i["row_date"],
    #             "image" : i["image"],
    #             "maqolalar" : o
    #         }
    #         authors.append(d)
    #     return Response({"authors" : authors})
    def list(self, request, *args, **kwargs):
        serializers = self.get_serializer(self.queryset, many=True)
        authors = []
        for i in self.queryset:
            articels = Articel.objects.filter(author=i.id)
            o = []
            s, m = 0, "maqola"
            for item in articels:
                s += 1
                cud = m + str(s)
                f = {
                    cud: item.name
                }
                o.append(f)
            d = {
                "id": i.id,
                "level": i.level,
                "user": i.user.username,
                "faculty": i.faculty,
                "cafedra": i.cafedra,
                "row_date": i.row_date,
                "imageURL": i.imageURL,
                "maqolalar": o
            }
            authors.append(d)
        return Response({"authors": authors})


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ArticelViewset(viewsets.ModelViewSet):
    queryset = Articel.objects.all()
    serializer_class = ArticelSerializer

    def list(self, request, *args, **kwargs):
        serializers = self.get_serializer(self.queryset, many=True)
        datas = []
        for item in serializers.data:
            files = LinkedFiles.objects.filter(articel=item["id"])
            file = []
            for i in files:
                f = {
                    "fileURL": i.file_URL
                }
                file.append(f)
            d = {
                "id": item["id"],
                "name": item["name"],
                "text": item["text"],
                "tags": item["tags"],
                "author": item["author"],
                "files": file,
            }
            datas.append(d)
        return Response({"datas": datas})


class LinkedFilesViewset(viewsets.ModelViewSet):
    queryset = LinkedFiles.objects.all()
    serializer_class = FileSerializer


class TopshiriqViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = TopshiriqSerializer

    def list(self, request, *args, **kwargs):
        serializers = self.get_serializer(self.queryset, many=True)
        datas = []
        for item in serializers.data:
            articel = Articel.objects.filter(author=item["id"])
            f = []
            for i in articel:
                g = {
                    "blog": i.name
                }
                f.append(g)
            d = {
                "id": item["id"],
                "level": item["level"],
                "user": item["user"],
                "bloglari": f,
            }
            datas.append(d)
        return Response({"datas": datas})


class ArticelByTagViewset(viewsets.ModelViewSet):
    queryset = Articel.objects.all()
    serializer_class = ArticelSerializer
    def retrieve(self, request, *args, **kwargs):
        tag = kwargs["pk"]
        serial = self.queryset.filter(tags__contains = tag)
        data = []
        for item in serial:
            d = {
                "id" : item.id,
                "name" : item.name,
                "text" : item.text,
                "tags" : item.tags,
                "author" : item.id,
            }
            data.append(d)
        return Response({
            "data" : data
        })
