import hashlib
import hmac
import json

from django.http import JsonResponse
from django.shortcuts import render, redirect , HttpResponse
import razorpay
from .models import *


RAZORPAY_KEY_ID = "rzp_test_Dv0ftDlmfxUGmM"
RAZORPAY_KEY_SECRET = "jKxGhwAQjVssZQ3vwzKhvAv4"


razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
def registration_form(request):
    if request.method == "POST":
        event = request.POST.get("event")
        team_name = request.POST.get("team_name")
        leader_name = request.POST.get("leader_name")
        leader_email = request.POST.get("leader_email")
        leader_phone = request.POST.get("leader_mobile")
        theme = request.POST.get("theme")
        college = request.POST.get("leader_college")
        amount = int(request.POST.get("amount")) * 100  # Convert to paise

        members = []
        for i in range(1, 5):  # Max 5 members
            member_name = request.POST.get(f"member_{i}_name")
            member_email = request.POST.get(f"member_{i}_email")
            member_phone = request.POST.get(f"member_{i}_mobile")
            if member_name and member_email and member_phone:
                members.append({"name": member_name, "email": member_email, "phone": member_phone})

        # Store form data in session before payment
        request.session["team_data"] = {
            "event": event,
            "team_name": team_name,
            "leader_name": leader_name,
            "leader_email": leader_email,
            "leader_phone": leader_phone,
            "college": college,
            "amount": amount // 100,  # Convert to rupees for storage
            "members": members
        }
        # Create Razorpay Order
        order_data = {
            "amount": amount,
            "currency": "INR",
            "receipt": f"{leader_phone}_{team_name}",
            "payment_capture": 1,
        }
        razorpay_order = razorpay_client.order.create(order_data)
        request.session["order_id"] = razorpay_order["id"]
        context = {
            "razorpay_key": RAZORPAY_KEY_ID,
            "order_id": razorpay_order["id"],
            "amount": amount,
            "event": event,
            "theme": theme,
            "leader_name": leader_name,
            "leader_email": leader_email,
            "leader_phone": leader_phone,
        }
        order_creation = razorpay_order["id"]
        # return render(request , 'form.html' )
        return render(request , 'integration.html' , {'context':context , 'order_creation':order_creation})
    return render(request, 'integration.html')


def payment_success(request):
    team_data = request.session.get("team_data")

    if not team_data:
        return HttpResponse("Error: No team data found in session", status=400)

    # Debugging: Print session data to check what is stored
    print("Session Data:", team_data)

    # Ensure 'college' is present and not None
    college = team_data.get("college", "").strip()
    if not college:
        return HttpResponse("Error: College field is missing or empty", status=400)

    event = team_data["event"]

    if event == "Dreambrush":
        team = DreambrushTeam.objects.create(
            team_name=team_data["team_name"],
            leader_name=team_data["leader_name"],
            leader_email=team_data["leader_email"],
            leader_phone=team_data["leader_phone"],
            college=college,  # Ensure this is not None
            amount_paid=team_data["amount"]
        )
        for member in team_data["members"]:
            DreambrushMember.objects.create(team=team, **member)

    elif event == "AIverse":
        team = AIverseTeam.objects.create(
            team_name=team_data["team_name"],
            leader_name=team_data["leader_name"],
            leader_email=team_data["leader_email"],
            leader_phone=team_data["leader_phone"],
            college=college,  # Ensure this is not None
            amount_paid=team_data["amount"]
        )
        for member in team_data["members"]:
            AIverseMember.objects.create(team=team, **member)

    # Clear session data after storing
    request.session.pop("team_data", None)

    return render(request, "integration.html")

