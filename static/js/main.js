function confirmerAnnulation() {
    return confirm("Voulez-vous vraiment annuler cette reservation ?");
}

function confirmerSuppression() {
    return confirm("Voulez-vous vraiment supprimer cet element ?");
}

const placesDisponibles = parseInt("{{ trajet.get_places_disponibles }}");