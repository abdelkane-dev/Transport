from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Q, Avg
from django.db.models import F, FloatField
from django.db.models.functions import Cast
from django.utils import timezone
from datetime import timedelta
from .models import User
from apps.reservations.models import Reservation
from apps.trajets.models import Trajet
from apps.bus.models import Bus

@staff_member_required
def admin_user_list(request):
    """Liste des utilisateurs avec leurs statistiques"""
    users = User.objects.annotate(
        total_reservations=Count('reservations'),
        reservations_confirmees=Count('reservations', filter=Q(reservations__statut='CONFIRMEE')),
        total_depense=Sum('reservations__prix_total')
    ).order_by('-date_joined')
    
    context = {
        'users': users,
        'total_users': users.count(),
        'title': 'Gestion des utilisateurs'
    }
    return render(request, 'accounts/admin_user_list.html', context)

@staff_member_required
def admin_user_detail(request, user_id):
    """Détail d'un utilisateur avec ses réservations"""
    user = get_object_or_404(User, id=user_id)
    reservations = user.reservations.all().select_related('trajet', 'trajet__bus').order_by('-date_reservation')
    
    stats = {
        'total_reservations': reservations.count(),
        'reservations_confirmees': reservations.filter(statut='CONFIRMEE').count(),
        'reservations_annulees': reservations.filter(statut='ANNULEE').count(),
        'total_depense': reservations.aggregate(total=Sum('prix_total'))['total'] or 0,
        'derniere_reservation': reservations.first().date_reservation if reservations.exists() else None
    }
    
    context = {
        'user_detail': user,
        'reservations': reservations,
        'stats': stats,
        'title': f'Détail - {user.get_nom_complet()}'
    }
    return render(request, 'accounts/admin_user_detail.html', context)

@staff_member_required
def admin_dashboard(request):
    """Dashboard administrateur avec statistiques globales"""
    now = timezone.now()
    last_30_days = now - timedelta(days=30)
    
    stats = {
        'total_users': User.objects.count(),
        'total_bus': Bus.objects.count(),
        'bus_actifs': Bus.objects.filter(statut='ACTIF').count(),
        'total_trajets': Trajet.objects.filter(date_depart__gte=now.date()).count(),
        'total_reservations': Reservation.objects.count(),
        'reservations_mois': Reservation.objects.filter(date_reservation__gte=last_30_days).count(),
        'chiffre_affaires': Reservation.objects.filter(statut='CONFIRMEE').aggregate(total=Sum('prix_total'))['total'] or 0,
        'chiffre_affaires_mois': Reservation.objects.filter(
            statut='CONFIRMEE',
            date_reservation__gte=last_30_days
        ).aggregate(total=Sum('prix_total'))['total'] or 0,
        'taux_occupation_moyen': calculer_taux_occupation_moyen(),
    }
    
    # Top utilisateurs
    top_users = User.objects.annotate(
        total_reservations=Count('reservations')
    ).order_by('-total_reservations')[:5]
    
    # Top trajets
    top_trajets = Trajet.objects.annotate(
        total_reservations=Count('reservations')
    ).order_by('-total_reservations')[:5]
    
    context = {
        'stats': stats,
        'top_users': top_users,
        'top_trajets': top_trajets,
        'title': 'Dashboard Administrateur'
    }
    return render(request, 'accounts/admin_dashboard.html', context)

def calculer_taux_occupation_moyen():
    """Calcule le taux d'occupation moyen des trajets"""
    result = Trajet.objects.annotate(
        places_reservees=Sum('reservations__nombre_places')
    ).aggregate(
        taux_moyen=Avg(
            Cast(F('places_reservees'), FloatField()) / Cast(F('bus__nombre_places'), FloatField()) * 100
        )
    )
    return round(result['taux_moyen'] or 0, 2)
