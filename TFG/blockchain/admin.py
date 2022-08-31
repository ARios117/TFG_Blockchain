from django.contrib import admin
from blockchain.models import Member, Block


# Register your models here.

class BlockAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('title', 'date', )}
    readonly_fields = ["previousHash", "index", "date", "hash"]
    

class MemberAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('title', 'date', )}
    readonly_fields = ["publicKey", "privateKey"]

admin.site.register(Member, MemberAdmin)
admin.site.register(Block, BlockAdmin)
