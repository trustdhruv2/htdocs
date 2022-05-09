from django.shortcuts import render

class response:
    def __init__(self,useragent):
        self.useragent =useragent.lower()

    def response(self, request, html, mobilehtml, *data):
        if self.useragent.find("android") != -1 or self.useragent.find("iphone") != -1 or self.useragent.find("ios") != -1:
            if len(data) > 0:
                return render(request, mobilehtml, data[0])
            return render(request, mobilehtml)
        else:
            if len(data) > 0:
                return render(request, html, data[0])
            return render(request, html)
