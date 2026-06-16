"""
Vues de l'application Comptes (Accounts).
Gère l'inscription, la connexion, la déconnexion et le profil utilisateur.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import UpdateView, DetailView
from django.urls import reverse_lazy

# Importations DRF pour l'API
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .forms import InscriptionForm, ConnexionForm, ProfilForm
from .serializers import UserSerializer, UserRegistrationSerializer

User = get_user_model()


# ============================================================
# VUES HTML (Interface web)
# ============================================================

class InscriptionView(View):
    """
    Vue d'inscription d'un nouvel utilisateur.
    GET  : affiche le formulaire d'inscription vide
    POST : valide le formulaire et crée le compte
    """
    template_name = 'accounts/inscription.html'

    def get(self, request):
        # Si l'utilisateur est déjà connecté, le rediriger vers le dashboard
        if request.user.is_authenticated:
            return redirect('reservations:dashboard')
        form = InscriptionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = InscriptionForm(request.POST)
        if form.is_valid():
            # Sauvegarder l'utilisateur (mot de passe hashé dans save())
            user = form.save()
            # Connecter automatiquement l'utilisateur après l'inscription
            login(request, user)
            messages.success(
                request,
                f"Bienvenue {user.prenom} ! Votre compte a été créé avec succès."
            )
            return redirect('reservations:dashboard')
        else:
            # Afficher les erreurs de validation
            messages.error(
                request,
                "Des erreurs ont été trouvées dans le formulaire. Veuillez les corriger."
            )
        return render(request, self.template_name, {'form': form})


class ConnexionView(View):
    """
    Vue de connexion.
    GET  : affiche le formulaire de connexion
    POST : authentifie l'utilisateur et le redirige
    """
    template_name = 'accounts/connexion.html'

    def get(self, request):
        # Rediriger si déjà connecté
        if request.user.is_authenticated:
            return redirect('reservations:dashboard')
        form = ConnexionForm(request)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Connexion réussie ! Bonjour {user.prenom}.")
            # Rediriger vers la page demandée avant la connexion, ou le dashboard
            next_url = request.GET.get('next', reverse_lazy('reservations:dashboard'))
            return redirect(next_url)
        else:
            messages.error(request, "E-mail ou mot de passe incorrect.")
        return render(request, self.template_name, {'form': form})


class DeconnexionView(View):
    """
    Vue de déconnexion.
    Déconnecte l'utilisateur et le redirige vers l'accueil.
    """
    def post(self, request):
        # Vérifier que la méthode est POST (protection CSRF)
        prenom = request.user.prenom if request.user.is_authenticated else "visiteur"
        logout(request)
        messages.info(request, f"Au revoir {prenom} ! Vous êtes déconnecté(e).")
        return redirect('home')

    def get(self, request):
        # Autoriser aussi GET pour la simplicité des templates
        logout(request)
        return redirect('home')


class ProfilView(LoginRequiredMixin, View):
    """
    Vue du profil utilisateur.
    Accessible uniquement aux utilisateurs connectés (LoginRequiredMixin).
    Permet de visualiser et modifier les informations personnelles.
    """
    template_name = 'accounts/profil.html'
    login_url = '/accounts/connexion/'

    def get(self, request):
        form = ProfilForm(instance=request.user)
        return render(request, self.template_name, {
            'form': form,
            'user': request.user,
        })

    def post(self, request):
        form = ProfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('accounts:profil')
        else:
            messages.error(request, "Erreur lors de la mise à jour du profil.")
        return render(request, self.template_name, {'form': form})


# ============================================================
# VUES API REST (DRF)
# ============================================================

class APIInscriptionView(generics.CreateAPIView):
    """
    API : Créer un nouveau compte utilisateur.
    POST /api/accounts/inscription/
    Accessible sans authentification.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Créer un token d'authentification pour l'utilisateur
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Compte créé avec succès.',
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIConnexionView(APIView):
    """
    API : Connexion et obtention d'un token.
    POST /api/accounts/connexion/
    Corps : { "email": "...", "password": "..." }
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'erreur': 'Email et mot de passe requis.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authentifier avec l'email (notre USERNAME_FIELD)
        user = authenticate(request, username=email, password=password)
        if user:
            if user.is_active:
                # Récupérer ou créer le token
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'message': 'Connexion réussie.',
                    'token': token.key,
                    'user': UserSerializer(user).data
                })
            return Response(
                {'erreur': 'Ce compte est désactivé.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return Response(
            {'erreur': 'Identifiants incorrects.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class APIDeconnexionView(APIView):
    """
    API : Déconnexion (suppression du token).
    POST /api/accounts/deconnexion/
    Requiert authentification.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Supprimer le token de l'utilisateur
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response({'message': 'Déconnexion réussie.'}, status=status.HTTP_200_OK)


class APIProfilView(generics.RetrieveUpdateAPIView):
    """
    API : Voir et modifier le profil de l'utilisateur connecté.
    GET  /api/accounts/profil/ → voir le profil
    PUT  /api/accounts/profil/ → modifier le profil
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Retourner uniquement le profil de l'utilisateur connecté
        return self.request.user
