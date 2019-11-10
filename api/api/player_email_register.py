"Player Email Register"

from flask import current_app, redirect, request, make_response, abort, json
from flask.views import MethodView

from api.app import db
from api.database import rowify, fetch_query_string
from api.user import user_id_from_ip, user_not_banned
from api.constants import EMAIL_MAXLENGTH


class PlayerEmailRegisterView(MethodView):
    """
    """
    decorators = [user_not_banned]

    def post(self):
        ""
        response = {
            "message": "",
            "name": "error"
        }

        is_shareduser = False
        user = current_app.secure_cookie.get(u'user')
        if not user:
            user = user_id_from_ip(request.headers.get('X-Real-IP'))
            is_shareduser = True

        if user == None:
            response["message"] = "User not signed in."
            response["name"] = "error"
            return make_response(json.jsonify(response), 400)

        user = int(user)

        args = {}
        if request.form:
            args.update(request.form.to_dict(flat=True))

        email = args.get('email', '').strip().lower()
        if len(email) > EMAIL_MAXLENGTH:
            response["message"] = "E-mail is too long."
            response["name"] = "error"
            return make_response(json.jsonify(response), 400)

        cur = db.cursor()

        result = cur.execute(fetch_query_string('user-has-player-account.sql'), {'player_id': user}).fetchone()
        if not result or result[0] == 0:
            cur.execute(fetch_query_string('init-player-account-for-user.sql'), {
                'player_id': user
            })

        result = cur.execute(fetch_query_string('select-player-details-for-player-id.sql'), {'player_id': user}).fetchall()
        if not result:
            cur.close()
            response["message"] = "No player account."
            response["name"] = "error"
            return make_response(json.jsonify(response), 400)
        (result, col_names) = rowify(result, cur.description)
        existing_player_data = result[0]

        # Prevent shareduser changing the verified email address.
        if is_shareduser and existing_player_data['is_verifying_email']:
            response["message"] = "A player on this same network has already submitted an email address. Changing it is not allowed until the account has been claimed or the verify email token expires."
            response["name"] = "error"
            return make_response(json.jsonify(response), 400)

        if existing_player_data['email'] == email:
            response["message"] = "No changes made to e-mail address ({}).  The e-mail address is stored as lowercase.".format(email)
            response["name"] = "error"
        else:
            if email == '':
                cur.execute(fetch_query_string('remove-player-account-email.sql'), {
                    'player_id': user
                })
                response["message"] = "Removed e-mail from player account."
                response["name"] = "success"
            else:
                cur.execute(fetch_query_string('update-player-account-email.sql'), {
                    'player_id': user,
                    'email': email
                })
                cur.execute(fetch_query_string('update-player-account-email-verified.sql'), {
                    'player_id': user,
                    'email_verified': 0,
                })

                #TODO: send verification e-mail
                cur.execute(fetch_query_string('update-player-account-email-verify-token.sql'), {
                    'player_id': user,
                    'email_verify_token': 'asdfasdf', #TODO: generate token
                    'expire_token_timeout': '+1 hour',
                })

                response["message"] = "Updated e-mail ({}) for player account.  ".format(email)
                response["name"] = "success"

        db.commit()
        cur.close()
        return make_response(json.jsonify(response), 202)
