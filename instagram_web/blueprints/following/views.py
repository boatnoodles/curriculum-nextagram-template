from flask import Blueprint, redirect
from flask_login import current_user, login_required
from models.following import Following


following = Blueprint('following', __name__, template_folder='templates')


@following.route('/', methods=["POST"])
@login_required
def create(id):
    new_following = Following(fan=current_user.id, idol=id)

    new_following.save()

    return redirect('index.html')


@following.route('/delete', methods=["POST"])
def delete(id):
    unfollowing = Following.get(fan=current_user.id, idol=id)

    if unfollowing:
        # Delete from records to unfollow
        unfollowing.delete_instance()

    return redirect("index.html")
