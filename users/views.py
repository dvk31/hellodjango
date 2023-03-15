from django.shortcuts import render, redirect
from .forms import RegistrationForm
import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            # Call register_user function to create user in Supabase
            user_id = register_user(email, password)
            if user_id is not None:
                # User created successfully, redirect to success page or other page as needed
                return redirect("home")
            else:
                # User creation failed, handle error
                return redirect("register")
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})


def register_user(email, password):
    response = requests.post(
        f"{SUPABASE_URL}/auth/v1/signup",
        headers={
            "apikey": SUPABASE_API_KEY,
            "Content-Type": "application/json",
        },
        json={"email": email, "password": password},
    )
    print(response.text)
    if response.status_code == 200:
        user_id = response.json()["email"]
        return user_id
    else:
        # Handle error
        return None
