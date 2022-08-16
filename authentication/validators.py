from django.core.exceptions import ValidationError


class ContainsLetterValidator:
    """vérifier si le mot de passe contient au moins une lettre

    Raises:
        ValidationError: _description_

    Returns:
        _type_: _description_
    """

    def validate(self, password, user=None):
        """si charactères pas alpha, on lève une exception
        cela retourne une chaine de caractère qui guide l'utilisateur
        Args:
            password (_type_): _description_
            user (_type_, optional): _description_. Defaults to None.

        Raises:
            ValidationError: _description_
        """
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir une lettre',
                code='password_no_letters'
            )

    def get_help_text(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return 'Le mdp doit contenir au moins une lettre maj ou min.'


class ContainsNumberValidator:
    """_summary_
    """
    def validate(self, password, user=None):
        """_summary_

        Args:
            password (_type_): _description_
            user (_type_, optional): _description_. Defaults to None.

        Raises:
            ValidationError: _description_
        """
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir un chiffre',
                code='password_no_number'
            )

    def get_help_text(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return 'Votre mot de passe doit contenir au moins un chiffre.'
