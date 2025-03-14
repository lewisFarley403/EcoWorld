from django.shortcuts import render, redirect
from .models import GlassDisposalEntry
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import GlassDisposalForm

@login_required
def submit_disposal(request):
    """Handles glass disposal submissions"""
    if request.method == 'POST':
        form = GlassDisposalForm(request.POST, request.FILES)
        if form.is_valid():
            disposal_entry = form.save(commit=False)
            disposal_entry.user = request.user
            disposal_entry.coins_awarded = disposal_entry.bottle_count * settings.GLASS_DISPOSAL_REWARD_PER_BOTTLE
            disposal_entry.save()

            #update user's coin balance
            request.user.profile.number_of_coins += disposal_entry.coins_awarded
            request.user.profile.save()

            return redirect('thankyou', coins_earned=disposal_entry.coins_awarded)

    else:
        form = GlassDisposalForm()

    return render(request, 'glassDisposal/submit_disposal.html', {'form': form})

def thankyou(request, coins_earned):
    """view to display thank you page with earned coins."""
    return render(request, 'glassDisposal/thankyou.html', {'coins_earned': coins_earned})