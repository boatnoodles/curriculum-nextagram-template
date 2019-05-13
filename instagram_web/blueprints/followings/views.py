from flask import Blueprint, flash, redirect, request, url_for
from flask_login import current_user, login_required
from peewee import IntegrityError
from models.followerfollowing import FollowerFollowing as FF
from models.user import User
import pysnooper


followings_blueprint = Blueprint(
    'followings', __name__, template_folder='templates')


@followings_blueprint.route('/<following_username>', methods=["POST"])
@login_required
def create(following_username):
    # Get the user current_user wants to follow
    idol = User.get_or_none(User.username == following_username)

    # If the following user is not found
    if not idol:
        flash("No user found with this id!", "warning")
        return redirect(url_for('home'))

    # Create a new query
    new_following = FF(
        fan=current_user.id, idol=idol.id)

    # Immediately approve the follower request if the target account is not private
    if not idol.is_private:
        new_following.approved = True

    # Flash a message if unable save
    try:
        new_following.save()
    except IntegrityError:
        flash("You're already following this user, dumdum!", "danger")
        return redirect(url_for('users.show', username=idol.username))
    except:
        flash("Unable to follow this user!", "danger")
        return redirect(url_for('users.show', username=idol.username))

    # If the follower request has been approved (in other words, the account is not private)
    if new_following.is_approved:
        flash(f'You are now following {following_username}', 'success')
        return redirect(url_for('users.show', username=idol.username))

    # If account is private
    flash('Your follower request has been sent', 'info')
    return redirect(url_for('users.show', username=idol.username))


@followings_blueprint.route('/delete/<following_username>', methods=["POST"])
def delete(following_username):
    ex_idol = User.get_or_none(User.username == following_username)

    if not ex_idol:
        flash("User not found", "danger")
        return redirect(url_for('users.show', username=following_username))

    # Delete from records to unfollow
    try:
        FF.get_or_none(FF.idol == ex_idol).delete_instance()
    except AttributeError:
        flash(
            f"Unable to unfollow, you're not currently following {following_username}.", "warning")
        return redirect(url_for("users.show", username=following_username))
    except:
        flash("An error occurred, please try again later.", "warning")
        return redirect(url_for("users.show", username=following_username))

    flash(f"You have successfully unfollowed {following_username}", "warning")
    return redirect(url_for('users.show', username=following_username))


@followings_blueprint.route('<req_id>/requests/accept', methods=["GET"])
def accept(req_id):
    # Select the instance of follow request
    follow_request = FF.get_by_id(req_id)
    fan = User.get_by_id(follow_request.fan_id)
    # Turn approved to true (.update)
    u = follow_request.update({FF.approved: True}).where(
        FF.idol_id == current_user.id)
    print(request.args.get('next'))
    if not u.execute():
        flash("Failed to accept the follow_request, please try again later", "warning")
        return redirect(url_for(request.args.get('next')))

    flash(f"{follow_request.fan_id} now following you!")
    return redirect(url_for(request.args.get('next')))


@followings_blueprint.route('<req_id>/requests/reject', methods=["GET"])
def reject(req_id):
    # Select the instance of follow request
    follow_request = FF.get_or_none(FF.id == req_id)

    if not follow_request:
        flash("Request not found", "danger")
        return redirect(request.args.get('next'))

    if not follow_request.delete_instance():
        flash("Failed to reject the follow_request, please try again later", "warning")
        return redirect(request.args.get('next'))

    flash("Request deleted.", "info")
    return redirect(request.args.get('next'))
