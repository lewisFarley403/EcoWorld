from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import GlassDisposalEntry
from .forms import GlassDisposalForm
from django.conf import settings
from django.shortcuts import render

@login_required
def submit_disposal(request):
    """handles glass disposal submissions"""
    form = GlassDisposalForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        disposal_entry = form.save(commit=False)
        disposal_entry.user = request.user
        disposal_entry.coins_awarded = disposal_entry.bottle_count * settings.GLASS_DISPOSAL_REWARD_PER_BOTTLE
        disposal_entry.save()

        #update users coin balance
        request.user.profile.number_of_coins += disposal_entry.coins_awarded
        request.user.profile.save()

        return redirect('thankyou')  #redirect to success page

    return render(request, 'glassDisposal/submit_disposal.html', {'form': form})

def thankyou(request):
    """thankyou page after form submission"""
    return render(request, 'glassDisposal/thankyou.html')