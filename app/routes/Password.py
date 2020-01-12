from app import app
from flask import render_template
from Modules.forms import PasswordResetForm
@app.route('/forgotPass', methods=['GET', 'POST'])
def forgotPass():
    PasswordResetform = PasswordResetForm()
    # grab data from form
    email = PasswordResetform.email.data
    password = PasswordResetform.password.data
    confirmpassword = PasswordResetform.passwordConfirm.data
    return render_template('PasswordReset/PasswordReset.html', PasswordResetform = PasswordResetform)

@app.route('/PasswordReset', methods=['GET','POST'])
def passwordReset():
    print("WIP")
