from adrf import viewsets
from django.contrib.auth.models import Group, User
from django.shortcuts import aget_object_or_404 as _aget_object_or_404
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import GroupSerializer, UserSerializer


async def aget_object_or_404(queryset, *filter_args, **filter_kwargs):
    """
    Same as Django's standard shortcut, but make sure to also raise 404
    if the filter_kwargs don't match the required types.
    """
    try:
        return _aget_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError, ValidationError):
        raise Http404


class GenericishViewSetMixin:
    async def get_queryset(self):
        raise NotImplementedError()

    async def get_serializer(self, *args, **kwargs):
        context = {
            "request": self.request,
            "format": self.format_kwarg,
            "view": self,
        }
        kwargs.setdefault("context", context)
        return self.serializer_class(*args, **kwargs)

    async def list(self, request):
        queryset = await self.get_queryset()
        serializer = await self.get_serializer(queryset, many=True)
        return Response(data=await serializer.adata)

    async def create(self, request):
        serializer = await self.get_serializer(data=request.data)
        nspserializer.is_valid(raise_exception=True)
        instance = await serializer.asave()
        serializer = await self.get_serializer(data=instance)
        return Response(data=await serializer.adata, status_code=200)

    async def retrieve(self, request, pk=None):
        queryset = await self.get_queryset()
        instance = await aget_object_or_404(queryset, pk=pk)
        serializer = await self.get_serializer(instance)
        return Response(data=await serializer.adata)

    async def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        queryset = await self.get_queryset()
        instance = await aget_object_or_404(queryset, pk=kwargs["pk"])
        serializer = await self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        await serializer.asave()
        return Response(data=await serializer.adata, status_code=202 if partial else 200)

    async def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    async def destroy(self, request, pk=None):
        queryset = await self.get_queryset()
        instance = await aget_object_or_404(queryset, pk=pk)
        await instance.adelete()
        return Response(data={}, status_code=204)


class UserViewSet(GenericishViewSetMixin, viewsets.ViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = UserSerializer
    permission_classes = []

    async def get_queryset(self):
        return User.objects.all().order_by("-date_joined")


class GroupViewSet(GenericishViewSetMixin, viewsets.ViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = GroupSerializer
    permission_classes = []

    async def get_queryset(self):
        return Group.objects.all().order_by("name")
