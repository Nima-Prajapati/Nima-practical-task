from django.shortcuts import render

# Create your views here.


def register_user(request):
    pass
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     email = request.POST['email']
    #     password = request.POST['password']
    #
    #     if User.objects.filter(email=email).exists():
    #         messages.error(request, "Email already registered.")
    #         return redirect('register')
    #
    #     if User.objects.filter(username=username).exists():
    #         messages.error(request, "Username already exists.")
    #         return redirect('register')
    #
    #     user = User.objects.create_user(email=email, username=username, password=password)
    #     messages.success(request, "Registration successful.")
    #     return redirect('login')
    #
    # return render(request, 'registration.html')
