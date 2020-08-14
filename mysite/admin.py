from django.contrib import admin
from .models import ConsentPageResults, InstructionPageResults, ImagePool, MessagePool, Response, Results, Score, Users, CameraPermission


admin.site.register(ConsentPageResults)
admin.site.register(InstructionPageResults)
admin.site.register(ImagePool)
admin.site.register(MessagePool)
admin.site.register(Response)
admin.site.register(Results)
admin.site.register(Score)
admin.site.register(Users)
admin.site.register(CameraPermission)