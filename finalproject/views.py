# Application was built upon Emilio's TicketMaster project from CS 416
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import *
from .utils import *


# Inherited from TicketMaster project
def logout_view(request):
    # This is the method to log out the user
    logout(request)
    # redirect the user to index page after logout
    return redirect('login')


# Code updated by William, added key generation and assignment when users make their account
def signup(request):
    if request.user.is_authenticated:
        return redirect('view-notes')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            publicKey, privateKey = generate_keys(32)
            newUserPrivatePublic = PrivatePublicKey()
            newUserPrivatePublic.user = request.user
            newUserPrivatePublic.privateKey1, newUserPrivatePublic.privateKey2 = privateKey
            newUserPrivatePublic.publicKey1, newUserPrivatePublic.publicKey2 = publicKey
            newUserPrivatePublic.save()

            messages.success(request, 'Account created successfully. You are now logged in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'landing.html', context)


# Login code inherited from TicketMaster project, William pointed redirect to new view-notes page
def login_view(request):
    if request.method == 'POST':
        form = BootstrapAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('view-notes')
    else:
        form = BootstrapAuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Code updated by William
@login_required(login_url='login')
def view_notes(request):  # view saved events
    notes = SavedNotes.objects.filter(user=request.user)
    context = {'notes': notes}
    return render(request, 'saved-notes.html', context)


# Code updated by William
@login_required(login_url='login')
def create_note(request):
    # Create a form instance and populate it with data from the request
    form = SavedNotesForm(request.POST or None)
    # check whether it's valid:
    if form.is_valid():
        form.instance.user = request.user
        form.instance.username = request.user.username
        obj = form.save(commit=False)

        # obj.accountUser = request.user.username
        # save the record into the db
        obj.save()
        form.save()
        # after saving redirect to view_product page
        return redirect('view-notes')

    # if the request does not have post data, a blank form will be rendered
    return render(request, 'create-note-form.html', {'form': form})


# Code by William
@login_required(login_url='login')
def update_note(request, note_id):  # favorite events that are saved
    note = SavedNotes.objects.get(id=note_id, user=request.user)
    form = SavedNotesForm(request.POST or None, instance=note)
    favorite = form.save(commit=False)
    favorite.favorite = 1 - favorite.favorite  # swaps between true and false whenever favorite is clicked
    favorite.save()
    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect('view-notes')
    notes = SavedNotes.objects.filter(user=request.user)
    context = {'notes': notes}
    return render(request, 'saved-notes.html', context)


# Code updated by William
@login_required(login_url='login')
def delete_note(request, id):  # delete events from saved database
    note = SavedNotes.objects.get(id=id)
    if request.method == 'POST':
        note.delete()
        return redirect('view-notes')
    return render(request, 'delete-confirm.html', {'note': note})


# Code by William
@login_required(login_url='/login/1/')
def update_comp_note(request, note_id):
    note = SavedNotes.objects.get(id=note_id)

    form = SavedNotesForm(request.POST or None, instance=note)
    if form.is_valid():
        form.save()
        return redirect('view-notes')
    return render(request, 'create-note-form.html', {'form': form})


# Code by William
@login_required(login_url='login')
def send_note(request, note_id):
    note = SavedNotes.objects.get(id=note_id)
    form = SendNotesForm(request.POST)
    if form.is_valid():
        user = User.objects.get(username=form.cleaned_data.get("Username"))
        if user is None:
            return redirect('view-notes')

        newNote = note
        plainText = newNote.content
        plainText1 = plainText.replace('\x00', '')

        # hash plainText1 to store hash
        hash1 = tiger_hash(plainText1.encode())

        # get private and public of current user
        privatePublicKey = PrivatePublicKey.objects.get(user=request.user)
        privateKey = privatePublicKey.privateKey1, privatePublicKey.privateKey2
        publicKey = privatePublicKey.publicKey1, privatePublicKey.publicKey2

        # encrypt
        cipherText = encrypt(plainText.encode(), publicKey)
        newNote.content = cipherText

        # send note
        newNote.user_id = user.id
        newNote.save()

        # decrypt
        decryptedNote = SavedNotes.objects.get(id=note_id)
        encryptedNoteText = eval(decryptedNote.content.encode())
        decryptedText = decrypt(encryptedNoteText, privateKey).decode()
        decryptedNote.content = decryptedText
        plainText2 = decryptedText.replace('\x00', '')

        # hash to check if message is the same
        hash2 = tiger_hash(plainText2.encode())
        message2 = ""

        print(list(plainText1))
        print(list(plainText2))

        if hash1 == hash2:
            message2 = "Message was successfully checked using tiger hash!"
        else:
            message2 = "Message was successfully checked and the message has been changed in between sending and receiving."

        decryptedNote.save()

        message1 = "Message was encrypted and decrypted successfully using public key crypto while sending! Sent to user: " + form.cleaned_data.get(
            "Username")
        notes = SavedNotes.objects.filter(user=request.user)
        context = {
            'notes': notes,
            'plainText': plainText,
            'privateKey': privateKey,
            'publicKey': publicKey,
            'cipherText': cipherText,
            'decryptedText': decryptedText,
            'message1': message1,
            'plainText1': plainText1,
            'plainText2': plainText2,
            'hash1': hash1,
            'hash2': hash2,
            'message2': message2,

        }
        return render(request, 'saved-notes.html', context)
    return render(request, 'send-note-form.html', {'form': form})


# Page to test encryption, refer to utils.py for functions. This code was done by Emilio Espada.
@login_required(login_url='test')
def test_crypto(request):
    notes = SavedNotes.objects.filter(user=request.user)
    if request.method == 'POST':
        plaintext = request.POST.get('plaintext')
        # Generate keys
        public_key, private_key = generate_keys(32)
        # Encrypt the plaintext, will be shown as byte-string with escape characters (\x)
        ciphertext = encrypt(plaintext.encode(), public_key)
        # Decrypt the ciphertext
        decrypted_text = decrypt(ciphertext, private_key).decode()
        # Prepare the context data
        context = {
            'notes': notes,
            'publicKey': public_key,
            'privateKey': private_key,
            'plaintext': plaintext,
            'ciphertext': ciphertext,
            'decrypted_text': decrypted_text,
        }
    else:
        context = {
            'notes': notes
        }
    return render(request, 'test-crypto.html', context)
