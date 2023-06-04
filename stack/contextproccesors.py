from stack.models import Questions,Answer
def activities(request):
    if request.user.is_authenticated:
        cnt=Questions.objects.filter(user=request.user).count()
        ant=Answer.objects.filter(user=request.user).count
        return {"qcnt":cnt,"acnt":ant}
    else:
        return{"qcnt":0}