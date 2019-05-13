from flask import Blueprint, flash, redirect, url_for
from flask_login import current_user, login_required
from peewee import IntegrityError
from models.followerfollowing import FollowerFollowing as FF
from models.user import User
import pysnooper


follows_blueprint = Blueprint(
    'followings', __name__, template_folder='templates')


@follows_blueprint.route('/<following_username>', methods=["POST"])
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
        flash("You're already following this user!", "danger")
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


@follows_blueprint.route('/delete/<following_username>', methods=["POST"])
@pysnooper.snoop('test/follow.log')
def delete(following_username):
    user_to_unfollow = User.get_or_none(User.username == following_username)

    if not user_to_unfollow:
        flash("User not found", "danger")
        return redirect(url_for('users.show', username=following_username))

    # Delete from records to unfollow
    try:
        FF.get_or_none(FF.idol == user_to_unfollow).delete_instance()
    except AttributeError:
        flash(
            f"Unable to unfollow, you're not currently following {following_username}.", "warning")
        return redirect(url_for("users.show", username=following_username))
    except:
        flash("An error occurred, please try again later.", "warning")
        return redirect(url_for("users.show", username=following_username))

    flash(f"You have successfully unfollowed {following_username}", "warning")
    return redirect(url_for('users.show', username=following_username))
