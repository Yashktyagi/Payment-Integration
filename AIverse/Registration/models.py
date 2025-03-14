from django.db import models

class DreambrushTeam(models.Model):
    team_name = models.CharField(max_length=100)
    leader_name = models.CharField(max_length=100)
    leader_email = models.EmailField()
    leader_phone = models.CharField(max_length=15)
    college = models.CharField(max_length=200)
    amount_paid = models.IntegerField(default=0)  # Payment by leader
    timestamp = models.DateTimeField(auto_now_add=True)  # When registered

    def __str__(self):
        return f"{self.team_name}"

class DreambrushMember(models.Model):
    team = models.ForeignKey(DreambrushTeam, on_delete=models.CASCADE, related_name="members")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    def __str__(self):
        return f"{self.team}"


class AIverseTeam(models.Model):
    team_name = models.CharField(max_length=100)
    leader_name = models.CharField(max_length=100)
    leader_email = models.EmailField()
    leader_phone = models.CharField(max_length=15)
    college = models.CharField(max_length=200)
    amount_paid = models.IntegerField(default=0)  # Payment by leader
    timestamp = models.DateTimeField(auto_now_add=True)  # When registered

    def __str__(self):
        return f"{self.team_name}"

class AIverseMember(models.Model):
    team = models.ForeignKey(AIverseTeam, on_delete=models.CASCADE, related_name="members")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.team}"

