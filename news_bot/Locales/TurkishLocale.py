
TurkishLocale = {
    "AlarmSetResponse": 
    "Alarm **%02d.%02d** saatine **'%s'** kanalına kuruldu.", #hour, min, channel
    "AlarmUnsetResponseSuccess": 
    "Alarm **%02d.%02d**, **'%s'** kaldırıldı.", #hour, min, channel
    "AlarmUnsetResponseFail": "Alarm kaldırılamadı.",
    "AlarminfoBegin": "Sunucuda kurulu alarmlar:\n",
    "AlarminfoItem": ">\t**%d** indexinde **%02d.%02d** saatinde, **'%s'** kanalında\n", #index, hour, min, channel
    "AlarminfoEnd": "Dikkat: Alarm sildikten sonra indexler değişir.",
    "NewsRetrieveError": "**HATA**\nHaberler yenilenemedi.",
    "NewsPrettifyError": "**HATA**\nHaberler gösterilemedi.\nLütfen geliştiriciye bu hatayı bildirin.",
    "NewsPrettifyHeadline": "**Kaynak:** %s\n", # Source
    "NewsPrettifySourceBegin": "Kaynaklar:\n**kategori** - **isim** - **id** - **url**:\n",
    "NewsPrettifySource": "**%s**\t**%s**\t**%s**\t**`%s`**", #category, name, id, url
    "NewsPrettifySourceRetrieveError": "**HATA**\nKaynaklar listelenemedi.",
    "NotAuthorizedError": "Bu bota erişmek için yetkiniz yok.\nDetaylar için `$setup` komutunu kullanın.",
    "SetupCmd": """Merhabalar!
Burada botun kullanımını anlatacağım sana.
Bot komutlarını listelemek için `$help` komutunu kullan.
Bir komut hakkında detaylı bilgi istiyorsan `$help [komut adı]` şeklinde kullan.
Böylece komutların kullanımını öğrenmiş olursun.

**Dikkat!** Bot komutlarını kullanabilmek için yetkiye ihtiyacın var.
Bu yetki **'%s'** rolüne sahip kişilere veriliyor.
O yüzden bu isimde bir komut yarat ve bota erişmesini istediğin kişilere bu rolü ver.
İyi eğlenceler :)"""#Config.AUTH_ROLE
}