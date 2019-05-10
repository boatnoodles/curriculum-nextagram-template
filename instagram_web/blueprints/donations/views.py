import os
import braintree
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from instagram_web.util.helpers.donations import *
from models.donation import Donation
from models.post import Post
from models.user import User

donations_blueprint = Blueprint(
    'donations', __name__, template_folder='templates')


@donations_blueprint.route('/<recipient>/new', methods=["GET"])
def new(recipient):
    client_token = generate_client_token()
    url = Post.get(Post.path == recipient).post_url
    return render_template('donations/new.html', client_token=client_token, recipient=recipient, url=url)


@donations_blueprint.route('/<recipient>', methods=['POST'])
@login_required
def create(recipient):
    amount = request.form.get('amount')

    result = make_transaction(amount)

    # If transaction is successful
    if result.is_success or result.transaction:
        post = Post.get(Post.path == recipient)
        recipient_email = User.get(User.id == post.user_id).email
        # Save amount into database
        q = Donation(donor=User.get_by_id(current_user.id),
                     recipient_post=post, amount=amount)
        if q.save():
            # Display on the screen
            # Send an email
            send_email(recipient_email)
            return redirect(url_for('donations.show', transaction_id=result.transaction.id))

        else:
            return redirect(url_for('donations.new', recipient=recipient))

    else:
        for x in result.errors.deep_errors:
            flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('donations.new', recipient=recipient))


@donations_blueprint.route('/show/<transaction_id>', methods=['GET'])
def show(transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('donations/show.html', transaction=transaction, result=result)
