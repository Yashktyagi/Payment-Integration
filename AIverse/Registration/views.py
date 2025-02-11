import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *

UPI_GATEWAY_API_KEY = "7ca270a2-3bac-4c2f-bc52-0f175e10b1d4"
UPI_GATEWAY_URL = "https://api.ekqr.in/api/create_order"

def registration_form(request):
    if request.method == "POST":
        event = request.POST.get("event")  # Either Dreambrush or AIverse
        team_name = request.POST.get("team_name")
        leader_name = request.POST.get("leader_name")
        leader_email = request.POST.get("leader_email")
        leader_phone = request.POST.get("leader_phone")
        college = request.POST.get("college")
        amount = 500  # Fixed price (modify if dynamic)

        members = []
        for i in range(1, 6):  # Max 5 members
            member_name = request.POST.get(f"member_name_{i}")
            member_email = request.POST.get(f"member_email_{i}")
            member_phone = request.POST.get(f"member_phone_{i}")
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
            "amount": amount,
            "members": members
        }

        # Create a payment request on UPIGateway
        payment_payload = {
            "key": UPI_GATEWAY_API_KEY,
            "client_txn_id": f"{leader_phone}_{team_name}",
            "amount": amount,
            "p_info": f"{event} Team Registration",
            "customer_name": leader_name,
            "customer_email": leader_email,
            "customer_phone": leader_phone,
            "redirect_url": request.build_absolute_uri("/payment-success/"),
            "webhook_url": request.build_absolute_uri("/payment-webhook/")
        }

        response = requests.post(UPI_GATEWAY_URL, data=payment_payload)
        response_data = response.json()

        if response_data.get("status") == "success":
            return redirect(response_data["payment_url"])  # Redirect to payment page
        else:
            return JsonResponse({"error": "Payment gateway error"}, status=400)

    return render(request, "form.html")

def payment_success(request):
    team_data = request.session.get("team_data", None)
    if not team_data:
        return JsonResponse({"error": "No team data found in session"}, status=400)

    # Store the team in the respective event table
    event = team_data["event"]
    if event == "Dreambrush":
        team = DreambrushTeam.objects.create(
            team_name=team_data["team_name"],
            leader_name=team_data["leader_name"],
            leader_email=team_data["leader_email"],
            leader_phone=team_data["leader_phone"],
            college=team_data["college"],
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
            college=team_data["college"],
            amount_paid=team_data["amount"]
        )
        for member in team_data["members"]:
            AIverseMember.objects.create(team=team, **member)

    # Clear session data
    del request.session["team_data"]

    return JsonResponse({"success": "Payment successful and team registered!"})

from django.views.decorators.csrf import csrf_exempt
import hashlib

@csrf_exempt
def payment_webhook(request):
    if request.method == "POST":
        data = request.POST
        received_signature = data.get("hash")
        txn_id = data.get("client_txn_id")
        status = data.get("status")

        # Verify signature (Check UPI Gateway docs for correct hashing method)
        hash_string = f"{UPI_GATEWAY_API_KEY}|{txn_id}|{status}"
        calculated_signature = hashlib.sha256(hash_string.encode()).hexdigest()

        if received_signature != calculated_signature:
            return JsonResponse({"error": "Invalid signature"}, status=400)

        if status == "success":
            return JsonResponse({"status": "Payment verified"})
        return JsonResponse({"error": "Payment failed"}, status=400)
